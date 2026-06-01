#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
管理员API测试脚本
测试所有管理员后台API是否正常工作
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json

BASE_URL = 'http://localhost:5000'

def test_admin_apis():
    """测试所有管理员API"""

    print('=' * 70)
    print('              管理员后台API测试')
    print('=' * 70)

    # 1. 登录获取token
    print('\n[1/5] 测试管理员登录...')
    login_data = {'username': 'admin', 'password': 'admin123'}

    try:
        login_resp = requests.post(f'{BASE_URL}/api/auth/login', json=login_data)

        if login_resp.status_code != 200:
            print(f'      [失败] 登录失败: {login_resp.text}')
            return False

        result = login_resp.json()
        token = result.get('access_token')
        print(f'      [成功] 登录成功')
        print(f'      Token: {token[:50]}...')

        headers = {'Authorization': f'Bearer {token}'}

        # 2. 测试统计API
        print('\n[2/5] 测试统计API (/api/admin/statistics)...')
        resp = requests.get(f'{BASE_URL}/api/admin/statistics', headers=headers)

        if resp.status_code == 200:
            data = resp.json()
            print(f'      [成功] 状态码: {resp.status_code}')
            print(f'      数据: 用户={data["user_count"]}, 菜谱={data["recipe_count"]}, 评论={data["comment_count"]}, 收藏={data["favorite_count"]}, 点赞={data["like_count"]}')
        else:
            print(f'      [失败] 状态码: {resp.status_code}')
            print(f'      错误: {resp.text}')

        # 3. 测试用户列表API
        print('\n[3/5] 测试用户列表API (/api/admin/users)...')
        resp = requests.get(f'{BASE_URL}/api/admin/users', headers=headers)

        if resp.status_code == 200:
            data = resp.json()
            print(f'      [成功] 状态码: {resp.status_code}')
            print(f'      数据: 获取到 {len(data["users"])} 个用户, 总计 {data["total"]} 个')
            if data['users']:
                print(f'      示例用户: {data["users"][0]["username"]}')
        else:
            print(f'      [失败] 状态码: {resp.status_code}')
            print(f'      错误: {resp.text}')

        # 4. 测试菜谱列表API
        print('\n[4/5] 测试菜谱列表API (/api/admin/recipes)...')
        resp = requests.get(f'{BASE_URL}/api/admin/recipes', headers=headers)

        if resp.status_code == 200:
            data = resp.json()
            print(f'      [成功] 状态码: {resp.status_code}')
            print(f'      数据: 获取到 {len(data["recipes"])} 个菜谱, 总计 {data["total"]} 个')
            if data['recipes']:
                print(f'      示例菜谱: {data["recipes"][0]["title"]}')
        else:
            print(f'      [失败] 状态码: {resp.status_code}')
            print(f'      错误: {resp.text}')

        # 5. 测试评论列表API
        print('\n[5/5] 测试评论列表API (/api/admin/comments)...')
        resp = requests.get(f'{BASE_URL}/api/admin/comments', headers=headers)

        if resp.status_code == 200:
            data = resp.json()
            print(f'      [成功] 状态码: {resp.status_code}')
            print(f'      数据: 获取到 {len(data["comments"])} 条评论, 总计 {data["total"]} 条')
            if data['comments']:
                print(f'      示例评论: {data["comments"][0]["content"][:30]}...')
        else:
            print(f'      [失败] 状态码: {resp.status_code}')
            print(f'      错误: {resp.text}')

        print('\n' + '=' * 70)
        print('           所有API测试完成！')
        print('=' * 70)

        return True

    except requests.exceptions.ConnectionError:
        print(f'\n[错误] 无法连接到服务器')
        print(f'       请确保后端服务器正在运行: python app.py')
        return False
    except Exception as e:
        print(f'\n[错误] 测试失败: {e}')
        return False

if __name__ == '__main__':
    test_admin_apis()
