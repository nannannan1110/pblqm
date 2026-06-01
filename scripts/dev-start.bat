@echo off
REM 菜谱分享系统开发环境启动脚本 (Windows版本)
REM 作者: 开发团队
REM 版本: 1.0.0

echo 🔧 启动菜谱分享系统开发环境...

REM 进入项目根目录
cd /d "%~dp0.."

REM 检查是否存在 .env 文件
if not exist "backend\.env" (
    echo 📝 创建后端环境配置文件...
    copy "backend\.env.example" "backend\.env"
    echo ⚠️  请编辑 backend\.env 文件配置您的环境变量
)

REM 启动后端服务
echo 🚀 启动后端服务...
cd backend

REM 检查 Python 环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安装，请先安装 Python
    pause
    exit /b 1
)

REM 检查虚拟环境
if not exist "venv" (
    echo 📦 创建 Python 虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 🔌 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo 📚 安装 Python 依赖...
pip install -r requirements.txt

REM 初始化数据库
echo 💾 初始化数据库...
python init_db.py

REM 创建种子数据（仅开发环境）
echo 🌱 创建种子数据...
python seed_data.py

REM 启动后端服务（后台运行）
echo 🚀 启动后端服务（端口 5000）...
start "Backend Server" python run-dev.py

REM 返回项目根目录
cd ..

REM 启动前端服务
echo 🎨 启动前端服务...
cd frontend

REM 检查 Node.js 环境
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js/npm 未安装，请先安装 Node.js
    pause
    exit /b 1
)

REM 安装依赖
if not exist "node_modules" (
    echo 📚 安装 Node.js 依赖...
    npm install
)

REM 启动前端服务
echo 🚀 启动前端服务（端口 8080）...
start "Frontend Server" npm run serve

echo ✅ 开发环境启动完成！
echo 🌐 前端地址: http://localhost:8080
echo 🔧 后端API: http://localhost:5000
echo.
echo 关闭此窗口不会停止服务，请手动关闭各个服务窗口
pause