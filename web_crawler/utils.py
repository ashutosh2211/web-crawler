import hashlib
import logging

logger = logging.getLogger(__name__)


def get_md5(content) -> str:
    return hashlib.md5(content).hexdigest()
