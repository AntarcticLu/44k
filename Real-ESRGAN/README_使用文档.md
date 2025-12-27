# Real-ESRGAN 图像超分辨率处理工具

## 项目简介

Real-ESRGAN 是一个基于深度学习的图像/视频超分辨率处理工具，可以将低分辨率的图像和视频提升到更高的分辨率，同时保持或改善图像质量。本项目使用纯合成数据训练，能够处理各种真实场景的图像修复任务。

**主要特性：**
- 支持多种超分辨率模型（2x、4x 放大）
- 专门优化的动漫图像处理模型
- 视频超分辨率处理
- 支持人脸增强功能（集成 GFPGAN）
- 支持多种图像格式（JPG、PNG、WEBP 等）
- 支持透明通道（RGBA）和灰度图像处理

---

## 环境要求

### 系统要求
- 操作系统：Windows / Linux / macOS
- Python 版本：Python >= 3.7
- GPU：建议使用 NVIDIA GPU（支持 CUDA）以获得更快的处理速度
- 显存：建议至少 4GB 显存

### 软件依赖
- PyTorch >= 1.7
- CUDA（如果使用 NVIDIA GPU）
- 其他 Python 依赖包（见下文安装步骤）

---

## 安装步骤

### 1. 安装 Anaconda/Miniconda（推荐）

如果还没有安装 Anaconda 或 Miniconda，请先安装：

- **Anaconda 下载**：https://www.anaconda.com/download/
- **Miniconda 下载**：https://docs.conda.io/en/latest/miniconda.html

### 2. 创建虚拟环境

```bash
# 创建一个名为 realesrgan 的 Python 3.8 虚拟环境
conda create -n realesrgan python=3.8 -y

# 激活虚拟环境
conda activate realesrgan
```

### 3. 安装 PyTorch

根据你的系统和 CUDA 版本安装 PyTorch。访问 https://pytorch.org/ 获取适合你的安装命令。

**示例（CUDA 11.8）：**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**CPU 版本（无 GPU）：**
```bash
pip install torch torchvision torchaudio
```

### 4. 克隆项目代码

```bash
git clone https://github.com/YOUR_USERNAME/Real-ESRGAN.git
cd Real-ESRGAN
```

### 5. 安装依赖包

```bash
# 安装 BasicSR（用于训练和推理）
pip install basicsr

# 安装人脸增强相关库（可选）
pip install facexlib
pip install gfpgan

# 安装其他依赖
pip install -r requirements.txt

# 安装本项目
python setup.py develop
```

### 6. 下载预训练模型

在使用前，需要下载对应的预训练模型文件。将模型文件放置在 `weights/` 目录下。

**常用模型下载链接：**

| 模型名称 | 说明 | 下载链接 |
|---------|------|---------|
| RealESRGAN_x4plus | 通用 4x 超分辨率模型 | [下载](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth) |
| RealESRGAN_x4plus_anime_6B | 动漫图像 4x 超分辨率模型 | [下载](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth) |
| RealESRGAN_x2plus | 通用 2x 超分辨率模型 | [下载](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth) |
| realesr-animevideov3 | 动漫视频模型（小型） | [下载](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-animevideov3.pth) |
| realesr-general-x4v3 | 通用模型 v3（支持降噪） | [下载](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth) |

**使用命令下载（以 RealESRGAN_x4plus 为例）：**
```bash
# Windows PowerShell
Invoke-WebRequest -Uri "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth" -OutFile "weights/RealESRGAN_x4plus.pth"

# Linux/macOS
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -P weights
```

---

## 使用说明

### 1. 图像超分辨率处理

#### 基本用法

```bash
# 使用默认模型处理 inputs 目录下的所有图片
python inference_realesrgan.py -n RealESRGAN_x4plus -i inputs -o results

# 处理单张图片
python inference_realesrgan.py -n RealESRGAN_x4plus -i input.jpg -o results
```

#### 常用参数说明

```bash
python inference_realesrgan.py [参数]

必选参数：
  -n, --model_name      模型名称
                        可选: RealESRGAN_x4plus | RealESRGAN_x4plus_anime_6B |
                              RealESRGAN_x2plus | realesr-animevideov3 |
                              realesr-general-x4v3

  -i, --input           输入图片或文件夹路径
  -o, --output          输出文件夹路径（默认: results）

可选参数：
  -s, --outscale        输出图像的缩放倍数（默认: 4）
  --suffix              输出图像的后缀名（默认: out）
  -t, --tile            分块大小，0 表示不分块（默认: 0）
                        显存不足时可设置为 256 或更小
  --face_enhance        是否使用 GFPGAN 增强人脸
  --fp32                使用 FP32 精度（默认 FP16，更快但占用更多显存）
  --ext                 输出图像格式 (auto | jpg | png)
  -g, --gpu-id          指定 GPU 设备 ID（默认自动选择）
```

#### 使用示例

**处理普通图片（4x 放大）：**
```bash
python inference_realesrgan.py -n RealESRGAN_x4plus -i inputs -o results
```

**处理动漫图片（4x 放大）：**
```bash
python inference_realesrgan.py -n RealESRGAN_x4plus_anime_6B -i anime_image.jpg -o results
```

**处理图片并增强人脸：**
```bash
python inference_realesrgan.py -n RealESRGAN_x4plus -i portrait.jpg --face_enhance -o results
```

**自定义输出缩放比例（3.5x 放大）：**
```bash
python inference_realesrgan.py -n RealESRGAN_x4plus -i input.jpg --outscale 3.5 -o results
```

**显存不足时使用分块处理：**
```bash
python inference_realesrgan.py -n RealESRGAN_x4plus -i large_image.jpg -t 256 -o results
```

**使用降噪模型：**
```bash
python inference_realesrgan.py -n realesr-general-x4v3 -i noisy_image.jpg -dn 0.5 -o results
```

### 2. 视频超分辨率处理

```bash
# 处理视频文件
python inference_realesrgan_video.py -n realesr-animevideov3 -i input_video.mp4 -o results
```

**视频处理参数：**
- `-i`：输入视频文件路径
- `-o`：输出目录
- `-n`：模型名称（建议使用 realesr-animevideov3）
- `-s`：输出缩放倍数
- `--fps`：输出视频帧率

---

## 模型选择建议

| 使用场景 | 推荐模型 | 说明 |
|---------|---------|------|
| 通用图片（照片、风景等） | RealESRGAN_x4plus | 效果好，模型较大 |
| 动漫插画、漫画 | RealESRGAN_x4plus_anime_6B | 专为二次元优化，模型小 |
| 动漫视频 | realesr-animevideov3 | 专为视频优化，速度快 |
| 需要降噪的图片 | realesr-general-x4v3 | 支持 -dn 参数控制降噪强度 |
| 2x 放大需求 | RealESRGAN_x2plus | 适合轻度放大 |

---

## 常见问题

### 1. CUDA out of memory 错误

**解决方法：**
- 使用 `-t` 参数设置分块大小，例如：`-t 256` 或 `-t 128`
- 减少输出缩放倍数：`--outscale 2`
- 使用 FP32 精度：`--fp32`（注意这会增加显存占用）

### 2. 处理速度慢

**解决方法：**
- 确保正确安装了 GPU 版本的 PyTorch
- 检查是否正确检测到 GPU：`python -c "import torch; print(torch.cuda.is_available())"`
- 使用更小的模型（如 realesr-animevideov3）

### 3. 找不到模型文件

**解决方法：**
- 确保模型文件已下载到 `weights/` 目录
- 检查文件名是否正确（区分大小写）
- 首次运行时程序会自动下载模型（需要网络连接）

### 4. 输出图片质量不理想

**解决方法：**
- 尝试不同的模型
- 对于照片类图片，使用 `--face_enhance` 增强人脸
- 调整 `-dn` 参数（仅 realesr-general-x4v3 模型支持）
- 不要过度放大，建议不超过 4x

---

## 项目结构

```
Real-ESRGAN/
├── inference_realesrgan.py       # 图像推理脚本
├── inference_realesrgan_video.py # 视频推理脚本
├── requirements.txt              # Python 依赖列表
├── setup.py                      # 安装脚本
├── realesrgan/                   # 核心代码库
│   ├── archs/                    # 模型架构
│   ├── data/                     # 数据处理
│   ├── models/                   # 模型定义
│   └── utils.py                  # 工具函数
├── weights/                      # 模型权重文件目录（需手动下载）
├── inputs/                       # 输入图片目录
└── results/                      # 输出结果目录
```

---

## 许可证

本项目基于原始 Real-ESRGAN 项目，遵循 BSD 3-Clause License。

详细信息请参考 LICENSE 文件。

---

## 致谢

本项目基于腾讯 ARC Lab 开发的 Real-ESRGAN：
- 原项目地址：https://github.com/xinntao/Real-ESRGAN
- 论文：Real-ESRGAN: Training Real-World Blind Super-Resolution with Pure Synthetic Data

感谢原作者的杰出工作！

---

## 联系方式

如有问题或建议，请通过 GitHub Issues 提交。
