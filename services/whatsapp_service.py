from decouple import config
import requests
from dotenv import load_dotenv
from services.models import Models

load_dotenv()


class WhatsAppService():
    def __init__(self) -> None:
        self.__access_token = str(config("ACCESS_TOKEN")).strip()
        self.phone_number_id = config("PHONE_NUMBER_ID")
        self.__graph_api_url = config("GRAPH_API_URL")
        self.__opne_ai_model = Models()

    def reply_whatsapp_message(self, to: str, query: str):
        try:
            url = f"{self.__graph_api_url}/{self.phone_number_id}/messages"
            reply_message = self.__opne_ai_model.generate_answer(query)

            headers = {
                "Authorization": f"Bearer {self.__access_token}",
                "Content-Type": "application/json"
            }

            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {"body": reply_message['answer']}
            }

            response = requests.post(url, headers=headers, json=payload)
            print(response.json())
            return response.json()
        except Exception as e:
            raise ProcessLookupError(str(e))
