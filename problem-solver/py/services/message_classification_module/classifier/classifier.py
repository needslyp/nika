"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Nikiforov Sergei
Author Kseniya Bantsevich
Author Anastasiya Vasilevskaya
"""

import os

from dotenv import load_dotenv
from common.sc_log import Log
from common_module.exception.custom_exception import CustomException
from message_classification_module.classifier.task.english_sentence_topic.core.wit_api_trainer import (
    WitAPI,
    WitApiTrainer,
)


class Classifier:
    def __init__(self):
        self.log = Log(self.__class__.__name__)

    CREDENTIALS_PATH = "../../resources/.env"

    def classify_message_topic(self, text: str) -> dict:
        credentials_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.CREDENTIALS_PATH)
        try:
            if os.path.isfile(credentials_path):
                load_dotenv(credentials_path)
                access_token = os.getenv("WIT_API_SERVER_ACCESS_TOKEN")
                if not access_token:
                    raise CustomException("The WIT token has None value.")
            else:
                self.log.error('The file with the name "{}" isn\'t found.'.format(credentials_path))
        except CustomException as ex:
            self.log.error(str(ex))
        wit_api_trainer = WitApiTrainer(wit_api=WitAPI(access_token=access_token), init_local_data=False)
        response = wit_api_trainer.test(text)
        return response
