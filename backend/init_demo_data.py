#!/usr/bin/env python3
"""
初始化演示数据
这个脚本用于创建和填充演示数据到数据库
"""

import os
import sys

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
                    'image': 'gbjd.jpg',
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
                    'image': 'mpdf.jpg',
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
                    'image': 'tcpdg.jpg',
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
                    'image': 'dcf.jpg',
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
                    'image': 'kljc.jpg',
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
            recipe1, recipe2, recipe3, recipe4, recipe5, recipe6, recipe7, recipe8 = recipe_objects
            
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
                Like(user_id=admin_user.id, recipe_id=recipe7.id)
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
                Favorite(user_id=normal_user.id, recipe_id=recipe8.id)
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
                Comment(content='我家孩子超爱吃这个！', user_id=chef_user.id, recipe_id=recipe8.id)
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
