# -*- coding: utf-8 -*-

"""
KiroGate 智能 Token 分配器。

实现基于成功率、新鲜度和负载均衡的 Token 智能分配算法。
支持多种分配策略：
- score_based: 评分优先（默认），综合考虑成功率、新鲜度、负载均衡
- round_robin: 轮询，多账号同时使用，均匀分配请求
- sequential: 顺序使用，用完一个再用下一个
"""

import asyncio
import time
from typing import Optional, Tuple, List

from loguru import logger

from kiro_gateway.database import user_db, DonatedToken
from kiro_gateway.auth import KiroAuthManager
from kiro_gateway.config import settings


class NoTokenAvailable(Exception):
    """No active token available for allocation."""
    pass


class SmartTokenAllocator:
    """智能 Token 分配器。"""

    def __init__(self):
        self._lock = asyncio.Lock()
        self._token_managers: dict[int, KiroAuthManager] = {}
        self._round_robin_index: dict[int, int] = {}  # user_id -> index
        self._global_round_robin_index: int = 0
        self._current_sequential_token: dict[int, int] = {}  # user_id -> token_id

    def calculate_score(self, token: DonatedToken) -> float:
        """
        计算 Token 评分 (0-100)。

        评分基于：
        - 成功率 (权重 60%)
        - 新鲜度 (权重 20%)
        - 负载均衡 (权重 20%)
        """
        now = int(time.time() * 1000)

        # 基础分: 成功率 (权重60%)
        total = token.success_count + token.fail_count
        if total == 0:
            success_rate = 1.0  # 新Token给予高分
        else:
            success_rate = token.success_count / total

        # 如果成功率低于阈值，大幅降分
        if success_rate < settings.token_min_success_rate and total > 10:
            base_score = success_rate * 30  # 降低权重
        else:
            base_score = success_rate * 60

        # 新鲜度: 最近使用时间 (权重20%)
        if token.last_used:
            hours_since_use = (now - token.last_used) / 3600000
        else:
            hours_since_use = 0  # 从未使用，视为新鲜

        if hours_since_use < 1:
            freshness = 20
        elif hours_since_use < 24:
            freshness = 15
        else:
            freshness = max(5, 20 - hours_since_use / 24)

        # 负载均衡: 使用频率 (权重20%)
        # 使用次数少的Token优先，避免单个Token过载
        usage_score = max(0, 20 - (total / 100))

        return base_score + freshness + usage_score

    def _select_by_strategy(
        self,
        tokens: List[DonatedToken],
        user_id: Optional[int],
        strategy: str
    ) -> DonatedToken:
        """
        根据策略选择 Token。

        Args:
            tokens: 可用 Token 列表
            user_id: 用户 ID（用于维护轮询状态）
            strategy: 分配策略

        Returns:
            选中的 Token
        """
        if not tokens:
            raise NoTokenAvailable("No tokens available")

        if strategy == "round_robin":
            # 轮询策略：均匀分配请求到所有 Token
            if user_id:
                idx = self._round_robin_index.get(user_id, 0)
                self._round_robin_index[user_id] = (idx + 1) % len(tokens)
            else:
                idx = self._global_round_robin_index
                self._global_round_robin_index = (idx + 1) % len(tokens)
            # 按 ID 排序确保顺序一致
            sorted_tokens = sorted(tokens, key=lambda t: t.id)
            return sorted_tokens[idx % len(sorted_tokens)]

        elif strategy == "sequential":
            # 顺序策略：用完一个再用下一个
            sorted_tokens = sorted(tokens, key=lambda t: t.id)
            key = user_id or 0

            # 获取当前使用的 token
            current_id = self._current_sequential_token.get(key)

            if current_id:
                # 检查当前 token 是否还可用
                current_token = next((t for t in sorted_tokens if t.id == current_id), None)
                if current_token and current_token.status == "active":
                    # 检查是否达到使用限制（可选：基于失败率判断是否切换）
                    total = current_token.success_count + current_token.fail_count
                    if total > 10 and current_token.success_rate < 0.3:
                        # 成功率太低，切换到下一个
                        idx = next((i for i, t in enumerate(sorted_tokens) if t.id == current_id), 0)
                        next_idx = (idx + 1) % len(sorted_tokens)
                        self._current_sequential_token[key] = sorted_tokens[next_idx].id
                        return sorted_tokens[next_idx]
                    return current_token

            # 没有当前 token 或当前 token 不可用，选择第一个
            self._current_sequential_token[key] = sorted_tokens[0].id
            return sorted_tokens[0]

        else:
            # 默认: score_based 评分策略
            return max(tokens, key=self.calculate_score)

    async def get_best_token(
        self,
        user_id: Optional[int] = None,
        strategy: Optional[str] = None
    ) -> Tuple[DonatedToken, KiroAuthManager]:
        """
        获取最优 Token。

        对于有用户的请求，优先使用用户自己的私有 Token。
        否则使用公共 Token 池。

        Args:
            user_id: 用户 ID
            strategy: 分配策略（可选，默认使用全局配置）

        Returns:
            (DonatedToken, KiroAuthManager) tuple

        Raises:
            NoTokenAvailable: 无可用 Token
        """
        from kiro_gateway.metrics import metrics
        self_use_enabled = metrics.is_self_use_enabled()

        # 使用指定策略或全局配置
        use_strategy = strategy or settings.token_allocation_strategy

        if user_id:
            # 用户请求: 优先使用用户自己的私有 Token
            user_tokens = user_db.get_user_tokens(user_id)
            active_tokens = [
                t for t in user_tokens
                if t.status == "active" and (not self_use_enabled or t.visibility == "private")
            ]
            if active_tokens:
                best = self._select_by_strategy(active_tokens, user_id, use_strategy)
                manager = await self._get_manager(best)
                return best, manager

        if self_use_enabled:
            raise NoTokenAvailable("Self-use mode: public token pool is disabled")

        # 使用公共 Token 池
        public_tokens = user_db.get_public_tokens()
        if not public_tokens:
            raise NoTokenAvailable("No public tokens available")

        # 过滤掉低成功率的 Token（仅对评分策略生效）
        if use_strategy == "score_based":
            good_tokens = [
                t for t in public_tokens
                if t.success_rate >= settings.token_min_success_rate or
                   (t.success_count + t.fail_count) < 10  # 给新Token机会
            ]
            if not good_tokens:
                good_tokens = public_tokens
        else:
            good_tokens = public_tokens

        best = self._select_by_strategy(good_tokens, user_id, use_strategy)
        manager = await self._get_manager(best)
        return best, manager

    async def _get_manager(self, token: DonatedToken) -> KiroAuthManager:
        """获取或创建 Token 对应的 AuthManager（线程安全）。"""
        async with self._lock:
            if token.id in self._token_managers:
                return self._token_managers[token.id]

            # 获取完整的 token 凭证（包括 client_id 和 client_secret）
            token_creds = user_db.get_token_credentials(token.id)
            if not token_creds:
                raise NoTokenAvailable(f"Failed to get credentials for token {token.id}")

            manager = KiroAuthManager(
                refresh_token=token_creds["refresh_token"],
                region=settings.region,
                profile_arn=settings.profile_arn,
                client_id=token_creds.get("client_id"),
                client_secret=token_creds.get("client_secret")
            )

            self._token_managers[token.id] = manager
            return manager

    def record_usage(self, token_id: int, success: bool) -> None:
        """记录 Token 使用结果。"""
        user_db.record_token_usage(token_id, success)

    def clear_manager(self, token_id: int) -> None:
        """清除缓存的 AuthManager。"""
        if token_id in self._token_managers:
            del self._token_managers[token_id]

    def reset_sequential_token(self, user_id: Optional[int] = None) -> None:
        """重置顺序策略的当前 Token（用于手动切换）。"""
        key = user_id or 0
        if key in self._current_sequential_token:
            del self._current_sequential_token[key]


# Global allocator instance
token_allocator = SmartTokenAllocator()
