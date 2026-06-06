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
            
            # 新菜谱数据
            new_recipes = [
                {
                    'title': '糖醋里脊',
                    'description': '酸甜可口，外酥里嫩',
                    'ingredients': '猪里脊肉 300g\n淀粉 适量\n番茄酱 2勺\n醋 1勺\n糖 2勺\n生抽 1勺',
                    'instructions': '1. 里脊肉切条，用盐腌制10分钟\n2. 裹淀粉，油炸至金黄\n3. 调制糖醋汁\n4. 倒入炸好的里脊翻炒\n5. 收汁出锅',
                    'prep_time': 15,
                    'cook_time': 20,
                    'difficulty': '中等',
                    'servings': 3,
                    'image': 'xhscjd.jpg',
                    'user_id': chef_user.id
                },
                {
                    'title': '水煮肉片',
                    'description': '麻辣鲜香，川菜经典',
                    'ingredients': '猪里脊肉 300g\n豆芽 200g\n干辣椒 10个\n花椒 1小把\n郫县豆瓣酱 1勺',
                    'instructions': '1. 肉片腌制10分钟\n2. 豆芽焯水铺碗底\n3. 炒香豆瓣酱，加水煮开\n4. 下肉片煮熟\n5. 连汤倒入碗中\n6. 铺辣椒花椒，浇热油',
                    'prep_time': 15,
                    'cook_time': 20,
                    'difficulty': '中等',
                    'servings': 3,
                    'image': 'hsr.jpg',
                    'user_id': chef_user.id
                },
                {
                    'title': '蒜蓉蒸虾',
                    'description': '蒜香浓郁，鲜美可口',
                    'ingredients': '大虾 500g\n大蒜 10瓣\n生抽 2勺\n蚝油 1勺\n葱花 适量',
                    'instructions': '1. 虾剪去虾须，开背去虾线\n2. 蒜蓉炒香加生抽蚝油\n3. 铺在虾上\n4. 蒸锅蒸5-6分钟\n5. 撒葱花',
                    'prep_time': 10,
                    'cook_time': 8,
                    'difficulty': '简单',
                    'servings': 3,
                    'image': 'srxlh.jpg',
                    'user_id': admin_user.id
                },
                {
                    'title': '红烧茄子',
                    'description': '软糯入味，下饭神器',
                    'ingredients': '茄子 2个\n大蒜 5瓣\n生抽 2勺\n老抽 1勺\n糖 1勺',
                    'instructions': '1. 茄子切条，盐水浸泡5分钟\n2. 油炸或煎至金黄\n3. 爆香蒜末\n4. 加调料，下茄子翻炒\n5. 加水焖煮入味',
                    'prep_time': 10,
                    'cook_time': 15,
                    'difficulty': '简单',
                    'servings': 2,
                    'image': 'fqcd.jpg',
                    'user_id': admin_user.id
                }
            ]
            
            # 添加新菜谱
            added_count = 0
            for recipe_data in new_recipes:
                existing = Recipe.query.filter_by(title=recipe_data['title']).first()
                if not existing:
                    recipe = Recipe(**recipe_data)
                    db.session.add(recipe)
                    added_count += 1
                else:
                    print(f"菜谱 '{recipe_data['title']}' 已存在")
            
            db.session.commit()
            print(f"成功添加 {added_count} 个新菜谱")
            
            total = Recipe.query.count()
            print(f"菜谱总数: {total}")
            
    except Exception as e:
        print(f"添加失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    add_more_recipes()
