#!/usr/bin/env python3
"""
种子数据创建脚本
为数据库创建初始测试数据
"""

from simple_server import app, db
from models import User, Recipe, Role, UserRole, Favorite, Comment, Rating

def create_seed_data():
    """创建种子数据"""
    with app.app_context():
        print("开始创建种子数据...")

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

        db.session.add_all([admin_user, normal_user])
        db.session.commit()

        # 3. 分配角色
        print("分配用户角色...")
        admin_role_assignment = UserRole(user_id=admin_user.id, role_id=admin_role.id)
        user_role_assignment = UserRole(user_id=normal_user.id, role_id=user_role.id)

        db.session.add_all([admin_role_assignment, user_role_assignment])
        db.session.commit()

        # 4. 创建菜谱
        print("创建菜谱...")
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

        db.session.add_all([recipe1, recipe2, recipe3])
        db.session.commit()

        # 6. 创建收藏
        print("创建收藏...")
        favorite1 = Favorite(user_id=normal_user.id, recipe_id=recipe1.id)
        favorite2 = Favorite(user_id=normal_user.id, recipe_id=recipe2.id)
        favorite3 = Favorite(user_id=admin_user.id, recipe_id=recipe3.id)

        db.session.add_all([favorite1, favorite2, favorite3])
        db.session.commit()

        # 7. 创建评论
        print("创建评论...")
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

        db.session.add_all([comment1, comment2])
        db.session.commit()

        # 回复评论
        reply1 = Comment(
            content='谢谢建议，下次试试！',
            user_id=normal_user.id,
            recipe_id=recipe1.id,
            parent_id=comment2.id
        )

        comment3 = Comment(
            content='红烧肉做起来有点复杂，但是真的很香！',
            user_id=normal_user.id,
            recipe_id=recipe2.id
        )

        db.session.add_all([reply1, comment3])
        db.session.commit()

        # 8. 创建评分
        print("创建评分...")
        rating1 = Rating(score=5, user_id=normal_user.id, recipe_id=recipe1.id)
        rating2 = Rating(score=4, user_id=admin_user.id, recipe_id=recipe1.id)
        rating3 = Rating(score=5, user_id=normal_user.id, recipe_id=recipe2.id)
        rating4 = Rating(score=4, user_id=admin_user.id, recipe_id=recipe3.id)

        db.session.add_all([rating1, rating2, rating3, rating4])
        db.session.commit()

        print("种子数据创建完成！")
        print(f"创建了 {Role.query.count()} 个角色")
        print(f"创建了 {User.query.count()} 个用户")
        print(f"创建了 {UserRole.query.count()} 个用户角色关联")
        print(f"创建了 {Recipe.query.count()} 个菜谱")
        print(f"创建了 {Favorite.query.count()} 个收藏")
        print(f"创建了 {Comment.query.count()} 个评论")
        print(f"创建了 {Rating.query.count()} 个评分")

if __name__ == '__main__':
    create_seed_data()