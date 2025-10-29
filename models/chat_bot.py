from pydantic import BaseModel

# ------------------------------------------------------------
# Model: ChatModel
# Description:
#   Defines the schema for a user's chat or query input.
#   Used for validating incoming request data in APIs.
# ------------------------------------------------------------
class ChatModel(BaseModel):
    query: str
