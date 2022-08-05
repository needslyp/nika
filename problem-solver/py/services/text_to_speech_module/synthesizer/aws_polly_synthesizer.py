"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

import os

from boto3 import Session
from botocore.exceptions import ClientError

from common_module.constant.extension import AudioExtension
from common_module.exception.custom_exception import CustomException
from text_to_speech_module.constant.synthesizer_constants import Engine
from text_to_speech_module.synthesizer.base_synthesizer import BaseSynthesizer


class AwsPollySynthesizer(BaseSynthesizer):
    def __init__(self, voices: dict):
        super().__init__(voices)
        self.access_key_id = os.getenv("POLLY_ACCESS_KEY_ID")
        self.secret_access_key = os.getenv("POLLY_SECRET_ACCESS_KEY")
        self.region = os.getenv("POLLY_REGION")
        self.AWS_CLIENT_NAME = "polly"
        self.AUDIO_STREAM = "AudioStream"

    def synthesize_voice(self, text: str, lang: str):
        voice = self._choose_voice(lang)
        if (
            self.access_key_id is not None
            and self.secret_access_key is not None
            and self.region is not None
            and voice is not None
        ):
            session = Session(
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key,
                region_name=self.region,
            )
            client = session.client(self.AWS_CLIENT_NAME)
            engine = Engine.STANDARD.value
            if voice.is_neural:
                engine = Engine.NEURAL.value
            try:
                res = client.synthesize_speech(
                    Engine=engine, Text=text, OutputFormat=AudioExtension.MP3.value, VoiceId=voice.id
                )
                if self.AUDIO_STREAM in res:
                    audio_content = res[self.AUDIO_STREAM].read()
                else:
                    raise CustomException("The audio content has not been synthesized.")
            except ClientError as e:
                raise CustomException from e
        else:
            raise CustomException("Some of the required parameters for the AwsPollySynthesizer are not set.")
        return audio_content
