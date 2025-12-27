"""
44K 图片处理工具 - AI 图文生图 + 4K 超分辨率放大

功能说明:
  整合 ai4pic.py 和 Real-ESRGAN 两个工具，实现从原图到 4K 高清图片的完整流程
  1. 使用 ai4pic.py 根据文字描述生成 2K AI 图片
  2. 使用 Real-ESRGAN 将 2K 图片升级到 4K 分辨率
  3. 支持单独使用任一功能

使用方法:

  【完整流程】生成 2K AI 图片并升级到 4K:
    python 44k.py <输入图片路径> [提示词] [输出图片路径]
    python 44k.py input.png
    python 44k.py input.png "去除图片上所有的文字"
    python 44k.py input.png "去除图片上所有的文字" output_4k.png

  【仅生成 2K】只使用 AI 生成 2K 图片:
    python 44k.py --only-2k <输入图片路径> [提示词] [输出图片路径]
    python 44k.py --only-2k input.png
    python 44k.py --only-2k input.png "去除图片上所有的文字" output_2k.png

  【仅升级 4K】只使用 Real-ESRGAN 将图片升级到 4K:
    python 44k.py --only-4k <输入图片路径> [输出图片路径]
    python 44k.py --only-4k input_2k.png
    python 44k.py --only-4k input_2k.png output_4k.png

参数说明:
  --only-2k        仅执行第一步：使用 ai4pic.py 生成 2K 图片
  --only-4k        仅执行第二步：使用 Real-ESRGAN 升级到 4K
  输入图片路径      必填，要处理的图片文件路径
  提示词           可选（仅 --only-2k 和完整流程支持），默认为 "去除图片上所有的文字，标题也要删除"
  输出图片路径      可选，默认为 "输入文件名_4k.png" 或 "输入文件名_2k.png"

输出说明:
  - 完整流程会生成中间 2K 图片（文件名_2k_temp.png）和最终 4K 图片
  - 中间文件会在流程结束后自动删除（除非出错）

依赖项:
  - ai4pic.py: AI 图文生图工具
  - Real-ESRGAN/inference_realesrgan.py: Real-ESRGAN 超分辨率工具

示例:
  # 完整流程：从原图生成去除文字的 4K 图片
  python 44k.py photo.png "清除图片中的所有文字" photo_4k.png

  # 仅生成 2K 图片
  python 44k.py --only-2k photo.png "清除文字" photo_2k.png

  # 仅将现有图片升级到 4K
  python 44k.py --only-4k photo_2k.png photo_4k.png
"""

import subprocess
import sys
import os
import tempfile

# 脚本路径配置
AI4PIC_SCRIPT = "ai4pic.py"
REALESRGAN_SCRIPT = os.path.join("Real-ESRGAN", "inference_realesrgan.py")
REALESRGAN_MODEL = "RealESRGAN_x4plus"
REALESRGAN_OUTPUT_DIR = "Real-ESRGAN/results"


def print_usage():
    """打印使用说明"""
    print("=" * 60)
    print("44K 图片处理工具 - AI 图文生图 + 4K 超分辨率放大")
    print("=" * 60)
    print("\n使用方法:")
    print("  【完整流程】生成 2K AI 图片并升级到 4K:")
    print("    python 44k.py <输入图片路径> [提示词] [输出图片路径]")
    print("  【仅生成 2K】只使用 AI 生成 2K 图片:")
    print("    python 44k.py --only-2k <输入图片路径> [提示词] [输出图片路径]")
    print("  【仅升级 4K】只使用 Real-ESRGAN 将图片升级到 4K:")
    print("    python 44k.py --only-4k <输入图片路径> [输出图片路径]")
    print("\n详细说明请查看脚本顶部的注释文档")
    print("=" * 60)


def run_ai4pic(input_path, prompt, output_path):
    """
    调用 ai4pic.py 生成 2K 图片

    Args:
        input_path: 输入图片路径
        prompt: 提示词
        output_path: 输出图片路径

    Returns:
        bool: 是否成功
    """
    print("\n" + "=" * 60)
    print("步骤 1/2: 使用 AI 生成 2K 图片")
    print("=" * 60)

    cmd = ["python", AI4PIC_SCRIPT, input_path, prompt, output_path]

    try:
        result = subprocess.run(cmd, check=True, capture_output=False, timeout=1200)
        return True
    except subprocess.TimeoutExpired:
        print(f"\n错误: ai4pic.py 执行超时（超过 5 分钟）")
        return False
    except subprocess.CalledProcessError as e:
        print(f"\n错误: ai4pic.py 执行失败")
        print(f"返回码: {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"\n错误: 找不到 {AI4PIC_SCRIPT} 脚本")
        return False


def run_realesrgan(input_path, output_path):
    """
    调用 Real-ESRGAN 将图片升级到 4K

    Args:
        input_path: 输入图片路径（2K 图片）
        output_path: 输出图片路径（4K 图片）

    Returns:
        bool: 是否成功
    """
    print("\n" + "=" * 60)
    print("步骤 2/2: 使用 Real-ESRGAN 升级到 4K")
    print("=" * 60)

    # Real-ESRGAN 输出到指定目录，文件名会添加后缀
    # 我们需要指定输出文件夹
    output_dir = os.path.dirname(output_path) or "."
    input_filename = os.path.basename(input_path)
    input_name, input_ext = os.path.splitext(input_filename)

    cmd = [
        "python", REALESRGAN_SCRIPT,
        "-i", input_path,
        "-o", output_dir,
        "-n", REALESRGAN_MODEL,
        "-s", "2",  # 2 倍放大（从 2K 到 4K）
        "--suffix", "4k_temp",
        "--fp32",  # 使用全精度（CPU 模式必需）
        "-t", "256",  # 分块大小，避免内存不足
        "--tile_pad", "0",  # 减少填充以节省内存
    ]

    print(f"  输入: {input_path}")
    print(f"  输出目录: {output_dir}")
    print(f"  模型: {REALESRGAN_MODEL}")
    print(f"  放大倍数: 2x")

    try:
        print(f"\n开始执行 Real-ESRGAN 命令...")
        print(f"命令: {' '.join(cmd)}")
        print(f"\n注意: CPU 模式处理较大图片可能需要 5-10 分钟，请耐心等待...")
        result = subprocess.run(cmd, check=True, capture_output=False, text=True, timeout=1200)

        print(f"\nReal-ESRGAN 执行完成")

        # Real-ESRGAN 会生成带后缀的文件名，需要重命名
        realesrgan_output = os.path.join(output_dir, f"{input_name}_4k_temp.png")

        if os.path.exists(realesrgan_output):
            # 重命名到最终输出路径
            if os.path.exists(output_path):
                os.remove(output_path)
            os.rename(realesrgan_output, output_path)
            print(f"\n已保存 4K 图片: {output_path}")
            file_size = os.path.getsize(output_path) / 1024
            print(f"文件大小: {file_size:.2f} KB")
            return True
        else:
            print(f"\n错误: 未找到 Real-ESRGAN 输出文件: {realesrgan_output}")
            return False

    except subprocess.TimeoutExpired:
        print(f"\n错误: Real-ESRGAN 执行超时（超过 20 分钟）")
        print(f"提示: CPU 模式下处理大图片非常慢，建议:")
        print(f"  1. 使用更小的 tile size (当前为 {cmd[cmd.index('-t')+1]})")
        print(f"  2. 使用 GPU 加速 (需要安装 CUDA 版本的 PyTorch)")
        print(f"  3. 缩小输入图片尺寸")
        return False
    except subprocess.CalledProcessError as e:
        print(f"\n错误: Real-ESRGAN 执行失败")
        print(f"返回码: {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"\n错误: 找不到 {REALESRGAN_SCRIPT} 脚本")
        return False


def main():
    """主函数"""
    # 解析命令行参数
    args = sys.argv[1:]

    if len(args) == 0:
        print_usage()
        sys.exit(1)

    # 检查模式
    mode = "full"  # full, only-2k, only-4k
    if args[0] == "--only-2k":
        mode = "only-2k"
        args = args[1:]
    elif args[0] == "--only-4k":
        mode = "only-4k"
        args = args[1:]

    # 根据不同模式解析参数
    if mode == "only-4k":
        # 仅升级 4K: python 44k.py --only-4k <输入图片路径> [输出图片路径]
        if len(args) < 1:
            print("错误: --only-4k 模式需要输入图片路径")
            print_usage()
            sys.exit(1)

        input_path = args[0]

        if len(args) > 1:
            output_path = args[1]
        else:
            # 默认输出路径
            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_4k.png"

        # 检查输入文件是否存在
        if not os.path.exists(input_path):
            print(f"错误: 输入图片文件不存在: {input_path}")
            sys.exit(1)

        print("=" * 60)
        print("模式: 仅升级到 4K")
        print("=" * 60)
        print(f"输入图片: {input_path}")
        print(f"输出图片: {output_path}")
        print("=" * 60)

        # 执行 Real-ESRGAN
        success = run_realesrgan(input_path, output_path)

        if success:
            print("\n" + "=" * 60)
            print("处理完成！")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("处理失败！")
            print("=" * 60)
            sys.exit(1)

    elif mode == "only-2k":
        # 仅生成 2K: python 44k.py --only-2k <输入图片路径> [提示词] [输出图片路径]
        if len(args) < 1:
            print("错误: --only-2k 模式需要输入图片路径")
            print_usage()
            sys.exit(1)

        input_path = args[0]

        if len(args) > 1:
            prompt = args[1]
        else:
            prompt = "去除图片上所有的文字，标题也要删除"

        if len(args) > 2:
            output_path = args[2]
        else:
            # 默认输出路径
            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_2k.png"

        # 检查输入文件是否存在
        if not os.path.exists(input_path):
            print(f"错误: 输入图片文件不存在: {input_path}")
            sys.exit(1)

        print("=" * 60)
        print("模式: 仅生成 2K AI 图片")
        print("=" * 60)
        print(f"输入图片: {input_path}")
        print(f"提示词: {prompt}")
        print(f"输出图片: {output_path}")
        print("=" * 60)

        # 执行 ai4pic
        success = run_ai4pic(input_path, prompt, output_path)

        if success:
            print("\n" + "=" * 60)
            print("处理完成！")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("处理失败！")
            print("=" * 60)
            sys.exit(1)

    else:
        # 完整流程: python 44k.py <输入图片路径> [提示词] [输出图片路径]
        if len(args) < 1:
            print("错误: 需要输入图片路径")
            print_usage()
            sys.exit(1)

        input_path = args[0]

        if len(args) > 1:
            prompt = args[1]
        else:
            prompt = "去除图片上所有的文字，标题也要删除"

        if len(args) > 2:
            output_path = args[2]
        else:
            # 默认输出路径
            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_4k.png"

        # 检查输入文件是否存在
        if not os.path.exists(input_path):
            print(f"错误: 输入图片文件不存在: {input_path}")
            sys.exit(1)

        # 生成中间 2K 图片的临时文件名
        name, ext = os.path.splitext(input_path)
        temp_2k_path = f"{name}_2k_temp.png"

        print("=" * 60)
        print("模式: 完整流程（2K AI 图片 → 4K 超分辨率）")
        print("=" * 60)
        print(f"输入图片: {input_path}")
        print(f"提示词: {prompt}")
        print(f"中间文件: {temp_2k_path}")
        print(f"最终输出: {output_path}")
        print("=" * 60)

        # 步骤 1: 执行 ai4pic 生成 2K 图片
        success = run_ai4pic(input_path, prompt, temp_2k_path)

        if not success:
            print("\n" + "=" * 60)
            print("处理失败！（步骤 1 失败）")
            print("=" * 60)
            sys.exit(1)

        # 步骤 2: 执行 Real-ESRGAN 升级到 4K
        success = run_realesrgan(temp_2k_path, output_path)

        # 清理临时文件
        if os.path.exists(temp_2k_path):
            try:
                os.remove(temp_2k_path)
                print(f"\n已删除中间文件: {temp_2k_path}")
            except Exception as e:
                print(f"\n警告: 无法删除中间文件 {temp_2k_path}: {e}")

        if success:
            print("\n" + "=" * 60)
            print("完整流程处理完成！")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("处理失败！（步骤 2 失败）")
            print("=" * 60)
            sys.exit(1)


if __name__ == "__main__":
    main()
