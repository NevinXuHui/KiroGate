# 🚀 KiroGate 快速启动指南

本项目提供了多个跨平台启动脚本，方便在不同操作系统上快速运行 KiroGate。

## 📋 可用脚本

| 脚本文件 | 适用平台 | 说明 |
|---------|---------|------|
| `run.sh` | Linux / macOS / Git Bash | Bash 脚本 |
| `run.bat` | Windows (CMD) | 批处理脚本 |
| `run.ps1` | Windows / Linux / macOS | PowerShell 脚本（推荐） |

## 🖥️ Windows 用户

### 方式一：使用批处理脚本（推荐新手）

```cmd
# 启动服务
run.bat

# 开发模式
run.bat dev

# 使用 Docker
run.bat docker

# 查看帮助
run.bat help
```

### 方式二：使用 PowerShell 脚本（推荐）

```powershell
# 首次使用需要允许脚本执行
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 启动服务
.\run.ps1

# 开发模式
.\run.ps1 dev

# 使用 Docker
.\run.ps1 docker

# 查看帮助
.\run.ps1 help
```

### 方式三：使用 Git Bash

```bash
# 启动服务
./run.sh

# 开发模式
./run.sh dev

# 查看帮助
./run.sh help
```

## 🐧 Linux / macOS 用户

### 方式一：使用 Bash 脚本（推荐）

```bash
# 首次使用需要添加执行权限
chmod +x run.sh

# 启动服务
./run.sh

# 开发模式
./run.sh dev

# 使用 Docker
./run.sh docker

# 查看帮助
./run.sh help
```

### 方式二：使用 PowerShell 脚本

```bash
# 需要先安装 PowerShell (可选)
# macOS: brew install --cask powershell
# Linux: 参考 https://docs.microsoft.com/powershell/scripting/install/installing-powershell

# 启动服务
pwsh run.ps1

# 开发模式
pwsh run.ps1 dev
```

## 📚 完整命令列表

所有脚本都支持以下命令：

| 命令 | 说明 | 示例 |
|-----|------|------|
| `start` | 启动服务（默认，生产模式） | `./run.sh start` 或 `./run.sh` |
| `dev` | 开发模式启动（带热重载） | `./run.sh dev` |
| `docker` | 使用 Docker Compose 启动 | `./run.sh docker` |
| `docker-build` | 构建并启动 Docker 容器 | `./run.sh docker-build` |
| `stop` | 停止 Docker 服务 | `./run.sh stop` |
| `logs` | 查看 Docker 日志 | `./run.sh logs` |
| `test` | 运行测试 | `./run.sh test` |
| `install` | 安装 Python 依赖 | `./run.sh install` |
| `check` | 检查环境配置 | `./run.sh check` |
| `help` | 显示帮助信息 | `./run.sh help` |

## 🔧 首次运行步骤

### 1. 克隆项目

```bash
git clone https://github.com/aliom-v/KiroGate.git
cd KiroGate
```

### 2. 配置环境变量

所有脚本都会自动检查 `.env` 文件，如果不存在会提示从 `.env.example` 创建。

**手动创建：**

```bash
# Linux / macOS / Git Bash
cp .env.example .env

# Windows CMD
copy .env.example .env

# Windows PowerShell
Copy-Item .env.example .env
```

然后编辑 `.env` 文件，填写你的配置。

### 3. 安装依赖（可选）

脚本会自动检测虚拟环境，推荐创建虚拟环境：

```bash
# 使用脚本安装（推荐）
./run.sh install        # Linux / macOS / Git Bash
run.bat install         # Windows CMD
.\run.ps1 install       # Windows PowerShell

# 或手动安装
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 4. 启动服务

```bash
# Linux / macOS / Git Bash
./run.sh

# Windows CMD
run.bat

# Windows PowerShell
.\run.ps1
```

服务将在 `http://localhost:8000` 启动 🎉

## 🐳 Docker 部署

### 快速启动

```bash
# Linux / macOS / Git Bash
./run.sh docker

# Windows CMD
run.bat docker

# Windows PowerShell
.\run.ps1 docker
```

### 查看日志

```bash
# Linux / macOS / Git Bash
./run.sh logs

# Windows CMD
run.bat logs

# Windows PowerShell
.\run.ps1 logs
```

### 停止服务

```bash
# Linux / macOS / Git Bash
./run.sh stop

# Windows CMD
run.bat stop

# Windows PowerShell
.\run.ps1 stop
```

## 🛠️ 开发模式

开发模式会启用热重载，代码修改后自动重启服务：

```bash
# Linux / macOS / Git Bash
./run.sh dev

# Windows CMD
run.bat dev

# Windows PowerShell
.\run.ps1 dev
```

## ✅ 环境检查

在启动前可以先检查环境是否配置正确：

```bash
# Linux / macOS / Git Bash
./run.sh check

# Windows CMD
run.bat check

# Windows PowerShell
.\run.ps1 check
```

脚本会自动检查：
- ✅ Python 版本（需要 3.10+）
- ✅ `.env` 配置文件是否存在
- ✅ 虚拟环境状态

## 🧪 运行测试

```bash
# Linux / macOS / Git Bash
./run.sh test

# Windows CMD
run.bat test

# Windows PowerShell
.\run.ps1 test
```

## ⚠️ 常见问题

### Windows PowerShell 报错 "无法加载文件，因为在此系统上禁止运行脚本"

**解决方案：**

```powershell
# 以管理员身份运行 PowerShell，执行：
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 或者仅针对当前会话：
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

### Linux / macOS 提示 "Permission denied"

**解决方案：**

```bash
# 添加执行权限
chmod +x run.sh

# 然后重新运行
./run.sh
```

### Git Bash 在 Windows 上中文乱码

**解决方案：**

```bash
# 设置 Git Bash 编码为 UTF-8
echo 'export LANG=zh_CN.UTF-8' >> ~/.bashrc
source ~/.bashrc
```

或者使用 `run.bat` 或 `run.ps1` 脚本，对中文支持更好。

## 📖 更多信息

详细的配置说明和 API 文档请参考主 README：
- [README.md](README.md)

项目地址：https://github.com/aliom-v/KiroGate

## 📄 许可证

AGPL-3.0 License - 详见 [LICENSE](LICENSE)
