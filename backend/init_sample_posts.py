#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化示例帖子数据
"""

import os
import sys
import io

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加backend目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import db
from app.models.post import Post

def init_sample_posts():
    """初始化示例帖子数据"""
    
    # 检查是否已有帖子数据
    existing_posts = Post.query.count()
    if existing_posts > 0:
        print(f"Database already has {existing_posts} posts. Skipping...")
        return
    
    print("Creating sample posts...")
    
    # 创建一些示例帖子
    sample_posts = [
        {
            'user_id': 1,  # admin用户
            'title': 'My First Homemade Pasta!',
            'content': 'Just tried making fresh pasta from scratch for the first time. It was challenging but the result was amazing! The key is to let the dough rest properly.',
            'image': 'srxlh.jpg'  # 使用已有的图片
        },
        {
            'user_id': 2,  # user1
            'title': 'Tips for Perfect Fried Rice',
            'content': 'After years of practice, here are my tips for perfect fried rice:\n1. Use day-old rice\n2. High heat is essential\n3. Keep everything moving\n4. Don\'t overcrowd the wok\n5. Add seasonings at the right time',
            'image': 'hsr.jpg'
        },
        {
            'user_id': 3,  # chef1
            'title': 'Mastering Stir-Fry Technique',
            'content': 'Stir-fry is all about timing and heat control. Today I\'m sharing my secret to getting that perfect "wok hei" (breath of the wok) at home.',
            'image': 'xhscjd.jpg'
        },
        {
            'user_id': 1,  # admin
            'title': 'Weekend Baking Adventure',
            'content': 'Spent the whole weekend baking! Made sourdough bread, croissants, and some cookies. Nothing beats the smell of fresh baked goods in the morning.',
            'image': '418b20a3838e4ae8a5808ceba994a87e.jpg'
        },
        {
            'user_id': 2,  # user1
            'title': 'Asian Fusion Recipe Ideas',
            'content': 'I\'ve been experimenting with fusion recipes combining Asian flavors with Western techniques. Here are some successful combinations I\'ve tried.',
            'image': '93dd19494ba44895a1d5772d05024c27.jpg'
        }
    ]
    
    for post_data in sample_posts:
        post = Post(**post_data)
        db.session.add(post)
    
    db.session.commit()
    print(f"Created {len(sample_posts)} sample posts!")

if __name__ == '__main__':
    # 直接导入app.py中的函数
    from init_demo_data import init_db
    
    # 简单的数据库初始化
    from app import db
    from app.models.post import Post
    
    # 注意：这需要在backend目录下运行
    # python init_sample_posts.py
    
    init_sample_posts()
    print("Sample posts initialization completed!")
