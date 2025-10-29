import logging
import os

# ------------------------------------------------------------
# Module: logger
# Description:
#   Configures centralized logging for the entire application.
#   Supports console and file logging with timestamped entries.
# ------------------------------------------------------------

# Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configure log file
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Basic configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Create a logger instance
logger = logging.getLogger("app_logger")
