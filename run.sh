#!/bin/bash

# KiroGate 启动脚本
# 用于快速启动 KiroGate 服务

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 Python 版本
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 未安装，请先安装 Python 3.8+"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_info "检测到 Python 版本: $PYTHON_VERSION"
}

# 检查虚拟环境
check_venv() {
    if [ ! -d "venv" ]; then
        print_warning "虚拟环境不存在，正在创建..."
        python3 -m venv venv
        print_success "虚拟环境创建完成"
    fi
}

# 激活虚拟环境
activate_venv() {
    print_info "激活虚拟环境..."
    source venv/bin/activate
}

# 安装依赖
install_deps() {
    if [ ! -f "venv/installed" ]; then
        print_info "安装依赖包..."
        pip install -q --upgrade pip
        pip install -q -r requirements.txt
        touch venv/installed
        print_success "依赖安装完成"
    else
        print_info "依赖已安装，跳过安装步骤"
    fi
}

# 检查 .env 文件
check_env() {
    if [ ! -f ".env" ]; then
        print_warning ".env 文件不存在"
        if [ -f ".env.example" ]; then
            print_info "从 .env.example 复制配置文件..."
            cp .env.example .env
            print_warning "请编辑 .env 文件配置你的凭证"
            exit 0
        else
            print_error "未找到 .env 或 .env.example 文件"
            exit 1
        fi
    fi
}

# 创建必要的目录
create_dirs() {
    mkdir -p data
    mkdir -p debug_logs
}

# 启动服务
start_service() {
    print_info "启动 KiroGate 服务..."
    print_info "访问地址: http://localhost:9000"
    print_info "按 Ctrl+C 停止服务"
    echo ""

    # 使用 uvicorn 启动（main.py 在根目录）
    python -m uvicorn main:app --host 0.0.0.0 --port 9000 --reload
}

# 主函数
main() {
    print_info "KiroGate 启动脚本"
    echo ""
    
    check_python
    check_venv
    activate_venv
    install_deps
    check_env
    create_dirs
    start_service
}

# 运行主函数
main
