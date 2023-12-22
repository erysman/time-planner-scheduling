from typing import Literal, Optional


class Task:
    def __init__(
        self,
        id: str,
        name: str,
        projectId: str,
        priority: Literal[1, 2, 3, 4],
        startTime: Optional[float],
        duration: int,
    ):
        self.id = id
        self.name = name
        self.projectId = projectId
        self.priority = priority
        self.startTime = startTime
        self.duration = duration


class Project:
    def __init__(self, id: str, name: str, timeRangeStart: float, timeRangeEnd: float):
        self.id = id
        self.name = name
        self.timeRangeStart = timeRangeStart
        self.timeRangeEnd = timeRangeEnd
