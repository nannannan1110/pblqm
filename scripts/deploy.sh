#!/bin/bash

# 菜谱分享系统部署脚本
# 作者: 开发团队
# 版本: 1.0.0

set -e

echo "🚀 开始部署菜谱分享系统..."

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 进入项目根目录
cd "$(dirname "$0")/.."

# 停止现有服务
echo "🛑 停止现有服务..."
docker-compose down

# 构建镜像
echo "🔨 构建 Docker 镜像..."
docker-compose build

# 启动服务
echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 30

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose ps

# 初始化数据库
echo "💾 初始化数据库..."
docker-compose exec backend python init_db.py

# 创建种子数据
echo "🌱 创建种子数据..."
docker-compose exec backend python seed_data.py

echo "✅ 部署完成！"
echo "🌐 前端地址: http://localhost:8080"
echo "🔧 后端API: http://localhost:5000"
echo "📊 API文档: http://localhost:5000/api/docs"

# 显示日志
echo "📋 显示服务日志 (Ctrl+C 退出):"
docker-compose logs -f