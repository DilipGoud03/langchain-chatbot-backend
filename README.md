# 🧠 LangChain Chatbot Backend

Welcome to the backend powerhouse for your AI-driven chatbot experience! This project combines cutting-edge language models, seamless messaging integrations, robust authentication, and reliable database connectivity to deliver smart, secure, and interactive conversations across platforms.

## 🚀 Features

- **LangChain-powered AI**: Advanced natural language processing with LangChain.
- **Multi-platform Messaging**: Chatbot integration for Telegram (via BotFather) and WhatsApp (via Cloud APIs like Twilio or Meta).
- **FastAPI Framework**: Lightning-fast, modern Python backend.
- **MySQL Database Support**: Persistent data storage and retrieval; ready-made tables in `AI.sql`.
- **User Authentication**: Secure login system—authenticated employees gain access to private documents and personalized database queries.
- **Access Control**: Granular permission system restricts sensitive resources to logged-in employees.
- **Modular & Scalable**: Easily extend or adapt for new use cases.
- **Easy Frontend Integration**: Works perfectly with [langchain-chatbot-ui](https://github.com/DilipGoud03/langchain-chatbot-ui).

## 🛠 Technologies Used

- **Python**
- **FastAPI**
- **LangChain**
- **Telegram Bot API**
- **WhatsApp Cloud API** (Meta)
- **MySQL**
- **Authentication** (JWT)

## 🔒 Authentication & Access Control

- **Login Required**: employees must authenticate to access private documents or sensitive database records.
- **Private Document Access**: Authenticated employees can query and receive information from protected sources (e.g., company docs, internal files).
- **Database Security**: Only logged-in employees can perform advanced or personalized queries on MySQL tables.

## 📱 Messaging Platform Integrations

### Telegram (via BotFather)

1. Talk to [BotFather](https://t.me/botfather) on Telegram.
2. Run `/newbot` and follow instructions to get your **Bot Token**.
3. Add your token to `.env`:
   ```
   TELEGRAM_BOT_TOKEN=your-bot-token-here
   ```
4. (Optional for cloud) Set webhook for your deployed backend:
   ```
   https://api.telegram.org/bot<YourBotToken>/setWebhook?url=https://your-domain.com/telegram-webhook
   ```
5. Your bot will authenticate employees as needed before providing access to private or sensitive information.

### WhatsApp (via Cloud API)

1. provider [Meta Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api/)).
2. Register your WhatsApp number & get API credentials.
3. Add credentials to `.env`:
   ```
   WHATSAPP_API_KEY=your-api-key
   WHATSAPP_PHONE_NUMBER=your-number
   WHATSAPP_CLOUD_URL=https://your-cloud-provider.com/endpoint
   ```
4. Set webhook URL in provider dashboard → points to your backend WhatsApp endpoint.
5. WhatsApp conversations can require authentication for access to private data.

## 🗄 Database Integration

- Uses MySQL to store user data, conversations, and more.
- **Setup**: Import the provided `AI.sql` file to create required tables:
  ```bash
  mysql -u <username> -p <database_name> < AI.sql
  ```
- Configure your DB connection in `.env`.
- Authenticated employees can access additional data and features from the database.

## ⚡ Installation

1. **Clone this repo**

   ```bash
   git clone https://github.com/DilipGoud03/langchain-chatbot-backend.git
   cd langchain-chatbot-backend
   ```
   
2. **Create and Activate virtual Enviorment**

   1. Create a virtual environment.

      ```bash
      python -m venv langchain-chatbot-venv
      ```

   2. Activate virtual environment.

      ```bash
      source langchain-chatbot-venv/bin/activate
      ```
2. **Install dependencies**

      ```bash
      pip install -r requirements.txt
      ```

3. **Configure environment**

   - Copy `.env.example` to `.env`
   - Fill in your DB credentials, API keys, tokens, etc.

4. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```
   OR
   ```bash
   fastapi dev main.py
   ```

## 💬 Usage

- **API**: Interact at `http://localhost:8000`
  - Example:
    ```bash
        'curl -X 'POST' \
        'http://127.0.0.1:8000/chat-bot/' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "query": "Hii"
            }'
    ```
- **Authentication**: Login via API or messaging platform to unlock private document and database access.
- **Telegram**: Chat with your bot via Telegram.
- **WhatsApp**: Send/receive messages via WhatsApp (cloud API setup).

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.

---

**Unleash intelligent, secure conversations across platforms with LangChain, FastAPI, authentication, and seamless messaging integrations. Start building your smart chatbot backend today!**
