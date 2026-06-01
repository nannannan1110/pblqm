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

from models import db, Recipe

app = app_module.create_app()

def update_difficulties():
    """更新菜谱难度"""
    with app.app_context():
        # 查找所有菜谱
        recipes = Recipe.query.all()

        for recipe in recipes:
            if recipe.title == '蒜蓉西兰花':
                recipe.difficulty = '中等'
                print(f"✓ 更新 {recipe.title} 难度: 简单 → 中等")
            elif recipe.title == '红烧肉':
                recipe.difficulty = '困难'
                print(f"✓ 更新 {recipe.title} 难度: 中等 → 困难")
            elif recipe.title == '西红柿炒鸡蛋':
                # 保持简单
                print(f"- {recipe.title} 难度保持: {recipe.difficulty}")

        try:
            db.session.commit()
            print("\n✓ 所有菜谱难度更新成功！")
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ 更新失败: {str(e)}")

if __name__ == '__main__':
    update_difficulties()
