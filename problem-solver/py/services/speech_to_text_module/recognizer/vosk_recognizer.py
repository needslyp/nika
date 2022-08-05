"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from enum import Enum
import json
from json.decoder import JSONDecodeError
import os
import requests
from requests.exceptions import RequestException

from common_module.constant.http_status import HttpStatus
from common_module.exception.custom_exception import CustomException
from speech_to_text_module.constant.recognizer_constants import VOSK_SPEECH_TO_TEXT_LANGS
from speech_to_text_module.recognizer.recognizer import BaseRecognizer


class VoskJsonField(Enum):
    TEXT = "text"
    ERROR_MESSAGE = "error_message"


class VoskRecognizer(BaseRecognizer):
    def __init__(self):
        self.host = os.getenv("VOSK_SERVICE_HOST", "localhost")
        self.port = os.getenv("VOSK_SERVICE_PORT", "9000")
        try:
            r = requests.get("http://{}:{}/models".format(self.host, self.port))
            if r:
                self.models = json.loads(r.text)
            else:
                raise CustomException("Not possible to receive a response from the Vosk service.")
        except (RequestException, JSONDecodeError) as ex:
            raise CustomException(str(ex)) from ex

    def recognize_text(self, audio_bytes: str, lang: str):
        if lang not in VOSK_SPEECH_TO_TEXT_LANGS:
            raise CustomException('The language "{}" isn\'t supported by the Vosk recognizer.'.format(lang))
        lang = VOSK_SPEECH_TO_TEXT_LANGS[lang].value
        if lang not in self.models or len(self.models[lang]) == 0:
            raise CustomException('The language "{}" isn\'t supported by the Vosk recognizer.'.format(lang))

        result_text = None
        error_message = None
        for model in self.models[lang]:
            try:
                req = requests.post(
                    "http://{}:{}/generate_text/{}/{}".format(self.host, self.port, lang, model),
                    data={"audio_bytes": audio_bytes, "get_words": 0},
                )
                if req:
                    result_dict = json.loads(req.text)
                    if req.status_code == HttpStatus.OK.value:
                        result_text = result_dict[VoskJsonField.TEXT.value]
                        break
                    error_message = result_dict[VoskJsonField.ERROR_MESSAGE.value]
            except (ConnectionError, JSONDecodeError) as ex:
                raise CustomException(str(ex)) from ex

        if result_text is None:
            if error_message is None:
                raise CustomException("The Vosk recognizer hasn't recognized the text.")
            raise CustomException("Vosk recognizer error: {}".format(error_message))

        return result_text
