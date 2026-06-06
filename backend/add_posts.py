#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加示例帖子数据
"""

import sys
sys.path.insert(0, '.')

import models
import app as app_module
from app.models.post import Post

# 创建应用上下文
app = app_module.create_app()
with app.app_context():
    # 检查是否已有帖子
    post_count = Post.query.count()
    print(f"当前数据库中有 {post_count} 篇帖子")
    
    if post_count == 0:
        print("正在添加示例帖子...")
        
        # 创建示例帖子
        sample_posts = [
            {
                'user_id': 1,
                'title': '第一次做手工意大利面',
                'content': '今天尝试第一次做手工意大利面，虽然过程有点挑战，但结果非常棒！关键是要让面团充分休息。'
            },
            {
                'user_id': 2,
                'title': '完美炒饭的秘诀',
                'content': '经过多年的实践，我总结出完美炒饭的几个要点：\n1. 使用隔夜饭\n2. 火候要大\n3. 不停翻炒\n4. 不要让锅太满\n5. 适时添加调味料'
            },
            {
                'user_id': 3,
                'title': '掌握炒菜技巧',
                'content': '炒菜的关键在于时间和火候的控制。今天我来分享在家做出完美"锅气"的秘诀。'
            },
            {
                'user_id': 1,
                'title': '周末烘焙之旅',
                'content': '整个周末都在烘焙！做了酸面包、可颂和一些饼干。早上新鲜出炉的香气真是太棒了！'
            },
            {
                'user_id': 2,
                'title': '亚洲融合菜谱创意',
                'content': '我一直在尝试将亚洲风味与西方烹饪技巧相结合。这里分享一些我成功尝试过的组合。'
            }
        ]
        
        for post_data in sample_posts:
            post = Post(**post_data)
            models.db.session.add(post)
        
        models.db.session.commit()
        print("✅ 成功添加了 5 篇示例帖子！")
    else:
        print("数据库中已有帖子，跳过添加")
