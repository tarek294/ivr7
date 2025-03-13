import os

class DefaultConfig:
    APP_ID = os.getenv("MicrosoftAppId","1c5524dc-0c09-4925-bca8-d633afc9c070")
    APP_PASSWORD = os.getenv("MicrosoftAppPassword", "Kca8Q~mJIubZW7vwUSD2bG1SPQ4_FCWARDezPa31")
    SPEECH_KEY = os.getenv("AzureSpeechKey", "3c358ec45fdc4e6daeecb7a30002a9df")
    SPEECH_REGION = os.getenv("AzureSpeechRegion", "westus2")
