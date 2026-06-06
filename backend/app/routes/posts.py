from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Post, PostLike, PostComment
import os
import uuid

# 允许的图片文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    """检查文件扩展名是否被允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    """保存上传的文件"""
    # 获取文件扩展名
    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
    # 生成唯一文件名
    filename = f"{uuid.uuid4().hex}.{ext}"
    # 获取上传目录
    upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'uploads', 'images')
    os.makedirs(upload_dir, exist_ok=True)
    # 保存文件
    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)
    return filename

posts_bp = Blueprint('posts', __name__)


@posts_bp.route('', methods=['GET'])
def get_posts():
    """获取帖子列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # 按创建时间倒序排列
    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'posts': [post.to_dict() for post in posts.items],
        'total': posts.total,
        'pages': posts.pages,
        'current_page': page
    })


@posts_bp.route('', methods=['POST'])
@jwt_required()
def create_post():
    """创建新帖子"""
    user_id = get_jwt_identity()
    data = request.form.to_dict()

    # 处理图片上传
    image = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            image = save_uploaded_file(file)

    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if not title or not content:
        return jsonify({'error': '标题和内容不能为空'}), 400

    post = Post(
        user_id=user_id,
        title=title,
        content=content,
        image=image
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({
        'message': '帖子创建成功',
        'post': post.to_dict()
    }), 201


@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """获取单个帖子"""
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())


@posts_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    """更新帖子"""
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)

    # 检查权限
    if post.user_id != user_id:
        return jsonify({'error': '没有权限修改此帖子'}), 403

    data = request.get_json()

    if 'title' in data:
        post.title = data['title'].strip()
    if 'content' in data:
        post.content = data['content'].strip()

    db.session.commit()

    return jsonify({
        'message': '帖子更新成功',
        'post': post.to_dict()
    })


@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    """删除帖子"""
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)

    # 检查权限
    if post.user_id != user_id:
        return jsonify({'error': '没有权限删除此帖子'}), 403

    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': '帖子删除成功'})


@posts_bp.route('/<int:post_id>/like', methods=['POST'])
@jwt_required()
def toggle_like(post_id):
    """点赞/取消点赞"""
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)

    # 检查是否已经点赞
    existing_like = PostLike.query.filter_by(
        user_id=user_id,
        post_id=post_id
    ).first()

    if existing_like:
        # 取消点赞
        db.session.delete(existing_like)
        db.session.commit()
        return jsonify({
            'message': '取消点赞成功',
            'liked': False,
            'likes_count': len(post.likes)
        })
    else:
        # 添加点赞
        new_like = PostLike(user_id=user_id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()
        return jsonify({
            'message': '点赞成功',
            'liked': True,
            'likes_count': len(post.likes)
        })


@posts_bp.route('/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    """获取帖子评论"""
    post = Post.query.get_or_404(post_id)

    comments = PostComment.query.filter_by(post_id=post_id)\
        .order_by(PostComment.created_at.desc()).all()

    return jsonify({
        'comments': [comment.to_dict() for comment in comments],
        'total': len(comments)
    })


@posts_bp.route('/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    """添加评论"""
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)

    data = request.get_json()
    content = data.get('content', '').strip()

    if not content:
        return jsonify({'error': '评论内容不能为空'}), 400

    comment = PostComment(
        user_id=user_id,
        post_id=post_id,
        content=content
    )

    db.session.add(comment)
    db.session.commit()

    return jsonify({
        'message': '评论成功',
        'comment': comment.to_dict()
    }), 201


@posts_bp.route('/<int:post_id>/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(post_id, comment_id):
    """删除评论"""
    user_id = get_jwt_identity()
    comment = PostComment.query.filter_by(
        id=comment_id,
        post_id=post_id
    ).first_or_404()

    # 检查权限
    if comment.user_id != user_id:
        return jsonify({'error': '没有权限删除此评论'}), 403

    db.session.delete(comment)
    db.session.commit()

    return jsonify({'message': '评论删除成功'})


@posts_bp.route('/my', methods=['GET'])
@jwt_required()
def get_my_posts():
    """获取当前用户的帖子"""
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    posts = Post.query.filter_by(user_id=user_id)\
        .order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'posts': [post.to_dict() for post in posts.items],
        'total': posts.total,
        'pages': posts.pages,
        'current_page': page
    })
