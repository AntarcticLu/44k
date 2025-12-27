# 44K - AI 驱动的图像超分辨率处理工具

<div align="center">

**🚀 从原图到 4K 超清，一键完成 AI 图像处理与超分辨率放大 🚀**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.9.1-orange.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-BSD--3--Clause-green.svg)](LICENSE)

</div>

---

## 📖 项目简介

**44K** 是一款强大的 AI 图像处理工具，将先进的 AI 图像编辑技术与 Real-ESRGAN 超分辨率算法深度整合，实现从普通图片到 4K 超清图像的一站式处理流程。

### ✨ 核心特性

- 🎨 **AI 图像编辑**：基于 DMXAPI 的 nano-banana-2 模型，智能处理图片（如去除水印、文字等）
- 🔍 **4K 超分辨率**：集成 Real-ESRGAN 算法，将图像分辨率提升至 4K 级别
- ⚡ **灵活组合**：支持单独使用 AI 编辑或超分辨率，也可一键完成全流程
- 🎯 **精准控制**：通过自然语言提示词精确控制图像处理效果
- 💪 **工业级稳定**：完善的错误处理与重试机制，确保处理成功率

### 🎬 典型应用场景

- 📷 老照片修复与高清化
- 🖼️ 去除图片水印、文字后制作高清壁纸
- 🎨 漫画、插画的超分辨率处理
- 📊 低分辨率图表、海报的高清重制
- 🎥 视频截图的画质提升

---

## 🛠️ 技术架构

### 核心组件

1. **ai4pic.py** - AI 图像编辑引擎
   - 基于 DMXAPI 图文生图接口
   - 支持自然语言描述的图像编辑
   - 输出 2K 分辨率 (16:9) 图像

2. **Real-ESRGAN** - 超分辨率处理引擎
   - 支持多种预训练模型
   - 可处理普通图像和动漫图像
   - 2x/4x 自适应放大

3. **44k.py** - 流程整合工具
   - 自动化处理流程
   - 智能中间文件管理
   - 三种工作模式切换

### 技术栈

- **深度学习框架**：PyTorch 2.9.1
- **图像处理**：OpenCV 4.12.0, Pillow 12.0.0
- **AI 模型**：Real-ESRGAN, GFPGAN (可选)
- **API 集成**：DMXAPI nano-banana-2 模型

---

## 📋 环境要求

### 系统要求

- **操作系统**：Windows 10/11, Linux, macOS
- **Python 版本**：3.8 - 3.14
- **内存**：建议 8GB 及以上
- **存储空间**：至少 5GB（包含模型文件）
- **GPU**：可选，建议使用 NVIDIA GPU 以加速处理

### 软件依赖

| 包名 | 版本 | 说明 |
|------|------|------|
| torch | 2.9.1 | PyTorch 深度学习框架 |
| torchvision | 0.24.1 | PyTorch 视觉库 |
| numpy | 2.2.6 | 数值计算库 |
| opencv-python | 4.12.0.88 | 图像处理库 |
| Pillow | 12.0.0 | 图像处理库 |
| requests | 2.32.5 | HTTP 请求库 |
| basicsr | 1.3.3.3 | 图像恢复框架 |
| facexlib | 0.3.0 | 人脸处理库 |
| gfpgan | 1.3.8 | 人脸增强模型 |
| tqdm | 4.67.1 | 进度条显示 |

---

## 🚀 快速开始

### 1️⃣ 克隆项目

```bash
git clone https://github.com/AntarcticLu/44k.git
cd 44k
```

### 2️⃣ 创建虚拟环境（推荐）

#### Windows
```bash
# 使用 Conda（推荐）
conda create -n 44k python=3.11 -y
conda activate 44k

# 或使用 venv
python -m venv venv
.\venv\Scripts\activate
```

#### Linux/macOS
```bash
# 使用 Conda（推荐）
conda create -n 44k python=3.11 -y
conda activate 44k

# 或使用 venv
python -m venv venv
source venv/bin/activate
```

### 3️⃣ 安装 PyTorch

根据你的系统和是否有 GPU，选择合适的安装命令：

#### GPU 版本（推荐，需要 NVIDIA GPU）
```bash
# CUDA 11.8
pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cu121
```

#### CPU 版本
```bash
pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cpu
```

### 4️⃣ 安装项目依赖

```bash
# 安装核心依赖
pip install numpy==2.2.6
pip install opencv-python==4.12.0.88
pip install Pillow==12.0.0
pip install requests==2.32.5
pip install tqdm==4.67.1

# 安装 Real-ESRGAN 相关依赖
pip install basicsr==1.3.3.3
pip install facexlib==0.3.0
pip install gfpgan==1.3.8

# 安装 Real-ESRGAN
cd Real-ESRGAN
pip install -r requirements.txt
python setup.py develop
cd ..
```

### 5️⃣ 配置 API 密钥

编辑 `ai4pic.py` 文件，设置你的 DMXAPI 密钥：

```python
# 方法 1: 直接修改代码
API_KEY = "你的_API_KEY"

# 方法 2: 使用环境变量（推荐）
export DMXAPI_KEY="你的_API_KEY"  # Linux/macOS
set DMXAPI_KEY=你的_API_KEY        # Windows CMD
$env:DMXAPI_KEY="你的_API_KEY"     # Windows PowerShell
```

> 💡 **获取 API 密钥**：访问 [DMXAPI](https://www.dmxapi.cn/) 注册并获取 API Key

### 6️⃣ 下载预训练模型

下载 Real-ESRGAN 模型文件到 `Real-ESRGAN/weights/` 目录：

```bash
# 创建 weights 目录
mkdir -p Real-ESRGAN/weights

# 下载通用 4x 模型（必需）
cd Real-ESRGAN/weights
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth

# 可选：下载其他模型
# 动漫专用模型
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth
```

#### Windows 用户下载方法
```powershell
# 使用 PowerShell
cd Real-ESRGAN\weights
Invoke-WebRequest -Uri "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth" -OutFile "RealESRGAN_x4plus.pth"
```

### 7️⃣ 验证安装

```bash
# 测试 PyTorch 是否正确安装
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}')"

# 测试 Real-ESRGAN
cd Real-ESRGAN
python inference_realesrgan.py --help
```

---

## 📚 使用指南

### 工作模式

44K 提供三种工作模式，满足不同的使用需求：

#### 🔵 模式一：完整流程（AI 编辑 + 4K 超分辨率）

将原图通过 AI 处理后，直接输出 4K 高清图像。

```bash
# 基础用法（使用默认提示词）
python 44k.py input.png

# 自定义提示词
python 44k.py input.png "去除图片上所有的文字和水印"

# 指定输出文件名
python 44k.py input.png "去除文字" output_4k.png
```

**处理流程：**
```
原图 → AI 编辑（2K） → 超分辨率（4K） → 最终输出
```

---

#### 🟢 模式二：仅 AI 编辑（输出 2K）

只使用 AI 处理图片，不进行超分辨率放大。

```bash
# 基础用法
python 44k.py --only-2k input.png

# 自定义提示词
python 44k.py --only-2k input.png "清除所有文字，保留背景"

# 指定输出文件名
python 44k.py --only-2k input.png "去除水印" output_2k.png
```

**适用场景：**
- 只需要 AI 编辑功能
- 对输出分辨率要求不高
- 快速预览处理效果

---

#### 🟡 模式三：仅 4K 超分辨率

将已有的图片（如 2K 图片）直接放大到 4K。

```bash
# 基础用法
python 44k.py --only-4k input_2k.png

# 指定输出文件名
python 44k.py --only-4k input_2k.png output_4k.png
```

**适用场景：**
- 已有处理好的图片，只需放大
- 老照片、扫描图像高清化
- 低分辨率图像质量提升

---

### 💡 高级用法

#### 1. 直接使用 AI 编辑工具

```bash
# 去除文字
python ai4pic.py photo.png "去除图片上所有的文字"

# 去除水印
python ai4pic.py photo.png "清除水印，保持画面干净" output.png

# 修复图片
python ai4pic.py old_photo.png "修复图片，提升清晰度"
```

#### 2. 直接使用 Real-ESRGAN

```bash
cd Real-ESRGAN

# 基础 4x 放大
python inference_realesrgan.py -n RealESRGAN_x4plus -i ../input.png

# 动漫图片处理
python inference_realesrgan.py -n RealESRGAN_x4plus_anime_6B -i ../anime.png

# 人脸增强
python inference_realesrgan.py -n RealESRGAN_x4plus -i ../portrait.png --face_enhance

# 自定义放大倍数
python inference_realesrgan.py -n RealESRGAN_x4plus -i ../input.png --outscale 3.5

# CPU 模式 + 分块处理（显存不足时）
python inference_realesrgan.py -n RealESRGAN_x4plus -i ../input.png --fp32 -t 256
```

详细说明请参考：[Real-ESRGAN 使用文档](Real-ESRGAN/README_使用文档.md)

---

## 🎯 使用示例

### 示例 1：老照片修复

```bash
# 步骤 1: AI 修复 + 去除划痕
python 44k.py old_photo.jpg "修复图片，去除划痕和污渍" restored_4k.png

# 输出：高清修复后的 4K 照片
```

### 示例 2：去除图片水印

```bash
# 完整流程：去水印 + 高清化
python 44k.py watermarked.png "去除所有水印和标识" clean_4k.png

# 仅去水印（2K 输出）
python 44k.py --only-2k watermarked.png "清除水印" clean_2k.png
```

### 示例 3：漫画/插画高清化

```bash
# 步骤 1: 使用动漫模型放大到 4K
cd Real-ESRGAN
python inference_realesrgan.py -n RealESRGAN_x4plus_anime_6B -i ../manga.png -o ../output

# 步骤 2: 如需进一步 AI 编辑
cd ..
python 44k.py --only-2k output/manga_out.png "去除对话框文字"
```

### 示例 4：批量处理

```bash
# 批量处理多张图片
for file in *.jpg; do
    python 44k.py "$file" "去除文字" "processed/${file%.jpg}_4k.png"
done
```

---

## ⚙️ 配置说明

### AI 编辑参数（ai4pic.py）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `model` | AI 模型名称 | nano-banana-2 |
| `aspect_ratio` | 输出宽高比 | 16:9 |
| `size` | 输出分辨率 | 2k |
| `response_format` | 响应格式 | url |

### Real-ESRGAN 参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `-n, --model_name` | 模型选择 | RealESRGAN_x4plus |
| `-s, --outscale` | 放大倍数 | 2, 4 |
| `-t, --tile` | 分块大小 | 256 |
| `--fp32` | 使用 FP32 精度 | - |
| `--face_enhance` | 人脸增强 | - |

---

## ❓ 常见问题

<details>
<summary><b>Q1: 为什么处理速度很慢？</b></summary>

**原因：**
- 使用 CPU 模式处理大图片
- 网络带宽限制（AI 编辑步骤）

**解决方案：**
1. 安装 GPU 版本的 PyTorch
2. 使用 `-t 256` 参数减小分块大小
3. 检查网络连接
</details>

<details>
<summary><b>Q2: CUDA out of memory 错误</b></summary>

**解决方案：**
```bash
# 方法 1: 使用分块处理
python 44k.py --only-4k input.png -t 256

# 方法 2: 减小放大倍数
cd Real-ESRGAN
python inference_realesrgan.py -n RealESRGAN_x4plus -i ../input.png --outscale 2

# 方法 3: 使用 CPU 模式
python inference_realesrgan.py -n RealESRGAN_x4plus -i ../input.png --fp32
```
</details>

<details>
<summary><b>Q3: API 请求失败</b></summary>

**检查清单：**
1. ✅ API_KEY 是否正确配置
2. ✅ 网络是否能访问 dmxapi.cn
3. ✅ API 额度是否充足
4. ✅ 图片格式是否支持（PNG/JPG）

**调试方法：**
```python
# 在 ai4pic.py 中添加调试信息
print(f"API_KEY: {API_KEY[:10]}...")  # 只显示前 10 个字符
```
</details>

<details>
<summary><b>Q4: 找不到模型文件</b></summary>

**错误信息：**
```
FileNotFoundError: [Errno 2] No such file or directory: 'weights/RealESRGAN_x4plus.pth'
```

**解决方案：**
```bash
# 重新下载模型
cd Real-ESRGAN/weights
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth
```
</details>

<details>
<summary><b>Q5: 输出图片质量不理想</b></summary>

**优化建议：**
1. 尝试不同的提示词描述
2. 使用专用模型（如动漫图片用 anime 模型）
3. 调整放大倍数（避免过度放大）
4. 启用人脸增强功能（人像照片）

```bash
# 人像照片优化示例
cd Real-ESRGAN
python inference_realesrgan.py -n RealESRGAN_x4plus -i portrait.png --face_enhance --outscale 2
```
</details>

---

## 📁 项目结构

```
44k/
├── 44k.py                      # 主程序（流程整合）
├── ai4pic.py                   # AI 图像编辑工具
├── README.md                   # 项目说明文档
├── .gitignore                  # Git 忽略规则
├── Real-ESRGAN/                # Real-ESRGAN 超分辨率引擎
│   ├── inference_realesrgan.py        # 图像推理脚本
│   ├── inference_realesrgan_video.py  # 视频推理脚本
│   ├── README_使用文档.md              # 中文使用文档
│   ├── requirements.txt               # Python 依赖
│   ├── setup.py                       # 安装脚本
│   ├── weights/                       # 模型权重目录
│   │   └── RealESRGAN_x4plus.pth     # 预训练模型（需下载）
│   ├── realesrgan/                    # 核心代码库
│   │   ├── archs/                    # 模型架构
│   │   ├── data/                     # 数据处理
│   │   ├── models/                   # 模型定义
│   │   └── utils.py                  # 工具函数
│   └── docs/                          # 文档目录
└── output/                     # 输出目录（自动创建）
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 参与贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发建议

- 遵循 PEP 8 代码规范
- 添加必要的注释和文档
- 编写单元测试（如适用）
- 确保向后兼容

---

## 📄 许可证

本项目采用 BSD 3-Clause License 许可证 - 详见 [LICENSE](LICENSE) 文件

### 第三方组件许可

- **Real-ESRGAN**: BSD 3-Clause License
- **PyTorch**: BSD-style License
- **OpenCV**: Apache 2.0 License

---

## 🙏 致谢

本项目基于以下开源项目构建：

- [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) - 腾讯 ARC Lab 出品的超分辨率算法
- [GFPGAN](https://github.com/TencentARC/GFPGAN) - 人脸增强算法
- [BasicSR](https://github.com/xinntao/BasicSR) - 图像恢复工具箱
- [DMXAPI](https://www.dmxapi.cn/) - AI 图像编辑 API 服务

特别感谢所有开源贡献者！

---

## 📞 联系方式

- **GitHub Issues**: [提交问题](https://github.com/AntarcticLu/44k/issues)
- **项目主页**: [https://github.com/AntarcticLu/44k](https://github.com/AntarcticLu/44k)

---

## 🌟 Star History

如果这个项目对你有帮助，请给个 ⭐️ Star 支持一下！

<div align="center">

**[⬆ 回到顶部](#44k---ai-驱动的图像超分辨率处理工具)**

Made with ❤️ by [AntarcticLu](https://github.com/AntarcticLu)

</div>
