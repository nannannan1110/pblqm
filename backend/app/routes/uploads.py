import os
import uuid
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

# 创建上传蓝图
uploads_bp = Blueprint('uploads', __name__)

# 允许的图片文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
# 最大文件大小 (16MB)
MAX_FILE_SIZE = 16 * 1024 * 1024

def allowed_file(filename):
    """检查文件扩展名是否被允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_upload_dir():
    """获取上传目录的绝对路径"""
    # __file__ 是 D:\pbl5\myproject\backend\app\routes\uploads.py
    # 需要向上3层到backend目录: routes -> app -> backend
    current_dir = os.path.dirname(os.path.abspath(__file__))  # backend/app/routes
    app_dir = os.path.dirname(current_dir)  # backend/app
    backend_dir = os.path.dirname(app_dir)  # backend

    upload_dir = os.path.join(backend_dir, 'static', 'uploads', 'images')

    # 确保目录存在
    os.makedirs(upload_dir, exist_ok=True)

    current_app.logger.info(f'计算上传目录: {upload_dir}')

    return upload_dir

def get_file_extension(filename):
    """安全地获取文件扩展名"""
    # 先尝试从原始文件名获取扩展名
    if '.' in filename:
        ext = filename.rsplit('.', 1)[1].lower()
        if ext in ALLOWED_EXTENSIONS:
            return ext

    # 如果原始文件名没有扩展名，返回默认扩展名
    current_app.logger.warning(f'无法从文件名获取扩展名: {filename}，使用默认扩展名jpg')
    return 'jpg'

@uploads_bp.route('/upload-image', methods=['POST'])
@jwt_required()
def upload_image():
    """上传图片文件"""
    try:
        current_app.logger.info('=== 开始处理图片上传请求 ===')

        # 检查是否有文件
        if 'image' not in request.files:
            current_app.logger.warning('请求中没有image字段')
            return jsonify({'error': '没有文件部分'}), 400

        file = request.files['image']
        current_app.logger.info(f'接收到文件: {file.filename}')

        # 检查文件名
        if file.filename == '':
            current_app.logger.warning('文件名为空')
            return jsonify({'error': '没有选择文件'}), 400

        # 检查文件类型
        if not allowed_file(file.filename):
            current_app.logger.warning(f'不支持的文件类型: {file.filename}')
            return jsonify({'error': '不支持的文件类型，请上传PNG、JPG、JPEG、GIF或WebP格式的图片'}), 400

        # 检查文件大小
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        current_app.logger.info(f'文件大小: {file_size} bytes')

        if file_size > MAX_FILE_SIZE:
            current_app.logger.warning(f'文件超过大小限制: {file_size} > {MAX_FILE_SIZE}')
            return jsonify({'error': '文件大小超过16MB限制'}), 400

        # 生成唯一文件名
        file_extension = get_file_extension(file.filename)
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"

        # 获取上传目录
        upload_dir = get_upload_dir()

        # 保存文件
        file_path = os.path.join(upload_dir, unique_filename)
        file.save(file_path)

        current_app.logger.info(f'文件已保存: {file_path}')

        # 验证文件是否真的保存成功
        if not os.path.exists(file_path):
            current_app.logger.error(f'文件保存失败，路径不存在: {file_path}')
            return jsonify({'error': '文件保存失败'}), 500

        # 返回文件访问路径
        file_url = f"/static/uploads/images/{unique_filename}"

        current_app.logger.info(f'图片上传成功: {unique_filename}')

        return jsonify({
            'message': '图片上传成功',
            'filename': unique_filename,
            'url': file_url,
            'size': file_size
        }), 201

    except Exception as e:
        current_app.logger.error(f'文件上传异常: {str(e)}', exc_info=True)
        return jsonify({'error': f'文件上传失败: {str(e)}'}), 500

@uploads_bp.route('/images/<filename>')
def get_image(filename):
    """获取上传的图片"""
    try:
        upload_dir = get_upload_dir()
        return send_from_directory(upload_dir, filename)
    except Exception as e:
        current_app.logger.error(f"获取图片错误: {str(e)}")
        return jsonify({'error': '图片不存在'}), 404

@uploads_bp.route('/delete-image/<filename>', methods=['DELETE'])
@jwt_required()
def delete_image(filename):
    """删除上传的图片"""
    try:
        upload_dir = get_upload_dir()
        file_path = os.path.join(upload_dir, filename)

        # 安全检查：确保文件名不包含路径遍历
        if '..' in filename or '/' in filename or '\\' in filename:
            current_app.logger.warning(f'检测到路径遍历攻击: {filename}')
            return jsonify({'error': '无效的文件名'}), 400

        if os.path.exists(file_path):
            os.remove(file_path)
            current_app.logger.info(f'图片删除成功: {filename}')
            return jsonify({'message': '图片删除成功'}), 200
        else:
            current_app.logger.warning(f'图片不存在: {filename}')
            return jsonify({'error': '图片不存在'}), 404

    except Exception as e:
        current_app.logger.error(f"删除图片错误: {str(e)}")
        return jsonify({'error': '删除图片失败，请稍后重试'}), 500