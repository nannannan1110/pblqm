from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config
from models import db  # 使用统一的models中的db实例
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)

    # 配置CORS
    CORS(app,
         resources={r"/api/*": {"origins": ["http://localhost:8080", "http://127.0.0.1:8080"]}},
         supports_credentials=False,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

    jwt = JWTManager(app)

    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.recipes import recipes_bp
    from app.routes.users import users_bp
    from app.routes.comments import comments_bp
    from app.routes.uploads import uploads_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(recipes_bp, url_prefix='/api/recipes')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(comments_bp, url_prefix='/api/comments')
    app.register_blueprint(uploads_bp, url_prefix='/api/uploads')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    # 添加请求日志（跳过OPTIONS和静态文件请求）
    from flask import request, jsonify
    import json

    @app.before_request
    def log_request():
        # 跳过OPTIONS请求（CORS preflight）和静态文件
        if request.method == 'OPTIONS' or request.path.startswith('/static'):
            return

        print(f"=== BEFORE REQUEST ===")
        print(f"Method: {request.method}")
        print(f"Path: {request.path}")
        print(f"Content-Type: {request.content_type}")

        # 打印Content-Length
        content_length = request.headers.get('Content-Length')
        print(f"Content-Length: {content_length}")

        # 跳过文件上传请求（multipart/form-data）
        if request.content_type and 'multipart/form-data' in request.content_type:
            print("File upload request detected, skipping JSON parsing")
            return

        # 尝试解析JSON数据（仅对application/json请求）
        if request.method == 'POST' and request.content_type and 'application/json' in request.content_type:
            print(f"Raw data length: {len(request.data) if request.data else 0}")
            print(f"Raw data (first 1000 chars): {request.data[:1000] if request.data else 'None'}")

            try:
                data = request.get_json(force=False, silent=True)
                if data is not None:
                    print(f"JSON data successfully parsed: {data}")
                else:
                    print("ERROR: request.get_json() returned None - JSON parse failed")
                    # 尝试手动解析
                    try:
                        data = json.loads(request.data.decode('utf-8'))
                        print(f"Manual JSON parse successful: {data}")
                    except Exception as e:
                        print(f"Manual JSON parse also failed: {e}")
                        return jsonify({'message': f'无效的JSON数据: {str(e)}'}), 400
            except Exception as e:
                print(f"ERROR: Unexpected error during JSON parsing: {e}")
                return jsonify({'message': f'JSON解析错误: {str(e)}'}), 400
        else:
            print(f"Data: {request.data[:200] if request.data else 'None'}")

    # 静态文件服务（带CORS支持）
    from flask import send_from_directory, make_response
    import logging

    @app.route('/static/uploads/images/<filename>')
    def serve_image(filename):
        """提供上传的图片文件服务"""
        upload_dir = os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'images')

        # 检查文件是否存在
        file_path = os.path.join(upload_dir, filename)
        if not os.path.exists(file_path):
            # 静默返回404响应，不记录日志
            response = make_response('', 404)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = make_response(send_from_directory(upload_dir, filename))
        # 添加CORS头
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    @app.route('/static/images/<filename>')
    def serve_background_image(filename):
        """提供背景图片文件服务"""
        images_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')

        # 检查文件是否存在
        file_path = os.path.join(images_dir, filename)
        if not os.path.exists(file_path):
            # 记录日志，方便调试
            print(f"背景图片文件不存在: {file_path}")
            print(f"请将背景图片放置到: {images_dir}")
            # 返回404响应
            response = make_response('', 404)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        response = make_response(send_from_directory(images_dir, filename))
        # 添加CORS头
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
