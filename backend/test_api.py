#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试所有API接口"""

import requests

def test_api():
    base_url = 'http://localhost:5000/api'
    
    tests = [
        ('GET', '/recipes', None),
        ('GET', '/posts', None),
        ('POST', '/auth/login', {'username': 'user1', 'password': 'user123'})
    ]
    
    for method, endpoint, data in tests:
        url = f"{base_url}{endpoint}"
        try:
            if method == 'GET':
                response = requests.get(url)
            elif method == 'POST':
                response = requests.post(url, json=data)
            
            print(f"{method} {endpoint}: {response.status_code}")
            if response.status_code != 200:
                print(f"  Error: {response.text[:200]}")
            else:
                print(f"  Success")
        except Exception as e:
            print(f"{method} {endpoint}: ERROR - {e}")

if __name__ == '__main__':
    test_api()
