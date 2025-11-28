from abc import ABC, abstractmethod
from typing import Any, Dict

from celery import Task

from chainswarm_core.observability import log_errors


class BaseTask(Task, ABC):

    @log_errors
    @abstractmethod
    def execute_task(self, context) -> Dict[str, Any]:
        pass

    @log_errors
    def run(self, context) -> Dict[str, Any]:
        return self.execute_task(context)