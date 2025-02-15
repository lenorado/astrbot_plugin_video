from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Video
from astrbot.api import logger
import random
import asyncio

@register("video_plugin", "Your Name", "随机输出短视频插件", "1.0.0", "repo url")
class VideoPlugin(Star):
   def __init__(self, context: Context):
       super().__init__(context)
       self.video_types = [
           "jk", "YuMeng", "NvDa", "NvGao", "ReWu", "QingCun", "YuZu", "SheJie",
           "ChuanDa", "GaoZhiLiangXiaoJieJie", "HanFu", "HeiSi", "BianZhuang", "LuoLi", "TianMei", "BaiSi"
       ]
       self.cooldown = 60  # 默认冷却时间为 60 秒
       self.last_video_time = 0  # 上次发送视频的时间

   @filter.command("video")
   async def video(self, event: AstrMessageEvent):
       current_time = event.message_obj.timestamp
       if current_time - self.last_video_time < self.cooldown:
           yield event.plain_result("请稍等，视频冷却时间还未结束。")
           return

       video_type = random.choice(self.video_types)
       video_url = f"http://api.mmp.cc/api/ksvideo?type=mp4&id={video_type}"
       video_component = Video.fromURL(video_url)
       yield event.chain_result([video_component])
       self.last_video_time = current_time

   @filter.command("videohelp")
   async def videohelp(self, event: AstrMessageEvent):
       help_message = (
           "欢迎使用视频插件！\n"
           "使用方法：\n"
           "/video：随机输出一个短视频\n"
           "/videohelp：查看插件帮助\n"
           "/cd [时间]：设置视频输出冷却时间，单位为秒，默认为 60 秒\n"
       )
       yield event.plain_result(help_message)

   @filter.command("cd")
   async def cooldown(self, event: AstrMessageEvent, time: int):
       self.cooldown = time
       yield event.plain_result(f"视频输出冷却时间已设置为 {time} 秒。")