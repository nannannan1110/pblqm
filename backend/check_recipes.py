#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查菜谱数据"""

import requests

try:
    r = requests.get('http://localhost:5000/api/recipes')
    data = r.json()
    recipes = data.get('recipes', [])
    print(f'当前菜谱数量: {len(recipes)}')
    for r in recipes:
        print(f"  - {r['title']} ({r['image']})")
except Exception as e:
    print(f'Error: {e}')
