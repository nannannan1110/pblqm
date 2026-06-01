"""
检查数据库中的菜谱数据
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入应用和模型
from app import create_app
from models import db, Recipe, User

def check_recipes():
    """检查菜谱是否存在"""
    app = create_app()

    with app.app_context():
        # 查找目标菜谱
        target_recipes = ['蒜蓉西兰花', '红烧肉', '西红柿炒鸡蛋']

        print("=" * 60)
        print("检查数据库中的菜谱...")
        print("=" * 60)

        existing_recipes = []
        missing_recipes = []

        for recipe_name in target_recipes:
            recipe = Recipe.query.filter_by(title=recipe_name).first()
            if recipe:
                existing_recipes.append(recipe)
                print(f"\n✓ 找到菜谱: {recipe.title}")
                print(f"  ID: {recipe.id}")
                print(f"  创建者: {recipe.user.username if recipe.user else '未知'}")
                print(f"  描述: {recipe.description}")
            else:
                missing_recipes.append(recipe_name)
                print(f"\n✗ 未找到菜谱: {recipe_name}")

        print("\n" + "=" * 60)
        print(f"找到 {len(existing_recipes)} 个菜谱，缺失 {len(missing_recipes)} 个菜谱")
        print("=" * 60)

        # 如果有缺失的菜谱，显示所有菜谱列表
        if missing_recipes:
            print("\n数据库中所有菜谱列表：")
            all_recipes = Recipe.query.all()
            for i, recipe in enumerate(all_recipes, 1):
                print(f"{i}. {recipe.title} (ID: {recipe.id})")

        return existing_recipes, missing_recipes

if __name__ == '__main__':
    existing, missing = check_recipes()
