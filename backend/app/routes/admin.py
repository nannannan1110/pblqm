from flask import Blueprint, jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models import db, User, Recipe, Comment, Favorite, Like, Role, UserRole

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/statistics', methods=['GET'], endpoint='admin_statistics')
def admin_get_statistics():
    """获取系统统计数据"""
    try:
        # 验证JWT
        verify_jwt_in_request()

        # 统计用户数量
        user_count = db.session.query(User).count()

        # 统计菜谱数量
        recipe_count = db.session.query(Recipe).count()

        # 统计评论数量
        comment_count = db.session.query(Comment).count()

        # 统计收藏数量
        favorite_count = db.session.query(Favorite).count()

        # 统计点赞数量
        like_count = db.session.query(Like).count()

        return jsonify({
            'user_count': user_count,
            'recipe_count': recipe_count,
            'comment_count': comment_count,
            'favorite_count': favorite_count,
            'like_count': like_count
        })
    except Exception as e:
        # 判断是否是JWT相关错误
        if 'authorization' in str(e).lower() or 'token' in str(e).lower():
            return jsonify({'message': '请先登录'}), 401
        return jsonify({'message': f'获取统计数据失败: {str(e)}'}), 500

@admin_bp.route('/users', methods=['GET'], endpoint='admin_users')
def admin_get_users():
    """获取所有用户列表"""
    try:
        # 验证JWT
        verify_jwt_in_request()

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # 分页查询用户
        users = db.session.query(User).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': page
        })
    except Exception as e:
        # 判断是否是JWT相关错误
        if 'authorization' in str(e).lower() or 'token' in str(e).lower():
            return jsonify({'message': '请先登录'}), 401
        return jsonify({'message': f'获取用户列表失败: {str(e)}'}), 500

@admin_bp.route('/recipes', methods=['GET'], endpoint='admin_recipes')
def admin_get_recipes():
    """获取所有菜谱列表"""
    try:
        # 验证JWT
        verify_jwt_in_request()

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # 分页查询菜谱
        recipes = db.session.query(Recipe).order_by(Recipe.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            'recipes': [recipe.to_dict() for recipe in recipes.items],
            'total': recipes.total,
            'pages': recipes.pages,
            'current_page': page
        })
    except Exception as e:
        # 判断是否是JWT相关错误
        if 'authorization' in str(e).lower() or 'token' in str(e).lower():
            return jsonify({'message': '请先登录'}), 401
        return jsonify({'message': f'获取菜谱列表失败: {str(e)}'}), 500

@admin_bp.route('/comments', methods=['GET'], endpoint='admin_comments')
def admin_get_comments():
    """获取所有评论列表"""
    try:
        # 验证JWT
        verify_jwt_in_request()

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # 分页查询评论
        comments = db.session.query(Comment).order_by(Comment.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            'comments': [comment.to_dict() for comment in comments.items],
            'total': comments.total,
            'pages': comments.pages,
            'current_page': page
        })
    except Exception as e:
        # 判断是否是JWT相关错误
        if 'authorization' in str(e).lower() or 'token' in str(e).lower():
            return jsonify({'message': '请先登录'}), 401
        return jsonify({'message': f'获取评论列表失败: {str(e)}'}), 500

@admin_bp.route('/users/<int:user_id>/toggle-admin', methods=['PUT'], endpoint='toggle_admin')
def toggle_user_admin(user_id):
    """设置/取消用户为管理员"""
    try:
        # 验证JWT
        verify_jwt_in_request()

        # 获取当前登录用户
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        # 检查当前用户是否为管理员
        if not current_user or not current_user.is_admin():
            return jsonify({'message': '权限不足，只有管理员才能执行此操作'}), 403

        # 获取目标用户
        target_user = User.query.get(user_id)
        if not target_user:
            return jsonify({'message': '用户不存在'}), 404

        # 防止取消自己的管理员权限
        if target_user.id == current_user.id:
            return jsonify({'message': '不能修改自己的管理员权限'}), 400

        # 查找管理员角色
        admin_role = Role.query.filter_by(name='管理员').first()
        if not admin_role:
            return jsonify({'message': '系统错误：管理员角色不存在'}), 500

        # 检查用户是否已经是管理员
        existing_role = UserRole.query.filter_by(
            user_id=user_id,
            role_id=admin_role.id
        ).first()

        if existing_role:
            # 取消管理员权限 - 从数据库删除 UserRole 记录
            print(f"[数据库操作] 删除用户角色关联 - 用户ID: {user_id}, 角色ID: {admin_role.id}")
            db.session.delete(existing_role)
            db.session.commit()
            print(f"[数据库同步] 已从 user_role 表删除记录，用户 {target_user.username} 不再是管理员")

            return jsonify({
                'message': f'已取消 {target_user.username} 的管理员权限',
                'is_admin': False
            })
        else:
            # 添加管理员权限 - 向数据库插入 UserRole 记录
            print(f"[数据库操作] 添加用户角色关联 - 用户ID: {user_id}, 角色ID: {admin_role.id}")
            new_role = UserRole(user_id=user_id, role_id=admin_role.id)
            db.session.add(new_role)
            db.session.commit()
            print(f"[数据库同步] 已向 user_role 表插入记录，用户 {target_user.username} 现在是管理员")

            return jsonify({
                'message': f'已将 {target_user.username} 设置为管理员',
                'is_admin': True
            })

    except Exception as e:
        db.session.rollback()
        print(f"[错误] 数据库操作失败: {str(e)}")
        # 判断是否是JWT相关错误
        if 'authorization' in str(e).lower() or 'token' in str(e).lower():
            return jsonify({'message': '请先登录'}), 401
        return jsonify({'message': f'操作失败: {str(e)}'}), 500

@admin_bp.route('/users/<int:user_id>/deactivate', methods=['PUT'], endpoint='deactivate_user')
def deactivate_user(user_id):
    """注销用户（硬删除 - 从数据库中完全移除）"""
    try:
        # 验证JWT
        verify_jwt_in_request()

        # 获取当前登录用户
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        # 检查当前用户是否为管理员
        if not current_user or not current_user.is_admin():
            return jsonify({'message': '权限不足，只有管理员才能执行此操作'}), 403

        # 获取目标用户
        target_user = User.query.get(user_id)
        if not target_user:
            return jsonify({'message': '用户不存在'}), 404

        # 防止注销自己
        if target_user.id == current_user.id:
            return jsonify({'message': '不能注销自己的账户'}), 400

        # 保存用户信息用于日志
        original_username = target_user.username
        original_email = target_user.email

        # 统计要删除的相关数据
        recipe_count = len(target_user.recipes) if target_user.recipes else 0
        comment_count = len(target_user.comments) if target_user.comments else 0
        favorite_count = len(target_user.favorites) if target_user.favorites else 0
        like_count = len(target_user.likes) if target_user.likes else 0
        rating_count = len(target_user.ratings) if target_user.ratings else 0
        role_count = len(target_user.user_roles) if target_user.user_roles else 0

        print(f"[数据库操作] 准备删除用户: {original_username} (ID: {user_id})")
        print(f"[数据统计] 菜谱: {recipe_count}, 评论: {comment_count}, 收藏: {favorite_count}, 点赞: {like_count}, 评分: {rating_count}, 角色: {role_count}")

        # 硬删除用户 - 由于配置了 cascade='all, delete-orphan'，相关数据会自动被删除
        db.session.delete(target_user)
        db.session.commit()

        print(f"[数据库同步] 已从 user 表删除用户 {original_username} (ID: {user_id})")
        print(f"[数据库同步] 级联删除完成 - 菜谱: {recipe_count}, 评论: {comment_count}, 收藏: {favorite_count}, 点赞: {like_count}, 评分: {rating_count}, 角色: {role_count}")
        print(f"[数据库同步] 用户 {original_username} 及其所有相关数据已从数据库中完全移除")

        return jsonify({
            'message': f'已成功注销用户 {original_username}，其所有数据已从数据库中移除',
            'user_id': user_id,
            'deleted_data': {
                'recipes': recipe_count,
                'comments': comment_count,
                'favorites': favorite_count,
                'likes': like_count,
                'ratings': rating_count,
                'roles': role_count
            }
        })

    except Exception as e:
        db.session.rollback()
        print(f"[错误] 数据库删除失败: {str(e)}")
        # 判断是否是JWT相关错误
        if 'authorization' in str(e).lower() or 'token' in str(e).lower():
            return jsonify({'message': '请先登录'}), 401
        return jsonify({'message': f'操作失败: {str(e)}'}), 500
