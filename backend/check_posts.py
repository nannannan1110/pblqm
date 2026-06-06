#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查帖子API"""

import requests

try:
    r = requests.get('http://localhost:5000/api/posts')
    print(f'Status: {r.status_code}')
    data = r.json()
    print(f'Total posts: {data.get("total", 0)}')
    posts = data.get('posts', [])
    for p in posts[:5]:
        print(f"  - {p['title']}")
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
