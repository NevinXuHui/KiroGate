#!/bin/bash
# 完整性测试 - 验证所有启动脚本

echo "=========================================="
echo "  🧪 KiroGate 启动脚本完整性测试"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 计数器
total=0
passed=0
failed=0

# 测试函数
test_file() {
    local file=$1
    local description=$2
    total=$((total + 1))

    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ PASS${NC} - $description ($file)"
        passed=$((passed + 1))
    else
        echo -e "${RED}❌ FAIL${NC} - $description ($file)"
        failed=$((failed + 1))
    fi
}

# 测试文件可执行性
test_executable() {
    local file=$1
    local description=$2
    total=$((total + 1))

    if [ -x "$file" ]; then
        echo -e "${GREEN}✅ PASS${NC} - $description 可执行 ($file)"
        passed=$((passed + 1))
    else
        echo -e "${YELLOW}⚠️  WARN${NC} - $description 不可执行 ($file)"
    fi
}

echo -e "${BLUE}📋 检查启动脚本...${NC}"
echo ""

test_file "run.sh" "Bash 启动脚本"
test_executable "run.sh" "Bash 脚本"

test_file "run.bat" "Windows 批处理脚本"

test_file "run.ps1" "PowerShell 脚本"
test_executable "run.ps1" "PowerShell 脚本"

test_file "run" "通用启动器"
test_executable "run" "通用启动器"

test_file "启动.bat" "Windows 快速启动（中文）"

echo ""
echo -e "${BLUE}📖 检查文档文件...${NC}"
echo ""

test_file "QUICKSTART.md" "快速启动指南"
test_file "SCRIPTS_GUIDE.md" "脚本使用指南"
test_file "SCRIPTS_SUMMARY.md" "完成总结文档"
test_file "启动脚本使用说明.md" "中文使用说明"

echo ""
echo -e "${BLUE}🎬 检查演示脚本...${NC}"
echo ""

test_file "demo-scripts.sh" "功能演示脚本"
test_executable "demo-scripts.sh" "演示脚本"

echo ""
echo "=========================================="
echo -e "  测试结果: ${GREEN}$passed 通过${NC} / ${RED}$failed 失败${NC} / 总计 $total"
echo "=========================================="
echo ""

# 测试脚本功能
if [ -f "run.sh" ] && [ -x "run.sh" ]; then
    echo -e "${BLUE}🔧 测试 run.sh 基本功能...${NC}"
    echo ""

    # 测试 help 命令
    if ./run.sh help > /dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} run.sh help - 工作正常"
    else
        echo -e "${RED}❌${NC} run.sh help - 执行失败"
    fi

    echo ""
fi

# 显示文件大小
echo -e "${BLUE}📊 文件大小统计...${NC}"
echo ""
ls -lh run* *.md 启动.bat demo-scripts.sh 2>/dev/null | grep -v "^d" | awk '{printf "  %-30s %8s\n", $9, $5}'

echo ""
echo "=========================================="
echo "  ✅ 完整性测试完成！"
echo "=========================================="
echo ""
echo -e "${YELLOW}💡 提示：${NC}"
echo "  - 运行 ./demo-scripts.sh 查看功能演示"
echo "  - 运行 ./run.sh help 查看帮助信息"
echo "  - 阅读 QUICKSTART.md 了解详细用法"
echo ""
