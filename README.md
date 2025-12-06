# nonebot_plugin_mhy_choose

一个用于从指定文件夹随机发送图片（包括GIF）的NoneBot2插件

## 功能特点

- 🎲 随机从指定文件夹发送图片
- 🖼️ 支持多种图片格式：jpg, jpeg, png, gif, bmp, webp
- 📁 自动递归扫描子文件夹
- ⚙️ 可配置图片文件夹路径

## 安装

使用 pip 安装：

```bash
pip install nonebot-plugin-mhy-choose
```

或者使用 nb-cli：

```bash
nb plugin install nonebot-plugin-mhy-choose
```

## 配置

在 NoneBot2 的 `.env` 文件中添加以下配置：

```env
# 图片文件夹路径，默认为 "images"
MHY_CHOOSE_IMAGE_PATH=images
```

配置项说明：
- `MHY_CHOOSE_IMAGE_PATH`: 图片文件夹的路径，可以是相对路径或绝对路径。插件会递归扫描该文件夹及其子文件夹中的所有支持格式的图片。

## 使用方法

将图片放入配置的文件夹中，然后在群聊或私聊中发送以下命令之一：

- `抽卡`
- `来一张`
- `随机图片`

机器人会随机发送一张图片。

## 示例

```
用户：抽卡
机器人：[发送随机图片]
```

## 支持的图片格式

- `.jpg` / `.jpeg`
- `.png`
- `.gif`
- `.bmp`
- `.webp`

## 许可证

MIT License