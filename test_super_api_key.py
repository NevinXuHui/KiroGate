#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超级 API Key 功能测试脚本

用法:
    python test_super_api_key.py

功能:
    1. 测试创建超级 API Key
    2. 测试使用超级 API Key 发送请求
    3. 验证 Token 池访问
"""

import requests
import json
import sys
from typing import Optional, Dict, Any


class Colors:
    """终端颜色"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """打印标题"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")


def print_success(text: str):
    """打印成功信息"""
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")


def print_error(text: str):
    """打印错误信息"""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")


def print_info(text: str):
    """打印信息"""
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")


def print_warning(text: str):
    """打印警告"""
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")


class SuperAPIKeyTester:
    """超级 API Key 测试器"""

    def __init__(self, base_url: str = "http://127.0.0.1:9000"):
        self.base_url = base_url
        self.admin_session: Optional[str] = None
        self.super_api_key: Optional[str] = None

    def login_admin(self, password: str = "admin123") -> bool:
        """登录管理后台"""
        print_header("步骤 1: 登录管理后台")

        try:
            response = requests.post(
                f"{self.base_url}/admin/login",
                data={"password": password},
                allow_redirects=False
            )

            if response.status_code in [200, 302, 303]:
                # 从 Set-Cookie 中提取 session
                cookies = response.cookies
                if "admin_session" in cookies:
                    self.admin_session = cookies["admin_session"]
                    print_success(f"管理员登录成功")
                    print_info(f"Session: {self.admin_session[:20]}...")
                    return True
                else:
                    print_error("未找到 admin_session cookie")
                    return False
            else:
                print_error(f"登录失败: HTTP {response.status_code}")
                return False

        except Exception as e:
            print_error(f"登录异常: {e}")
            return False

    def get_users(self) -> Optional[list]:
        """获取用户列表"""
        print_header("步骤 2: 获取用户列表")

        if not self.admin_session:
            print_error("未登录，请先调用 login_admin()")
            return None

        try:
            response = requests.get(
                f"{self.base_url}/admin/api/users",
                params={"page": 1, "page_size": 10},
                cookies={"admin_session": self.admin_session}
            )

            if response.status_code == 200:
                data = response.json()
                users = data.get("users", [])
                print_success(f"获取到 {len(users)} 个用户")

                for user in users[:5]:  # 只显示前5个
                    print_info(f"  用户 ID: {user['id']}, 用户名: {user['username']}, Token数: {user.get('token_count', 0)}")

                return users
            else:
                print_error(f"获取用户列表失败: HTTP {response.status_code}")
                return None

        except Exception as e:
            print_error(f"获取用户列表异常: {e}")
            return None

    def create_super_api_key(self, user_id: int, name: str = "测试超级密钥") -> Optional[str]:
        """创建超级 API Key"""
        print_header("步骤 3: 创建超级 API Key")

        if not self.admin_session:
            print_error("未登录，请先调用 login_admin()")
            return None

        try:
            response = requests.post(
                f"{self.base_url}/admin/api/super-api-keys",
                data={
                    "user_id": user_id,
                    "name": name
                },
                cookies={"admin_session": self.admin_session}
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.super_api_key = data.get("key")
                    print_success("超级 API Key 创建成功！")
                    print_info(f"  用户 ID: {data.get('user_id')}")
                    print_info(f"  Key 前缀: {data.get('key_prefix')}")
                    print_info(f"  是否超级: {data.get('is_super')}")
                    print_info(f"  完整密钥: {self.super_api_key}")
                    return self.super_api_key
                else:
                    print_error(f"创建失败: {data.get('error', '未知错误')}")
                    return None
            else:
                print_error(f"创建失败: HTTP {response.status_code}")
                try:
                    error_data = response.json()
                    print_error(f"错误详情: {error_data}")
                except:
                    print_error(f"响应内容: {response.text[:200]}")
                return None

        except Exception as e:
            print_error(f"创建超级 API Key 异常: {e}")
            return None

    def test_super_api_key(self, api_key: Optional[str] = None) -> bool:
        """测试超级 API Key"""
        print_header("步骤 4: 测试超级 API Key")

        test_key = api_key or self.super_api_key
        if not test_key:
            print_error("没有可用的超级 API Key")
            return False

        print_info(f"使用密钥: {test_key[:20]}...")

        # 测试 OpenAI 格式
        print_info("\n测试 OpenAI 格式 API...")
        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {test_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "claude-sonnet-4-5",
                    "messages": [
                        {"role": "user", "content": "请用一句话介绍你自己"}
                    ],
                    "max_tokens": 100,
                    "stream": False
                },
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                print_success("OpenAI 格式测试成功！")
                print_info(f"  响应内容: {content[:100]}...")
                return True
            elif response.status_code == 503:
                print_warning("服务不可用 (503)")
                print_warning("可能原因: 没有可用的公开 Token")
                print_info("解决方法: 请先添加公开的 Token")
                return False
            else:
                print_error(f"请求失败: HTTP {response.status_code}")
                try:
                    error_data = response.json()
                    print_error(f"错误详情: {error_data}")
                except:
                    print_error(f"响应内容: {response.text[:200]}")
                return False

        except requests.exceptions.Timeout:
            print_error("请求超时")
            return False
        except Exception as e:
            print_error(f"测试异常: {e}")
            return False

    def check_token_pool(self) -> bool:
        """检查 Token 池状态"""
        print_header("步骤 5: 检查 Token 池状态")

        if not self.admin_session:
            print_error("未登录，请先调用 login_admin()")
            return False

        try:
            response = requests.get(
                f"{self.base_url}/admin/api/donated-tokens",
                params={"page": 1, "page_size": 10},
                cookies={"admin_session": self.admin_session}
            )

            if response.status_code == 200:
                data = response.json()
                tokens = data.get("tokens", [])
                total = data.get("pagination", {}).get("total", 0)

                print_success(f"Token 池共有 {total} 个 Token")

                public_tokens = [t for t in tokens if t.get("is_public")]
                print_info(f"  公开 Token: {len(public_tokens)} 个")

                active_tokens = [t for t in tokens if t.get("is_valid")]
                print_info(f"  有效 Token: {len(active_tokens)} 个")

                if len(public_tokens) == 0:
                    print_warning("\n⚠️  警告: 没有公开的 Token！")
                    print_info("超级 API Key 需要至少一个公开 Token 才能工作")
                    print_info("请在用户中心添加 Token 并设置为公开")

                return True
            else:
                print_error(f"获取 Token 池失败: HTTP {response.status_code}")
                return False

        except Exception as e:
            print_error(f"检查 Token 池异常: {e}")
            return False

    def run_full_test(self, user_id: int = 1):
        """运行完整测试"""
        print_header("🔑 超级 API Key 功能测试")
        print_info(f"测试目标: {self.base_url}")
        print_info(f"目标用户 ID: {user_id}")

        # 步骤 1: 登录
        if not self.login_admin():
            print_error("\n测试失败: 无法登录管理后台")
            return False

        # 步骤 2: 获取用户列表
        users = self.get_users()
        if not users:
            print_error("\n测试失败: 无法获取用户列表")
            return False

        # 检查目标用户是否存在
        target_user = next((u for u in users if u["id"] == user_id), None)
        if not target_user:
            print_warning(f"\n警告: 用户 ID {user_id} 不存在")
            if users:
                user_id = users[0]["id"]
                print_info(f"使用第一个用户: ID={user_id}, 用户名={users[0]['username']}")
            else:
                print_error("没有可用的用户")
                return False

        # 步骤 3: 创建超级 API Key
        api_key = self.create_super_api_key(user_id)
        if not api_key:
            print_error("\n测试失败: 无法创建超级 API Key")
            return False

        # 步骤 4: 测试超级 API Key
        if not self.test_super_api_key(api_key):
            print_warning("\n测试部分失败: 超级 API Key 无法使用")
            print_info("这可能是因为没有可用的公开 Token")

        # 步骤 5: 检查 Token 池
        self.check_token_pool()

        # 总结
        print_header("测试总结")
        print_success("✅ 管理员登录: 成功")
        print_success("✅ 获取用户列表: 成功")
        print_success("✅ 创建超级 API Key: 成功")
        print_info(f"✅ 生成的密钥: {api_key}")

        print_header("下一步操作")
        print_info("1. 保存上面生成的超级 API Key")
        print_info("2. 在用户中心添加公开 Token（如果还没有）")
        print_info("3. 使用超级 API Key 发送请求")
        print_info("4. 在管理后台查看使用统计")

        return True


def main():
    """主函数"""
    print(f"{Colors.BOLD}{Colors.OKCYAN}")
    print(r"""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║        🔑 超级 API Key 功能测试脚本                       ║
    ║                                                           ║
    ║        KiroGate v2.1.0                                    ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    print(Colors.ENDC)

    # 创建测试器
    tester = SuperAPIKeyTester()

    # 运行测试
    try:
        success = tester.run_full_test(user_id=1)

        if success:
            print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 测试完成！{Colors.ENDC}")
            sys.exit(0)
        else:
            print(f"\n{Colors.FAIL}{Colors.BOLD}❌ 测试失败{Colors.ENDC}")
            sys.exit(1)

    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}⚠️  测试被用户中断{Colors.ENDC}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ 测试异常: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
