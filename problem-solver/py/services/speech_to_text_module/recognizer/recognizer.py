"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

import asyncio
import base64
import os

import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioStreamFormat

from common_module.exception.custom_exception import CustomException
from speech_to_text_module.constant.recognizer_constants import AzureLangNames, AZURE_SPEECH_TO_TEXT_LANGS


class BaseRecognizer:
    def recognize_text(self, audio_bytes: str, lang: str):
        raise NotImplementedError('Method "recognize_text" isn\'t implemented.')


class AzureRecognizer(BaseRecognizer):
    CHANNELS = 1
    BITS_PER_SAMPLE = 16
    SAMPLE_RATE = 16000

    def __init__(self):
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.service_region = os.getenv("AZURE_SERVICE_REGION")

    def recognize_text(self, audio_bytes: str, lang: str) -> str:
        if lang not in AZURE_SPEECH_TO_TEXT_LANGS:
            raise CustomException('The language "{}" isn\'t supported by Azure recognizer.'.format(lang))
        lang = AZURE_SPEECH_TO_TEXT_LANGS[lang]

        if self.speech_key is None or self.service_region is None:
            raise CustomException("Azure credentials have None value.")
        if not audio_bytes:
            raise CustomException("audio bytes has incorrect value.")
        if lang is None:
            raise CustomException("lang isn't set.")

        speech_recognizer = self.create_speech_recognizer(base64.b64decode(audio_bytes), lang)
        futures = [self.process_audio(speech_recognizer)]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        text = loop.run_until_complete(asyncio.gather(*futures))

        if text[0].lstrip() == "":
            raise CustomException("Azure recognizer didn't recognize text.")
        return text[0].lstrip()

    async def process_audio(self, speech_recognizer) -> str:
        result = None
        done = False
        text = ""

        def concatenate_strings(env):
            nonlocal text
            text = "{} {}".format(text, env.result.text)

        def cancel(evt):
            nonlocal result, done
            result = evt.result
            speech_recognizer.stop_continuous_recognition_async()
            done = True

        speech_recognizer.recognized.connect(concatenate_strings)
        speech_recognizer.canceled.connect(cancel)

        speech_recognizer.start_continuous_recognition_async()
        while not done:
            await asyncio.sleep(0.1)
        if result is not None:
            self.process_result(result)
        return text

    def create_speech_recognizer(self, audio_bytes, lang: AzureLangNames):
        speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, region=self.service_region, speech_recognition_language=lang.value
        )

        audio_format = AudioStreamFormat(self.SAMPLE_RATE, self.BITS_PER_SAMPLE, self.CHANNELS)

        stream = speechsdk.audio.PushAudioInputStream(stream_format=audio_format)
        audio_config = speechsdk.audio.AudioConfig(stream=stream)

        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        stream.write(audio_bytes)
        stream.close()

        return speech_recognizer

    @staticmethod
    def process_result(result):
        if result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            if cancellation_details.reason != speechsdk.CancellationReason.EndOfStream:
                error_msg = "{}: {}".format(cancellation_details.reason, cancellation_details.error_details)
                raise CustomException(error_msg)
