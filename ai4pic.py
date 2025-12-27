"""
DMXAPI 图文生图工具 (nano-banana-2)

功能说明:
  - 使用 DMXAPI 的图片编辑接口，根据原图和文字描述生成 AI 图片
  - 支持命令行参数指定提示词、输入图片路径和输出路径
  - 生成的图片自动保存到指定位置

使用模型: nano-banana-2
接口地址: https://www.dmxapi.cn/v1/images/edits

使用方法:
  python ai4pic.py <输入图片路径> [提示词] [输出图片路径]

参数说明:
  输入图片路径: 必填，要处理的图片文件路径
  提示词: 可选，默认为 "去除图片上所有的文字，标题也要删除"
  输出图片路径: 可选，默认与输入图片路径相同（会覆盖原文件）

示例:
  python ai4pic.py image.png
  python ai4pic.py image.png "清除图片中的所有文字"
  python ai4pic.py image.png "清除图片中的所有文字" output.png
"""

import requests
import base64
from datetime import datetime
import os
import sys

# API 配置
# 请在环境变量中设置 DMXAPI_KEY，或直接修改下面的 API_KEY
API_KEY = os.environ.get("DMXAPI_KEY", "YOUR_API_KEY_HERE")
API_URL = "https://www.dmxapi.cn/v1/images/edits"

# 解析命令行参数
if len(sys.argv) < 2:
    print("错误: 缺少输入图片路径参数")
    print("\n使用方法:")
    print("  python ai4pic.py <输入图片路径> [提示词] [输出图片路径]")
    print("\n示例:")
    print("  python ai4pic.py image.png")
    print("  python ai4pic.py image.png \"清除图片中的所有文字\"")
    print("  python ai4pic.py image.png \"清除图片中的所有文字\" output.png")
    sys.exit(1)

# 获取输入图片路径
input_image_path = sys.argv[1]

# 获取提示词（可选）
if len(sys.argv) > 2:
    user_prompt = sys.argv[2]
else:
    user_prompt = "去除图片上所有的文字，标题也要删除"

# 获取输出图片路径（可选）
if len(sys.argv) > 3:
    output_image_path = sys.argv[3]
else:
    output_image_path = input_image_path

# 检查输入文件是否存在
if not os.path.exists(input_image_path):
    print(f"错误: 输入图片文件不存在: {input_image_path}")
    sys.exit(1)

print("=" * 60)
print("DMXAPI 图文生图工具")
print("=" * 60)
print(f"输入图片: {input_image_path}")
print(f"提示词: {user_prompt}")
print(f"输出图片: {output_image_path}")
print("=" * 60)

# 构建请求参数
payload = {
    "prompt": user_prompt,
    "n": 1,
    "model": "nano-banana-2",
    "aspect_ratio": "16:9",
    "size": "2k",
    "response_format": "url"  # 使用 URL 格式，然后下载图片
}

# HTTP 请求头配置
headers = {
    "Authorization": f"Bearer {API_KEY}",
}

try:
    print("\n正在加载图片文件...")

    # 准备图片文件
    file_name = os.path.basename(input_image_path)
    mime_type = "image/png" if input_image_path.lower().endswith(".png") else "image/jpeg"

    with open(input_image_path, "rb") as f:
        files = [("image", (file_name, f, mime_type))]

        print(f"  已加载: {input_image_path}")

        # 发送 API 请求
        print(f"\n正在向 API 发送请求...")
        print(f"  模型: {payload['model']}")
        print(f"  宽高比: {payload['aspect_ratio']}")
        print(f"  分辨率: {payload['size']}")

        response = requests.post(API_URL, headers=headers, data=payload, files=files)
        response.raise_for_status()

    # 解析 API 响应
    result = response.json()
    print(f"\nAPI 响应成功！")

    # 处理并保存图片
    if 'data' in result and len(result['data']) > 0:
        image_data = result['data'][0]

        if 'url' in image_data:
            image_url = image_data['url']
            print(f"\n图片 URL: {image_url}")

            # 下载图片（添加重试机制）
            print(f"正在下载图片...")
            max_retries = 3
            retry_count = 0
            img_response = None

            while retry_count < max_retries:
                try:
                    img_response = requests.get(image_url, timeout=60)
                    if img_response.status_code == 200:
                        break
                    else:
                        print(f"  下载失败 (HTTP {img_response.status_code})，重试 {retry_count + 1}/{max_retries}...")
                        retry_count += 1
                except Exception as e:
                    print(f"  下载出错: {e}，重试 {retry_count + 1}/{max_retries}...")
                    retry_count += 1
                    if retry_count < max_retries:
                        import time
                        time.sleep(2)

            if img_response and img_response.status_code == 200:
                # 保存图片
                with open(output_image_path, 'wb') as f:
                    f.write(img_response.content)

                file_size = os.path.getsize(output_image_path) / 1024
                print(f"已保存: {output_image_path} ({file_size:.2f} KB)")

                print("\n" + "=" * 60)
                print("图片处理完成！")
                print("=" * 60)
            else:
                print(f"错误: 下载失败 - HTTP {img_response.status_code}")
                sys.exit(1)

        elif 'b64_json' in image_data:
            # 如果返回的是 base64 格式
            base64_data = image_data['b64_json']
            image_bytes = base64.b64decode(base64_data)

            with open(output_image_path, 'wb') as f:
                f.write(image_bytes)

            file_size = os.path.getsize(output_image_path) / 1024
            print(f"已保存: {output_image_path} ({file_size:.2f} KB)")

            print("\n" + "=" * 60)
            print("图片处理完成！")
            print("=" * 60)
        else:
            print("错误: API 响应中没有图片数据")
            sys.exit(1)
    else:
        print("错误: 未找到图片数据，请检查 API 响应")
        print(f"响应内容: {result}")
        sys.exit(1)

except requests.exceptions.RequestException as e:
    print("\n" + "=" * 60)
    print("请求失败！")
    print("=" * 60)
    print(f"错误信息: {e}")

    if hasattr(e, 'response') and e.response:
        print(f"HTTP 状态码: {e.response.status_code}")
        print(f"响应内容: {e.response.text}")
    sys.exit(1)

except Exception as e:
    print("\n" + "=" * 60)
    print("发生未知错误！")
    print("=" * 60)
    print(f"错误信息: {e}")
    sys.exit(1)
