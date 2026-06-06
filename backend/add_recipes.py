#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""添加更多菜谱数据"""

import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def add_more_recipes():
    """添加更多菜谱"""
    print("添加更多菜谱...")
    
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("app_py", os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py"))
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)
        
        from models import db, Recipe, User
        
        app = app_module.create_app()
        
        with app.app_context():
            # 获取现有用户
            admin_user = User.query.filter_by(username='admin').first()
            chef_user = User.query.filter_by(username='chef1').first()
            normal_user = User.query.filter_by(username='user1').first()
            
            if not admin_user or not chef_user or not normal_user:
                print("错误：找不到用户")
                return
            
            # 现有图片文件
            existing_images = [
                'srxlh.jpg',  # 蒜蓉西兰花
                'hsr.jpg',    # 红烧肉
                'fqcd.jpg',   # 番茄炒蛋
                'gbjd.jpg',   # 宫保鸡丁
                'qzly.jpg',   # 清蒸鲈鱼
                'mpdf.jpg',   # 麻婆豆腐
                'xhscjd.jpg'  # 西红柿炒鸡蛋
            ]
            
            # 新菜谱数据
            new_recipes = [
                {
                    'title': '红烧排骨',
                    'description': '经典红烧排骨，色泽红亮，肉质鲜嫩',
                    'ingredients': '排骨 500g\n生抽 2勺\n老抽 1勺\n料酒 2勺\n冰糖 20g\n葱姜适量',
                    'instructions': '1. 排骨焯水去腥\n2. 炒糖色，下排骨翻炒上色\n3. 加料酒、生抽、老抽\n4. 加水炖煮30分钟\n5. 大火收汁',
                    'prep_time': 10,
                    'cook_time': 40,
                    'difficulty': '中等',
                    'servings': 4,
                    'image': 'hsr.jpg',
                    'user_id': chef_user.id
                },
                {
                    'title': '青椒土豆丝',
                    'description': '家常快手菜，酸辣爽口',
                    'ingredients': '土豆 2个\n青椒 2个\n大蒜 3瓣\n醋 1勺\n盐 适量',
                    'instructions': '1. 土豆切丝泡水去淀粉\n2. 青椒切丝，大蒜切末\n3. 热锅放油，爆香蒜末\n4. 下土豆丝翻炒\n5. 加青椒丝，放醋和盐调味',
                    'prep_time': 8,
                    'cook_time': 10,
                    'difficulty': '简单',
                    'servings': 2,
                    'image': 'fqcd.jpg',
                    'user_id': normal_user.id
                },
                {
                    'title': '鱼香肉丝',
                    'description': '酸甜微辣，下饭神器',
                    'ingredients': '猪肉丝 200g\n木耳 适量\n胡萝卜 半根\n青椒 1个\n葱姜蒜适量\n豆瓣酱 1勺',
                    'instructions': '1. 肉丝腌制10分钟\n2. 配菜切丝\n3. 调制鱼香酱汁\n4. 炒香豆瓣酱，下肉丝\n5. 加配菜翻炒，淋酱汁',
                    'prep_time': 15,
                    'cook_time': 15,
                    'difficulty': '中等',
                    'servings': 3,
                    'image': 'gbjd.jpg',
                    'user_id': chef_user.id
                },
                {
                    'title': '清蒸虾',
                    'description': '原汁原味，鲜美无比',
                    'ingredients': '大虾 500g\n葱姜丝 适量\n生抽 2勺\n料酒 1勺',
                    'instructions': '1. 虾剪去虾须，开背去虾线\n2. 料酒腌制5分钟\n3. 蒸锅上汽蒸5-8分钟\n4. 淋蒸鱼豉油，铺葱姜丝\n5. 浇热油',
                    'prep_time': 10,
                    'cook_time': 10,
                    'difficulty': '简单',
                    'servings': 3,
                    'image': 'qzly.jpg',
                    'user_id': admin_user.id
                },
                {
                    'title': '酸辣白菜',
                    'description': '酸爽开胃，简单易做',
                    'ingredients': '白菜 半颗\n干辣椒 3个\n花椒 少许\n醋 2勺\n糖 1勺\n盐 适量',
                    'instructions': '1. 白菜切块\n2. 热锅放油，爆香花椒辣椒\n3. 下白菜翻炒\n4. 加醋、糖、盐调味\n5. 快速翻炒出锅',
                    'prep_time': 5,
                    'cook_time': 8,
                    'difficulty': '简单',
                    'servings': 2,
                    'image': 'mpdf.jpg',
                    'user_id': normal_user.id
                },
                {
                    'title': '蒜蓉粉丝蒸扇贝',
                    'description': '海鲜美味，蒜香浓郁',
                    'ingredients': '扇贝 6个\n粉丝 1把\n大蒜 10瓣\n生抽 2勺\n蚝油 1勺',
                    'instructions': '1. 粉丝泡软铺盘底\n2. 扇贝洗净放粉丝上\n3. 蒜蓉炒香加生抽蚝油\n4. 淋在扇贝上\n5. 蒸锅蒸5-6分钟',
                    'prep_time': 15,
                    'cook_time': 8,
                    'difficulty': '中等',
                    'servings': 3,
                    'image': 'srxlh.jpg',
                    'user_id': chef_user.id
                }
            ]
            
            # 添加新菜谱
            added_count = 0
            for recipe_data in new_recipes:
                # 检查是否已存在
                existing = Recipe.query.filter_by(title=recipe_data['title']).first()
                if not existing:
                    recipe = Recipe(**recipe_data)
                    db.session.add(recipe)
                    added_count += 1
                else:
                    print(f"菜谱 '{recipe_data['title']}' 已存在")
            
            db.session.commit()
            print(f"成功添加 {added_count} 个新菜谱")
            
            # 显示总数
            total = Recipe.query.count()
            print(f"菜谱总数: {total}")
            
    except Exception as e:
        print(f"添加失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    add_more_recipes()
