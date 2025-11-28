import os
import sys
import time
import uuid
import threading
from typing import Optional

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

_correlation_context = threading.local()


def generate_correlation_id() -> str:
    return f"req_{uuid.uuid4().hex[:12]}"


def get_correlation_id() -> Optional[str]:
    return getattr(_correlation_context, 'correlation_id', None)


def set_correlation_id(correlation_id: str):
    _correlation_context.correlation_id = correlation_id


def _find_project_root() -> str:
    markers = ['pyproject.toml', 'requirements.txt', '.git', 'packages']
    
    start_dir = os.getcwd()
    current = start_dir
    
    for _ in range(10):
        for marker in markers:
            if os.path.exists(os.path.join(current, marker)):
                return current
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    
    return start_dir


def setup_logger(service_name: str, logs_dir: Optional[str] = None) -> str:
    def patch_record(record):
        record["extra"]["service"] = service_name
        correlation_id = get_correlation_id()
        if correlation_id:
            record["extra"]["correlation_id"] = correlation_id
        record["extra"]["timestamp"] = time.time()
        return True

    if logs_dir is None:
        logs_dir = os.environ.get('LOGS_DIR')
    
    if logs_dir is None:
        project_root = _find_project_root()
        logs_dir = os.path.join(project_root, "logs")

    os.makedirs(logs_dir, exist_ok=True)

    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()

    logger.remove()

    logger.add(
        os.path.join(logs_dir, f"{service_name}.log"),
        rotation="500 MB",
        level=log_level,
        filter=patch_record,
        serialize=True,
        format="{time} | {level} | {extra[service]} | {message} | {extra}"
    )

    console_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{extra[service]}</cyan> | {message} | <white>{extra}</white>"
    if get_correlation_id():
        console_format += " | <yellow>{extra[correlation_id]}</yellow>"

    logger.add(
        sys.stdout,
        format=console_format,
        level=log_level,
        filter=patch_record,
        enqueue=True,
        backtrace=False,
        diagnose=False,
    )

    logger.info(f"Logger configured with level: {log_level}")

    return service_name