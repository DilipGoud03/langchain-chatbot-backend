# ------------------------------------------------------------
# Module: gemini_model
# Description:
#   Implements Google Gemini LLM and embedding model configuration.
# ------------------------------------------------------------

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from .base_model import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):
    def get_chat_model(self):
        """Return Gemini chat model."""
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, verbose=True)

    def get_embedding_model(self):
        """Return Gemini embedding model."""
        return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
