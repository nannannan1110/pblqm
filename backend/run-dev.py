#!/usr/bin/env python3
"""
开发环境启动脚本
用于快速启动Flask开发服务器
"""

import os
import sys
from app import create_app
from models import db
from app.models.user import User
from app.models.recipe import Recipe

def init_database():
    """初始化数据库"""
    app = create_app()
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("✅ 数据库表创建成功")

        # 创建测试用户
        if not User.query.filter_by(email='admin@example.com').first():
            admin_user = User(
                username='admin',
                email='admin@example.com',
                bio='系统管理员'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)

            # 创建测试菜谱
            test_recipe = Recipe(
                title='番茄炒蛋',
                description='简单美味的家常菜',
                ingredients='番茄2个、鸡蛋3个、盐适量、葱花少许',
                instructions='1. 番茄切块；2. 鸡蛋打散；3. 热锅放油；4. 先炒鸡蛋盛起；5. 炒番茄；6. 加入鸡蛋翻炒',
                prep_time=10,
                cook_time=15,
                difficulty='简单',
                servings=2,
                user_id=1
            )
            db.session.add(test_recipe)

            db.session.commit()
            print("✅ 测试数据创建成功")
            print("管理员账号: admin@example.com / admin123")
        else:
            print("✅ 测试数据已存在")

def main():
    """主函数"""
    print("🚀 菜谱分享系统后端启动中...")

    try:
        # 初始化数据库
        init_database()

        # 创建Flask应用
        app = create_app()

        # 启动开发服务器
        print("🌐 开发服务器启动在 http://localhost:5000")
        print("📖 API文档: http://localhost:5000/api")
        print("🔧 调试模式: 开启")
        print("⏹️  按 Ctrl+C 停止服务器")

        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )

    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()