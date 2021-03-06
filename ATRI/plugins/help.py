import os
import json

from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.service import SERVICE_DIR
from ATRI.service import Service as sv


SERVICE_DIR = SERVICE_DIR / "services"


__doc__ = """
查询命令用法
权限组：所有人
用法：
  /h
  /h list
  /h info (cmd)
"""

help = sv.on_command(
    cmd="help",
    aliases={"h", "?", "？"},
    docs=__doc__,
)


@help.handle()
async def _help(bot: Bot, event: MessageEvent) -> None:
    msg = str(event.message).split(" ")
    if msg[0] == "":
        msg = (
            "呀？找不到路了？\n"
            "/h list 查看可用命令列表\n"
            "/h info (cmd) 查看命令具体帮助\n"
            "项目地址：github.com/Kyomotoi/ATRI\n"
            "咱只能帮你这么多了qwq"
        )
        await help.finish(msg)
    elif msg[0] == "list":
        files = []
        for _, _, i in os.walk(SERVICE_DIR):
            for a in i:
                files.append(a.replace(".json", ""))
        cmds = " | ".join(map(str, files))
        msg = "咱能做很多事！比如：\n" + cmds
        msg0 = msg + "\n具体用法呢，/(cmd) 就好！\n没反应可能是没权限..."
        await help.finish(msg0)
    elif msg[0] == "info":
        cmd = msg[1]
        data = {}
        path = SERVICE_DIR / f"{cmd.replace('/', '')}.json"
        try:
            data = json.loads(path.read_bytes())
        except:
            await help.finish("未找到相关命令...")

        msg = f"{cmd} INFO:\n" f"Enabled: {data['enabled']}\n" f"{data['docs']}"
        await help.finish(msg)
    else:
        await help.finish("请检查输入...")
