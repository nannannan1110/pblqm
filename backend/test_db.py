#!/usr/bin/env python3
"""测试数据库中的用户数据"""

from simple_server import app, db
from models import User, UserRole, Role

with app.app_context():
    print("=== 检查数据库中的用户 ===\n")
    
    users = User.query.all()
    for user in users:
        print(f"用户ID: {user.id}")
        print(f"用户名: {user.username}")
        print(f"邮箱: {user.email}")
        print(f"is_admin(): {user.is_admin()}")
        
        # 检查角色
        print("用户角色:")
        for ur in user.user_roles:
            role = Role.query.get(ur.role_id)
            if role:
                print(f"  - {role.name}: {role.description}")
        print("-" * 50)
