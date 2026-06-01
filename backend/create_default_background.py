"""
创建默认背景图片
"""
from PIL import Image, ImageDraw
import os

def create_default_background():
    """创建一个默认的渐变背景图片"""
    width = 1920
    height = 1080

    # 创建新图片
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    # 创建渐变效果
    for y in range(height):
        # 计算当前行的颜色
        # 从上到下：从紫蓝色渐变到深紫色
        r1, g1, b1 = 102, 126, 234  # #667eea
        r2, g2, b2 = 118, 75, 162   # #764ba2

        ratio = y / height
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)

        # 绘制这一行
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # 保存图片
    output_path = os.path.join(os.path.dirname(__file__), 'static', 'images', '背景.jpg')
    img.save(output_path, 'JPEG', quality=95)
    print(f"默认背景图片已创建: {output_path}")
    return output_path

if __name__ == '__main__':
    create_default_background()
