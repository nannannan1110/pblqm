#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除指定菜谱的脚本
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pymysql

def delete_recipe(recipe_title):
    """删除指定标题的菜谱及其所有关联数据"""

    try:
        # 连接数据库
        conn = pymysql.connect(host='localhost', user='root', password='123456', database='pbl')
        cursor = conn.cursor()

        # 查找菜谱
        cursor.execute('SELECT id, title FROM recipe WHERE title = %s', (recipe_title,))
        recipe = cursor.fetchone()

        if not recipe:
            print(f'[错误] 未找到菜谱: {recipe_title}')
            return False

        recipe_id = recipe[0]
        print(f'找到菜谱: ID={recipe_id}, 标题={recipe[1]}')

        # 开始删除事务
        try:
            # 1. 删除评论
            cursor.execute('DELETE FROM comment WHERE recipe_id = %s', (recipe_id,))
            comments_deleted = cursor.rowcount
            print(f'[OK] 删除了 {comments_deleted} 条评论')

            # 2. 删除评分
            cursor.execute('DELETE FROM rating WHERE recipe_id = %s', (recipe_id,))
            ratings_deleted = cursor.rowcount
            print(f'[OK] 删除了 {ratings_deleted} 条评分')

            # 3. 删除点赞
            cursor.execute('DELETE FROM `like` WHERE recipe_id = %s', (recipe_id,))
            likes_deleted = cursor.rowcount
            print(f'[OK] 删除了 {likes_deleted} 条点赞')

            # 4. 删除收藏
            cursor.execute('DELETE FROM favorite WHERE recipe_id = %s', (recipe_id,))
            favorites_deleted = cursor.rowcount
            print(f'[OK] 删除了 {favorites_deleted} 条收藏')

            # 5. 删除分类关联
            cursor.execute('DELETE FROM recipe_category WHERE recipe_id = %s', (recipe_id,))
            categories_deleted = cursor.rowcount
            print(f'[OK] 删除了 {categories_deleted} 条分类关联')

            # 6. 最后删除菜谱本身
            cursor.execute('DELETE FROM recipe WHERE id = %s', (recipe_id,))
            recipes_deleted = cursor.rowcount
            print(f'[OK] 删除了 {recipes_deleted} 条菜谱记录')

            # 提交事务
            conn.commit()
            print(f'\n[成功] 已删除菜谱 "{recipe_title}" 及其所有关联数据！')
            return True

        except Exception as e:
            # 发生错误，回滚事务
            conn.rollback()
            print(f'\n[错误] 删除失败，已回滚所有更改: {e}')
            return False

    except Exception as e:
        print(f'[错误] 数据库连接错误: {e}')
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python delete_recipe.py "<菜谱标题>"')
        print('示例: python delete_recipe.py "回锅肉"')
        sys.exit(1)

    recipe_title = sys.argv[1]
    delete_recipe(recipe_title)
