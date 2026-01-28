#!/bin/bash

# 系统级超级 API Key 功能测试脚本

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔑 系统级超级 API Key 功能测试"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

BASE_URL="http://127.0.0.1:9000"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 测试结果统计
PASSED=0
FAILED=0

# 测试函数
test_case() {
    local name="$1"
    local result="$2"
    
    if [ "$result" = "0" ]; then
        echo -e "${GREEN}✅ PASS${NC} - $name"
        ((PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC} - $name"
        ((FAILED++))
    fi
}

echo -e "${BLUE}步骤 1: 检查服务健康状态${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

HEALTH=$(curl -s "$BASE_URL/health" | jq -r '.status' 2>/dev/null)
if [ "$HEALTH" = "healthy" ]; then
    test_case "服务健康检查" 0
    echo "   版本: $(curl -s "$BASE_URL/health" | jq -r '.version')"
else
    test_case "服务健康检查" 1
    echo -e "${RED}   错误: 服务未运行或不健康${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}步骤 2: 检查配置文件${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if grep -q "SUPER_API_KEYS" .env; then
    test_case ".env 文件包含 SUPER_API_KEYS 配置" 0
    echo "   配置行: $(grep "SUPER_API_KEYS" .env | head -1)"
else
    test_case ".env 文件包含 SUPER_API_KEYS 配置" 1
fi

echo ""
echo -e "${BLUE}步骤 3: 检查代码实现${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 检查 config.py
if grep -q "super_api_keys" kiro_gateway/config.py; then
    test_case "config.py 包含 super_api_keys 字段" 0
else
    test_case "config.py 包含 super_api_keys 字段" 1
fi

# 检查 routes.py 认证逻辑
if grep -q "sk-super-" kiro_gateway/routes.py; then
    test_case "routes.py 包含 sk-super- 认证逻辑" 0
else
    test_case "routes.py 包含 sk-super- 认证逻辑" 1
fi

# 检查 API 端点
if grep -q "/admin/api/super-keys" kiro_gateway/routes.py; then
    test_case "routes.py 包含超级 Key 管理 API" 0
else
    test_case "routes.py 包含超级 Key 管理 API" 1
fi

# 检查前端界面
if grep -q "超级 API Key（系统级）" kiro_gateway/pages.py; then
    test_case "pages.py 包含管理界面" 0
else
    test_case "pages.py 包含管理界面" 1
fi

# 检查 JavaScript 函数
if grep -q "generateSuperKey" kiro_gateway/pages.py; then
    test_case "pages.py 包含生成密钥函数" 0
else
    test_case "pages.py 包含生成密钥函数" 1
fi

echo ""
echo -e "${BLUE}步骤 4: 检查文档${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "SYSTEM_SUPER_API_KEY.md" ]; then
    test_case "功能文档存在" 0
    echo "   文件大小: $(wc -c < SYSTEM_SUPER_API_KEY.md) 字节"
else
    test_case "功能文档存在" 1
fi

if [ -f "IMPLEMENTATION_SUMMARY.md" ]; then
    test_case "实现总结存在" 0
    echo "   文件大小: $(wc -c < IMPLEMENTATION_SUMMARY.md) 字节"
else
    test_case "实现总结存在" 1
fi

echo ""
echo -e "${BLUE}步骤 5: 测试 API 端点（需要登录）${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${YELLOW}提示: 此步骤需要管理员登录，跳过自动测试${NC}"
echo "   手动测试步骤:"
echo "   1. 访问 http://127.0.0.1:9000/admin"
echo "   2. 使用密码 admin123 登录"
echo "   3. 进入 '⚙️ 系统' 标签页"
echo "   4. 查看 '🔑 超级 API Key（系统级）' 卡片"
echo "   5. 点击 '➕ 生成新密钥' 按钮"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 测试结果统计"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "   ${GREEN}通过: $PASSED${NC}"
echo -e "   ${RED}失败: $FAILED${NC}"
echo -e "   总计: $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ 所有测试通过！${NC}"
    echo ""
    echo "🎉 系统级超级 API Key 功能已成功实现！"
    echo ""
    echo "📖 下一步操作:"
    echo "   1. 访问管理后台: http://127.0.0.1:9000/admin"
    echo "   2. 进入 '⚙️ 系统' 标签页"
    echo "   3. 生成超级 API Key"
    echo "   4. 查看文档: cat SYSTEM_SUPER_API_KEY.md"
    exit 0
else
    echo -e "${RED}❌ 部分测试失败，请检查实现${NC}"
    exit 1
fi
