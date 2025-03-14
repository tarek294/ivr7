from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity
from bot import handle_message_activity
from config import DefaultConfig

CONFIG = DefaultConfig()

adapter_settings = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

async def messages(req):
    print("Test")
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")
    response = await adapter.process_activity(activity, auth_header, handle_message_activity)
    return web.json_response(response)
    
def init_func(argv):
    app = web.Application()
    app.router.add_post("/api/messages", messages)
    return app

if __name__ == "__main__":
    app = init_func(None)
    import os
    port = int(os.environ.get("PORT", 3978))
    web.run_app(app, host="0.0.0.0", port=port)
