import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import sys
sys.path.insert(0, '.')

# 直接导入避免与app包冲突
import importlib.util
spec = importlib.util.spec_from_file_location("app_module", "app.py")
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

from models import db, Recipe, User

app = app_module.create_app()

def add_test_recipes():
    """添加测试菜谱数据"""
    with app.app_context():
        # 检查是否已有测试用户
        user = User.query.filter_by(username='testuser').first()
        if not user:
            print("测试用户不存在，请先运行 init_mysql_db.py 创建测试用户")
            return

        # 删除所有已存在的菜谱
        existing_recipes = Recipe.query.count()
        if existing_recipes > 0:
            print(f"删除数据库中已有的 {existing_recipes} 个菜谱...")
            Recipe.query.delete()
            db.session.commit()
            print("✓ 已删除旧菜谱数据")

        # 创建三个测试菜谱
        recipes = [
            Recipe(
                title='蒜蓉西兰花',
                description='健康素食，清爽可口，蒜香浓郁，营养丰富',
                ingredients='西兰花 1个（约500g）\n大蒜 1整头\n葱 1根\n姜 2片\n盐 1勺\n生抽 2勺\n蚝油 1勺\n食用油 适量\n鸡精 少许（可选）',
                instructions='1. 西兰花洗净切小朵，茎部去皮切片\n2. 大蒜去皮切成蒜末\n3. 葱切葱花，姜切片\n4. 烧一锅开水，加少许盐和几滴油\n5. 下西兰花焯水1分钟，捞出过凉水沥干\n6. 热锅下油，下姜片爆香\n7. 下一半蒜末炒至金黄\n8. 倒入西兰花大火翻炒\n9. 加生抽、蚝油、盐调味\n10. 撒上剩余蒜末翻炒均匀\n11. 最后撒葱花即可出锅',
                prep_time=10,
                cook_time=5,
                difficulty='简单',
                servings=3,
                user_id=user.id,
                image='/static/uploads/images/srxlh.jpg'
            ),
            Recipe(
                title='红烧肉',
                description='传统家常菜，肥而不腻，入口即化，色泽红亮',
                ingredients='五花肉 500g\n冰糖 30g\n葱 2根\n姜 3片\n蒜 3瓣\n八角 2个\n桂皮 1小块\n香叶 2片\n生抽 3勺\n老抽 2勺\n料酒 2勺\n盐 适量',
                instructions='1. 五花肉切块，冷水下锅焯水去腥\n2. 捞出沥干水分备用\n3. 葱切段，姜蒜切片\n4. 热锅不放油，直接下五花肉中小火煸炒出油\n5. 炒至肉块表面微黄，盛出备用\n6. 锅内留少许油，下冰糖小火炒糖色\n7. 糖色炒至焦糖色冒小泡\n8. 下肉块快速翻炒上色\n9. 加入葱姜蒜、八角、桂皮、香叶翻炒\n10. 加入料酒、生抽、老抽翻炒\n11. 加入开水没过肉块\n12. 大火烧开后转小火炖1小时\n13. 最后大火收汁即可',
                prep_time=15,
                cook_time=60,
                difficulty='中等',
                servings=6,
                user_id=user.id,
                image='/static/uploads/images/hsr.jpg'
            ),
            Recipe(
                title='西红柿炒鸡蛋',
                description='国民家常菜，酸甜可口，简单易学，营养均衡',
                ingredients='鸡蛋 4个\n西红柿 3个\n葱 1根\n盐 1勺\n糖 1勺\n油 适量\n番茄酱 1勺（可选）',
                instructions='1. 鸡蛋打散，加少许盐搅拌均匀\n2. 西红柿洗净切块\n3. 葱切葱花\n4. 热锅下油，油热后下蛋液\n5. 鸡蛋炒至凝固后盛出备用\n6. 锅内再加少许油，下西红柿块\n7. 中小火翻炒至西红柿出汁\n8. 可加一勺番茄酱增加风味\n9. 倒入鸡蛋翻炒均匀\n10. 加盐和糖调味\n11. 撒上葱花即可出锅',
                prep_time=10,
                cook_time=8,
                difficulty='简单',
                servings=2,
                user_id=user.id,
                image='/static/uploads/images/xhscjd.jpg'
            )
        ]

        try:
            db.session.bulk_save_objects(recipes)
            db.session.commit()
            print("✓ 成功添加 3 个测试菜谱！")
            print("\n添加的菜谱：")
            for recipe in recipes:
                print(f"  - {recipe.title}（{recipe.difficulty}）")
        except Exception as e:
            db.session.rollback()
            print(f"✗ 添加菜谱失败: {str(e)}")

if __name__ == '__main__':
    add_test_recipes()
