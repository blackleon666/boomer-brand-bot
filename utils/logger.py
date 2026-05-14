import logging
from logging.handlers import RotatingFileHandler
import os
from ..crypto.encrypt import encrypt_text

def setup_logger():
    """Set up a rotating file logger that encrypts log messages."""
    # This is a simplified version. In a real application, you might want to
    # encrypt each log message before writing, or encrypt the log file itself.
    # For simplicity, we'll just log to a file and rely on file-level encryption
    # or OS-level encryption for security. However, the requirement was to
    # encrypt chat logs, so we'll encrypt each message.

    # Create a custom formatter that encrypts the message
    class EncryptingFormatter(logging.Formatter):
        def format(self, record):
            # Format the message as usual
            message = super().format(record)
            # Encrypt the formatted message
            try:
                encrypted_message = encrypt_text(message)
                return encrypted_message
            except Exception:
                # If encryption fails, return the original message (or handle as needed)
                return message

    # Set up the logger
    logger = logging.getLogger('boomer_bot')
    logger.setLevel(logging.INFO)

    # Create a rotating file handler
    log_dir = os.path.dirname(os.getenv("LOG_PATH", "logs/chat.log.enc"))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    handler = RotatingFileHandler(
        os.getenv("LOG_PATH", "logs/chat.log.enc"),
        maxBytes=5*1024*1024,  # 5 MB
        backupCount=5,
        encoding='utf-8'
    )
    handler.setFormatter(EncryptingFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(handler)

    # Also keep a console handler for debugging (optional)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger
