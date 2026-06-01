from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Comment, Recipe, User

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/recipe/<int:recipe_id>', methods=['GET'])
def get_recipe_comments(recipe_id):
    """获取指定菜谱的所有评论"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # 验证菜谱是否存在
    recipe = Recipe.query.get_or_404(recipe_id)

    comments = Comment.query.filter_by(recipe_id=recipe_id)\
        .order_by(Comment.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'comments': [comment.to_dict() for comment in comments.items],
        'total': comments.total,
        'pages': comments.pages,
        'current_page': page
    })

@comments_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment():
    """创建新评论"""
    data = request.get_json()
    user_id = get_jwt_identity()

    # 验证必填字段
    if not data.get('content'):
        return jsonify({'message': '评论内容不能为空'}), 400

    if not data.get('recipe_id'):
        return jsonify({'message': '菜谱ID不能为空'}), 400

    # 验证菜谱是否存在
    recipe = Recipe.query.get_or_404(data['recipe_id'])

    # 验证评分范围
    rating = data.get('rating', 5)
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({'message': '评分必须在1-5之间'}), 400

    comment = Comment(
        content=data['content'],
        rating=rating,
        user_id=user_id,
        recipe_id=data['recipe_id']
    )

    db.session.add(comment)
    db.session.commit()

    # 返回评论详情，包含用户信息
    comment_data = comment.to_dict()
    comment_data['user'] = User.query.get(user_id).to_dict()

    return jsonify(comment_data), 201

@comments_bp.route('/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    """更新评论（只有评论作者可以更新）"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    comment = Comment.query.get_or_404(comment_id)

    # 检查权限（只有评论作者可以编辑）
    if comment.user_id != user_id:
        return jsonify({'message': '无权限编辑此评论，只有评论作者可以编辑'}), 403

    data = request.get_json()

    # 更新字段
    if 'content' in data:
        comment.content = data['content']

    if 'rating' in data:
        rating = data['rating']
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({'message': '评分必须在1-5之间'}), 400
        comment.rating = rating

    db.session.commit()
    return jsonify(comment.to_dict())

@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """删除评论（评论作者、菜谱创建者或管理员可以删除）"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    comment = Comment.query.get_or_404(comment_id)

    # 检查权限（评论作者、菜谱创建者或管理员可以删除）
    if not user.can_manage_comment(comment):
        return jsonify({'message': '无权限删除此评论，只有评论作者、菜谱创建者或管理员可以删除'}), 403

    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': '评论删除成功'})

@comments_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_comments(user_id):
    """获取指定用户的所有评论"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # 验证用户是否存在
    user = User.query.get_or_404(user_id)

    comments = Comment.query.filter_by(user_id=user_id)\
        .order_by(Comment.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    # 添加菜谱信息到评论
    comments_data = []
    for comment in comments.items:
        comment_dict = comment.to_dict()
        comment_dict['recipe'] = Recipe.query.get(comment.recipe_id).to_dict()
        comments_data.append(comment_dict)

    return jsonify({
        'comments': comments_data,
        'total': comments.total,
        'pages': comments.pages,
        'current_page': page
    })

@comments_bp.route('/recipe/<int:recipe_id>/stats', methods=['GET'])
def get_recipe_comment_stats(recipe_id):
    """获取菜谱的评论统计信息"""
    # 验证菜谱是否存在
    recipe = Recipe.query.get_or_404(recipe_id)

    # 获取评论数量
    total_comments = Comment.query.filter_by(recipe_id=recipe_id).count()

    if total_comments == 0:
        return jsonify({
            'total_comments': 0,
            'average_rating': 0,
            'rating_distribution': {
                1: 0, 2: 0, 3: 0, 4: 0, 5: 0
            }
        })

    # 计算平均评分
    avg_rating = db.session.query(db.func.avg(Comment.rating))\
        .filter_by(recipe_id=recipe_id).scalar() or 0

    # 获取评分分布
    rating_distribution = {}
    for rating in range(1, 6):
        count = Comment.query.filter_by(recipe_id=recipe_id, rating=rating).count()
        rating_distribution[rating] = count

    return jsonify({
        'total_comments': total_comments,
        'average_rating': round(float(avg_rating), 2),
        'rating_distribution': rating_distribution
    })