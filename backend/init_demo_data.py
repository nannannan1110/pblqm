#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化演示数据
这个脚本用于创建和填充演示数据到数据库
"""

import os
import sys
import io

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 确保我们能找到项目模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 检查我们是否有需要的依赖
try:
    from simple_server import app, db
    from models import User, Recipe, Role, UserRole, Favorite, Comment, Rating, Like
    print("[OK] 依赖检查通过")
except ImportError as e:
    print(f"[ERROR] 导入错误: {e}")
    print("\n请先安装所需依赖:")
    print("pip install flask flask-sqlalchemy flask-cors")
    sys.exit(1)

def init_database():
    """初始化数据库"""
    print("🚀 开始初始化演示数据库...")
    
    try:
        with app.app_context():
            # 删除所有现有数据
            print("📋 清理现有数据...")
            db.drop_all()
            
            # 创建所有表
            print("📊 创建数据库表...")
            db.create_all()
            
            # 1. 创建角色
            print("👥 创建角色...")
            admin_role = Role(name='管理员', description='系统管理员，拥有所有权限')
            user_role = Role(name='普通用户', description='普通用户，可以发布菜谱和评论')
            moderator_role = Role(name='版主', description='版主，可以管理评论和分类')
            
            db.session.add_all([admin_role, user_role, moderator_role])
            db.session.commit()
            
            # 2. 创建用户
            print("👤 创建用户...")
            admin_user = User(username='admin', email='admin@example.com')
            admin_user.set_password('admin123')
            
            normal_user = User(username='user1', email='user1@example.com')
            normal_user.set_password('user123')
            
            chef_user = User(username='chef1', email='chef1@example.com')
            chef_user.set_password('chef123')
            
            db.session.add_all([admin_user, normal_user, chef_user])
            db.session.commit()
            
            # 3. 分配角色
            print("🔑 分配角色...")
            admin_role_assignment = UserRole(user_id=admin_user.id, role_id=admin_role.id)
            user_role_assignment1 = UserRole(user_id=normal_user.id, role_id=user_role.id)
            user_role_assignment2 = UserRole(user_id=chef_user.id, role_id=user_role.id)
            
            db.session.add_all([admin_role_assignment, user_role_assignment1, user_role_assignment2])
            db.session.commit()
            
            # 4. 创建菜谱
            print("🍳 创建菜谱...")
            
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
                    'user_id': admin_user.id
                },
                {
                    'title': '西红柿炒鸡蛋',
                    'description': '经典家常菜，酸爽可口，营养丰富',
                    'ingredients': '西红柿 2个\n鸡蛋 3个\n葱 1根\n盐 适量\n糖 少许\n食用油 适量',
                    'instructions': '1. 西红柿洗净切块，鸡蛋打散\n2. 热锅放油，先炒鸡蛋盛起\n3. 锅中再放油，炒葱白香\n4. 下西红柿块炒出汤汁\n5. 加入炒蛋翻炒，调味即可',
                    'prep_time': 10,
                    'cook_time': 15,
                    'difficulty': '简单',
                    'servings': 2,
                    'image': 'xhscjd.jpg',
                    'user_id': admin_user.id
                },
                {
                    'title': '宫保鸡丁',
                    'description': '经典川菜，以"糊辣荔枝味"为特色，鸡丁嫩滑，花生香脆',
                    'ingredients': '鸡腿肉 400g\n油炸花生米 80g\n大葱白 30g\n干辣椒 8个\n花椒 10粒\n姜片 3片\n蒜瓣 3瓣\n生抽 2勺\n陈醋 2勺\n白糖 1勺\n料酒 1勺\n干淀粉 1勺\n盐 少许',
                    'instructions': '1. 鸡腿肉去骨切丁，加入料酒、少许盐和干淀粉抓匀，腌制10分钟\n2. 大葱白切小段，干辣椒剪段，姜蒜切片\n3. 调制碗汁：将生抽、陈醋、白糖、少许盐和1勺清水淀粉混合搅匀\n4. 热锅倒油，油热后下花椒和干辣椒段炒出香味\n5. 放入姜蒜片和葱段爆香\n6. 倒入腌制好的鸡丁，大火快速滑炒至变色断生\n7. 淋入调好的碗汁，翻炒均匀\n8. 待酱汁浓稠裹满鸡丁后，倒入花生米，快速翻炒几下即可出锅',
                    'prep_time': 15,
                    'cook_time': 10,
                    'difficulty': '简单',
                    'servings': 2,
                    'image': '418b20a3838e4ae8a5808ceba994a87e.jpg',
                    'user_id': chef_user.id
                },
                {
                    'title': '麻婆豆腐',
                    'description': '经典川菜，麻、辣、烫、香、酥、嫩、鲜、活',
                    'ingredients': '嫩豆腐 400g\n牛肉末 100g\n豆瓣酱 2勺\n花椒粉 1勺\n干辣椒面 1勺\n生抽 1勺\n老抽 半勺\n糖 半勺\n淀粉水 适量\n葱 1根\n姜 3片\n蒜 3瓣',
                    'instructions': '1. 豆腐切块，放入加了盐的开水中焯烫2分钟后捞出\n2. 葱姜蒜切末\n3. 热锅放油，下牛肉末炒散炒香\n4. 加入豆瓣酱、干辣椒面炒出红油\n5. 加入姜蒜末炒香\n6. 加入适量清水，放入豆腐块\n7. 加入生抽、老抽、糖调味\n8. 大火烧开后转小火煮3-5分钟\n9. 淋入淀粉水勾芡\n10. 出锅前撒上花椒粉和葱花',
                    'prep_time': 10,
                    'cook_time': 15,
                    'difficulty': '中等',
                    'servings': 3,
                    'image': 'xhscjd.jpg',
                    'user_id': chef_user.id
                },
                {
                    'title': '糖醋排骨',
                    'description': '酸甜可口，外酥里嫩，老少皆宜',
                    'ingredients': '猪小排 500g\n生姜 1块\n大葱 1根\n料酒 2勺\n生抽 2勺\n老抽 1勺\n醋 3勺\n糖 4勺\n番茄酱 2勺\n盐 适量\n白芝麻 少许',
                    'instructions': '1. 猪小排剁成小段，清水浸泡去血水\n2. 冷水下锅焯水，加姜片和料酒去腥\n3. 排骨捞出沥干水分\n4. 调制糖醋汁：生抽、老抽、醋、糖、番茄酱混合均匀\n5. 锅中放少许油，下排骨煎至两面金黄\n6. 倒入糖醋汁，加入适量清水\n7. 大火烧开转中火焖煮20分钟\n8. 大火收汁，汤汁浓稠时即可出锅\n9. 撒上白芝麻点缀',
                    'prep_time': 20,
                    'cook_time': 25,
                    'difficulty': '中等',
                    'servings': 4,
                    'image': '115febe3051840909d08205f720b23a4.jpg',
                    'user_id': chef_user.id
                },
                {
                    'title': '蛋炒饭',
                    'description': '经典主食，粒粒分明，香气扑鼻',
                    'ingredients': '米饭 1碗\n鸡蛋 2个\n火腿 50g\n青豆 30g\n胡萝卜 30g\n葱 1根\n盐 适量\n生抽 半勺\n食用油 适量',
                    'instructions': '1. 火腿、胡萝卜切丁，青豆洗净\n2. 鸡蛋打散\n3. 锅中放油，下蛋液炒熟盛出\n4. 锅中再放油，下火腿丁、胡萝卜丁、青豆翻炒\n5. 倒入米饭，用勺子压散\n6. 加入炒好的鸡蛋，加盐和生抽调味\n7. 大火翻炒均匀，撒上葱花即可出锅',
                    'prep_time': 5,
                    'cook_time': 8,
                    'difficulty': '简单',
                    'servings': 1,
                    'image': '93dd19494ba44895a1d5772d05024c27.jpg',
                    'user_id': admin_user.id
                },
                {
                    'title': '可乐鸡翅',
                    'description': '甜香软糯，小朋友最爱，简单易做',
                    'ingredients': '鸡翅中 8个\n可乐 1罐\n生姜 1块\n大葱 1根\n生抽 2勺\n老抽 1勺\n料酒 1勺\n盐 适量',
                    'instructions': '1. 鸡翅中洗净，两面各划两刀\n2. 冷水下锅焯水，加姜片和料酒去腥\n3. 鸡翅捞出沥干水分\n4. 锅中放少许油，下鸡翅煎至两面金黄\n5. 加入姜片、葱段、生抽、老抽\n6. 倒入可乐，没过鸡翅\n7. 大火烧开转小火焖煮15分钟\n8. 大火收汁即可出锅',
                    'prep_time': 15,
                    'cook_time': 20,
                    'difficulty': '简单',
                    'servings': 3,
                    'image': 'srxlh.jpg',
                    'user_id': chef_user.id
                },
                {
                    'title': '清蒸鲈鱼',
                    'description': '清淡鲜美，肉质细嫩，原汁原味',
                    'ingredients': '鲈鱼 1条\n生姜 1块\n大葱 1根\n蒸鱼豉油 2勺\n料酒 1勺\n盐 适量\n食用油 适量',
                    'instructions': '1. 鲈鱼处理干净，在鱼身上划几刀\n2. 鱼身和鱼肚内抹上盐和料酒，腌制10分钟\n3. 姜切丝，葱切段\n4. 盘子底部垫上葱段和姜丝，放上鲈鱼\n5. 鱼身上再铺一些姜丝和葱段\n6. 蒸锅加水烧开，放入鲈鱼蒸8-10分钟\n7. 取出蒸好的鱼，倒掉盘里的水\n8. 淋上蒸鱼豉油\n9. 另起锅烧热油，浇在鱼身上即可',
                    'prep_time': 10,
                    'cook_time': 12,
                    'difficulty': '简单',
                    'servings': 3,
                    'image': 'hsr.jpg',
                    'user_id': chef_user.id
                },
                {
                    'title': '红烧排骨',
                    'description': '色泽红亮，肉质软烂，酱香浓郁',
                    'ingredients': '猪排骨 500g\n生姜 1块\n大葱 1根\n八角 2个\n桂皮 1小块\n香叶 2片\n生抽 3勺\n老抽 1勺\n料酒 2勺\n冰糖 20g\n盐 适量',
                    'instructions': '1. 排骨剁成小段，清水浸泡去血水\n2. 冷水下锅焯水，加姜片和料酒去腥\n3. 排骨捞出沥干水分\n4. 热锅放少许油，下冰糖炒糖色\n5. 下排骨翻炒上色\n6. 加入姜片、葱段、八角、桂皮、香叶炒香\n7. 加入生抽、老抽、料酒炒匀\n8. 加没过排骨的热水\n9. 大火烧开转小火炖30分钟\n10. 大火收汁，加盐调味即可',
                    'prep_time': 20,
                    'cook_time': 35,
                    'difficulty': '中等',
                    'servings': 4,
                    'image': 'xhscjd.jpg',
                    'user_id': admin_user.id
                },
                {
                    'title': '酸菜鱼',
                    'description': '酸辣开胃，鱼肉滑嫩，川菜经典',
                    'ingredients': '草鱼 1条\n酸菜 200g\n泡椒 10个\n生姜 1块\n大蒜 4瓣\n干辣椒 5个\n花椒 1小把\n料酒 1勺\n盐 适量\n蛋清 1个\n淀粉 1勺',
                    'instructions': '1. 草鱼处理干净，片成鱼片\n2. 鱼片用盐、料酒、蛋清、淀粉抓匀腌制15分钟\n3. 酸菜洗净切小段，泡椒切半\n4. 姜蒜切末\n5. 热锅放油，下姜蒜末、泡椒、干辣椒、花椒炒香\n6. 下酸菜翻炒2分钟\n7. 加入适量清水或高汤\n8. 大火烧开后转小火煮10分钟\n9. 将酸菜捞出铺在碗底\n10. 锅中汤再次烧开，下入鱼片滑熟\n11. 连汤一起倒入碗中\n12. 另起锅烧热油，浇在鱼片上即可',
                    'prep_time': 25,
                    'cook_time': 20,
                    'difficulty': '困难',
                    'servings': 4,
                    'image': '418b20a3838e4ae8a5808ceba994a87e.jpg',
                    'user_id': chef_user.id
                },
                {
                    'title': '蒜蓉粉丝蒸扇贝',
                    'description': '鲜美多汁，蒜香浓郁，宴客必备',
                    'ingredients': '扇贝 6个\n粉丝 1小把\n大蒜 10瓣\n生抽 2勺\n蚝油 1勺\n料酒 1勺\n盐 少许\n食用油 适量\n葱花 适量',
                    'instructions': '1. 扇贝处理干净，洗净备用\n2. 粉丝用温水泡软\n3. 大蒜切成蒜末\n4. 取一半蒜末用热油泼香，制成蒜蓉\n5. 加入生抽、蚝油、料酒、少许盐调成酱汁\n6. 粉丝铺在扇贝肉下面\n7. 将蒜蓉酱铺在扇贝肉上\n8. 蒸锅加水烧开，放入扇贝蒸5-6分钟\n9. 取出后撒上葱花\n10. 另起锅烧热油，浇在扇贝上即可',
                    'prep_time': 15,
                    'cook_time': 8,
                    'difficulty': '中等',
                    'servings': 3,
                    'image': '115febe3051840909d08205f720b23a4.jpg',
                    'user_id': admin_user.id
                },
                {
                    'title': '糖醋里脊',
                    'description': '外酥里嫩，酸甜可口，经典鲁菜',
                    'ingredients': '猪里脊肉 300g\n生姜 1小块\n大蒜 2瓣\n面粉 50g\n淀粉 30g\n番茄酱 3勺\n糖 2勺\n醋 2勺\n生抽 1勺\n料酒 1勺\n盐 少许\n食用油 适量',
                    'instructions': '1. 猪里脊肉切成条\n2. 用盐、料酒腌制10分钟\n3. 面粉和淀粉混合，加适量水调成面糊\n4. 里脊肉条裹上面糊\n5. 锅中放油，油热后下入里脊条炸至金黄捞出\n6. 油温升高后复炸一次，使外皮更酥脆\n7. 调制糖醋汁：番茄酱、糖、醋、生抽、少许清水混合\n8. 锅中留少许油，下姜蒜末爆香\n9. 倒入糖醋汁，小火熬至浓稠\n10. 倒入炸好的里脊条，翻炒均匀即可出锅',
                    'prep_time': 20,
                    'cook_time': 15,
                    'difficulty': '中等',
                    'servings': 3,
                    'image': '93dd19494ba44895a1d5772d05024c27.jpg',
                    'user_id': chef_user.id
                },
                {
                    'title': '蒜蓉蒸虾',
                    'description': '简单快手，鲜美无比，原汁原味',
                    'ingredients': '大虾 10只\n大蒜 8瓣\n生姜 1小块\n生抽 2勺\n蚝油 1勺\n料酒 1勺\n盐 少许\n食用油 适量\n葱花 适量',
                    'instructions': '1. 大虾剪去虾须虾脚，从背部剪开，去除虾线\n2. 用料酒和少许盐腌制10分钟\n3. 大蒜切成蒜末，生姜切末\n4. 取一半蒜末用热油泼香\n5. 加入生抽、蚝油调成酱汁\n6. 虾平铺在盘子里，淋上蒜蓉酱\n7. 蒸锅加水烧开，放入虾蒸5-6分钟\n8. 取出后撒上葱花\n9. 另起锅烧热油，浇在虾上即可',
                    'prep_time': 10,
                    'cook_time': 8,
                    'difficulty': '简单',
                    'servings': 3,
                    'image': 'srxlh.jpg',
                    'user_id': admin_user.id
                },
                {
                    'title': '鱼香肉丝',
                    'description': '经典川菜，酸甜微辣，肉丝嫩滑',
                    'ingredients': '猪里脊肉 250g\n木耳 50g\n胡萝卜 1根\n青椒 1个\n葱姜蒜 适量\n豆瓣酱 1勺\n醋 2勺\n糖 1勺\n生抽 1勺\n料酒 1勺\n淀粉 适量',
                    'instructions': '1. 猪里脊肉切丝，用料酒、盐、淀粉抓匀腌制\n2. 木耳泡发切丝，胡萝卜、青椒切丝\n3. 葱姜蒜切末\n4. 调制鱼香汁：醋、糖、生抽、淀粉、清水混合\n5. 热锅放油，下肉丝滑炒变色盛出\n6. 锅中留油，下豆瓣酱炒出红油\n7. 下葱姜蒜末、木耳、胡萝卜、青椒翻炒\n8. 倒入肉丝，淋入鱼香汁\n9. 大火翻炒均匀即可出锅',
                    'prep_time': 15,
                    'cook_time': 10,
                    'difficulty': '中等',
                    'servings': 3,
                    'image': 'hsr.jpg',
                    'user_id': chef_user.id
                },
                {
                    'title': '麻婆豆腐',
                    'description': '经典川菜，麻辣鲜香，豆腐嫩滑',
                    'ingredients': '嫩豆腐 1块\n猪肉末 100g\n豆瓣酱 1勺\n花椒粉 1勺\n辣椒粉 1勺\n葱姜蒜 适量\n生抽 1勺\n料酒 1勺\n淀粉 适量\n小葱 适量',
                    'instructions': '1. 嫩豆腐切块，用盐水浸泡\n2. 热锅放油，下肉末炒散变色\n3. 加入豆瓣酱炒出红油\n4. 下葱姜蒜末、辣椒粉炒香\n5. 加入适量清水或高汤\n6. 下豆腐块，轻轻推动\n7. 加生抽调味，小火煮3分钟\n8. 淋入水淀粉勾芡\n9. 撒上花椒粉和葱花即可',
                    'prep_time': 10,
                    'cook_time': 12,
                    'difficulty': '简单',
                    'servings': 3,
                    'image': 'xhscjd.jpg',
                    'user_id': admin_user.id
                },
                {
                    'title': '水煮牛肉',
                    'description': '麻辣鲜香，牛肉嫩滑，川菜经典',
                    'ingredients': '牛里脊肉 300g\n豆芽 200g\n生菜 100g\n豆瓣酱 2勺\n干辣椒 10个\n花椒 1勺\n葱姜蒜 适量\n生抽 1勺\n料酒 1勺\n淀粉 适量\n蛋清 1个',
                    'instructions': '1. 牛肉切薄片，用料酒、生抽、蛋清、淀粉抓匀腌制\n2. 豆芽、生菜洗净焯水，铺在碗底\n3. 热锅放油，下豆瓣酱炒出红油\n4. 加入适量清水或高汤烧开\n5. 下牛肉片滑熟，连汤倒入碗中\n6. 撒上干辣椒段、花椒、蒜末\n7. 另起锅烧热油，浇在牛肉上\n8. 撒上葱花即可',
                    'prep_time': 20,
                    'cook_time': 15,
                    'difficulty': '中等',
                    'servings': 3,
                    'image': '418b20a3838e4ae8a5808ceba994a87e.jpg',
                    'user_id': chef_user.id
                },
                {
                    'title': '干锅花菜',
                    'description': '香辣下饭，花菜脆嫩，家常美味',
                    'ingredients': '花菜 1个\n五花肉 100g\n干辣椒 5个\n葱姜蒜 适量\n豆瓣酱 1勺\n生抽 1勺\n盐 适量\n食用油 适量',
                    'instructions': '1. 花菜洗净切小朵，五花肉切片\n2. 干辣椒剪段，葱姜蒜切末\n3. 热锅放油，下五花肉煸炒出油\n4. 下葱姜蒜末、干辣椒段炒香\n5. 加入豆瓣酱炒出红油\n6. 下花菜大火翻炒\n7. 加生抽、盐调味\n8. 炒至花菜断生即可出锅',
                    'prep_time': 10,
                    'cook_time': 10,
                    'difficulty': '简单',
                    'servings': 3,
                    'image': '115febe3051840909d08205f720b23a4.jpg',
                    'user_id': admin_user.id
                },
                {
                    'title': '回锅肉',
                    'description': '川菜之首，肥而不腻，香辣下饭',
                    'ingredients': '五花肉 300g\n青蒜 100g\n青椒 1个\n红椒 1个\n豆瓣酱 1勺\n甜面酱 1勺\n葱姜 适量\n料酒 1勺\n生抽 1勺\n糖 少许',
                    'instructions': '1. 五花肉冷水下锅，加葱姜、料酒煮20分钟\n2. 捞出晾凉切薄片\n3. 青蒜、青红椒切段\n4. 热锅放少许油，下五花肉片煸炒\n5. 炒至肉片卷曲出油，盛出\n6. 锅中留油，下豆瓣酱、甜面酱炒香\n7. 下青蒜、青红椒翻炒\n8. 倒入肉片，加生抽、糖调味\n9. 翻炒均匀即可出锅',
                    'prep_time': 15,
                    'cook_time': 15,
                    'difficulty': '中等',
                    'servings': 3,
                    'image': '93dd19494ba44895a1d5772d05024c27.jpg',
                    'user_id': chef_user.id
                }
            ]
            
            # 添加所有菜谱
            recipe_objects = []
            for recipe_data in recipes:
                recipe = Recipe(**recipe_data)
                recipe_objects.append(recipe)
                db.session.add(recipe)
            
            db.session.commit()
            
            # 获取菜谱对象以便后续使用
            recipe1, recipe2, recipe3, recipe4, recipe5, recipe6, recipe7, recipe8, recipe9, recipe10, recipe11, recipe12, recipe13, recipe14, recipe15, recipe16, recipe17, recipe18, recipe19 = recipe_objects

            # 5. 创建点赞
            print("❤️ 创建点赞...")
            likes = [
                Like(user_id=normal_user.id, recipe_id=recipe1.id),
                Like(user_id=normal_user.id, recipe_id=recipe2.id),
                Like(user_id=normal_user.id, recipe_id=recipe4.id),
                Like(user_id=normal_user.id, recipe_id=recipe5.id),
                Like(user_id=chef_user.id, recipe_id=recipe1.id),
                Like(user_id=chef_user.id, recipe_id=recipe3.id),
                Like(user_id=admin_user.id, recipe_id=recipe4.id),
                Like(user_id=admin_user.id, recipe_id=recipe5.id),
                Like(user_id=admin_user.id, recipe_id=recipe6.id),
                Like(user_id=normal_user.id, recipe_id=recipe8.id),
                Like(user_id=chef_user.id, recipe_id=recipe8.id),
                Like(user_id=admin_user.id, recipe_id=recipe7.id),
                Like(user_id=normal_user.id, recipe_id=recipe9.id),
                Like(user_id=chef_user.id, recipe_id=recipe10.id),
                Like(user_id=admin_user.id, recipe_id=recipe11.id),
                Like(user_id=normal_user.id, recipe_id=recipe12.id),
                Like(user_id=chef_user.id, recipe_id=recipe13.id)
            ]
            db.session.add_all(likes)
            db.session.commit()
            
            # 6. 创建收藏
            print("📚 创建收藏...")
            favorites = [
                Favorite(user_id=normal_user.id, recipe_id=recipe1.id),
                Favorite(user_id=normal_user.id, recipe_id=recipe2.id),
                Favorite(user_id=admin_user.id, recipe_id=recipe3.id),
                Favorite(user_id=normal_user.id, recipe_id=recipe4.id),
                Favorite(user_id=chef_user.id, recipe_id=recipe2.id),
                Favorite(user_id=chef_user.id, recipe_id=recipe8.id),
                Favorite(user_id=admin_user.id, recipe_id=recipe5.id),
                Favorite(user_id=normal_user.id, recipe_id=recipe8.id),
                Favorite(user_id=normal_user.id, recipe_id=recipe9.id),
                Favorite(user_id=chef_user.id, recipe_id=recipe10.id),
                Favorite(user_id=admin_user.id, recipe_id=recipe11.id),
                Favorite(user_id=normal_user.id, recipe_id=recipe13.id)
            ]
            db.session.add_all(favorites)
            db.session.commit()
            
            # 7. 创建评论
            print("💬 创建评论...")
            comments = [
                Comment(content='这道菜非常简单易做，味道也很好！', user_id=normal_user.id, recipe_id=recipe1.id),
                Comment(content='建议可以加点蚝油调味，会更好吃。', user_id=admin_user.id, recipe_id=recipe1.id),
                Comment(content='健康又美味，全家人都喜欢！', user_id=chef_user.id, recipe_id=recipe1.id),
                Comment(content='红烧肉做起来有点复杂，但是真的很香！', user_id=normal_user.id, recipe_id=recipe2.id),
                Comment(content='肥而不腻，入口即化，太棒了！', user_id=chef_user.id, recipe_id=recipe2.id),
                Comment(content='经典就是经典，永远吃不腻！', user_id=admin_user.id, recipe_id=recipe3.id),
                Comment(content='这道菜的味道太棒了！糊辣荔枝味很正宗！', user_id=normal_user.id, recipe_id=recipe4.id),
                Comment(content='花生很脆，鸡丁很嫩，完美！', user_id=admin_user.id, recipe_id=recipe4.id),
                Comment(content='麻辣鲜香，太下饭了！', user_id=normal_user.id, recipe_id=recipe5.id),
                Comment(content='我家孩子超爱吃这个！', user_id=chef_user.id, recipe_id=recipe8.id),
                Comment(content='鱼香肉丝太经典了，酸甜微辣刚刚好！', user_id=normal_user.id, recipe_id=recipe9.id),
                Comment(content='麻婆豆腐麻辣鲜香，超级下饭！', user_id=chef_user.id, recipe_id=recipe10.id),
                Comment(content='水煮牛肉太嫩了，麻辣过瘾！', user_id=admin_user.id, recipe_id=recipe11.id),
                Comment(content='干锅花菜简单又好吃，家常必备！', user_id=normal_user.id, recipe_id=recipe12.id),
                Comment(content='回锅肉真的是川菜之首，太香了！', user_id=chef_user.id, recipe_id=recipe13.id)
            ]
            db.session.add_all(comments)
            db.session.commit()
            
            # 创建回复评论
            replies = [
                Comment(content='谢谢建议，下次试试！', user_id=normal_user.id, recipe_id=recipe1.id, parent_id=comments[1].id),
                Comment(content='是的！我也经常做给家人吃。', user_id=admin_user.id, recipe_id=recipe1.id, parent_id=comments[2].id),
                Comment(content='谢谢夸奖！', user_id=chef_user.id, recipe_id=recipe4.id, parent_id=comments[6].id)
            ]
            db.session.add_all(replies)
            db.session.commit()
            
            # 8. 创建评分
            print("⭐ 创建评分...")
            ratings = [
                Rating(score=5, user_id=normal_user.id, recipe_id=recipe1.id),
                Rating(score=4, user_id=admin_user.id, recipe_id=recipe1.id),
                Rating(score=5, user_id=chef_user.id, recipe_id=recipe1.id),
                Rating(score=5, user_id=normal_user.id, recipe_id=recipe2.id),
                Rating(score=5, user_id=chef_user.id, recipe_id=recipe2.id),
                Rating(score=4, user_id=admin_user.id, recipe_id=recipe3.id),
                Rating(score=5, user_id=normal_user.id, recipe_id=recipe4.id),
                Rating(score=5, user_id=admin_user.id, recipe_id=recipe4.id),
                Rating(score=4, user_id=chef_user.id, recipe_id=recipe4.id),
                Rating(score=5, user_id=normal_user.id, recipe_id=recipe5.id),
                Rating(score=4, user_id=admin_user.id, recipe_id=recipe5.id),
                Rating(score=5, user_id=chef_user.id, recipe_id=recipe6.id),
                Rating(score=4, user_id=admin_user.id, recipe_id=recipe6.id),
                Rating(score=5, user_id=chef_user.id, recipe_id=recipe8.id),
                Rating(score=5, user_id=admin_user.id, recipe_id=recipe7.id),
                Rating(score=5, user_id=normal_user.id, recipe_id=recipe9.id),
                Rating(score=4, user_id=chef_user.id, recipe_id=recipe9.id),
                Rating(score=5, user_id=admin_user.id, recipe_id=recipe10.id),
                Rating(score=5, user_id=normal_user.id, recipe_id=recipe10.id),
                Rating(score=5, user_id=chef_user.id, recipe_id=recipe11.id),
                Rating(score=4, user_id=admin_user.id, recipe_id=recipe11.id),
                Rating(score=4, user_id=normal_user.id, recipe_id=recipe12.id),
                Rating(score=5, user_id=chef_user.id, recipe_id=recipe12.id),
                Rating(score=5, user_id=admin_user.id, recipe_id=recipe13.id),
                Rating(score=5, user_id=normal_user.id, recipe_id=recipe13.id),
            ]
            db.session.add_all(ratings)
            db.session.commit()
            
            # 统计创建的数据
            print("\n" + "="*50)
            print("✅ 演示数据初始化完成！")
            print("="*50)
            print(f"📊 创建了 {Role.query.count()} 个角色")
            print(f"👤 创建了 {User.query.count()} 个用户")
            print(f"🔗 创建了 {UserRole.query.count()} 个用户角色关联")
            print(f"🍳 创建了 {Recipe.query.count()} 个菜谱")
            print(f"❤️ 创建了 {Like.query.count()} 个点赞")
            print(f"📚 创建了 {Favorite.query.count()} 个收藏")
            print(f"💬 创建了 {Comment.query.count()} 个评论")
            print(f"⭐ 创建了 {Rating.query.count()} 个评分")
            print("="*50)
            
            print("\n📝 测试账号信息：")
            print("   管理员: admin / admin123")
            print("   用户1: user1 / user123")
            print("   用户2: chef1 / chef123")
            
            print("\n💾 数据库文件位置: recipe_platform.db")
            
            print("\n🎉 完成！现在可以启动应用查看演示数据了。")
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return False
    
    return True

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)
