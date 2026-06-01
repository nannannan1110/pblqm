"""
测试评论API是否正常工作
"""
import requests
import json

BASE_URL = 'http://localhost:5000/api'

def test_comments_api():
    """测试评论API"""
    print("=" * 60)
    print("测试评论API")
    print("=" * 60)

    # 测试获取菜谱1的评论
    print("\n1. 测试获取蒜蓉西兰花的评论...")
    response = requests.get(f'{BASE_URL}/comments/recipe/1')
    print(f"状态码: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"评论总数: {data['total']}")
        print(f"返回的评论数量: {len(data['comments'])}")

        if data['comments']:
            print("\n第一条评论:")
            comment = data['comments'][0]
            print(f"  ID: {comment['id']}")
            print(f"  内容: {comment['content'][:30]}...")
            print(f"  评分: {comment['rating']}")
            print(f"  用户: {comment['user']['username']}")
            print(f"  创建时间: {comment['created_at']}")
        else:
            print("⚠️ 没有返回评论数据!")
    else:
        print(f"❌ API调用失败: {response.text}")

    # 测试评论统计
    print("\n2. 测试获取评论统计...")
    response = requests.get(f'{BASE_URL}/comments/recipe/1/stats')
    print(f"状态码: {response.status_code}")

    if response.status_code == 200:
        stats = response.json()
        print(f"总评论数: {stats['total_comments']}")
        print(f"平均评分: {stats['average_rating']}")
        print(f"评分分布: {stats['rating_distribution']}")
    else:
        print(f"❌ 统计API调用失败: {response.text}")

    # 测试菜谱2和3
    print("\n3. 测试红烧肉评论...")
    response = requests.get(f'{BASE_URL}/comments/recipe/2')
    if response.status_code == 200:
        data = response.json()
        print(f"✓ 红烧肉: {data['total']}条评论")
    else:
        print(f"✗ 失败: {response.status_code}")

    print("\n4. 测试西红柿炒鸡蛋评论...")
    response = requests.get(f'{BASE_URL}/comments/recipe/3')
    if response.status_code == 200:
        data = response.json()
        print(f"✓ 西红柿炒鸡蛋: {data['total']}条评论")
    else:
        print(f"✗ 失败: {response.status_code}")

    print("\n" + "=" * 60)

if __name__ == '__main__':
    try:
        test_comments_api()
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
