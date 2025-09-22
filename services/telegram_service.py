from decouple import config
import requests
from services.models import Models


class TelegramService():
    def __init__(self):
        self.__telegram_token = str(config("BOT_TOKEN")).strip()
        self.__telegram_api_url = config("TELEGRAM_API_URL")
        self.__opne_ai_model = Models()

    def _start_app(self, chat_id):
        try:
            url = f"{self.__telegram_api_url}/bot{self.__telegram_token}"
            reply_text = "Hello Welcome to the OpenAI Bot!"
            payload = {"chat_id": chat_id, "text": reply_text}
            response = requests.post(f"{url}/sendMessage", json=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            raise ProcessLookupError(str(e))

    def _reply_message(self, chat_id, query: str):
        try:
            url = f"{self.__telegram_api_url}/bot{self.__telegram_token}"
            reply_text = self.__opne_ai_model.generate_answer(query)
            payload = {"chat_id": chat_id, "text": reply_text['answer']}
            response = requests.post(f"{url}/sendMessage", json=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            raise ProcessLookupError(str(e))
