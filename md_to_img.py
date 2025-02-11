# encoding:utf-8

import io
import re
import uuid

from PIL import Image
from markdown2image import sync_api as md2img

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from plugins import *


@plugins.register(
    name="MdToImg",
    desire_priority=10,
    hidden=False,
    enabled=False,
    desc="Markdown content convert to jpg",
    version="0.0.1",
    author="lin vx: Crewcut-",
)
class MdToImg(Plugin):
    def __init__(self):
        super().__init__()
        try:
            self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
            logger.info("[MdToImgPlugin] inited.")
        except Exception as e:
            logger.warn("[MdToImgPlugin] init failed, ignore.")
            raise e

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type != ContextType.TEXT:
            return

        content = e_context["context"].content.strip()

        if not re.search(r'[*#|]', content):
            return
        temp_img = '/tmp/img/' + str(uuid.uuid4()) + '.jpg'
        md2img.markdown2image(content, temp_img)
        with open(temp_img, 'rb') as f:
            image_bytes = f.read()
            image_data = Image.open(io.BytesIO(image_bytes))
            if image_data:
                reply = Reply(ReplyType.IMAGE, image_data)
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
            else:
                reply = Reply(ReplyType.TEXT, "无法保存Md图片，请稍后再试。")
                e_context["reply"] = reply

    def get_help_text(self, **kwargs):
        return ""


if __name__ == "__main__":
    plugin = MdToImg()
