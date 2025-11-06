from abc import ABC, abstractmethod
from typing import Optional
from src.se_course_scheduler import CourseScheduler


class BasePage(ABC):
    """Base class for all page classes"""

    def __init__(self, scheduler: Optional[CourseScheduler] = None):
        """Initialize the page with optional scheduler"""
        self.scheduler = scheduler

    @abstractmethod
    def render(self):
        """Render the page content"""
        raise NotImplementedError
