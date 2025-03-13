from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity
from bot import handle_message_activity
from config import DefaultConfig

CONFIG = DefaultConfig()

adapter_settings = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

async def messages(req):
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")
    response = await adapter.process_activity(activity, auth_header, handle_message_activity)
    return web.json_response(response)
    
# Async Handler for Call Events (callback)
async def process_calling_event(request):
    data = await request.json()
    print("Received Calling Event:", data)

    # Here, you would process the calling event
    return web.json_response({"status": "Event Processed"})

# Async Handler for Incoming Calls (call)
async def process_incoming_call(request):
    data = await request.json()
    print("Incoming Call Data:", data)

    # Handle call logic (e.g., answer, play a message, forward)
    return web.json_response({"status": "Incoming Call Processed"})
    
def init_func(argv):
    app = web.Application()
    app.router.add_post("/api/messages", messages)
    return app

if __name__ == "__main__":
    app = init_func(None)
    import os
    port = int(os.environ.get("PORT", 3978))
    web.run_app(app, host="0.0.0.0", port=port)
