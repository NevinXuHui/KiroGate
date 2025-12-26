# -*- coding: utf-8 -*-

# KiroGate
# Based on kiro-openai-gateway by Jwadow (https://github.com/Jwadow/kiro-openai-gateway)
# Original Copyright (C) 2025 Jwadow
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
长文档分段处理器。

当文档过长时，自动将其分段处理，然后拼接结果。
这可以有效避免超时问题，特别是对于 Opus 等慢模型。
"""

import re
from typing import List, Optional, Tuple
from loguru import logger

from kiro_gateway.config import settings


# 默认配置
DEFAULT_MAX_TOKENS_PER_CHUNK = 50000  # 每个分段的最大 token 数
DEFAULT_OVERLAP_TOKENS = 500  # 分段之间的重叠 token 数（保持上下文连贯）
CHARS_PER_TOKEN_ESTIMATE = 4  # 估算：平均每个 token 约 4 个字符


class ChunkedDocumentProcessor:
    """
    长文档分段处理器。

    将超长文档分成多个较小的片段，以避免超时问题。
    支持自定义分段大小和重叠区域。
    """

    def __init__(
        self,
        max_tokens_per_chunk: int = DEFAULT_MAX_TOKENS_PER_CHUNK,
        overlap_tokens: int = DEFAULT_OVERLAP_TOKENS
    ):
        """
        初始化分段处理器。

        Args:
            max_tokens_per_chunk: 每个分段的最大 token 数
            overlap_tokens: 分段之间的重叠 token 数
        """
        self.max_tokens_per_chunk = max_tokens_per_chunk
        self.overlap_tokens = overlap_tokens
        self.max_chars_per_chunk = max_tokens_per_chunk * CHARS_PER_TOKEN_ESTIMATE
        self.overlap_chars = overlap_tokens * CHARS_PER_TOKEN_ESTIMATE

    def estimate_tokens(self, text: str) -> int:
        """
        估算文本的 token 数。

        使用简单的字符数估算，比精确计算更快。

        Args:
            text: 要估算的文本

        Returns:
            估算的 token 数
        """
        return len(text) // CHARS_PER_TOKEN_ESTIMATE

    def needs_chunking(self, text: str) -> bool:
        """
        判断文本是否需要分段。

        Args:
            text: 要检查的文本

        Returns:
            如果文本超过阈值则返回 True
        """
        return len(text) > self.max_chars_per_chunk

    def find_split_point(self, text: str, target_pos: int) -> int:
        """
        在目标位置附近找到合适的分割点。

        优先在段落、句子或单词边界分割，以保持语义完整性。

        Args:
            text: 要分割的文本
            target_pos: 目标分割位置

        Returns:
            实际分割位置
        """
        if target_pos >= len(text):
            return len(text)

        # 搜索范围：目标位置前后 500 字符
        search_start = max(0, target_pos - 500)
        search_end = min(len(text), target_pos + 500)
        search_text = text[search_start:search_end]

        # 优先级 1：段落边界（双换行）
        paragraph_breaks = list(re.finditer(r'\n\n+', search_text))
        if paragraph_breaks:
            # 找到最接近目标位置的段落边界
            best_match = min(paragraph_breaks, key=lambda m: abs((search_start + m.end()) - target_pos))
            return search_start + best_match.end()

        # 优先级 2：句子边界
        sentence_breaks = list(re.finditer(r'[.!?。！？]\s+', search_text))
        if sentence_breaks:
            best_match = min(sentence_breaks, key=lambda m: abs((search_start + m.end()) - target_pos))
            return search_start + best_match.end()

        # 优先级 3：单换行
        line_breaks = list(re.finditer(r'\n', search_text))
        if line_breaks:
            best_match = min(line_breaks, key=lambda m: abs((search_start + m.end()) - target_pos))
            return search_start + best_match.end()

        # 优先级 4：空格（单词边界）
        word_breaks = list(re.finditer(r'\s+', search_text))
        if word_breaks:
            best_match = min(word_breaks, key=lambda m: abs((search_start + m.end()) - target_pos))
            return search_start + best_match.end()

        # 如果没有找到合适的分割点，直接在目标位置分割
        return target_pos

    def split_text(self, text: str) -> List[str]:
        """
        将长文本分割成多个片段。

        Args:
            text: 要分割的文本

        Returns:
            文本片段列表
        """
        if not self.needs_chunking(text):
            return [text]

        chunks = []
        current_pos = 0
        text_length = len(text)

        while current_pos < text_length:
            # 计算这个分段的结束位置
            chunk_end = current_pos + self.max_chars_per_chunk

            if chunk_end >= text_length:
                # 最后一个分段
                chunks.append(text[current_pos:])
                break

            # 找到合适的分割点
            split_pos = self.find_split_point(text, chunk_end)

            # 提取分段
            chunk = text[current_pos:split_pos]
            chunks.append(chunk)

            # 移动到下一个位置（考虑重叠）
            current_pos = split_pos - self.overlap_chars
            if current_pos <= 0 or current_pos >= split_pos:
                current_pos = split_pos  # 避免无限循环

        logger.info(f"Split document into {len(chunks)} chunks")
        for i, chunk in enumerate(chunks):
            logger.debug(f"Chunk {i+1}: {len(chunk)} chars, ~{self.estimate_tokens(chunk)} tokens")

        return chunks

    def create_chunk_prompt(
        self,
        chunk: str,
        chunk_index: int,
        total_chunks: int,
        original_prompt: str
    ) -> str:
        """
        为分段创建带上下文的提示词。

        Args:
            chunk: 文档片段
            chunk_index: 当前片段索引（从 0 开始）
            total_chunks: 总片段数
            original_prompt: 原始用户提示词

        Returns:
            带上下文的提示词
        """
        if total_chunks == 1:
            return f"{original_prompt}\n\n{chunk}"

        context_info = f"[文档片段 {chunk_index + 1}/{total_chunks}]"

        if chunk_index == 0:
            instruction = "这是一个长文档的第一部分。请处理这部分内容，后续会提供剩余部分。"
        elif chunk_index == total_chunks - 1:
            instruction = "这是文档的最后一部分。请结合之前的内容完成处理。"
        else:
            instruction = f"这是文档的第 {chunk_index + 1} 部分。请继续处理。"

        return f"{context_info}\n{instruction}\n\n{original_prompt}\n\n---\n{chunk}\n---"

    def merge_responses(self, responses: List[str]) -> str:
        """
        合并多个分段的响应。

        Args:
            responses: 各分段的响应列表

        Returns:
            合并后的完整响应
        """
        if len(responses) == 1:
            return responses[0]

        # 简单拼接，用分隔符连接
        merged = "\n\n".join(responses)

        logger.info(f"Merged {len(responses)} responses into one")
        return merged


def extract_document_from_messages(messages: List[dict]) -> Tuple[Optional[str], int]:
    """
    从消息列表中提取可能的长文档内容。

    Args:
        messages: 消息列表

    Returns:
        (文档内容, 消息索引) 或 (None, -1)
    """
    for i, msg in enumerate(messages):
        content = msg.get("content", "")
        if isinstance(content, str) and len(content) > DEFAULT_MAX_TOKENS_PER_CHUNK * CHARS_PER_TOKEN_ESTIMATE:
            return content, i
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text = block.get("text", "")
                    if len(text) > DEFAULT_MAX_TOKENS_PER_CHUNK * CHARS_PER_TOKEN_ESTIMATE:
                        return text, i

    return None, -1


# 全局实例
chunked_processor = ChunkedDocumentProcessor()
