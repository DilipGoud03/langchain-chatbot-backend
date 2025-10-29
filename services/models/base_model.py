# ------------------------------------------------------------
# Module: base_model
# Description:
#   Defines a standard interface for all LLM provider classes.
#   Each provider must implement chat and embedding models.
# ------------------------------------------------------------

class BaseLLMProvider:
    def get_chat_model(self):
        """Return an initialized chat model instance."""
        raise NotImplementedError

    def get_embedding_model(self):
        """Return an initialized embedding model instance."""
        raise NotImplementedError
