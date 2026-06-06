import sys
sys.path.insert(0, '.')

# 直接导入 app.py
import app
from app.models.post import Post

# 创建应用上下文
flask_app = app.create_app()
with flask_app.app_context():
    from app import db
    # 检查是否已有帖子
    if Post.query.count() == 0:
        print("Adding sample posts...")
        
        # 创建示例帖子
        posts_data = [
            {
                'user_id': 1,
                'title': 'My First Homemade Pasta!',
                'content': 'Just tried making fresh pasta from scratch for the first time. It was challenging but the result was amazing!'
            },
            {
                'user_id': 2,
                'title': 'Tips for Perfect Fried Rice',
                'content': 'After years of practice, here are my tips for perfect fried rice: Use day-old rice, high heat is essential, keep everything moving.'
            },
            {
                'user_id': 3,
                'title': 'Mastering Stir-Fry Technique',
                'content': 'Stir-fry is all about timing and heat control. Today I\'m sharing my secret to getting that perfect wok hei at home.'
            }
        ]
        
        for data in posts_data:
            post = Post(**data)
            db.session.add(post)
        
        db.session.commit()
        print("Sample posts added successfully!")
    else:
        print(f"Already have {Post.query.count()} posts in database.")
