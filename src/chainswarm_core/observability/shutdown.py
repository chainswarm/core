import signal
import threading
import time

from loguru import logger

terminate_event = threading.Event()


def shutdown_handler(signum, frame):
    logger.info(f"Shutdown signal received (signal={signum}). Waiting for current processing to complete...")
    terminate_event.set()
    time.sleep(2)


def install_shutdown_handlers():
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)