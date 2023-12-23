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

    def __str__(self):
        return (
            f"Task(id={self.id}, name={self.name}, projectId={self.projectId}, "
            f"priority={self.priority}, startTime={self.startTime}, duration={self.duration})"
        )

class TimeRange:
    def __init__(self, timeRangeStart: float, timeRangeEnd: float):
        self.timeRangeStart = timeRangeStart
        self.timeRangeEnd = timeRangeEnd

    def __str__(self):
        return f"timeRangeStart={self.timeRangeStart}, timeRangeEnd={self.timeRangeEnd}"

    
class Project:
    def __init__(self, id: str, name: str, timeRangeStart: float, timeRangeEnd: float):
        self.id = id
        self.name = name
        self.timeRangeStart = timeRangeStart
        self.timeRangeEnd = timeRangeEnd

    def __str__(self):
        return (
            f"Project(id={self.id}, name={self.name}, "
            f"timeRangeStart={self.timeRangeStart}, timeRangeEnd={self.timeRangeEnd})"
        )


class BannedRange(TimeRange):
    def __init__(self, id: str, timeRangeStart: float, timeRangeEnd: float):
        super().__init__(timeRangeStart, timeRangeEnd)
        self.id = id

    def __str__(self):
        return f"BannedRange(id={self.id}, {super().__str__()})"

