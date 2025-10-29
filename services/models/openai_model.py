# ------------------------------------------------------------
# Module: openai_model
# Description:
#   Implements OpenAI LLM and embedding model configuration.
# ------------------------------------------------------------

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from .base_model import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    def get_chat_model(self):
        """Return OpenAI chat model."""
        return ChatOpenAI(model="gpt-4o-mini", temperature=0, verbose=True)

    def get_embedding_model(self):
        """Return OpenAI embedding model."""
        return OpenAIEmbeddings(model="text-embedding-ada-002")
