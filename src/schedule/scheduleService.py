import logging
import uuid
from src.model import scheduleTasks
from src.schedule.type import ScheduleTasksRequestDTO, ScheduleTasksResponseDTO


class ScheduleService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ScheduleService, cls).__new__(cls)
        return cls._instance

    def schedule(self, dto: ScheduleTasksRequestDTO) -> ScheduleTasksResponseDTO:
        logging.debug(dto)
        runId = uuid.uuid4()
        self.validateDTO(dto)
        scheduledTasks = scheduleTasks(dto.tasks, dto.projects, dto.bannedRanges)
        return ScheduleTasksResponseDTO(scheduledTasks, runId)
    
    def validateDTO(self, dto: ScheduleTasksRequestDTO):
        isValid = True
        isValid = len(dto.tasks) > 0
        # czas rozpoczęcia zadania nie może być większy niż czas zakończenia
        # zadania nie mogą na siebie nachodzić
        # czas rozpoczęcia projektu nie może być większy niż czas zakończenia
        # czas rozpoczęcia banned range nie może być większy niż czas zakończenia
        # banned ranges nie mogą na siebie nachodzić
        # priorytety między 1 a 4

        # czasy rozpoczęcia nie mogą być mniejsze od 0
        # czasy zakończenia nie mogą być większe niż 24
        # żadne id nie mogą się dublować
        # id projektów w taskach muszą istnieć w liście projektów
        if not isValid:
            raise Exception("DTO is not valid")
        