from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.service import Service as sv
from ATRI.rule import is_in_service
from ATRI.utils.list import count_list, del_list_aim
from ATRI.utils.request import get_text
from ATRI.exceptions import RequestTimeOut


URL = "https://zuanbot.com/api.php?level=min&lang=zh_cn"
sick_list = []


__doc__ = """
口臭一下
权限组：所有人
用法：
  口臭，口臭一下，骂我
"""

curse = sv.on_message(rule=is_in_service("口臭"))
sv.manual_reg_service("口臭", __doc__)


@curse.handle()
async def _curse(bot: Bot, event: MessageEvent) -> None:
    global sick_list
    msg = str(event.message)
    user = event.get_user_id()
    curse_key = ["口臭", "口臭一下", "骂我"]

    if msg not in curse_key:
        return

    if count_list(sick_list, user) == 3:
        sick_list.append(user)
        repo = "不是？？你这么想被咱骂的嘛？？" "被咱骂就这么舒服的吗？！" "该......你该不会是.....M吧！"
        await curse.finish(repo)
    elif count_list(sick_list, user) == 6:
        sick_list = del_list_aim(sick_list, user)
        await curse.finish("给我适可而止阿！？")
    else:
        sick_list.append(user)
        try:
            await curse.finish(await get_text(URL))
        except RequestTimeOut:
            raise RequestTimeOut("Time out!")
