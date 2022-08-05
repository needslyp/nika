"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

import os

import azure.cognitiveservices.speech as speechsdk

from common_module.exception.custom_exception import CustomException
from text_to_speech_module.synthesizer.base_synthesizer import BaseSynthesizer


class AzureSynthesizer(BaseSynthesizer):
    def __init__(self, voices: dict):
        super().__init__(voices)
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.service_region = os.getenv("AZURE_SERVICE_REGION")

    def synthesize_voice(self, text: str, lang: str):
        voice = self._choose_voice(lang)
        if self.speech_key is not None and self.service_region is not None and voice is not None:
            speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.service_region)
            speech_config.speech_synthesis_voice_name = voice.id

            synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
            result = synthesizer.speak_text_async(text).get()
            audio_content = self.process_synthesize_result(result)
        else:
            raise CustomException("Some of the required parameters for the AzureSynthesizer are not set.")
        return audio_content

    @staticmethod
    def process_synthesize_result(result):
        audio_content = None
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            audio_content = result.audio_data
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            error_msg = "AzureSynthesizer can't synthesize speech."
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                error_msg = "{}: {}".format(cancellation_details.reason, cancellation_details.error_details)
            raise CustomException(error_msg)
        return audio_content
