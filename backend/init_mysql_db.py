#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL数据库初始化脚本
创建pbl数据库及所有数据表
"""

import sys
import io
import pymysql
from werkzeug.security import generate_password_hash
from flask import Flask
from models import db, User, Role, UserRole, Category
from datetime import datetime

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# MySQL连接配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'charset': 'utf8mb4'
}

DB_NAME = 'pbl'


def create_database():
    """创建MySQL数据库"""
    try:
        print(f"正在连接MySQL服务器...")
        connection = pymysql.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()

        # 检查数据库是否存在
        cursor.execute(f"SHOW DATABASES LIKE '{DB_NAME}'")
        result = cursor.fetchone()

        if result:
            print(f"数据库 '{DB_NAME}' 已存在")
        else:
            # 创建数据库
            cursor.execute(f"CREATE DATABASE {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✓ 成功创建数据库 '{DB_NAME}'")

        cursor.close()
        connection.close()
        return True

    except Exception as e:
        print(f"✗ 创建数据库失败: {e}")
        return False


def init_flask_app():
    """初始化Flask应用"""
    app = Flask(__name__)

    # 配置数据库连接
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:123456@localhost/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
        'pool_size': 10,
        'max_overflow': 20
    }

    # 初始化数据库
    db.init_app(app)

    return app


def create_tables():
    """创建所有数据表"""
    try:
        app = init_flask_app()

        with app.app_context():
            print("正在创建数据表...")

            # 删除所有表（如果存在，谨慎使用）
            # db.drop_all()

            # 创建所有表
            db.create_all()

            print("✓ 成功创建所有数据表")

            # 初始化基础数据
            init_base_data()

            return True

    except Exception as e:
        print(f"✗ 创建数据表失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def init_base_data():
    """初始化基础数据"""
    try:
        print("\n正在初始化基础数据...")

        # 1. 创建角色
        if not Role.query.filter_by(name='管理员').first():
            admin_role = Role(name='管理员', description='系统管理员，拥有所有权限')
            db.session.add(admin_role)
            print("  ✓ 创建角色：管理员")

        if not Role.query.filter_by(name='普通用户').first():
            user_role = Role(name='普通用户', description='普通用户，可以发布菜谱、评论、点赞和收藏')
            db.session.add(user_role)
            print("  ✓ 创建角色：普通用户")

        db.session.flush()  # 刷新以获取角色ID

        # 2. 创建默认管理员账号
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@recipe.com',
                password_hash=generate_password_hash('admin123'),
                created_at=datetime.utcnow()
            )
            db.session.add(admin_user)
            db.session.flush()  # 刷新以获取用户ID

            # 分配管理员角色
            admin_role = Role.query.filter_by(name='管理员').first()
            user_role = UserRole(user_id=admin_user.id, role_id=admin_role.id)
            db.session.add(user_role)
            print("  ✓ 创建默认管理员账号")
            print("    用户名: admin")
            print("    密码: admin123")
            print("    邮箱: admin@recipe.com")

        # 3. 创建测试用户
        test_user = User.query.filter_by(username='testuser').first()
        if not test_user:
            test_user = User(
                username='testuser',
                email='test@recipe.com',
                password_hash=generate_password_hash('test123'),
                created_at=datetime.utcnow()
            )
            db.session.add(test_user)
            db.session.flush()

            # 分配普通用户角色
            user_role_obj = Role.query.filter_by(name='普通用户').first()
            test_user_role = UserRole(user_id=test_user.id, role_id=user_role_obj.id)
            db.session.add(test_user_role)
            print("  ✓ 创建测试用户账号")
            print("    用户名: testuser")
            print("    密码: test123")
            print("    邮箱: test@recipe.com")

        # 4. 创建默认分类
        categories = [
            {'name': '家常菜', 'description': '简单易做的家常菜谱', 'sort_order': 1},
            {'name': '川菜', 'description': '四川风味菜谱', 'sort_order': 2},
            {'name': '粤菜', 'description': '广东风味菜谱', 'sort_order': 3},
            {'name': '湘菜', 'description': '湖南风味菜谱', 'sort_order': 4},
            {'name': '西餐', 'description': '西式餐点', 'sort_order': 5},
            {'name': '甜品', 'description': '各种甜品制作', 'sort_order': 6},
            {'name': '汤羹', 'description': '各种汤品', 'sort_order': 7},
            {'name': '素食', 'description': '素食菜谱', 'sort_order': 8},
        ]

        for cat_data in categories:
            if not Category.query.filter_by(name=cat_data['name']).first():
                category = Category(
                    name=cat_data['name'],
                    description=cat_data['description'],
                    sort_order=cat_data['sort_order']
                )
                db.session.add(category)
                print(f"  ✓ 创建分类：{cat_data['name']}")

        # 提交所有更改
        db.session.commit()
        print("\n✓ 基础数据初始化完成")

        # 显示数据库统计信息
        print("\n数据库统计：")
        print(f"  - 用户数: {User.query.count()}")
        print(f"  - 角色数: {Role.query.count()}")
        print(f"  - 分类数: {Category.query.count()}")

    except Exception as e:
        print(f"✗ 初始化基础数据失败: {e}")
        db.session.rollback()
        raise


def show_tables():
    """显示数据库中的所有表"""
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database=DB_NAME,
            charset='utf8mb4'
        )
        cursor = connection.cursor()

        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        print(f"\n数据库 '{DB_NAME}' 中的表：")
        for table in tables:
            print(f"  - {table[0]}")

        cursor.close()
        connection.close()

    except Exception as e:
        print(f"✗ 查询数据表失败: {e}")


def main():
    """主函数"""
    print("=" * 60)
    print("菜谱分享系统 - MySQL数据库初始化")
    print("=" * 60)

    # 1. 创建数据库
    if not create_database():
        print("\n初始化失败！")
        sys.exit(1)

    # 2. 创建数据表
    if not create_tables():
        print("\n初始化失败！")
        sys.exit(1)

    # 3. 显示所有表
    show_tables()

    print("\n" + "=" * 60)
    print("数据库初始化完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
