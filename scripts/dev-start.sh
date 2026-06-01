#!/bin/bash
echo "🚀 启动开发环境..."

# 启动后端
echo "启动后端服务..."
cd ../backend
source venv/bin/activate 2>/dev/null || python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export FLASK_ENV=development
python app.py &
BACKEND_PID=$!

# 启动前端
echo "启动前端服务..."
cd ../frontend
npm install
npm run serve &
FRONTEND_PID=$!

echo "✅ 开发环境启动完成！"
echo "前端: http://localhost:8080"
echo "后端: http://localhost:5000"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待用户中断
trap "echo '停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
