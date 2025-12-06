"""
NoneBot Plugin MHY Choose
一个用于从指定文件夹随机发送图片（包括GIF）的NoneBot插件
"""
from pathlib import Path
from typing import List
import random
import os

from nonebot import on_command, get_driver
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, GroupMessageEvent, PrivateMessageEvent
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.log import logger
from pydantic import BaseModel, Field

__plugin_meta__ = PluginMetadata(
    name="MHY Choose",
    description="从指定文件夹随机发送图片（包括GIF）",
    usage="发送 '抽卡' 或 '来一张' 来获取随机图片",
    type="application",
    homepage="https://github.com/leafliber/nonebot_plugin_mhy_choose",
    supported_adapters={"~onebot.v11"},
)


class Config(BaseModel):
    """Plugin configuration"""
    mhy_choose_image_path: str = Field(default="images", description="图片文件夹路径")


# 获取配置
driver = get_driver()
plugin_config = Config.parse_obj(driver.config.dict())

# 支持的图片格式
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}


def get_image_files(folder_path: str) -> List[Path]:
    """
    获取指定文件夹内的所有图片文件
    
    Args:
        folder_path: 图片文件夹路径
        
    Returns:
        图片文件路径列表
    """
    image_files = []
    path = Path(folder_path)
    
    if not path.exists():
        logger.warning(f"图片文件夹不存在: {folder_path}")
        return image_files
    
    if not path.is_dir():
        logger.warning(f"路径不是文件夹: {folder_path}")
        return image_files
    
    # 遍历文件夹获取所有图片文件
    for file_path in path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS:
            image_files.append(file_path)
    
    return image_files


def get_random_image() -> Path | None:
    """
    从配置的文件夹中随机获取一张图片
    
    Returns:
        随机图片的路径，如果没有图片则返回 None
    """
    image_files = get_image_files(plugin_config.mhy_choose_image_path)
    
    if not image_files:
        logger.warning("没有找到任何图片文件")
        return None
    
    return random.choice(image_files)


# 创建命令处理器
mhy_choose = on_command("抽卡", aliases={"来一张", "随机图片"}, priority=5, block=True)


@mhy_choose.handle()
async def handle_mhy_choose(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent):
    """处理抽卡命令"""
    try:
        # 获取随机图片
        image_path = get_random_image()
        
        if image_path is None:
            await mhy_choose.finish("未找到任何图片，请检查配置的图片文件夹")
            return
        
        # 发送图片
        logger.info(f"发送图片: {image_path}")
        image_msg = MessageSegment.image(image_path.as_uri())
        await mhy_choose.finish(image_msg)
        
    except Exception as e:
        logger.error(f"发送图片时出错: {e}")
        await mhy_choose.finish(f"发送图片时出错: {str(e)}")
