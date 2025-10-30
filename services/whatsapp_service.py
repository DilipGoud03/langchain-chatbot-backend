from decouple import config
import requests
from dotenv import load_dotenv
from services.langchain_service import LangchainService

load_dotenv()


# ------------------------------------------------------------
# Module: whatsapp_service
# Description:
#   Handles communication with WhatsApp via the Meta Graph API.
#   - Sends text replies to users.
#   - Uses OpenAI models to generate dynamic responses.
# ------------------------------------------------------------

class WhatsAppService:
    # ------------------------------------------------------------
    # Method: __init__
    # Description:
    #   Initializes the WhatsApp service with required credentials.
    #   Loads access tokens, phone number ID, and Graph API URL from .env.
    #   Instantiates the OpenAI model service for generating responses.
    # ------------------------------------------------------------
    def __init__(self) -> None:
        self.__access_token = str(config("ACCESS_TOKEN")).strip()
        self.phone_number_id = config("PHONE_NUMBER_ID")
        self.__graph_api_url = config("GRAPH_API_URL")
        self.__langchain_service = LangchainService()

    # ------------------------------------------------------------
    # Method: reply_whatsapp_message
    # Description:
    #   Sends a WhatsApp message reply to a specific recipient.
    #
    # Workflow:
    #     1. Calls OpenAI model to generate a response for the given query.
    #     2. Sends the response text via the WhatsApp Cloud API.
    #
    # Parameters:
    #   - to (str): The recipient’s WhatsApp phone number (with country code).
    #   - query (str): The user’s input or message to process.
    #
    # Returns:
    #   - dict: JSON response from the WhatsApp API.
    #
    # Raises:
    #   - ProcessLookupError: If any API or network error occurs.
    # ------------------------------------------------------------
    def reply_whatsapp_message(self, to: str, query: str):
        try:
            url = f"{self.__graph_api_url}/{self.phone_number_id}/messages"
            reply_message = self.__langchain_service.generate_answer(query)

            headers = {
                "Authorization": f"Bearer {self.__access_token}",
                "Content-Type": "application/json"
            }

            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {"body": reply_message["answer"]}
            }

            response = requests.post(url, headers=headers, json=payload)
            print("WhatsApp API Response:", response.json())

            return response.json()

        except Exception as e:
            raise ProcessLookupError(str(e))
