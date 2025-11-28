from dataclasses import dataclass
from typing import Optional


@dataclass
class BaseTaskContext:
    network: str
    processing_date: Optional[str] = None
    window_days: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    batch_size: Optional[int] = None


@dataclass
class BaseTaskResult:
    network: str
    status: str
    processing_date: Optional[str] = None
    window_days: Optional[int] = None