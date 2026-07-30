# <img src="public/BizyAir.svg" alt="BizyAir" width="40" height="40"> BizyAirPlus

[English](README.md) | **简体中文**

BizyAirPlus 为 ComfyUI 提供 BizyAir 云端执行能力，同时保留熟悉的本地工作流编辑体验。你可以在本地搭建和编辑工作流，将任务提交到 BizyAir 执行，并直接在 ComfyUI 中查看进度和接收结果。

## 功能

- 通过 ComfyUI action bar 中独立的 **BizyAirPlus ON/OFF** 按钮切换云端与本地执行。
- 在支持的模型 widget 中直接选择 BizyAir 云端模型，包括 LoRA、Checkpoint、ControlNet 和 VAE。
- 按模型类型、基础模型和关键词筛选，并浏览社区或个人模型。
- 支持 promoted model widget、嵌套子图和同一子图的多个实例。
- 支持 LiteGraph 节点和 Vue Nodes（Node 2.0）的模型选择。
- 实时查看进度、预览和结果，并可中断或取消云端任务。
- 自动上传工作流输入，并将生成结果返回本地 ComfyUI。
- 跟随 ComfyUI 中设置的界面语言。

![BizyAirPlus ON/OFF 开关](public/switch.png)

![BizyAir 模型选择器](public/community.png)

## 安装

将本仓库克隆到 ComfyUI 的 `custom_nodes` 目录，并使用启动 ComfyUI 的同一个 Python 环境安装依赖：

```bash
cd /path/to/ComfyUI/custom_nodes
git clone https://github.com/siliconflow/BizyAirPlus.git
cd BizyAirPlus
python -m pip install -r requirements.txt
```

安装完成后重启 ComfyUI。

BizyAirPlus 会在启动时确保所需依赖已经安装，并检查 PyPI 上是否存在更新的 `bizyair-cloudberry`：

- 设置 `BIZYAIRPLUS_SKIP_UPDATE=1` 可跳过最新版本检查。
- 设置 `BIZYAIRPLUS_CHECK_ONLY=1` 可提示有新版本，但不安装该更新。

即使启用了上述选项，为满足最低依赖版本要求，缺失或版本过低的依赖仍可能被安装。

## 快速开始

1. 启动 ComfyUI，在 action bar 中找到 **BizyAirPlus** 按钮。
2. 点击按钮，将 BizyAirPlus 切换为 **ON**。
3. 如果是首次使用 BizyAir，请前往 [bizyair.ai](https://bizyair.ai) 注册账户并获取 API Key，然后根据提示填写。
4. 点击支持的模型 widget，通过 BizyAir 模型选择器选择模型。
5. 像平常一样提交工作流。
6. 在 ComfyUI 中查看进度，并在执行完成后获取结果。

需要恢复本地执行时，将 BizyAirPlus 按钮切换为 **OFF**。

示例工作流位于 [`example_workflows/`](example_workflows/)。

## 配置

### API Key

首次使用的用户需要先前往 [bizyair.ai](https://bizyair.ai) 注册账户并获取 API Key。推荐开启 BizyAirPlus 后通过提示框配置，也可以前往：

```text
Settings > BizyAirPlus > API Key
```

保存后的 API Key 位于：

```text
~/.BizyAirPlus/apikey.ini
```

也可以设置 `BIZYAIR_API_KEY` 环境变量。环境变量的优先级高于已保存的 Key。

Linux 和 macOS：

```bash
export BIZYAIR_API_KEY=sk-xxxxxx
```

Windows PowerShell：

```powershell
$env:BIZYAIR_API_KEY="sk-xxxxxx"
```

### 语言

在以下位置切换界面语言：

```text
Settings > Comfy > Locale
```

BizyAirPlus 设置页提供英文、简体中文和繁体中文翻译。运行时按钮、提示和模型选择器目前使用英文或简体中文。

## 常见问题

### 找不到 BizyAirPlus 按钮

确认依赖安装在 ComfyUI 实际使用的 Python 环境中，然后重启 ComfyUI。可以通过以下命令检查运行时包：

```bash
python -m pip show bizyair-cloudberry
```

### 提示未配置 API Key

通过 BizyAirPlus 提示框或 `Settings > BizyAirPlus > API Key` 输入，也可以在启动 ComfyUI 前设置 `BIZYAIR_API_KEY`。

### 云端执行失败

检查 API Key 是否有效以及网络是否正常。详细错误通常可以在 ComfyUI 控制台中找到。

### 如何恢复本地执行？

点击 action bar 中的 BizyAirPlus 按钮，使其显示为 **OFF**。

## 支持

如需报告问题或提出功能建议，请使用 [GitHub Issues](https://github.com/siliconflow/BizyAirPlus/issues)。
