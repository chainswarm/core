import os
import json
import logging
from typing import List, Optional, Dict, Any

from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def _setup_loguru(**kwargs):
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(logging.INFO)
    
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True


def load_beat_schedule(schedule_path: Optional[str] = None) -> Dict[str, Any]:

    env_path = os.getenv('CELERY_BEAT_SCHEDULE_PATH')
    if env_path and os.path.exists(env_path):
        logger.info(
            "Using custom beat schedule from environment",
            extra={"schedule_path": env_path}
        )
        schedule_path = env_path

    if schedule_path is None:
        return {}

    if not os.path.exists(schedule_path):
        return {}
    
    try:
        with open(schedule_path, 'r') as f:
            schedule = json.load(f)

        filtered_schedule = {}
        for task_name, task_config in schedule.items():
            if not isinstance(task_config, dict):
                continue
                
            if 'args' in task_config and isinstance(task_config['args'], list):
                task_config['args'] = tuple(task_config['args'])
            
            if 'schedule' in task_config and isinstance(task_config['schedule'], str):
                cron_parts = task_config['schedule'].split()
                if len(cron_parts) == 5:
                    minute, hour, day, month, day_of_week = cron_parts
                    task_config['schedule'] = crontab(
                        minute=minute,
                        hour=hour,
                        day_of_month=day,
                        month_of_year=month,
                        day_of_week=day_of_week
                    )
            
            filtered_schedule[task_name] = task_config
        
        return filtered_schedule
    except json.JSONDecodeError as e:
        logger.error(
            "Invalid JSON in beat_schedule.json",
            extra={
                "error": str(e),
                "schedule_path": schedule_path
            }
        )
        return {}
    except Exception as e:
        logger.error(
            "Failed to load beat_schedule.json",
            extra={
                "error": str(e),
                "schedule_path": schedule_path
            }
        )
        return {}


def create_celery_app(
    name: str,
    autodiscover: List[str],
    beat_schedule_path: Optional[str] = None,
    broker_url: Optional[str] = None,
    result_backend: Optional[str] = None,
    **config_overrides
) -> Celery:
    setup_logging.connect(_setup_loguru)
    
    celery_app = Celery(name)
    
    beat_schedule = load_beat_schedule(beat_schedule_path)
    
    default_broker = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    config = {
        'broker_url': broker_url or default_broker,
        'result_backend': result_backend or default_broker,
        'task_serializer': 'json',
        'result_serializer': 'json',
        'accept_content': ['json'],
        'timezone': 'UTC',
        'result_expires': 86400,
        'task_acks_late': True,
        'worker_prefetch_multiplier': 1,
        'task_track_started': True,
        'task_reject_on_worker_lost': True,
        'beat_schedule': beat_schedule,
        'worker_hijack_root_logger': False,
        'worker_log_color': False,
    }
    
    config.update(config_overrides)
    celery_app.config_from_object(config)
    
    celery_app.autodiscover_tasks(autodiscover)
    
    return celery_app


def run_dev_worker(celery_app: Celery, loglevel: str = 'info'):
    import threading
    
    logger.info(
        "Starting Celery for local development",
        extra={
            "mode": "development",
            "components": ["beat", "worker"]
        }
    )
    
    def run_beat():
        logger.info(
            "Starting Celery Beat scheduler",
            extra={
                "thread": "daemon",
                "loglevel": loglevel
            }
        )
        celery_app.start(['beat', f'--loglevel={loglevel}'])
    
    beat_thread = threading.Thread(target=run_beat)
    beat_thread.daemon = True
    beat_thread.start()
    
    logger.info(
        "Starting Celery Worker",
        extra={
            "thread": "main",
            "loglevel": loglevel
        }
    )
    celery_app.worker_main(['worker', f'--loglevel={loglevel}'])