#!/usr/bin/env python3
"""
数据库初始化脚本
运行此脚本来创建数据库表和添加初始数据
"""

import os
import sys
from flask import Flask
from werkzeug.security import generate_password_hash

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 直接导入模块
from app import db
from app.models.user import User
from app.models.recipe import Recipe
from app.models.comment import Comment

def init_database():
    """初始化数据库"""
    # 创建Flask应用
    from flask import Flask
    from flask_cors import CORS
    from flask_jwt_extended import JWTManager
    from app.config import Config

    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    CORS(app)
    JWTManager(app)

    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.recipes import recipes_bp
    from app.routes.users import users_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(recipes_bp, url_prefix='/api/recipes')
    app.register_blueprint(users_bp, url_prefix='/api/users')

    with app.app_context():
        # 创建所有表
        print("正在创建数据库表...")
        db.create_all()
        print("数据库表创建完成！")

        # 添加测试数据
        add_test_data()
        print("测试数据添加完成！")

def add_test_data():
    """添加测试数据"""
    print("正在添加测试用户...")

    # 检查是否已有用户
    if User.query.first():
        print("数据库中已有用户，跳过用户创建")
        return

    # 创建测试用户
    users = [
        {
            'username': 'admin',
            'email': 'admin@recipe.com',
            'password': 'admin123',
            'bio': '系统管理员，热爱美食',
            'is_admin': True
        },
        {
            'username': 'chef1',
            'email': 'chef1@recipe.com',
            'password': 'chef123',
            'bio': '专业厨师，擅长中西料理',
            'is_admin': False
        },
        {
            'username': 'foodie',
            'email': 'foodie@recipe.com',
            'password': 'food123',
            'bio': '美食爱好者，喜欢分享家常菜',
            'is_admin': False
        }
    ]

    for user_data in users:
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            bio=user_data['bio'],
            is_admin=user_data.get('is_admin', False)
        )
        user.set_password(user_data['password'])
        db.session.add(user)

    db.session.commit()
    print(f"创建了 {len(users)} 个测试用户")

    # 获取用户用于创建菜谱和评论
    admin = User.query.filter_by(username='admin').first()
    chef1 = User.query.filter_by(username='chef1').first()
    foodie = User.query.filter_by(username='foodie').first()

    print("正在添加测试菜谱...")

    recipes = [
        {
            'title': '经典番茄炒蛋',
            'description': '简单易学的家常菜，酸甜可口，营养搭配均衡',
            'ingredients': '鸡蛋 3个\n番茄 2个\n葱 1根\n盐 适量\n糖 1小勺\n生抽 1勺\n食用油 适量',
            'instructions': '1. 番茄洗净切块，鸡蛋打散\n2. 热锅放油，先炒鸡蛋盛起\n3. 锅中再放油，炒香葱白\n4. 下番茄块炒出汁水\n5. 加入炒蛋翻炒，调味即可',
            'prep_time': 10,
            'cook_time': 15,
            'difficulty': '简单',
            'servings': 2,
            'image': 'tomato_egg.jpg',
            'user_id': admin.id
        },
        {
            'title': '红烧肉',
            'description': '传统名菜，肥瘦相间，色泽红润，入口即化',
            'ingredients': '五花肉 500g\n冰糖 30g\n生抽 3勺\n老抽 1勺\n料酒 2勺\n八角 2个\n桂皮 1小块\n葱段 适量\n姜片 3片',
            'instructions': '1. 五花肉切块，冷水下锅焯水\n2. 锅中放冰糖，小火炒糖色\n3. 下肉块翻炒上色\n4. 加生抽、老抽、料酒\n5. 加开水没过肉，放香料\n6. 大火烧开，小火炖煮1小时\n7. 大火收汁即可',
            'prep_time': 20,
            'cook_time': 60,
            'difficulty': '中等',
            'servings': 4,
            'image': 'braised_pork.jpg',
            'user_id': chef1.id
        },
        {
            'title': '蒜蓉西兰花',
            'description': '清淡健康的素食做法，保持蔬菜的鲜嫩口感',
            'ingredients': '西兰花 1个\n大蒜 5瓣\n盐 适量\n食用油 适量\n蚝油 1勺\n鸡精 少许',
            'instructions': '1. 西兰花切小朵，焯水备用\n2. 大蒜切末\n3. 热锅放油，爆香蒜末\n4. 下西兰花翻炒\n5. 加盐、蚝油调味\n6. 最后撒鸡精炒匀即可',
            'prep_time': 10,
            'cook_time': 8,
            'difficulty': '简单',
            'servings': 2,
            'image': 'broccoli_garlic.jpg',
            'user_id': admin.id
        }
    ]

    for recipe_data in recipes:
        recipe = Recipe(
            title=recipe_data['title'],
            description=recipe_data['description'],
            ingredients=recipe_data['ingredients'],
            instructions=recipe_data['instructions'],
            prep_time=recipe_data['prep_time'],
            cook_time=recipe_data['cook_time'],
            difficulty=recipe_data['difficulty'],
            servings=recipe_data['servings'],
            image=recipe_data['image'],
            user_id=recipe_data['user_id']
        )
        db.session.add(recipe)

    db.session.commit()
    print(f"创建了 {len(recipes)} 个测试菜谱")

    # 添加一些评论
    print("正在添加测试评论...")

    recipe1 = Recipe.query.filter_by(title='经典番茄炒蛋').first()
    recipe2 = Recipe.query.filter_by(title='红烧肉').first()

    comments = [
        {
            'content': '这个菜谱很详细，做出来味道很好！家人都很喜欢。',
            'rating': 5,
            'user_id': chef1.id,
            'recipe_id': recipe1.id
        },
        {
            'content': '简单又美味，新手也能成功。建议番茄可以多放一个。',
            'rating': 4,
            'user_id': foodie.id,
            'recipe_id': recipe1.id
        },
        {
            'content': '红烧肉的做法很正宗，肉质软糯香甜，下次还做！',
            'rating': 5,
            'user_id': foodie.id,
            'recipe_id': recipe2.id
        }
    ]

    for comment_data in comments:
        comment = Comment(
            content=comment_data['content'],
            rating=comment_data['rating'],
            user_id=comment_data['user_id'],
            recipe_id=comment_data['recipe_id']
        )
        db.session.add(comment)

    db.session.commit()
    print(f"创建了 {len(comments)} 个测试评论")

    print("\n数据库初始化完成！")
    print("测试用户账号：")
    print("管理员: admin / admin123")
    print("厨师: chef1 / chef123")
    print("美食爱好者: foodie / food123")

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        sys.exit(1)