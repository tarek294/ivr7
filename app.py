from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity
from bot import handle_message_activity
from config import DefaultConfig

CONFIG = DefaultConfig()

adapter_settings = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

async def messages(req: web.Request) -> web.Response:
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")

    await adapter.process_activity(activity, auth_header, handle_message_activity)
    return web.Response(status=200)
def init_func(argv):
    app = web.Application()
    app.router.add_post("/api/messages", messages)
    return app

if __name__ == "__main__":
    import os
    app = init_func(None)
    port = int(os.environ.get("PORT", 3978))
    web.run_app(app, host="0.0.0.0", port=port)
