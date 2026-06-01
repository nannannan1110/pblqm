from datetime import datetime
from app import db

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    prep_time = db.Column(db.Integer)  # 分钟
    cook_time = db.Column(db.Integer)  # 分钟
    difficulty = db.Column(db.String(20))  # 简单/中等/困难
    servings = db.Column(db.Integer)
    image = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 暂时移除关系以避免循环导入
    # comments = db.relationship('Comment', backref='recipe', lazy=True)
    # tags = db.relationship('Tag', secondary='recipe_tags', backref='recipes')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'difficulty': self.difficulty,
            'servings': self.servings,
            'image': self.image,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat()
        }
