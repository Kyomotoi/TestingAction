from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.service import Service as sv
from ATRI.config import Config
from ATRI.utils.apscheduler import scheduler
from ATRI.utils.list import count_list


repo_list = []
__doc__ = """
给维护者留言
权限组：所有人
用法：
  /来杯红茶 (msg)
"""

repo = sv.on_command(cmd="来杯红茶", docs=__doc__)


@repo.handle()
async def _repo(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["msg"] = msg


@repo.got("msg", prompt="请告诉咱需要反馈的内容~！")
async def _repo_(bot: Bot, event: MessageEvent, state: T_State) -> None:
    global repo_list
    msg = state["msg"]
    user = event.user_id

    if count_list(repo_list, user) == 5:
        await repo.finish("吾辈已经喝了五杯红茶啦！明天再来吧。")

    repo_list.append(user)

    for sup in Config.BotSelfConfig.superusers:
        await bot.send_private_msg(user_id=sup, message=f"来自用户[{user}]反馈：\n{msg}")

    await repo.finish("吾辈的心愿已由咱转告给咱的维护者了~！")


@scheduler.scheduled_job("cron", hour=0, misfire_grace_time=60)
async def _() -> None:
    global repo_list
    repo_list.clear()


__doc__ = """
重置给维护者的留言次数
权限组：维护者
用法：
  /重置红茶
"""

reset_repo = sv.on_command(cmd="重置红茶", docs=__doc__, permission=SUPERUSER)


@reset_repo.handle()
async def _reset_repo(bot: Bot, event: MessageEvent) -> None:
    global repo_list
    repo_list.clear()
    await reset_repo.finish("红茶重置完成~！")
