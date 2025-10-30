from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler
from routers import employees, whatsapp, telegram, document, chat_bot, address
from middleware.auth_middleware import AuthMiddleware
from services.document_ingestion_service import DocumentIngestionService
from utils.logger import logger
import os

ingestion_service = DocumentIngestionService()
# ------------------------------------------------------------
# Application: FastAPI Server
# Description:
#   This module initializes the FastAPI application, configures
#   middleware, mounts static directories, registers routers, and
#   starts a background scheduler for periodic tasks.
# ------------------------------------------------------------


# ------------------------------------------------------------
# Initialize FastAPI Application
# ------------------------------------------------------------
app = FastAPI(
    title="chat-bot",
    version="1.0",
    description="A backend service for managing document, employees, and chat integrations."
)


# ------------------------------------------------------------
# Middleware Configuration
# ------------------------------------------------------------
# Enables Cross-Origin Resource Sharing (CORS)
# to allow secure API calls from web clients.
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow all origins (adjust for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# Directory Setup for Static Files
# ------------------------------------------------------------
os.makedirs("documents", exist_ok=True)
app.mount("/files", StaticFiles(directory="documents"), name="files")


# ------------------------------------------------------------
# Custom Middleware
# ------------------------------------------------------------
# Authentication middleware for validating requests.
# ------------------------------------------------------------
app.add_middleware(AuthMiddleware)


# ------------------------------------------------------------
# Router Registration
# ------------------------------------------------------------
# Each router handles a specific feature domain.
# ------------------------------------------------------------
app.include_router(whatsapp.router)
app.include_router(telegram.router)
app.include_router(employees.router)
app.include_router(document.router)
app.include_router(chat_bot.router)
app.include_router(address.router)


# ------------------------------------------------------------
# Background Scheduler Setup
# ------------------------------------------------------------
# The APScheduler runs recurring background jobs without
# blocking the main FastAPI event loop.
# ------------------------------------------------------------
scheduler = BackgroundScheduler()


# ------------------------------------------------------------
# Event: Application Startup
# Description:
#   Starts the background scheduler and registers the main loop
#   job that executes at defined intervals.
# ------------------------------------------------------------
@app.on_event("startup")
def start_scheduler():
    logger.info("Scheduler starting...")
    scheduler.add_job(ingestion_service.main_loop, 'interval', id='main_loop_job', seconds=10)
    scheduler.start()
    logger.info("Scheduler started successfully.")


# ------------------------------------------------------------
# Event: Application Shutdown
# Description:
#   Safely stops the background scheduler to avoid thread leaks.
# ------------------------------------------------------------
@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()
    logger.info("Scheduler stopped.")


# ------------------------------------------------------------
# Endpoint: Root
# Description:
#   Simple health-check endpoint to verify the API is running.
# ------------------------------------------------------------
@app.get("/")
async def root():
    logger.info("Root endpoint accessed.")
    return {"message": "FastAPI Running "}
