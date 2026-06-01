#!/usr/bin/env python3
"""
种子数据创建脚本
为数据库创建初始测试数据
"""

from simple_server import app, db
from models import User, Recipe, Role, UserRole, Favorite, Comment, Rating, Like

def create_seed_data():
    """创建种子数据"""
    with app.app_context():
        print("开始创建种子数据...")

        # 删除所有现有数据
        print("清理现有数据...")
        db.drop_all()
        
        # 创建所有表
        print("创建数据库表...")
        db.create_all()

        # 1. 创建角色
        print("创建角色...")
        admin_role = Role(name='管理员', description='系统管理员，拥有所有权限')
        user_role = Role(name='普通用户', description='普通用户，可以发布菜谱和评论')
        moderator_role = Role(name='版主', description='版主，可以管理评论和分类')

        db.session.add_all([admin_role, user_role, moderator_role])
        db.session.commit()

        # 2. 创建用户
        print("创建用户...")
        admin_user = User(
            username='admin',
            email='admin@example.com'
        )
        admin_user.set_password('admin123')

        normal_user = User(
            username='user1',
            email='user1@example.com'
        )
        normal_user.set_password('user123')

        chef_user = User(
            username='chef1',
            email='chef1@example.com'
        )
        chef_user.set_password('chef123')

        db.session.add_all([admin_user, normal_user, chef_user])
        db.session.commit()

        # 3. 分配角色
        print("分配用户角色...")
        admin_role_assignment = UserRole(user_id=admin_user.id, role_id=admin_role.id)
        user_role_assignment1 = UserRole(user_id=normal_user.id, role_id=user_role.id)
        user_role_assignment2 = UserRole(user_id=chef_user.id, role_id=user_role.id)

        db.session.add_all([admin_role_assignment, user_role_assignment1, user_role_assignment2])
        db.session.commit()

        # 4. 创建菜谱
        print("创建菜谱...")
        
        # 菜品1：蒜蓉西兰花
        recipe1 = Recipe(
            title='蒜蓉西兰花',
            description='清淡爽口的健康蔬菜，营养丰富，制作简单',
            ingredients='西兰花 1个\n大蒜 5瓣\n生抽 1勺\n盐 适量\n食用油 适量',
            instructions='1. 西兰花洗净切小朵，大蒜切末\n2. 锅中烧开水，放入西兰花焯水2分钟\n3. 热锅放油，爆香蒜末\n4. 倒入西兰花翻炒\n5. 加生抽、盐调味即可\n6. 出锅前可以撒点香油提味',
            prep_time=8,
            cook_time=8,
            difficulty='简单',
            servings=2,
            image='srxlh.jpg',
            user_id=admin_user.id
        )
        
        # 菜品2：红烧肉
        recipe2 = Recipe(
            title='红烧肉',
            description='经典中式红烧肉，肥而不腻，入口即化',
            ingredients='五花肉 500g\n生抽 3勺\n老抽 1勺\n料酒 2勺\n冰糖 30g\n葱 2根\n姜 3片\n八角 2个',
            instructions='1. 五花肉切块，冷水下锅焯水去腥\n2. 热锅放少许油，下冰糖炒糖色\n3. 下肉块翻炒上色\n4. 加入生抽、老抽、料酒炒匀\n5. 加没过肉的热水，放葱姜八角\n6. 大火烧开转小火炖40分钟\n7. 大火收汁即可',
            prep_time=15,
            cook_time=45,
            difficulty='中等',
            servings=4,
            image='hsr.jpg',
            user_id=admin_user.id
        )
        
        # 菜品3：西红柿炒鸡蛋
        recipe3 = Recipe(
            title='西红柿炒鸡蛋',
            description='经典家常菜，酸爽可口，营养丰富',
            ingredients='西红柿 2个\n鸡蛋 3个\n葱 1根\n盐 适量\n糖 少许\n食用油 适量',
            instructions='1. 西红柿洗净切块，鸡蛋打散\n2. 热锅放油，先炒鸡蛋盛起\n3. 锅中再放油，炒葱白香\n4. 下西红柿块炒出汤汁\n5. 加入炒蛋翻炒，调味即可',
            prep_time=10,
            cook_time=15,
            difficulty='简单',
            servings=2,
            image='xhscjd.jpg',
            user_id=admin_user.id
        )
        
        # 菜品4：宫保鸡丁
        recipe4 = Recipe(
            title='宫保鸡丁',
            description='经典川菜，以"糊辣荔枝味"为特色，鸡丁嫩滑，花生香脆',
            ingredients='鸡腿肉 400g\n油炸花生米 80g\n大葱白 30g\n干辣椒 8个\n花椒 10粒\n姜片 3片\n蒜瓣 3瓣\n生抽 2勺\n陈醋 2勺\n白糖 1勺\n料酒 1勺\n干淀粉 1勺\n盐 少许',
            instructions='1. 鸡腿肉去骨切丁，加入料酒、少许盐和干淀粉抓匀，腌制10分钟\n2. 大葱白切小段，干辣椒剪段，姜蒜切片\n3. 调制碗汁：将生抽、陈醋、白糖、少许盐和1勺清水淀粉混合搅匀\n4. 热锅倒油，油热后下花椒和干辣椒段炒出香味\n5. 放入姜蒜片和葱段爆香\n6. 倒入腌制好的鸡丁，大火快速滑炒至变色断生\n7. 淋入调好的碗汁，翻炒均匀\n8. 待酱汁浓稠裹满鸡丁后，倒入花生米，快速翻炒几下即可出锅',
            prep_time=15,
            cook_time=10,
            difficulty='简单',
            servings=2,
            image='gbjd.jpg',
            user_id=chef_user.id
        )
        
        # 菜品5：麻婆豆腐
        recipe5 = Recipe(
            title='麻婆豆腐',
            description='经典川菜，麻、辣、烫、香、酥、嫩、鲜、活',
            ingredients='嫩豆腐 400g\n牛肉末 100g\n豆瓣酱 2勺\n花椒粉 1勺\n干辣椒面 1勺\n生抽 1勺\n老抽 半勺\n糖 半勺\n淀粉水 适量\n葱 1根\n姜 3片\n蒜 3瓣',
            instructions='1. 豆腐切块，放入加了盐的开水中焯烫2分钟后捞出\n2. 葱姜蒜切末\n3. 热锅放油，下牛肉末炒散炒香\n4. 加入豆瓣酱、干辣椒面炒出红油\n5. 加入姜蒜末炒香\n6. 加入适量清水，放入豆腐块\n7. 加入生抽、老抽、糖调味\n8. 大火烧开后转小火煮3-5分钟\n9. 淋入淀粉水勾芡\n10. 出锅前撒上花椒粉和葱花',
            prep_time=10,
            cook_time=15,
            difficulty='中等',
            servings=3,
            image='mpdf.jpg',
            user_id=chef_user.id
        )
        
        # 菜品6：糖醋排骨
        recipe6 = Recipe(
            title='糖醋排骨',
            description='酸甜可口，外酥里嫩，老少皆宜',
            ingredients='猪小排 500g\n生姜 1块\n大葱 1根\n料酒 2勺\n生抽 2勺\n老抽 1勺\n醋 3勺\n糖 4勺\n番茄酱 2勺\n盐 适量\n白芝麻 少许',
            instructions='1. 猪小排剁成小段，清水浸泡去血水\n2. 冷水下锅焯水，加姜片和料酒去腥\n3. 排骨捞出沥干水分\n4. 调制糖醋汁：生抽、老抽、醋、糖、番茄酱混合均匀\n5. 锅中放少许油，下排骨煎至两面金黄\n6. 倒入糖醋汁，加入适量清水\n7. 大火烧开转中火焖煮20分钟\n8. 大火收汁，汤汁浓稠时即可出锅\n9. 撒上白芝麻点缀',
            prep_time=20,
            cook_time=25,
            difficulty='中等',
            servings=4,
            image='tcpdg.jpg',
            user_id=chef_user.id
        )
        
        # 菜品7：鱼香肉丝
        recipe7 = Recipe(
            title='鱼香肉丝',
            description='川菜经典，鱼香味浓郁，肉丝嫩滑爽口',
            ingredients='猪里脊肉 300g\n木耳 50g\n胡萝卜 1根\n青椒 1个\n泡椒 5个\n葱姜蒜 适量\n生抽 2勺\n老抽 半勺\n醋 2勺\n糖 2勺\n淀粉 1勺\n料酒 1勺\n盐 适量',
            instructions='1. 猪里脊切丝，加料酒、盐、淀粉抓匀腌制15分钟\n2. 木耳泡发切丝，胡萝卜和青椒切丝\n3. 泡椒切碎，葱姜蒜切末\n4. 调制鱼香汁：生抽、老抽、醋、糖、淀粉和适量清水混合\n5. 热锅放油，下肉丝滑炒至变色盛出\n6. 锅中留底油，下泡椒、葱姜蒜炒香\n7. 放入木耳丝、胡萝卜丝、青椒丝翻炒\n8. 倒入肉丝，淋入鱼香汁\n9. 快速翻炒均匀即可出锅',
            prep_time=15,
            cook_time=10,
            difficulty='中等',
            servings=3,
            image='yxrs.jpg',
            user_id=normal_user.id
        )
        
        # 菜品8：清蒸鲈鱼
        recipe8 = Recipe(
            title='清蒸鲈鱼',
            description='原汁原味，鱼肉鲜嫩，营养健康',
            ingredients='鲈鱼 1条\n生姜 1块\n大葱 1根\n料酒 2勺\n蒸鱼豉油 2勺\n食用油 适量\n盐 少许',
            instructions='1. 鲈鱼处理干净，在鱼身两侧划几刀\n2. 鱼身抹上料酒和少许盐，腌制10分钟\n3. 鱼身放上姜片和葱段\n4. 锅中加水烧开，放入鲈鱼蒸8-10分钟\n5. 蒸好后倒掉盘中的水分\n6. 放上新鲜的葱丝，淋上蒸鱼豉油\n7. 锅中烧热油，淋在鱼身上即可',
            prep_time=15,
            cook_time=12,
            difficulty='简单',
            servings=3,
            image='qcly.jpg',
            user_id=normal_user.id
        )
        
        # 菜品9：酸辣土豆丝
        recipe9 = Recipe(
            title='酸辣土豆丝',
            description='爽口开胃，简单快手，家常必备',
            ingredients='土豆 2个\n干辣椒 5个\n花椒 10粒\n大蒜 3瓣\n醋 2勺\n生抽 1勺\n盐 适量\n食用油 适量',
            instructions='1. 土豆去皮切丝，用清水浸泡去除淀粉\n2. 干辣椒剪段，大蒜切末\n3. 锅中放油，下花椒和干辣椒爆香\n4. 捞出花椒不要，放入蒜末炒香\n5. 放入土豆丝大火快炒\n6. 加入醋、生抽、盐调味\n7. 炒至土豆丝断生即可出锅',
            prep_time=10,
            cook_time=8,
            difficulty='简单',
            servings=2,
            image='sltds.jpg',
            user_id=normal_user.id
        )
        
        # 菜品10：可乐鸡翅
        recipe10 = Recipe(
            title='可乐鸡翅',
            description='甜香软糯，小朋友最爱，简单易做',
            ingredients='鸡翅中 8个\n可乐 1罐\n生姜 1块\n大葱 1根\n生抽 2勺\n老抽 1勺\n料酒 1勺\n盐 适量',
            instructions='1. 鸡翅中洗净，两面各划两刀\n2. 冷水下锅焯水，加姜片和料酒去腥\n3. 鸡翅捞出沥干水分\n4. 锅中放少许油，下鸡翅煎至两面金黄\n5. 加入姜片、葱段、生抽、老抽\n6. 倒入可乐，没过鸡翅\n7. 大火烧开转小火焖煮15分钟\n8. 大火收汁即可出锅',
            prep_time=15,
            cook_time=20,
            difficulty='简单',
            servings=3,
            image='kljc.jpg',
            user_id=chef_user.id
        )
        
        # 菜品11：蛋炒饭
        recipe11 = Recipe(
            title='蛋炒饭',
            description='经典主食，粒粒分明，香气扑鼻',
            ingredients='米饭 1碗\n鸡蛋 2个\n火腿 50g\n青豆 30g\n胡萝卜 30g\n葱 1根\n盐 适量\n生抽 半勺\n食用油 适量',
            instructions='1. 火腿、胡萝卜切丁，青豆洗净\n2. 鸡蛋打散\n3. 锅中放油，下蛋液炒熟盛出\n4. 锅中再放油，下火腿丁、胡萝卜丁、青豆翻炒\n5. 倒入米饭，用勺子压散\n6. 加入炒好的鸡蛋，加盐和生抽调味\n7. 大火翻炒均匀，撒上葱花即可出锅',
            prep_time=5,
            cook_time=8,
            difficulty='简单',
            servings=1,
            image='dcf.jpg',
            user_id=admin_user.id
        )
        
        # 菜品12：水煮肉片
        recipe12 = Recipe(
            title='水煮肉片',
            description='麻辣鲜香，肉片嫩滑，川菜经典',
            ingredients='猪里脊肉 300g\n豆芽 200g\n生菜 适量\n郫县豆瓣酱 2勺\n干辣椒 10个\n花椒 1勺\n葱姜蒜 适量\n生抽 2勺\n淀粉 1勺\n料酒 1勺\n盐 适量',
            instructions='1. 猪里脊切片，加料酒、盐、淀粉抓匀腌制15分钟\n2. 豆芽和生菜洗净\n3. 锅中烧水，豆芽和生菜焯水后铺在碗底\n4. 热锅放油，下豆瓣酱炒出红油\n5. 加入姜蒜末炒香\n6. 加入适量清水烧开\n7. 放入肉片滑熟\n8. 加入生抽调味\n9. 将肉片和汤汁倒入碗中\n10. 放上干辣椒和花椒\n11. 淋上烧热的油即可',
            prep_time=20,
            cook_time=15,
            difficulty='中等',
            servings=3,
            image='szrp.jpg',
            user_id=chef_user.id
        )

        db.session.add_all([recipe1, recipe2, recipe3, recipe4, recipe5, recipe6, recipe7, recipe8, recipe9, recipe10, recipe11, recipe12])
        db.session.commit()

        # 5. 创建点赞
        print("创建点赞...")
        like1 = Like(user_id=normal_user.id, recipe_id=recipe1.id)
        like2 = Like(user_id=normal_user.id, recipe_id=recipe2.id)
        like3 = Like(user_id=normal_user.id, recipe_id=recipe4.id)
        like4 = Like(user_id=normal_user.id, recipe_id=recipe5.id)
        like5 = Like(user_id=chef_user.id, recipe_id=recipe1.id)
        like6 = Like(user_id=chef_user.id, recipe_id=recipe3.id)
        like7 = Like(user_id=admin_user.id, recipe_id=recipe4.id)
        like8 = Like(user_id=admin_user.id, recipe_id=recipe5.id)
        like9 = Like(user_id=admin_user.id, recipe_id=recipe6.id)
        like10 = Like(user_id=normal_user.id, recipe_id=recipe8.id)
        like11 = Like(user_id=chef_user.id, recipe_id=recipe10.id)
        like12 = Like(user_id=admin_user.id, recipe_id=recipe11.id)

        db.session.add_all([like1, like2, like3, like4, like5, like6, like7, like8, like9, like10, like11, like12])
        db.session.commit()

        # 6. 创建收藏
        print("创建收藏...")
        favorite1 = Favorite(user_id=normal_user.id, recipe_id=recipe1.id)
        favorite2 = Favorite(user_id=normal_user.id, recipe_id=recipe2.id)
        favorite3 = Favorite(user_id=admin_user.id, recipe_id=recipe3.id)
        favorite4 = Favorite(user_id=normal_user.id, recipe_id=recipe4.id)
        favorite5 = Favorite(user_id=chef_user.id, recipe_id=recipe2.id)
        favorite6 = Favorite(user_id=chef_user.id, recipe_id=recipe8.id)
        favorite7 = Favorite(user_id=admin_user.id, recipe_id=recipe5.id)
        favorite8 = Favorite(user_id=normal_user.id, recipe_id=recipe10.id)

        db.session.add_all([favorite1, favorite2, favorite3, favorite4, favorite5, favorite6, favorite7, favorite8])
        db.session.commit()

        # 7. 创建评论
        print("创建评论...")
        
        # 蒜蓉西兰花的评论
        comment1 = Comment(
            content='这道菜非常简单易做，味道也很好！',
            user_id=normal_user.id,
            recipe_id=recipe1.id
        )
        comment2 = Comment(
            content='建议可以加点蚝油调味，会更好吃。',
            user_id=admin_user.id,
            recipe_id=recipe1.id
        )
        comment3 = Comment(
            content='健康又美味，全家人都喜欢！',
            user_id=chef_user.id,
            recipe_id=recipe1.id
        )
        
        # 红烧肉的评论
        comment4 = Comment(
            content='红烧肉做起来有点复杂，但是真的很香！',
            user_id=normal_user.id,
            recipe_id=recipe2.id
        )
        comment5 = Comment(
            content='肥而不腻，入口即化，太棒了！',
            user_id=chef_user.id,
            recipe_id=recipe2.id
        )
        
        # 西红柿炒鸡蛋的评论
        comment6 = Comment(
            content='经典就是经典，永远吃不腻！',
            user_id=admin_user.id,
            recipe_id=recipe3.id
        )
        
        # 宫保鸡丁的评论
        comment7 = Comment(
            content='这道菜的味道太棒了！糊辣荔枝味很正宗！',
            user_id=normal_user.id,
            recipe_id=recipe4.id
        )
        comment8 = Comment(
            content='花生很脆，鸡丁很嫩，完美！',
            user_id=admin_user.id,
            recipe_id=recipe4.id
        )
        
        # 麻婆豆腐的评论
        comment9 = Comment(
            content='麻辣鲜香，太下饭了！',
            user_id=normal_user.id,
            recipe_id=recipe5.id
        )
        
        # 可乐鸡翅的评论
        comment10 = Comment(
            content='我家孩子超爱吃这个！',
            user_id=chef_user.id,
            recipe_id=recipe10.id
        )
        
        db.session.add_all([comment1, comment2, comment3, comment4, comment5, comment6, comment7, comment8, comment9, comment10])
        db.session.commit()
        
        # 回复评论
        reply1 = Comment(
            content='谢谢建议，下次试试！',
            user_id=normal_user.id,
            recipe_id=recipe1.id,
            parent_id=comment2.id
        )
        reply2 = Comment(
            content='是的！我也经常做给家人吃。',
            user_id=admin_user.id,
            recipe_id=recipe1.id,
            parent_id=comment3.id
        )
        reply3 = Comment(
            content='谢谢夸奖！',
            user_id=chef_user.id,
            recipe_id=recipe4.id,
            parent_id=comment7.id
        )
        
        db.session.add_all([reply1, reply2, reply3])
        db.session.commit()

        # 8. 创建评分
        print("创建评分...")
        rating1 = Rating(score=5, user_id=normal_user.id, recipe_id=recipe1.id)
        rating2 = Rating(score=4, user_id=admin_user.id, recipe_id=recipe1.id)
        rating3 = Rating(score=5, user_id=chef_user.id, recipe_id=recipe1.id)
        
        rating4 = Rating(score=5, user_id=normal_user.id, recipe_id=recipe2.id)
        rating5 = Rating(score=5, user_id=chef_user.id, recipe_id=recipe2.id)
        
        rating6 = Rating(score=4, user_id=admin_user.id, recipe_id=recipe3.id)
        
        rating7 = Rating(score=5, user_id=normal_user.id, recipe_id=recipe4.id)
        rating8 = Rating(score=5, user_id=admin_user.id, recipe_id=recipe4.id)
        rating9 = Rating(score=4, user_id=chef_user.id, recipe_id=recipe4.id)
        
        rating10 = Rating(score=5, user_id=normal_user.id, recipe_id=recipe5.id)
        rating11 = Rating(score=4, user_id=admin_user.id, recipe_id=recipe5.id)
        
        rating12 = Rating(score=5, user_id=chef_user.id, recipe_id=recipe6.id)
        rating13 = Rating(score=4, user_id=admin_user.id, recipe_id=recipe6.id)
        
        rating14 = Rating(score=4, user_id=normal_user.id, recipe_id=recipe8.id)
        
        rating15 = Rating(score=5, user_id=chef_user.id, recipe_id=recipe10.id)
        
        rating16 = Rating(score=5, user_id=admin_user.id, recipe_id=recipe11.id)
        
        rating17 = Rating(score=5, user_id=normal_user.id, recipe_id=recipe12.id)

        db.session.add_all([
            rating1, rating2, rating3, rating4, rating5, rating6, rating7, rating8, 
            rating9, rating10, rating11, rating12, rating13, rating14, rating15, 
            rating16, rating17
        ])
        db.session.commit()

        print("种子数据创建完成！")
        print(f"创建了 {Role.query.count()} 个角色")
        print(f"创建了 {User.query.count()} 个用户")
        print(f"创建了 {UserRole.query.count()} 个用户角色关联")
        print(f"创建了 {Recipe.query.count()} 个菜谱")
        print(f"创建了 {Like.query.count()} 个点赞")
        print(f"创建了 {Favorite.query.count()} 个收藏")
        print(f"创建了 {Comment.query.count()} 个评论")
        print(f"创建了 {Rating.query.count()} 个评分")

if __name__ == '__main__':
    create_seed_data()