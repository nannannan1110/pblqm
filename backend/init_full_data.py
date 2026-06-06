#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化完整的演示数据
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
        # 使用 importlib 来导入 app.py 文件
        import importlib.util
        spec = importlib.util.spec_from_file_location("app_py", os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py"))
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)
        
        from models import db, User, Recipe, Post
        
        # 创建应用
        app = app_module.create_app()
        
        with app.app_context():
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
            
            # 创建菜谱
            print("创建菜谱...")
            recipes = [
                {
                    'title': '蒜蓉西兰花',
                    'description': '清淡爽口的健康蔬菜，营养丰富，制作简单',
                    'ingredients': '西兰花 1个\n大蒜 5瓣\n生抽 1勺\n盐 适量\n食用油 适量',
                    'instructions': '1. 西兰花洗净切小朵，大蒜切末\n2. 锅中烧开水，放入西兰花焯水2分钟\n3. 热锅放油，爆香蒜末\n4. 倒入西兰花翻炒\n5. 加生抽、盐调味即可\n6. 出锅前可以撒点香油提味',
                    'prep_time': 8,
                    'cook_time': 8,
                    'difficulty': '简单',
                    'servings': 2,
                    'image': 'srxlh.jpg',
                    'user_id': admin_user.id
                },
                {
                    'title': '红烧肉',
                    'description': '经典中式红烧肉，肥而不腻，入口即化',
                    'ingredients': '五花肉 500g\n生抽 3勺\n老抽 1勺\n料酒 2勺\n冰糖 30g\n葱 2根\n姜 3片\n八角 2个',
                    'instructions': '1. 五花肉切块，冷水下锅焯水去腥\n2. 热锅放少许油，下冰糖炒糖色\n3. 下肉块翻炒上色\n4. 加入生抽、老抽、料酒炒匀\n5. 加没过肉的热水，放葱姜八角\n6. 大火烧开转小火炖40分钟\n7. 大火收汁即可',
                    'prep_time': 15,
                    'cook_time': 45,
                    'difficulty': '中等',
                    'servings': 4,
                    'image': 'hsr.jpg',
                    'user_id': chef_user.id
                },
                {
                    'title': '番茄炒蛋',
                    'description': '最简单又最美味的家常菜，酸甜可口',
                    'ingredients': '番茄 2个\n鸡蛋 3个\n盐 适量\n糖 少许\n葱花 适量',
                    'instructions': '1. 番茄切块，鸡蛋打散\n2. 热锅放油，倒入鸡蛋液炒至凝固盛出\n3. 锅中留底油，下番茄翻炒出汁\n4. 加少许糖提鲜，加盐调味\n5. 倒入炒好的鸡蛋翻炒均匀\n6. 撒葱花出锅',
                    'prep_time': 5,
                    'cook_time': 10,
                    'difficulty': '简单',
                    'servings': 2,
                    'image': 'fqcd.jpg',
                    'user_id': normal_user.id
                },
                {
                    'title': '宫保鸡丁',
                    'description': '经典川菜，麻辣鲜香，花生酥脆',
                    'ingredients': '鸡胸肉 300g\n花生米 50g\n干辣椒 10个\n花椒 1小把\n葱姜蒜适量\n生抽 2勺\n料酒 1勺\n白糖 1勺\n醋 1勺',
                    'instructions': '1. 鸡胸肉切丁，用生抽、料酒腌制10分钟\n2. 花生米炸熟备用\n3. 干辣椒剪段，葱姜蒜切末\n4. 热锅放油，爆香花椒和干辣椒\n5. 下鸡丁翻炒至变色\n6. 加葱姜蒜末炒香\n7. 倒入调好的酱汁（生抽+糖+醋）\n8. 加花生米翻炒均匀即可',
                    'prep_time': 15,
                    'cook_time': 15,
                    'difficulty': '中等',
                    'servings': 3,
                    'image': 'gbjd.jpg',
                    'user_id': chef_user.id
                },
                {
                    'title': '清蒸鲈鱼',
                    'description': '鲜嫩可口的清蒸鱼，原汁原味',
                    'ingredients': '鲈鱼 1条\n葱姜丝 适量\n蒸鱼豉油 2勺\n料酒 1勺\n盐 少许\n食用油 适量',
                    'instructions': '1. 鲈鱼处理干净，两面划刀\n2. 用料酒和盐涂抹鱼身腌制10分钟\n3. 盘底铺葱姜丝，放上鲈鱼\n4. 蒸锅烧开，放入鲈鱼蒸8-10分钟\n5. 取出倒掉蒸出的水，铺上新鲜葱姜丝\n6. 淋上蒸鱼豉油，浇热油即可',
                    'prep_time': 10,
                    'cook_time': 12,
                    'difficulty': '中等',
                    'servings': 2,
                    'image': 'qzly.jpg',
                    'user_id': admin_user.id
                },
                {
                    'title': '麻婆豆腐',
                    'description': '麻辣鲜香的经典川菜，下饭神器',
                    'ingredients': '嫩豆腐 1块\n猪肉末 100g\n豆瓣酱 1勺\n花椒粉 适量\n葱姜蒜适量\n生抽 1勺\n料酒 半勺',
                    'instructions': '1. 豆腐切块，开水焯烫一下\n2. 热锅放油，下猪肉末炒至变色\n3. 加豆瓣酱炒出红油\n4. 加葱姜蒜末炒香\n5. 加少许水，放豆腐轻轻翻炒\n6. 加生抽调味，勾薄芡\n7. 出锅撒花椒粉和葱花',
                    'prep_time': 10,
                    'cook_time': 15,
                    'difficulty': '中等',
                    'servings': 2,
                    'image': 'mpdf.jpg',
                    'user_id': chef_user.id
                }
            ]
            
            for recipe_data in recipes:
                recipe = Recipe(**recipe_data)
                db.session.add(recipe)
            
            db.session.commit()
            
            # 创建帖子
            print("创建帖子...")
            posts = [
                {
                    'user_id': normal_user.id,
                    'title': '第一次做手工意大利面',
                    'content': '今天尝试第一次做手工意大利面，虽然过程有点挑战，但结果非常棒！关键是要让面团充分休息。'
                },
                {
                    'user_id': chef_user.id,
                    'title': '完美炒饭的秘诀',
                    'content': '经过多年的实践，我总结出完美炒饭的几个要点：\n1. 使用隔夜饭\n2. 火候要大\n3. 不停翻炒\n4. 不要让锅太满\n5. 适时添加调味料'
                },
                {
                    'user_id': admin_user.id,
                    'title': '掌握炒菜技巧',
                    'content': '炒菜的关键在于时间和火候的控制。今天我来分享在家做出完美"锅气"的秘诀。'
                },
                {
                    'user_id': normal_user.id,
                    'title': '周末烘焙之旅',
                    'content': '整个周末都在烘焙！做了酸面包、可颂和一些饼干。早上新鲜出炉的香气真是太棒了！'
                },
                {
                    'user_id': chef_user.id,
                    'title': '亚洲融合菜谱创意',
                    'content': '我一直在尝试将亚洲风味与西方烹饪技巧相结合。这里分享一些我成功尝试过的组合。'
                }
            ]
            
            for post_data in posts:
                post = Post(**post_data)
                db.session.add(post)
            
            db.session.commit()
            
            print("✅ 初始化完成!")
            print(f"用户: admin / admin123, user1 / user123, chef1 / chef123")
            print(f"菜谱: 6 个")
            print(f"帖子: 5 个")
            
    except Exception as e:
        print(f"初始化失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    init_database()
