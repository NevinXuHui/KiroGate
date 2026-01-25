@echo off
REM KiroGate 启动脚本 (Windows)
REM 用法: run.bat [选项]
REM
REM 选项:
REM   start       - 启动服务（默认）
REM   dev         - 开发模式启动（带热重载）
REM   docker      - 使用 Docker Compose 启动
REM   docker-build - 构建并启动 Docker 容器
REM   stop        - 停止 Docker 服务
REM   logs        - 查看 Docker 日志
REM   test        - 运行测试
REM   install     - 安装依赖
REM   check       - 检查环境配置
REM   help        - 显示帮助信息

setlocal enabledelayedexpansion

REM 设置代码页为 UTF-8 支持中文
chcp 65001 >nul 2>&1

REM 颜色代码（Windows 10+ 支持 ANSI）
set "INFO=[94m[INFO][0m"
set "SUCCESS=[92m[SUCCESS][0m"
set "WARNING=[93m[WARNING][0m"
set "ERROR=[91m[ERROR][0m"

REM 获取命令参数，默认为 start
set "COMMAND=%~1"
if "%COMMAND%"=="" set "COMMAND=start"

REM 执行对应命令
if /i "%COMMAND%"=="start" goto :start_server
if /i "%COMMAND%"=="dev" goto :start_dev
if /i "%COMMAND%"=="docker" goto :docker_start
if /i "%COMMAND%"=="docker-build" goto :docker_build
if /i "%COMMAND%"=="stop" goto :docker_stop
if /i "%COMMAND%"=="logs" goto :docker_logs
if /i "%COMMAND%"=="test" goto :run_tests
if /i "%COMMAND%"=="install" goto :install_dependencies
if /i "%COMMAND%"=="check" goto :check_env
if /i "%COMMAND%"=="help" goto :show_help
if /i "%COMMAND%"=="--help" goto :show_help
if /i "%COMMAND%"=="-h" goto :show_help

echo %ERROR% 未知选项: %COMMAND%
goto :show_help

REM ========================================
REM 检查 Python
REM ========================================
:check_python
python --version >nul 2>&1
if errorlevel 1 (
    echo %ERROR% Python 未安装，请先安装 Python 3.10+
    echo.
    echo 下载地址: https://www.python.org/downloads/
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo %INFO% Python 版本: %PYTHON_VERSION%

REM 检查版本是否 >= 3.10
python -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if errorlevel 1 (
    echo %ERROR% Python 版本过低，需要 3.10+，当前版本: %PYTHON_VERSION%
    exit /b 1
)
exit /b 0

REM ========================================
REM 检查环境配置
REM ========================================
:check_env
echo %INFO% 检查环境配置...

if not exist ".env" (
    echo %WARNING% .env 文件不存在
    if exist ".env.example" (
        echo.
        set /p response="是否从 .env.example 创建 .env？(y/n): "
        if /i "!response!"=="y" (
            copy .env.example .env >nul
            echo %SUCCESS% .env 文件已创建，请编辑配置后重新运行
            exit /b 0
        ) else (
            echo %ERROR% 需要 .env 文件才能运行
            exit /b 1
        )
    ) else (
        echo %ERROR% 未找到 .env.example 文件
        exit /b 1
    )
) else (
    echo %SUCCESS% 环境配置文件存在
)

if "%~1"=="check_only" exit /b 0
goto :eof

REM ========================================
REM 安装依赖
REM ========================================
:install_dependencies
echo %INFO% 安装 Python 依赖...

call :check_python
if errorlevel 1 exit /b 1

if not exist "requirements.txt" (
    echo %ERROR% requirements.txt 文件不存在
    exit /b 1
)

REM 检查虚拟环境
if not exist "venv" (
    echo %INFO% 检测到未创建虚拟环境
    set /p response="是否创建虚拟环境？(y/n): "
    if /i "!response!"=="y" (
        echo %INFO% 创建虚拟环境...
        python -m venv venv
        echo %SUCCESS% 虚拟环境已创建
    )
)

REM 激活虚拟环境
if exist "venv\Scripts\activate.bat" (
    echo %INFO% 激活虚拟环境...
    call venv\Scripts\activate.bat
)

echo %INFO% 安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo %ERROR% 依赖安装失败
    exit /b 1
)

echo %SUCCESS% 依赖安装完成
exit /b 0

REM ========================================
REM 启动服务（生产模式）
REM ========================================
:start_server
echo %INFO% 启动 KiroGate 服务器...

call :check_python
if errorlevel 1 exit /b 1

call :check_env check_only
if errorlevel 1 exit /b 1

REM 创建数据目录
if not exist "data" mkdir data

REM 激活虚拟环境
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

echo.
echo %SUCCESS% 服务器启动中... (http://localhost:8000)
echo.
python main.py
exit /b 0

REM ========================================
REM 开发模式（热重载）
REM ========================================
:start_dev
echo %INFO% 启动开发模式（热重载）...

call :check_python
if errorlevel 1 exit /b 1

call :check_env check_only
if errorlevel 1 exit /b 1

REM 创建数据目录
if not exist "data" mkdir data

REM 激活虚拟环境
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

echo.
echo %SUCCESS% 开发服务器启动中... (http://localhost:8000)
echo.
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
exit /b 0

REM ========================================
REM Docker Compose 启动
REM ========================================
:docker_start
echo %INFO% 使用 Docker Compose 启动...

docker --version >nul 2>&1
if errorlevel 1 (
    echo %ERROR% Docker 未安装
    echo.
    echo 下载地址: https://www.docker.com/products/docker-desktop
    exit /b 1
)

call :check_env check_only
if errorlevel 1 exit /b 1

REM 优先使用 docker compose，回退到 docker-compose
docker compose version >nul 2>&1
if errorlevel 1 (
    docker-compose up -d
) else (
    docker compose up -d
)

if errorlevel 1 (
    echo %ERROR% Docker 启动失败
    exit /b 1
)

echo.
echo %SUCCESS% Docker 容器已启动
echo %INFO% 查看日志: run.bat logs
exit /b 0

REM ========================================
REM Docker 构建并启动
REM ========================================
:docker_build
echo %INFO% 构建并启动 Docker 容器...

docker --version >nul 2>&1
if errorlevel 1 (
    echo %ERROR% Docker 未安装
    echo.
    echo 下载地址: https://www.docker.com/products/docker-desktop
    exit /b 1
)

call :check_env check_only
if errorlevel 1 exit /b 1

REM 优先使用 docker compose，回退到 docker-compose
docker compose version >nul 2>&1
if errorlevel 1 (
    docker-compose up -d --build
) else (
    docker compose up -d --build
)

if errorlevel 1 (
    echo %ERROR% Docker 构建失败
    exit /b 1
)

echo.
echo %SUCCESS% Docker 容器已构建并启动
echo %INFO% 查看日志: run.bat logs
exit /b 0

REM ========================================
REM 停止 Docker 服务
REM ========================================
:docker_stop
echo %INFO% 停止 Docker 服务...

docker compose version >nul 2>&1
if errorlevel 1 (
    docker-compose down
) else (
    docker compose down
)

echo %SUCCESS% Docker 服务已停止
exit /b 0

REM ========================================
REM 查看 Docker 日志
REM ========================================
:docker_logs
echo %INFO% 查看 Docker 日志...
echo.

docker compose version >nul 2>&1
if errorlevel 1 (
    docker-compose logs -f
) else (
    docker compose logs -f
)
exit /b 0

REM ========================================
REM 运行测试
REM ========================================
:run_tests
echo %INFO% 运行测试...

call :check_python
if errorlevel 1 exit /b 1

REM 激活虚拟环境
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM 检查 pytest 是否安装
pytest --version >nul 2>&1
if errorlevel 1 (
    echo %WARNING% pytest 未安装，安装中...
    pip install pytest
)

if exist "tests" (
    pytest tests\ -v
) else (
    echo %WARNING% tests 目录不存在
)
exit /b 0

REM ========================================
REM 显示帮助信息
REM ========================================
:show_help
echo.
echo KiroGate 启动脚本 (Windows)
echo.
echo 用法: run.bat [选项]
echo.
echo 选项:
echo   start           启动服务（默认，生产模式）
echo   dev             开发模式启动（带热重载）
echo   docker          使用 Docker Compose 启动
echo   docker-build    构建并启动 Docker 容器
echo   stop            停止 Docker 服务
echo   logs            查看 Docker 日志
echo   test            运行测试
echo   install         安装 Python 依赖
echo   check           检查环境配置
echo   help            显示此帮助信息
echo.
echo 示例:
echo   run.bat                  # 启动服务
echo   run.bat dev              # 开发模式
echo   run.bat docker           # Docker 启动
echo   run.bat logs             # 查看日志
echo.
echo 更多信息: https://github.com/aliom-v/KiroGate
echo.
exit /b 0
