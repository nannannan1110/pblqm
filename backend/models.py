#!/usr/bin/env python3
"""
数据库模型定义
包含所有数据表的SQLAlchemy模型定义
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# 创建SQLAlchemy实例
db = SQLAlchemy()


class User(db.Model):
    """用户表"""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    recipes = db.relationship('Recipe', backref='user', lazy=True, cascade='all, delete-orphan')
    user_roles = db.relationship('UserRole', backref='user', lazy=True, cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', backref='user', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='user', lazy=True, cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='user', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        """检查用户是否为管理员"""
        # 检查用户是否有管理员角色
        return UserRole.query.filter_by(user_id=self.id).join(Role).filter(
            Role.name == '管理员'
        ).first() is not None

    def has_role(self, role_name):
        """检查用户是否拥有指定角色"""
        return UserRole.query.filter_by(user_id=self.id).join(Role).filter(
            Role.name == role_name
        ).first() is not None

    def can_edit_recipe(self, recipe):
        """检查用户是否可以编辑菜谱（只有菜谱创建者可以编辑）"""
        return self.id == recipe.user_id

    def can_delete_recipe(self, recipe):
        """检查用户是否可以删除菜谱（菜谱创建者或管理员可以删除）"""
        return self.id == recipe.user_id or self.is_admin()

    def can_manage_comment(self, comment):
        """检查用户是否可以管理评论（评论作者、菜谱创建者或管理员）"""
        return self.id == comment.user_id or self.id == comment.recipe.user_id or self.is_admin()

    def has_liked_recipe(self, recipe_id):
        """检查用户是否已点赞菜谱"""
        return Like.query.filter_by(user_id=self.id, recipe_id=recipe_id).first() is not None

    def has_favorited_recipe(self, recipe_id):
        """检查用户是否已收藏菜谱"""
        return Favorite.query.filter_by(user_id=self.id, recipe_id=recipe_id).first() is not None

    def to_dict(self, include_roles=False):
        """转换为字典"""
        result = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'is_admin': self.is_admin()
        }

        if include_roles:
            result['roles'] = [ur.to_dict() for ur in self.user_roles]

        return result


class Recipe(db.Model):
    """菜谱表"""
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    prep_time = db.Column(db.Integer)  # 准备时间(分钟)
    cook_time = db.Column(db.Integer)  # 烹饪时间(分钟)
    difficulty = db.Column(db.String(20))
    servings = db.Column(db.Integer)  # 份数
    image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # 关系
    favorites = db.relationship('Favorite', backref='recipe', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='recipe', lazy=True, cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='recipe', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='recipe', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, current_user_id=None):
        """转换为字典"""
        # 计算统计信息
        likes_count = len(self.likes) if self.likes else 0
        favorites_count = len(self.favorites) if self.favorites else 0
        comments_count = len(self.comments) if self.comments else 0

        # 计算平均评分
        avg_rating = 0
        if self.ratings:
            avg_rating = sum(r.score for r in self.ratings) / len(self.ratings)
            avg_rating = round(avg_rating, 1)

        # 检查当前用户的交互状态
        is_liked = False
        is_favorited = False
        user_rating = None

        if current_user_id:
            is_liked = any(like.user_id == current_user_id for like in self.likes) if self.likes else False
            is_favorited = any(fav.user_id == current_user_id for fav in self.favorites) if self.favorites else False
            user_rating_obj = next((r for r in self.ratings if r.user_id == current_user_id), None)
            user_rating = user_rating_obj.score if user_rating_obj else None

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
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id,
            'author': self.user.username if self.user else None,
            'stats': {
                'likes_count': likes_count,
                'favorites_count': favorites_count,
                'comments_count': comments_count,
                'avg_rating': avg_rating,
                'ratings_count': len(self.ratings) if self.ratings else 0
            },
            'user_interaction': {
                'is_liked': is_liked,
                'is_favorited': is_favorited,
                'user_rating': user_rating
            } if current_user_id else None
        }


class Role(db.Model):
    """角色表"""
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    user_roles = db.relationship('UserRole', backref='role', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }


class UserRole(db.Model):
    """用户角色关联表"""
    __tablename__ = 'user_role'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 复合唯一索引
    __table_args__ = (
        db.UniqueConstraint('user_id', 'role_id', name='unique_user_role'),
    )

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'role_id': self.role_id,
            'role_name': self.role.name if self.role else None,
            'created_at': self.created_at.isoformat()
        }


class Favorite(db.Model):
    """收藏表"""
    __tablename__ = 'favorite'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 复合唯一索引
    __table_args__ = (
        db.UniqueConstraint('user_id', 'recipe_id', name='unique_user_favorite'),
    )

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'recipe_id': self.recipe_id,
            'recipe_title': self.recipe.title if self.recipe else None,
            'created_at': self.created_at.isoformat()
        }


class Comment(db.Model):
    """评论表"""
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=5)  # 评分(1-5)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))  # 支持回复评论
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 自关联（支持回复评论）
    parent = db.relationship('Comment', remote_side=[id], backref='replies')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'content': self.content,
            'rating': self.rating,  # 添加评分字段
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'recipe_id': self.recipe_id,
            'parent_id': self.parent_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'replies_count': len(self.replies) if self.replies else 0,
            'user': {
                'id': self.user.id,
                'username': self.user.username if self.user else None
            } if self.user else None
        }


class Rating(db.Model):
    """评分表"""
    __tablename__ = 'rating'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)  # 1-5分
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 复合唯一索引（每个用户对每个菜谱只能评分一次）
    __table_args__ = (
        db.UniqueConstraint('user_id', 'recipe_id', name='unique_user_rating'),
        db.CheckConstraint('score >= 1 AND score <= 5', name='check_score_range'),
    )

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'score': self.score,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'recipe_id': self.recipe_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Like(db.Model):
    """点赞表"""
    __tablename__ = 'like'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 复合唯一索引（每个用户对每个菜谱只能点赞一次）
    __table_args__ = (
        db.UniqueConstraint('user_id', 'recipe_id', name='unique_user_like'),
    )

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'recipe_id': self.recipe_id,
            'recipe_title': self.recipe.title if self.recipe else None,
            'created_at': self.created_at.isoformat()
        }