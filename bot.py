from botbuilder.core import TurnContext
from botbuilder.schema import Activity, ActivityTypes
from botbuilder.ai.speech import SpeechConfig, SpeechSynthesizer
from config import DefaultConfig

CONFIG = DefaultConfig()

speech_config = SpeechConfig(subscription=CONFIG.SPEECH_KEY, region=CONFIG.SPEECH_REGION)
speech_synthesizer = SpeechSynthesizer(speech_config)

async def handle_message_activity(turn_context: TurnContext):
    user_text = turn_context.activity.text
    reply_text = f"You said: {user_text}"

    speech_result = speech_synthesizer.speak_text(reply_text)

    reply_activity = Activity(
        type=ActivityTypes.message,
        text=reply_text,
        speak=reply_text,
        input_hint="acceptingInput",
    )

    await turn_context.send_activity(reply_activity)
