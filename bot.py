from botbuilder.core import TurnContext
from botbuilder.schema import Activity, ActivityTypes
import azure.cognitiveservices.speech as speechsdk
from config import DefaultConfig

CONFIG = DefaultConfig()

speech_config = speechsdk.SpeechConfig(subscription=CONFIG.SPEECH_KEY, region=CONFIG.SPEECH_REGION)

async def handle_message_activity(turn_context: TurnContext):
    user_text = turn_context.activity.text
    reply_text = f"You said: {user_text}"

    # Synthesize speech
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = synthesizer.speak_text_async(reply_text).get()

    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesis failed: {result.reason}")

    reply_activity = Activity(
        type=ActivityTypes.message,
        text=reply_text,
        speak=reply_text,  # Azure Bot Framework uses this field to speak via Skype
        input_hint="acceptingInput",
    )

    await turn_context.send_activity(reply_activity)
