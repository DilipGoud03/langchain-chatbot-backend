# ------------------------------------------------------------
# Module: llm_service
# Description:
#   This module provides a unified interface to access different
#   Large Language Model (LLM) providers such as:
#     - OpenAI (GPT models)
#     - Google (Gemini models)
#   It supports both chat models and embedding models.
# ------------------------------------------------------------

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


# ------------------------------------------------------------
# Class: LLMService
# Description:
#   Handles initialization of LLMs (chat & embedding) based on
#   the selected provider ("openai" or "google").
#   This class provides abstraction to easily switch between
#   Gemini (Google) and GPT (OpenAI) models.
# ------------------------------------------------------------
class LLMService:
    # ------------------------------------------------------------
    # Method: __init__
    # Description:
    #   Initializes the LLMService with the specified provider.
    #   Example:
    #       llm = LLMService(provider="openai")
    # ------------------------------------------------------------
    def __init__(self, provider) -> None:
        self.provider = provider

    # ------------------------------------------------------------
    # Method: gemini_chat_model
    # Description:
    #   Returns the Google Gemini chat model instance using
    #   the latest "gemini-2.5-flash" version.
    # ------------------------------------------------------------
    def gemini_chat_model(self):
        return ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    # ------------------------------------------------------------
    # Method: gemini_embedding_model
    # Description:
    #   Returns the Google Gemini embedding model used for
    #   vector-based operations such as semantic search.
    # ------------------------------------------------------------
    def gemini_embedding_model(self):
        return GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # ------------------------------------------------------------
    # Method: openai_chat_model
    # Description:
    #   Returns the OpenAI GPT chat model instance.
    #   Uses "gpt-4o-mini" for cost-effective responses.
    # ------------------------------------------------------------
    def openai_chat_model(self):
        return ChatOpenAI(model="gpt-4o-mini", temperature=0, verbose=True)

    # ------------------------------------------------------------
    # Method: openai_embedding_model
    # Description:
    #   Returns the OpenAI embedding model used for text
    #   similarity, clustering, or semantic search.
    # ------------------------------------------------------------
    def openai_embedding_model(self):
        return OpenAIEmbeddings(model="text-embedding-ada-002")

    # ------------------------------------------------------------
    # Method: chat_model
    # Description:
    #   Automatically returns the appropriate chat model
    #   depending on the configured provider.
    # ------------------------------------------------------------
    def chat_model(self):
        if self.provider == 'openai':
            return self.openai_chat_model()
        return self.gemini_chat_model()

    # ------------------------------------------------------------
    # Method: embedding_model
    # Description:
    #   Automatically returns the appropriate embedding model
    #   depending on the configured provider.
    # ------------------------------------------------------------
    def embedding_model(self):
        if self.provider == 'openai':
            return self.openai_embedding_model()
        return self.gemini_embedding_model()
