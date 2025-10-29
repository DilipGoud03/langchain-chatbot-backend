from decouple import config
import requests
from services.llm_modelss import LLMModels

# ------------------------------------------------------------
# Module: telegram_service
# Description:
#   Handles all Telegram Bot API interactions.
#   - Integrates with LLMModels for intelligent replies.
#   - Sends and receives chat messages through Telegram.
# ------------------------------------------------------------


class TelegramService:
    # ------------------------------------------------------------
    # Method: __init__
    # Description:
    #   Initializes Telegram service configuration.
    #   - Loads bot token and API URL from environment variables.
    #   - Instantiates OpenAI model handler for generating replies.
    # ------------------------------------------------------------
    def __init__(self):
        self.__telegram_token = str(config("BOT_TOKEN")).strip()
        self.__telegram_api_url = str(config("TELEGRAM_API_URL")).strip()
        self.__llm_models = LLMModels()

    # ------------------------------------------------------------
    # Method: _start_app
    # Description:
    #   Sends a welcome message to a user when they start the bot.
    #
    # Parameters:
    #   - chat_id (int): Unique identifier for the Telegram chat.
    #
    # Returns:
    #   - dict: Telegram API response JSON.
    # ------------------------------------------------------------
    def _start_app(self, chat_id):
        try:
            url = f"{self.__telegram_api_url}/bot{self.__telegram_token}"
            reply_text = "👋 Hello! Welcome to the OpenAI Bot. Ask me anything!"
            payload = {"chat_id": chat_id, "text": reply_text}

            response = requests.post(f"{url}/sendMessage", json=payload)
            return response.json()
        except Exception as e:
            raise ProcessLookupError(str(e))

    # ------------------------------------------------------------
    # Method: _reply_message
    # Description:
    #   Handles user messages and returns AI-generated responses.
    #
    # Workflow:
    #     1. Receives a user query from Telegram.
    #     2. Passes the query to the OpenAI model for response generation.
    #     3. Sends the AI’s response back to the Telegram chat.
    #
    # Parameters:
    #   - chat_id (int): The chat where the message originated.
    #   - query (str): The user’s message text.
    #
    # Returns:
    #   - dict: Telegram API response JSON.
    # ------------------------------------------------------------
    def _reply_message(self, chat_id, query: str):
        try:
            url = f"{self.__telegram_api_url}/bot{self.__telegram_token}"

            # Generate AI response
            reply_text = self.__llm_models.generate_answer(query)

            payload = {"chat_id": chat_id, "text": reply_text['answer']}
            response = requests.post(f"{url}/sendMessage", json=payload)
            return response.json()
        except Exception as e:
            raise ProcessLookupError(str(e))
