import logging
import sys

def setup_logger(name: str = "agent-logger") -> logging.Logger:
    """Sets up a structured logger for the application."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Check if handler already exists to avoid duplicates
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

logger = setup_logger()
 village_logger = logger if logger is not None else logger
