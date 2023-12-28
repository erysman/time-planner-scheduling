from typing import Literal, Optional

class ScheduledTask:
    def __init__(self, id: str, startTime: float):
        self.id = id
        self.startTime = startTime

    def __str__(self):
        return f"ScheduledTask(id={self.id}, startTime={self.startTime})"

    def __eq__(self, other):
        if not isinstance(other, ScheduledTask):
            return False
        return self.id == other.id and self.startTime == other.startTime

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

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        return (
            self.id == other.id and
            self.name == other.name and
            self.projectId == other.projectId and
            self.priority == other.priority and
            self.startTime == other.startTime and
            self.duration == other.duration
        )

class TimeRange:
    def __init__(self, timeRangeStart: float, timeRangeEnd: float):
        self.timeRangeStart = timeRangeStart
        self.timeRangeEnd = timeRangeEnd

    def __str__(self):
        return f"timeRangeStart={self.timeRangeStart}, timeRangeEnd={self.timeRangeEnd}"

    def __eq__(self, other):
        if not isinstance(other, TimeRange):
            return False
        return (
            self.timeRangeStart == other.timeRangeStart and
            self.timeRangeEnd == other.timeRangeEnd
        )

class Project(TimeRange):
    def __init__(self, id: str, name: str, timeRangeStart: float, timeRangeEnd: float):
        super().__init__(timeRangeStart, timeRangeEnd)
        self.id = id
        self.name = name

    def __str__(self):
        return (
            f"Project(id={self.id}, name={self.name}, "
            f"{super().__str__()})"
        )

    def __eq__(self, other):
        if not isinstance(other, Project):
            return False
        return (
            self.id == other.id and
            self.name == other.name and
            super().__eq__(other)  # Check equality of TimeRange attributes
        )

class BannedRange(TimeRange):
    def __init__(self, id: str, timeRangeStart: float, timeRangeEnd: float):
        super().__init__(timeRangeStart, timeRangeEnd)
        self.id = id

    def __str__(self):
        return f"BannedRange(id={self.id}, {super().__str__()})"

    def __eq__(self, other):
        if not isinstance(other, BannedRange):
            return False
        return (
            self.id == other.id and
            super().__eq__(other)  # Check equality of TimeRange attributes
        )
