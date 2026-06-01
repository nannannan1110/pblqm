#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除分类管理相关的数据库表
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pymysql

def delete_category_tables():
    """删除分类相关的数据库表"""

    try:
        # 连接数据库
        conn = pymysql.connect(host='localhost', user='root', password='123456', database='pbl')
        cursor = conn.cursor()

        print('=' * 60)
        print('           删除分类相关表')
        print('=' * 60)

        # 先查看有哪些表
        cursor.execute('SHOW TABLES')
        all_tables = [t[0] for t in cursor.fetchall()]
        print(f'\n当前数据库共有 {len(all_tables)} 个表')

        # 检查分类表是否存在
        category_exists = 'category' in all_tables
        recipe_category_exists = 'recipe_category' in all_tables

        if not category_exists and not recipe_category_exists:
            print('\n[提示] 分类表不存在，无需删除')
            return True

        # 开始删除事务
        try:
            # 1. 先删除关联表 recipe_category（因为它有外键）
            if recipe_category_exists:
                cursor.execute('SELECT COUNT(*) FROM recipe_category')
                rc_count = cursor.fetchone()[0]
                print(f'\n[1/2] 删除 recipe_category 表 ({rc_count} 条记录)...')
                cursor.execute('DROP TABLE recipe_category')
                print(f'      [OK] recipe_category 表已删除')

            # 2. 删除 category 表
            if category_exists:
                cursor.execute('SELECT COUNT(*) FROM category')
                c_count = cursor.fetchone()[0]
                print(f'\n[2/2] 删除 category 表 ({c_count} 条记录)...')
                cursor.execute('DROP TABLE category')
                print(f'      [OK] category 表已删除')

            # 提交事务
            conn.commit()

            print('\n' + '=' * 60)
            print('[成功] 分类相关的表已全部删除！')
            print('=' * 60)

            # 验证删除结果
            cursor.execute('SHOW TABLES')
            remaining_tables = [t[0] for t in cursor.fetchall()]
            print(f'\n剩余表数量: {len(remaining_tables)}')

            category_related = [t for t in remaining_tables if 'category' in t.lower()]
            if category_related:
                print(f'[警告] 仍有分类相关表: {category_related}')
            else:
                print('[验证] 无分类相关表残留')

            return True

        except Exception as e:
            # 发生错误，回滚事务
            conn.rollback()
            print(f'\n[错误] 删除失败，已回滚: {e}')
            return False

    except Exception as e:
        print(f'[错误] 数据库连接错误: {e}')
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    delete_category_tables()
