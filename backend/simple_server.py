#!/usr/bin/env python3
"""
简化的Flask服务器
"""

import os
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, jsonify, request, g
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

# 创建Flask应用
app = Flask(__name__)

# 配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key-2024'

# 初始化扩展
from models import db
db.init_app(app)
CORS(app, origins=['http://localhost:8080', 'http://localhost:8081', 'http://127.0.0.1:8080', 'http://127.0.0.1:8081'])

# 导入所有模型
from models import (
    User, Recipe, Role, UserRole,
    Favorite, Comment, Rating, Like,
    Category, RecipeCategory
)


# ============= 权限验证装饰器 =============
def require_admin(f):
    """管理员权限验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从请求头获取用户信息 (实际应用中应该使用JWT)
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return jsonify({'error': '需要登录'}), 401

        try:
            user = User.query.get(int(user_id))
            if not user or not user.is_admin():
                return jsonify({'error': '需要管理员权限'}), 403

            g.current_user = user
            return f(*args, **kwargs)
        except (ValueError, TypeError):
            return jsonify({'error': '无效的用户ID'}), 401

    return decorated_function


def require_auth(f):
    """用户认证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从请求头获取用户信息 (实际应用中应该使用JWT)
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return jsonify({'error': '需要登录'}), 401

        try:
            user = User.query.get(int(user_id))
            if not user:
                return jsonify({'error': '用户不存在'}), 401

            g.current_user = user
            return f(*args, **kwargs)
        except (ValueError, TypeError):
            return jsonify({'error': '无效的用户ID'}), 401

    return decorated_function


# ============= 管理员用户管理 API =============
@app.route('/api/admin/users', methods=['GET'])
@require_admin
def get_users_admin():
    """管理员获取用户列表"""
    try:
        # 获取分页和搜索参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        role_filter = request.args.get('role', '')

        # 构建查询
        query = User.query

        # 搜索功能
        if search:
            query = query.filter(
                (User.username.contains(search)) |
                (User.email.contains(search))
            )

        # 角色过滤
        if role_filter:
            query = query.join(UserRole).join(Role).filter(Role.name == role_filter)

        # 执行分页查询
        pagination = query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        users = pagination.items
        return jsonify({
            'users': [user.to_dict(include_roles=True) for user in users],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/users/<int:user_id>', methods=['GET'])
@require_admin
def get_user_admin(user_id):
    """管理员获取单个用户详情"""
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict(include_roles=True))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/users/<int:user_id>', methods=['PUT'])
@require_admin
def update_user_admin(user_id):
    """管理员编辑用户信息"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()

        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400

        # 更新用户信息
        if 'username' in data and data['username'] != user.username:
            # 检查用户名是否已存在
            if User.query.filter_by(username=data['username']).first():
                return jsonify({'error': '用户名已存在'}), 400
            user.username = data['username']

        if 'email' in data and data['email'] != user.email:
            # 检查邮箱是否已存在
            if User.query.filter_by(email=data['email']).first():
                return jsonify({'error': '邮箱已存在'}), 400
            user.email = data['email']

        if 'password' in data and data['password']:
            user.set_password(data['password'])

        db.session.commit()

        return jsonify({
            'message': '用户信息更新成功',
            'user': user.to_dict(include_roles=True)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@require_admin
def delete_user_admin(user_id):
    """管理员删除用户"""
    try:
        user = User.query.get_or_404(user_id)

        # 防止删除自己
        if g.current_user.id == user_id:
            return jsonify({'error': '不能删除自己'}), 400

        # 检查用户是否有菜谱
        recipes_count = Recipe.query.filter_by(user_id=user_id).count()
        if recipes_count > 0:
            return jsonify({
                'error': f'该用户有 {recipes_count} 个菜谱，无法删除',
                'has_recipes': True,
                'recipes_count': recipes_count
            }), 400

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': '用户删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============= 管理员角色管理 API =============
@app.route('/api/admin/users/<int:user_id>/roles', methods=['PUT'])
@require_admin
def update_user_roles_admin(user_id):
    """管理员更新用户角色"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()

        if not data or 'role_ids' not in data:
            return jsonify({'error': '角色ID列表不能为空'}), 400

        # 防止修改自己的角色
        if g.current_user.id == user_id:
            return jsonify({'error': '不能修改自己的角色'}), 400

        # 删除用户现有角色
        UserRole.query.filter_by(user_id=user_id).delete()

        # 分配新角色
        for role_id in data['role_ids']:
            role = Role.query.get(role_id)
            if role:
                user_role = UserRole(user_id=user_id, role_id=role_id)
                db.session.add(user_role)

        db.session.commit()

        return jsonify({
            'message': '用户角色更新成功',
            'roles': [ur.to_dict() for ur in user.user_roles]
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# API路由
@app.route('/')
def index():
    return jsonify({
        'message': '菜谱分享系统API',
        'version': '1.0.0',
        'status': 'running'
    })

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/recipes', methods=['GET'])
@app.route('/api/recipes/', methods=['GET'])
def get_recipes():
    try:
        # 获取当前用户ID（如果已登录）
        current_user_id = None
        user_id_header = request.headers.get('X-User-ID')
        if user_id_header:
            try:
                current_user_id = int(user_id_header)
            except ValueError:
                pass
                
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)

        # 获取过滤参数
        difficulty = request.args.get('difficulty')
        search = request.args.get('search')

        # 构建查询
        query = Recipe.query

        # 应用过滤条件
        if difficulty:
            query = query.filter(Recipe.difficulty == difficulty)

        if search:
            query = query.filter(Recipe.title.contains(search) | Recipe.description.contains(search))

        # 执行分页查询
        pagination = query.order_by(Recipe.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        recipes = pagination.items

        return jsonify({
            'recipes': [recipe.to_dict(current_user_id) for recipe in recipes],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
@app.route('/api/recipes/<int:recipe_id>/', methods=['GET'])
def get_recipe(recipe_id):
    # 获取当前用户ID（如果已登录）
    current_user_id = None
    user_id_header = request.headers.get('X-User-ID')
    if user_id_header:
        try:
            current_user_id = int(user_id_header)
        except ValueError:
            pass
            
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify(recipe.to_dict(current_user_id))

@app.route('/api/recipes', methods=['POST'])
@app.route('/api/recipes/', methods=['POST'])
@require_auth
def create_recipe():
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['title', 'ingredients', 'instructions']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} 不能为空'}), 400
        
        # 创建新菜谱
        recipe = Recipe(
            title=data['title'],
            description=data.get('description', ''),
            ingredients=data['ingredients'],
            instructions=data['instructions'],
            prep_time=data.get('prep_time'),
            cook_time=data.get('cook_time'),
            difficulty=data.get('difficulty', '简单'),
            servings=data.get('servings'),
            image=data.get('image', ''),
            user_id=g.current_user.id
        )
        
        db.session.add(recipe)
        db.session.commit()
        
        return jsonify({
            'message': '菜谱创建成功',
            'recipe': recipe.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
@app.route('/api/recipes/<int:recipe_id>/', methods=['PUT'])
@require_auth
def update_recipe(recipe_id):
    try:
        recipe = Recipe.query.get_or_404(recipe_id)
        
        # 检查权限
        if not g.current_user.can_edit_recipe(recipe) and not g.current_user.is_admin():
            return jsonify({'error': '无权限修改此菜谱'}), 403
        
        data = request.get_json()
        
        # 更新字段
        if 'title' in data:
            recipe.title = data['title']
        if 'description' in data:
            recipe.description = data['description']
        if 'ingredients' in data:
            recipe.ingredients = data['ingredients']
        if 'instructions' in data:
            recipe.instructions = data['instructions']
        if 'prep_time' in data:
            recipe.prep_time = data['prep_time']
        if 'cook_time' in data:
            recipe.cook_time = data['cook_time']
        if 'difficulty' in data:
            recipe.difficulty = data['difficulty']
        if 'servings' in data:
            recipe.servings = data['servings']
        if 'image' in data:
            recipe.image = data['image']
        
        db.session.commit()
        
        return jsonify({
            'message': '菜谱更新成功',
            'recipe': recipe.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
@app.route('/api/recipes/<int:recipe_id>/', methods=['DELETE'])
@require_auth
def delete_recipe(recipe_id):
    try:
        recipe = Recipe.query.get_or_404(recipe_id)
        
        # 检查权限
        if not g.current_user.can_delete_recipe(recipe):
            return jsonify({'error': '无权限删除此菜谱'}), 403
        
        db.session.delete(recipe)
        db.session.commit()
        
        return jsonify({'message': '菜谱删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipes/difficulties', methods=['GET'])
@app.route('/api/recipes/difficulties/', methods=['GET'])
def get_difficulties():
    """获取难度列表"""
    try:
        # 获取所有不重复的难度
        difficulties = db.session.query(Recipe.difficulty).distinct().all()
        difficulty_list = [d[0] for d in difficulties if d[0]]
        return jsonify(difficulty_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= 点赞管理 API =============
@app.route('/api/likes', methods=['GET'])
@app.route('/api/likes/', methods=['GET'])
def get_likes():
    """获取用户点赞的菜谱"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'error': '用户ID不能为空'}), 400

        likes = Like.query.filter_by(user_id=user_id).order_by(Like.created_at.desc()).all()
        return jsonify([like.to_dict() for like in likes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/recipes/<int:recipe_id>/like', methods=['GET'])
@app.route('/api/recipes/<int:recipe_id>/like/', methods=['GET'])
def check_recipe_liked(recipe_id):
    """检查用户是否点赞了菜谱"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'error': '用户ID不能为空'}), 400

        like = Like.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
        return jsonify({'liked': like is not None})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/likes', methods=['POST'])
@app.route('/api/likes/', methods=['POST'])
@require_auth
def add_like():
    """添加点赞"""
    try:
        data = request.get_json()

        if not data or not data.get('recipe_id'):
            return jsonify({'error': '菜谱ID不能为空'}), 400

        # 检查是否已点赞
        existing = Like.query.filter_by(
            user_id=g.current_user.id,
            recipe_id=data['recipe_id']
        ).first()
        if existing:
            return jsonify({'error': '已点赞该菜谱'}), 400

        # 检查菜谱是否存在
        recipe = Recipe.query.get_or_404(data['recipe_id'])

        like = Like(user_id=g.current_user.id, recipe_id=data['recipe_id'])
        db.session.add(like)
        db.session.commit()

        return jsonify({
            'message': '点赞成功',
            'like': like.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/likes/<int:like_id>', methods=['DELETE'])
@app.route('/api/likes/<int:like_id>/', methods=['DELETE'])
@require_auth
def remove_like(like_id):
    """取消点赞"""
    try:
        like = Like.query.get_or_404(like_id)
        
        # 检查权限
        if like.user_id != g.current_user.id and not g.current_user.is_admin():
            return jsonify({'error': '无权限取消此点赞'}), 403

        db.session.delete(like)
        db.session.commit()

        return jsonify({'message': '取消点赞成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============= 用户管理 API =============
@app.route('/api/users/<int:user_id>/recipes', methods=['GET'])
@app.route('/api/users/<int:user_id>/recipes/', methods=['GET'])
def get_user_recipes(user_id):
    """获取用户创建的菜谱"""
    try:
        recipes = Recipe.query.filter_by(user_id=user_id).order_by(Recipe.created_at.desc()).all()
        return jsonify([recipe.to_dict() for recipe in recipes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/me', methods=['GET'])
@app.route('/api/users/me/', methods=['GET'])
@require_auth
def get_current_user():
    """获取当前登录用户信息"""
    try:
        return jsonify(g.current_user.to_dict(include_roles=True))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': '用户名和密码不能为空'}), 400

    user = User.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        # 生成JWT token
        token_payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        access_token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({
            'message': '登录成功',
            'access_token': access_token,
            'user': user.to_dict()
        })
    else:
        return jsonify({'error': '用户名或密码错误'}), 401

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': '用户名、邮箱和密码不能为空'}), 400

    # 检查用户名是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': '用户名已存在'}), 400

    # 检查邮箱是否已存在
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': '邮箱已存在'}), 400

    # 创建新用户
    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': '注册成功',
        'user': user.to_dict()
    }), 201

# ============= 角色管理 API =============
@app.route('/api/roles', methods=['GET'])
def get_roles():
    """获取所有角色"""
    try:
        roles = Role.query.all()
        return jsonify([role.to_dict() for role in roles])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/roles/<int:role_id>', methods=['GET'])
def get_role(role_id):
    """获取单个角色"""
    try:
        role = Role.query.get_or_404(role_id)
        return jsonify(role.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/roles', methods=['POST'])
def create_role():
    """创建角色"""
    try:
        data = request.get_json()

        if not data or not data.get('name'):
            return jsonify({'error': '角色名称不能为空'}), 400

        # 检查角色名是否已存在
        if Role.query.filter_by(name=data['name']).first():
            return jsonify({'error': '角色名已存在'}), 400

        role = Role(
            name=data['name'],
            description=data.get('description', '')
        )

        db.session.add(role)
        db.session.commit()

        return jsonify({
            'message': '角色创建成功',
            'role': role.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ============= 用户角色管理 API =============
@app.route('/api/users/<int:user_id>/roles', methods=['GET'])
def get_user_roles(user_id):
    """获取用户的角色"""
    try:
        user = User.query.get_or_404(user_id)
        user_roles = UserRole.query.filter_by(user_id=user_id).all()

        result = []
        for ur in user_roles:
            if ur.role:
                result.append(ur.to_dict())

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>/roles/<int:role_id>', methods=['POST'])
def assign_role_to_user(user_id, role_id):
    """给用户分配角色"""
    try:
        # 检查用户和角色是否存在
        user = User.query.get_or_404(user_id)
        role = Role.query.get_or_404(role_id)

        # 检查是否已分配
        existing = UserRole.query.filter_by(user_id=user_id, role_id=role_id).first()
        if existing:
            return jsonify({'error': '用户已有该角色'}), 400

        user_role = UserRole(user_id=user_id, role_id=role_id)
        db.session.add(user_role)
        db.session.commit()

        return jsonify({
            'message': '角色分配成功',
            'user_role': user_role.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>/roles/<int:role_id>', methods=['DELETE'])
def remove_role_from_user(user_id, role_id):
    """移除用户的角色"""
    try:
        user_role = UserRole.query.filter_by(user_id=user_id, role_id=role_id).first_or_404()

        db.session.delete(user_role)
        db.session.commit()

        return jsonify({'message': '角色移除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ============= 分类管理 API =============
@app.route('/api/categories', methods=['GET'])
def get_categories():
    """获取所有分类（树形结构）"""
    try:
        # 获取所有顶级分类
        root_categories = Category.query.filter_by(parent_id=None).order_by(Category.sort_order, Category.name).all()

        def build_category_tree(category):
            """递归构建分类树"""
            children = Category.query.filter_by(parent_id=category.id).order_by(Category.sort_order, Category.name).all()
            result = category.to_dict()
            result['children'] = [build_category_tree(child) for child in children]
            return result

        categories_tree = [build_category_tree(cat) for cat in root_categories]
        return jsonify(categories_tree)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['POST'])
def create_category():
    """创建分类"""
    try:
        data = request.get_json()

        if not data or not data.get('name'):
            return jsonify({'error': '分类名称不能为空'}), 400

        # 检查分类名是否已存在
        existing = Category.query.filter_by(name=data['name']).all()
        for cat in existing:
            if cat.parent_id == data.get('parent_id'):
                return jsonify({'error': '同级分类中名称已存在'}), 400

        category = Category(
            name=data['name'],
            description=data.get('description', ''),
            parent_id=data.get('parent_id'),
            sort_order=data.get('sort_order', 0)
        )

        db.session.add(category)
        db.session.commit()

        return jsonify({
            'message': '分类创建成功',
            'category': category.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """获取单个分类"""
    try:
        category = Category.query.get_or_404(category_id)
        return jsonify(category.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============= 菜谱分类关联 API =============
@app.route('/api/recipes/<int:recipe_id>/categories', methods=['GET'])
def get_recipe_categories(recipe_id):
    """获取菜谱的分类"""
    try:
        recipe_categories = RecipeCategory.query.filter_by(recipe_id=recipe_id).all()
        return jsonify([rc.to_dict() for rc in recipe_categories])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipes/<int:recipe_id>/categories', methods=['POST'])
def add_category_to_recipe(recipe_id):
    """为菜谱添加分类"""
    try:
        data = request.get_json()

        if not data or not data.get('category_id'):
            return jsonify({'error': '分类ID不能为空'}), 400

        # 检查菜谱和分类是否存在
        recipe = Recipe.query.get_or_404(recipe_id)
        category = Category.query.get_or_404(data['category_id'])

        # 检查是否已关联
        existing = RecipeCategory.query.filter_by(recipe_id=recipe_id, category_id=data['category_id']).first()
        if existing:
            return jsonify({'error': '菜谱已有该分类'}), 400

        recipe_category = RecipeCategory(recipe_id=recipe_id, category_id=data['category_id'])
        db.session.add(recipe_category)
        db.session.commit()

        return jsonify({
            'message': '分类添加成功',
            'recipe_category': recipe_category.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipes/<int:recipe_id>/categories/<int:category_id>', methods=['DELETE'])
def remove_category_from_recipe(recipe_id, category_id):
    """从菜谱移除分类"""
    try:
        recipe_category = RecipeCategory.query.filter_by(recipe_id=recipe_id, category_id=category_id).first_or_404()

        db.session.delete(recipe_category)
        db.session.commit()

        return jsonify({'message': '分类移除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ============= 收藏管理 API =============
@app.route('/api/favorites', methods=['GET'])
@app.route('/api/favorites/', methods=['GET'])
def get_favorites():
    """获取用户收藏的菜谱"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'error': '用户ID不能为空'}), 400

        favorites = Favorite.query.filter_by(user_id=user_id).order_by(Favorite.created_at.desc()).all()
        return jsonify([fav.to_dict() for fav in favorites])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/recipes/<int:recipe_id>/favorite', methods=['GET'])
@app.route('/api/recipes/<int:recipe_id>/favorite/', methods=['GET'])
def check_recipe_favorited(recipe_id):
    """检查用户是否收藏了菜谱"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'error': '用户ID不能为空'}), 400

        favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
        return jsonify({'favorited': favorite is not None})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/favorites', methods=['POST'])
@app.route('/api/favorites/', methods=['POST'])
@require_auth
def add_favorite():
    """添加收藏"""
    try:
        data = request.get_json()

        if not data or not data.get('recipe_id'):
            return jsonify({'error': '菜谱ID不能为空'}), 400

        # 检查是否已收藏
        existing = Favorite.query.filter_by(
            user_id=g.current_user.id,
            recipe_id=data['recipe_id']
        ).first()
        if existing:
            return jsonify({'error': '已收藏该菜谱'}), 400

        # 检查菜谱是否存在
        recipe = Recipe.query.get_or_404(data['recipe_id'])

        favorite = Favorite(user_id=g.current_user.id, recipe_id=data['recipe_id'])
        db.session.add(favorite)
        db.session.commit()

        return jsonify({
            'message': '收藏成功',
            'favorite': favorite.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/favorites/<int:favorite_id>', methods=['DELETE'])
@app.route('/api/favorites/<int:favorite_id>/', methods=['DELETE'])
@require_auth
def remove_favorite(favorite_id):
    """取消收藏"""
    try:
        favorite = Favorite.query.get_or_404(favorite_id)
        
        # 检查权限
        if favorite.user_id != g.current_user.id and not g.current_user.is_admin():
            return jsonify({'error': '无权限取消此收藏'}), 403

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({'message': '取消收藏成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ============= 评论管理 API =============
@app.route('/api/recipes/<int:recipe_id>/comments', methods=['GET'])
def get_recipe_comments(recipe_id):
    """获取菜谱的评论"""
    try:
        # 获取顶级评论（不包含回复）
        parent_comments = Comment.query.filter_by(
            recipe_id=recipe_id,
            parent_id=None
        ).order_by(Comment.created_at.desc()).all()

        # 为每个评论构建回复
        def build_comment_tree(comment):
            replies = Comment.query.filter_by(parent_id=comment.id).order_by(Comment.created_at.asc()).all()
            result = comment.to_dict()
            result['replies'] = [reply.to_dict() for reply in replies]
            return result

        comments = [build_comment_tree(comment) for comment in parent_comments]
        return jsonify(comments)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipes/<int:recipe_id>/comments', methods=['POST'])
def add_comment():
    """添加评论"""
    try:
        data = request.get_json()

        if not data or not data.get('content') or not data.get('user_id') or not data.get('recipe_id'):
            return jsonify({'error': '评论内容、用户ID和菜谱ID不能为空'}), 400

        # 检查用户和菜谱是否存在
        user = User.query.get_or_404(data['user_id'])
        recipe = Recipe.query.get_or_404(data['recipe_id'])

        comment = Comment(
            content=data['content'],
            user_id=data['user_id'],
            recipe_id=data['recipe_id'],
            parent_id=data.get('parent_id')
        )

        db.session.add(comment)
        db.session.commit()

        return jsonify({
            'message': '评论添加成功',
            'comment': comment.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/comments/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    """获取单个评论"""
    try:
        comment = Comment.query.get_or_404(comment_id)
        return jsonify(comment.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    """更新评论"""
    try:
        comment = Comment.query.get_or_404(comment_id)
        data = request.get_json()

        if not data or not data.get('content'):
            return jsonify({'error': '评论内容不能为空'}), 400

        comment.content = data['content']
        comment.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({
            'message': '评论更新成功',
            'comment': comment.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """删除评论"""
    try:
        comment = Comment.query.get_or_404(comment_id)

        # 检查是否有子评论
        child_comments = Comment.query.filter_by(parent_id=comment_id).first()
        if child_comments:
            return jsonify({'error': '请先删除子评论'}), 400

        db.session.delete(comment)
        db.session.commit()

        return jsonify({'message': '评论删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ============= 评分管理 API =============
@app.route('/api/recipes/<int:recipe_id>/ratings', methods=['GET'])
def get_recipe_ratings(recipe_id):
    """获取菜谱的评分"""
    try:
        ratings = Rating.query.filter_by(recipe_id=recipe_id).all()

        if not ratings:
            return jsonify({
                'average_score': 0,
                'total_ratings': 0,
                'ratings': []
            })

        # 计算平均分
        average_score = sum(r.score for r in ratings) / len(ratings)

        return jsonify({
            'average_score': round(average_score, 1),
            'total_ratings': len(ratings),
            'ratings': [rating.to_dict() for rating in ratings]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipes/<int:recipe_id>/ratings', methods=['POST'])
def add_rating():
    """添加评分"""
    try:
        data = request.get_json()

        if not data or not data.get('score') or not data.get('user_id') or not data.get('recipe_id'):
            return jsonify({'error': '评分、用户ID和菜谱ID不能为空'}), 400

        score = data['score']
        if score < 1 or score > 5:
            return jsonify({'error': '评分必须在1-5之间'}), 400

        # 检查用户和菜谱是否存在
        user = User.query.get_or_404(data['user_id'])
        recipe = Recipe.query.get_or_404(data['recipe_id'])

        # 检查是否已评分
        existing = Rating.query.filter_by(
            user_id=data['user_id'],
            recipe_id=data['recipe_id']
        ).first()

        if existing:
            # 更新现有评分
            existing.score = score
            existing.updated_at = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': '评分更新成功',
                'rating': existing.to_dict()
            })
        else:
            # 创建新评分
            rating = Rating(
                score=score,
                user_id=data['user_id'],
                recipe_id=data['recipe_id']
            )

            db.session.add(rating)
            db.session.commit()

            return jsonify({
                'message': '评分添加成功',
                'rating': rating.to_dict()
            }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/ratings/<int:rating_id>', methods=['DELETE'])
def delete_rating(rating_id):
    """删除评分"""
    try:
        rating = Rating.query.get_or_404(rating_id)

        db.session.delete(rating)
        db.session.commit()

        return jsonify({'message': '评分删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============= 管理员业务表管理 API =============
@app.route('/api/admin/recipes', methods=['DELETE'])
@require_admin
def delete_recipes_admin():
    """管理员批量删除菜谱"""
    try:
        data = request.get_json()
        if not data or 'recipe_ids' not in data:
            return jsonify({'error': '菜谱ID列表不能为空'}), 400

        recipe_ids = data['recipe_ids']
        deleted_count = Recipe.query.filter(Recipe.id.in_(recipe_ids)).delete(synchronize_session=False)

        db.session.commit()

        return jsonify({
            'message': f'成功删除 {deleted_count} 个菜谱',
            'deleted_count': deleted_count
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/comments', methods=['DELETE'])
@require_admin
def delete_comments_admin():
    """管理员批量删除评论"""
    try:
        data = request.get_json()
        if not data or 'comment_ids' not in data:
            return jsonify({'error': '评论ID列表不能为空'}), 400

        comment_ids = data['comment_ids']
        deleted_count = Comment.query.filter(Comment.id.in_(comment_ids)).delete(synchronize_session=False)

        db.session.commit()

        return jsonify({
            'message': f'成功删除 {deleted_count} 条评论',
            'deleted_count': deleted_count
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/categories', methods=['PUT'])
@require_admin
def update_category_admin():
    """管理员更新分类信息"""
    try:
        data = request.get_json()
        if not data or 'id' not in data:
            return jsonify({'error': '分类ID不能为空'}), 400

        category = Category.query.get_or_404(data['id'])

        if 'name' in data:
            # 检查分类名是否已存在（排除自己）
            existing = Category.query.filter(
                Category.name == data['name'],
                Category.id != category.id,
                Category.parent_id == category.parent_id
            ).first()
            if existing:
                return jsonify({'error': '同级分类中名称已存在'}), 400
            category.name = data['name']

        if 'description' in data:
            category.description = data['description']

        if 'parent_id' in data:
            # 防止循环引用
            if data['parent_id'] == category.id:
                return jsonify({'error': '不能将自己设为父分类'}), 400
            category.parent_id = data['parent_id']

        if 'sort_order' in data:
            category.sort_order = data['sort_order']

        db.session.commit()

        return jsonify({
            'message': '分类更新成功',
            'category': category.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/categories/<int:category_id>', methods=['DELETE'])
@require_admin
def delete_category_admin(category_id):
    """管理员删除分类"""
    try:
        category = Category.query.get_or_404(category_id)

        # 检查是否有子分类
        children_count = Category.query.filter_by(parent_id=category_id).count()
        if children_count > 0:
            return jsonify({
                'error': f'该分类有 {children_count} 个子分类，无法删除',
                'has_children': True,
                'children_count': children_count
            }), 400

        # 检查是否有菜谱使用该分类
        recipe_category_count = RecipeCategory.query.filter_by(category_id=category_id).count()
        if recipe_category_count > 0:
            return jsonify({
                'error': f'该分类有 {recipe_category_count} 个菜谱，无法删除',
                'has_recipes': True,
                'recipe_count': recipe_category_count
            }), 400

        db.session.delete(category)
        db.session.commit()

        return jsonify({'message': '分类删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============= 数据统计 API =============
@app.route('/api/admin/statistics', methods=['GET'])
@require_admin
def get_statistics():
    """获取系统统计数据"""
    try:
        # 基础统计
        stats = {
            'users': {
                'total': User.query.count(),
                'admin': User.query.join(UserRole).join(Role).filter(Role.name == '管理员').count(),
                'normal': User.query.join(UserRole).join(Role).filter(Role.name == '普通用户').count(),
                'moderator': User.query.join(UserRole).join(Role).filter(Role.name == '版主').count(),
            },
            'recipes': {
                'total': Recipe.query.count(),
                'by_difficulty': {},
                'by_month': {}
            },
            'categories': {
                'total': Category.query.count(),
                'top_level': Category.query.filter_by(parent_id=None).count(),
                'with_recipes': db.session.query(Category.id).filter(Category.recipe_categories.any()).count()
            },
            'interactions': {
                'comments': Comment.query.count(),
                'ratings': Rating.query.count(),
                'favorites': Favorite.query.count()
            }
        }

        # 按难度统计菜谱
        difficulties = db.session.query(Recipe.difficulty, db.func.count(Recipe.id)).group_by(Recipe.difficulty).all()
        for difficulty, count in difficulties:
            stats['recipes']['by_difficulty'][difficulty or '未知'] = count

        # 按月份统计菜谱（最近12个月）
        from sqlalchemy import extract, func
        recipe_months = db.session.query(
            extract('year', Recipe.created_at).label('year'),
            extract('month', Recipe.created_at).label('month'),
            func.count(Recipe.id).label('count')
        ).group_by(
            extract('year', Recipe.created_at),
            extract('month', Recipe.created_at)
        ).order_by(
            extract('year', Recipe.created_at).desc(),
            extract('month', Recipe.created_at).desc()
        ).limit(12).all()

        for year, month, count in recipe_months:
            month_key = f"{int(year)}-{int(month):02d}"
            stats['recipes']['by_month'][month_key] = count

        # 热门菜谱（按收藏数排序）
        popular_recipes = db.session.query(
            Recipe.id, Recipe.title,
            func.count(Favorite.id).label('favorite_count')
        ).join(Favorite).group_by(Recipe.id, Recipe.title).order_by(
            func.count(Favorite.id).desc()
        ).limit(10).all()

        stats['popular_recipes'] = [
            {'id': recipe.id, 'title': recipe.title, 'favorite_count': recipe.favorite_count}
            for recipe in popular_recipes
        ]

        # 活跃用户（按菜谱数排序）
        active_users = db.session.query(
            User.id, User.username,
            func.count(Recipe.id).label('recipe_count')
        ).join(Recipe).group_by(User.id, User.username).order_by(
            func.count(Recipe.id).desc()
        ).limit(10).all()

        stats['active_users'] = [
            {'id': user.id, 'username': user.username, 'recipe_count': user.recipe_count}
            for user in active_users
        ]

        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/dashboard', methods=['GET'])
@require_admin
def get_dashboard():
    """获取管理员仪表板数据"""
    try:
        dashboard = {
            'recent_users': [],
            'recent_recipes': [],
            'recent_comments': [],
            'system_status': 'healthy'
        }

        # 最近注册的用户
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        dashboard['recent_users'] = [user.to_dict() for user in recent_users]

        # 最近创建的菜谱
        recent_recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(5).all()
        dashboard['recent_recipes'] = [recipe.to_dict() for recipe in recent_recipes]

        # 最近的评论
        recent_comments = Comment.query.order_by(Comment.created_at.desc()).limit(5).all()
        dashboard['recent_comments'] = [comment.to_dict() for comment in recent_comments]

        return jsonify(dashboard)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        # 确保数据库表存在
        db.create_all()

    print("Recipe Sharing System Backend Starting...")
    print("Server Address: http://localhost:5000")
    print("API Documentation: http://localhost:5000/")
    print("Test Account: admin / admin123")
    print("")

    app.run(debug=True, host='0.0.0.0', port=5000)