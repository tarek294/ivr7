import os
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    ConversationState,
    MemoryStorage,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.integration.aiohttp import BotFrameworkAdapter, BotFrameworkHttpClient
from botbuilder.schema import Activity, ActivityTypes
from aiohttp import web

# Import speech-specific packages
from botbuilder.ai.speech import SpeechConfig, SpeechSynthesizer

# Environment variables (Set these in your Azure environment)
APP_ID = os.getenv("1c5524dc-0c09-4925-bca8-d633afc9c070")
APP_PASSWORD = os.getenv("Kca8Q~mJIubZW7vwUSD2bG1SPQ4_FCWARDezPa31")
SPEECH_KEY = os.getenv("3c358ec45fdc4e6daeecb7a30002a9df")
SPEECH_REGION = os.getenv("westus2")

speech_config = SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
speech_synthesizer = SpeechSynthesizer(speech_config)

# Bot Adapter
adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

# Simple Bot Logic
async def on_message_activity(turn_context: TurnContext):
    user_text = turn_context.activity.text
    reply_text = f"You said: {user_text}"

    # Speech synthesis
    speech_result = speech_synthesizer.speak_text(reply_text)

    reply_activity = Activity(
        type=ActivityTypes.message,
        text=reply_text,
        speak=reply_text,  # This enables voice responses
        input_hint="acceptingInput",
    )

    await turn_context.send_activity(reply_activity)

# Main request handler
async def messages(req: web.Request) -> web.Response:
    body = await req.json()
    activity = Activity().deserialize(body)

    auth_header = req.headers.get("Authorization", "")

    await adapter.process_activity(activity, auth_header, on_message_activity)
    return web.Response(status=200)

# Setup web server
app = web.Application(middlewares=[aiohttp_error_middleware])
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    web.run_app(app, host="localhost", port=3978)
