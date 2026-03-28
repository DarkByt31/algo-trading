import logging
from app.config import settings

def setup_logging():
    """Setup application logging"""
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


logger = logging.getLogger(__name__)
