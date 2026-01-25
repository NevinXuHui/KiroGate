# 🎯 KiroGate 启动脚本使用总结

## ✅ 已创建的启动脚本

我已经为 KiroGate 项目创建了完整的跨平台启动脚本套件：

| 文件 | 平台 | 说明 |
|------|------|------|
| `run` | 🌐 通用 | 自动检测系统并选择合适的脚本 |
| `run.sh` | 🐧 Linux/macOS/Git Bash | Bash 脚本，功能最完善 |
| `run.bat` | 🪟 Windows CMD | Windows 批处理脚本 |
| `run.ps1` | ⚡ PowerShell | 跨平台 PowerShell 脚本 |

## 🚀 快速开始

### Windows 用户（三选一）

```cmd
# 方式1: 批处理脚本（最简单）
run.bat
run.bat dev
run.bat help

# 方式2: PowerShell（推荐）
.\run.ps1
.\run.ps1 dev
.\run.ps1 help

# 方式3: Git Bash
./run.sh
./run.sh dev
./run.sh help
```

### Linux / macOS 用户

```bash
# 直接运行（推荐）
./run.sh
./run.sh dev
./run.sh help

# 或使用通用启动器
./run
./run dev
```

## 📋 所有可用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `start` | 启动服务（生产模式，默认） | `./run.sh start` |
| `dev` | 开发模式（热重载） | `./run.sh dev` |
| `docker` | Docker Compose 启动 | `./run.sh docker` |
| `docker-build` | 构建并启动 Docker | `./run.sh docker-build` |
| `stop` | 停止 Docker 服务 | `./run.sh stop` |
| `logs` | 查看 Docker 日志 | `./run.sh logs` |
| `test` | 运行测试 | `./run.sh test` |
| `install` | 安装依赖 | `./run.sh install` |
| `check` | 检查环境配置 | `./run.sh check` |
| `help` | 显示帮助 | `./run.sh help` |

## ✨ 脚本特性

### 🔍 智能检测
- ✅ 自动检测 Python 版本（需要 3.10+）
- ✅ 自动检查 .env 配置文件
- ✅ 自动检测并激活虚拟环境
- ✅ 自动创建必要的数据目录

### 🎨 友好输出
- ✅ 彩色日志输出（INFO/SUCCESS/WARNING/ERROR）
- ✅ 中文界面友好
- ✅ 清晰的错误提示

### 🛡️ 错误处理
- ✅ 完善的错误检测和提示
- ✅ 缺少依赖自动提示安装
- ✅ 配置文件缺失自动引导创建

## 📝 典型使用流程

### 首次运行

```bash
# 1. 克隆项目
git clone https://github.com/aliom-v/KiroGate.git
cd KiroGate

# 2. 检查环境（脚本会自动提示创建 .env）
./run.sh check
# 或: run.bat check (Windows)

# 3. 安装依赖
./run.sh install
# 或: run.bat install (Windows)

# 4. 启动服务
./run.sh
# 或: run.bat (Windows)
```

### 开发时使用

```bash
# 启动开发服务器（热重载）
./run.sh dev

# 代码会自动监听修改并重启
```

### Docker 部署

```bash
# 启动 Docker 容器
./run.sh docker

# 查看日志
./run.sh logs

# 停止服务
./run.sh stop
```

## 🔧 Windows 特别说明

### PowerShell 执行策略

首次使用 `run.ps1` 时，可能需要设置执行策略：

```powershell
# 设置允许本地脚本执行
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 推荐使用顺序

1. **run.bat** - 最简单，无需额外配置
2. **run.ps1** - 功能最完善，彩色输出最好
3. **run.sh** - 在 Git Bash 中使用

## 🐧 Linux/macOS 特别说明

### 添加执行权限

```bash
# 添加执行权限（首次使用）
chmod +x run.sh

# 或者使用已经添加权限的脚本
./run.sh
```

## 🎓 进阶用法

### 使用虚拟环境

脚本会自动检测并提示创建虚拟环境：

```bash
# 脚本会询问是否创建虚拟环境
./run.sh install

# 手动创建虚拟环境
python -m venv venv

# 再次运行脚本，会自动激活虚拟环境
./run.sh
```

### Docker 快速重建

```bash
# 代码修改后重新构建并启动
./run.sh docker-build
```

### 运行测试

```bash
# 自动安装 pytest 并运行测试
./run.sh test
```

## 📖 相关文档

- **QUICKSTART.md** - 详细的快速启动指南
- **README.md** - 完整的项目文档
- **run.sh help** - 查看帮助信息

## 🆘 常见问题

### ❓ 脚本无法执行

**Linux/macOS:**
```bash
chmod +x run.sh
```

**Windows PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### ❓ Python 版本过低

脚本会自动检测，需要 Python 3.10+

下载地址: https://www.python.org/downloads/

### ❓ .env 文件不存在

脚本会自动提示从 `.env.example` 创建，按提示操作即可。

### ❓ Docker 启动失败

确保 Docker Desktop 已安装并正在运行：
- Windows: https://www.docker.com/products/docker-desktop
- Mac: https://www.docker.com/products/docker-desktop
- Linux: https://docs.docker.com/engine/install/

## 🎉 总结

现在你可以使用这些启动脚本轻松管理 KiroGate 项目了！

**最简单的启动方式：**

```bash
# Windows
run.bat

# Linux/macOS/Git Bash
./run.sh
```

祝使用愉快！ 🚀
