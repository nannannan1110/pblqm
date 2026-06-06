#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化演示数据
"""

import os
import sys
import io

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 确保我们能找到项目模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def init_database():
    """初始化数据库"""
    print("开始初始化演示数据库...")
    
    try:
        # 导入应用和数据库 - 需要直接导入app.py文件
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # 使用 importlib 来导入 app.py
        import importlib.util
        spec = importlib.util.spec_from_file_location("app_py", os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py"))
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)
        
        from models import db, User, Recipe
        
        # 创建应用
        app = app_module.create_app()
        
        with app.app_context():
            # 检查是否已有用户
            if User.query.count() > 0:
                print("数据库中已有用户数据，跳过初始化")
                return
            
            # 创建所有表
            print("创建数据库表...")
            db.create_all()
            
            # 创建用户
            print("创建用户...")
            admin_user = User(username='admin', email='admin@example.com', is_admin=True)
            admin_user.set_password('admin123')
            
            normal_user = User(username='user1', email='user1@example.com', is_admin=False)
            normal_user.set_password('user123')
            
            chef_user = User(username='chef1', email='chef1@example.com', is_admin=False)
            chef_user.set_password('chef123')
            
            db.session.add_all([admin_user, normal_user, chef_user])
            db.session.commit()
            
            print("用户创建成功!")
            print(f"管理员账号: admin / admin123")
            print(f"普通用户: user1 / user123")
            print(f"厨师用户: chef1 / chef123")
            
    except Exception as e:
        print(f"初始化失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    init_database()
