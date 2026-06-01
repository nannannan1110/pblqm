"""
测试图片上传功能的简单脚本
"""
import requests
import os

BASE_URL = 'http://localhost:5000/api'

def test_upload():
    """测试图片上传"""
    # 首先需要登录获取token
    print("=== 步骤1: 登录获取token ===")
    login_data = {
        'username': 'admin',  # 替换为实际存在的用户名
        'password': 'admin123'  # 替换为实际密码
    }

    try:
        response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
        print(f"登录响应状态: {response.status_code}")

        if response.status_code != 200:
            print(f"登录失败: {response.text}")
            return

        token_data = response.json()
        access_token = token_data.get('access_token')
        print(f"获取到token: {access_token[:20]}...")

        # 准备上传文件
        print("\n=== 步骤2: 上传图片 ===")

        # 检查是否有测试图片
        test_image_path = 'test_image.jpg'
        if not os.path.exists(test_image_path):
            print(f"测试图片不存在: {test_image_path}")
            print("请将一个测试图片命名为 test_image.jpg 放在当前目录")
            return

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        files = {
            'image': open(test_image_path, 'rb')
        }

        upload_url = f'{BASE_URL}/uploads/upload-image'
        print(f"上传URL: {upload_url}")

        response = requests.post(upload_url, headers=headers, files=files)
        print(f"上传响应状态: {response.status_code}")
        print(f"上传响应内容: {response.text}")

        if response.status_code == 201:
            result = response.json()
            print(f"\n✅ 上传成功!")
            print(f"文件名: {result['filename']}")
            print(f"访问URL: {result['url']}")
            print(f"文件大小: {result['size']} bytes")

            # 验证文件是否存在
            file_path = f"D:\\pbl5\\myproject\\backend\\static\\uploads\\images\\{result['filename']}"
            if os.path.exists(file_path):
                print(f"✅ 文件已保存到: {file_path}")
                file_size = os.path.getsize(file_path)
                print(f"文件大小: {file_size} bytes")
            else:
                print(f"❌ 文件未找到: {file_path}")
        else:
            print(f"❌ 上传失败")

    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_upload()
