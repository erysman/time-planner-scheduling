from typing import List, Optional, Tuple
from src.model import scheduleTasks, Task, Project, BannedRange
import unittest

from src.model.type import ScheduledTask
from src.schedule.type import ScheduleTasksRequestDTO, ScheduleTasksRequestDTOSchema, ScheduleTasksResponseDTO, ScheduleTasksResponseDTOSchema


class TestCalculations(unittest.TestCase):
    # @classmethod
    # def setUpClass(self):
    #     self.a = 10
    def assertAllTasksAreScheduled(self, tasksCount, resultTasks):
        numberOfScheduledTasks = sum(
            1 for task in resultTasks if task.startTime != None
        )
        self.assertEqual(
            numberOfScheduledTasks, tasksCount, "Not all tasks were scheduled"
        )
        print("tasksCount", tasksCount)

    def test_should_skip_task_with_lowest_priority(self):
        task1 = Task("A1", "", "A", 4, None, 8.5)
        task2 = Task("B1", "", "B", 3, None, 7.5)
        task3 = Task("B2", "", "B", 2, None, 8)
        task4 = Task("C1", "", "C", 1, None, 8)
        tasks = [task1, task2, task3, task4]

        projectA = Project("A", "", 0, 24)
        projectB = Project("B", "", 0, 24)
        projectC = Project("C", "", 0, 24)
        projects = [projectA, projectB, projectC]

        resultTasks = scheduleTasks(tasks, projects, debug=True)
        self.assertAllTasksAreScheduled(3, resultTasks)
        assertTaskStartTime(self, ("A1", 0), resultTasks)
        assertTaskStartTime(self, ("B1", 8.5), resultTasks)
        assertTaskStartTime(self, ("B2", 16.0), resultTasks)

    def test_should_schedule_all_tasks_even_when_priorities_are_opposite1(self):
        tasks = [
            Task("A1", "", "A1", 1, None, 1),
            Task("A2", "", "A2", 2, None, 1),
            Task("A3", "", "A3", 3, None, 1),
            Task("A4", "", "A4", 4, None, 1),
        ]
        projects = [
            Project("A1", "", 0, 1),
            Project("A2", "", 1, 2),
            Project("A3", "", 2, 3),
            Project("A4", "", 3, 4),
        ]

        resultTasks = scheduleTasks(tasks, projects, debug=True)
        self.assertAllTasksAreScheduled(4, resultTasks)
        assertTaskStartTime(self, ("A1", 0), resultTasks)
        assertTaskStartTime(self, ("A2", 1.0), resultTasks)
        assertTaskStartTime(self, ("A3", 2.0), resultTasks)
        assertTaskStartTime(self, ("A4", 3.0), resultTasks)

    def test_should_schedule_all_tasks_even_when_priorities_are_opposite2(self):
        tasks = [
            Task("A1", "", "A1", 1, None, 1),
            Task("A2", "", "A2", 1, None, 1),
            Task("A3", "", "A3", 1, None, 1),
            Task("A4", "", "A4", 1, None, 1),
            Task("B1", "", "B1", 1, None, 1),
            Task("B2", "", "B2", 2, None, 1),
            Task("B3", "", "B3", 3, None, 1),
            Task("B4", "", "B4", 4, None, 1),
        ]
        projects = [
            Project("A1", "", 0, 1),
            Project("A2", "", 1, 2),
            Project("A3", "", 2, 3),
            Project("A4", "", 3, 4),
            Project("B1", "", 4, 5),
            Project("B2", "", 5, 6),
            Project("B3", "", 6, 7),
            Project("B4", "", 7, 8),
        ]

        resultTasks = scheduleTasks(tasks, projects, debug=True)
        assertTaskStartTime(self, ("A1", 0), resultTasks)
        assertTaskStartTime(self, ("A2", 1.0), resultTasks)
        assertTaskStartTime(self, ("A3", 2.0), resultTasks)
        assertTaskStartTime(self, ("A4", 3.0), resultTasks)
        assertTaskStartTime(self, ("B1", 4.0), resultTasks)
        assertTaskStartTime(self, ("B2", 5.0), resultTasks)
        assertTaskStartTime(self, ("B3", 6.0), resultTasks)
        assertTaskStartTime(self, ("B4", 7.0), resultTasks)

    def test_should_schedule_all_tasks_even_when_priorities_are_opposite3(self):
        tasks = [
            Task("A1", "", "A1", 1, None, 1),
            Task("A2", "", "A2", 1, None, 1),
            Task("A3", "", "A3", 1, None, 1),
            Task("A4", "", "A4", 1, None, 1),
            Task("B1", "", "B1", 1, None, 1),
            Task("B2", "", "B2", 1, None, 1),
            Task("B3", "", "B3", 1, None, 1),
            Task("B4", "", "B4", 1, None, 1),
            Task("C1", "", "C1", 1, None, 1),
            Task("C2", "", "C2", 1, None, 1),
            Task("C3", "", "C3", 1, None, 1),
            Task("C4", "", "C4", 1, None, 1),
            Task("D1", "", "D1", 1, None, 1),
            Task("D2", "", "D2", 1, None, 1),
            Task("D3", "", "D3", 1, None, 1),
            Task("D4", "", "D4", 1, None, 1),
            Task("E1", "", "E1", 1, None, 1),
            Task("E2", "", "E2", 2, None, 1),
            Task("E3", "", "E3", 3, None, 1),
            Task("E4", "", "E4", 4, None, 1),
        ]
        projects = [
            Project("A1", "", 0, 1),
            Project("A2", "", 1, 2),
            Project("A3", "", 2, 3),
            Project("A4", "", 3, 4),
            Project("B1", "", 4, 5),
            Project("B2", "", 5, 6),
            Project("B3", "", 6, 7),
            Project("B4", "", 7, 8),
            Project("C1", "", 8, 9),
            Project("C2", "", 9, 10),
            Project("C3", "", 10, 11),
            Project("C4", "", 11, 12),
            Project("D1", "", 12, 13),
            Project("D2", "", 13, 14),
            Project("D3", "", 14, 15),
            Project("D4", "", 15, 16),
            Project("E1", "", 16, 17),
            Project("E2", "", 17, 18),
            Project("E3", "", 18, 19),
            Project("E4", "", 19, 20),
        ]

        resultTasks = scheduleTasks(tasks, projects, debug=True)
        assertTaskStartTime(self, ("A1", 0), resultTasks)
        assertTaskStartTime(self, ("A2", 1.0), resultTasks)
        assertTaskStartTime(self, ("A3", 2.0), resultTasks)
        assertTaskStartTime(self, ("A4", 3.0), resultTasks)
        assertTaskStartTime(self, ("B1", 4.0), resultTasks)
        assertTaskStartTime(self, ("B2", 5.0), resultTasks)
        assertTaskStartTime(self, ("B3", 6.0), resultTasks)
        assertTaskStartTime(self, ("B4", 7.0), resultTasks)
        assertTaskStartTime(self, ("C1", 8.0), resultTasks)
        assertTaskStartTime(self, ("C2", 9.0), resultTasks)
        assertTaskStartTime(self, ("C3", 10.0), resultTasks)
        assertTaskStartTime(self, ("C4", 11.0), resultTasks)
        assertTaskStartTime(self, ("D1", 12.0), resultTasks)
        assertTaskStartTime(self, ("D2", 13.0), resultTasks)
        assertTaskStartTime(self, ("D3", 14.0), resultTasks)
        assertTaskStartTime(self, ("D4", 15.0), resultTasks)
        assertTaskStartTime(self, ("E1", 16.0), resultTasks)
        assertTaskStartTime(self, ("E2", 17.0), resultTasks)
        assertTaskStartTime(self, ("E3", 18.0), resultTasks)
        assertTaskStartTime(self, ("E4", 19.0), resultTasks)

    def test_should_prioritize_task_with_higher_priority_then_two_tasks_of_lower_priority(
        self,
    ):
        taskA1 = Task("A1", "", "A", 4, None, 8)
        taskA2 = Task("A2", "", "A", 3, None, 8)
        taskA3 = Task("A3", "", "A", 3, None, 8)
        tasks = [taskA1, taskA2, taskA3]

        projectA = Project("A", "", 0, 8)
        projects = [projectA]

        resultTasks = scheduleTasks(tasks, projects, debug=True)
        self.assertCountEqual([ScheduledTask("A1", 0)], resultTasks)

    def test_should_not_modify_initialized_start_time(
        self,
    ):
        tasks = [Task("A1", "", "A", 1, 0.0, 4), Task("A2", "", "A", 4, 10.0, 4)]
        projects = [Project("A", "", 0, 1)]

        resultTasks = scheduleTasks(tasks, projects, debug=True)
        assertTaskStartTime(self, ("A1", 0.0), resultTasks)
        assertTaskStartTime(self, ("A2", 10.0), resultTasks)

    def test_should_schedule_tasks_as_early_as_possible0(
        self,
    ):
        tasks = [
            Task("A1", "", "A", 4, None, 4.0),
            Task("A2", "", "A", 4, None, 4.0),
            Task("A3", "", "A", 4, None, 4.0),
        ]
        projects = [Project("A", "", 0, 24)]

        resultTasks = scheduleTasks(tasks, projects, debug=True)
        numberOfEarlyTasks = sum(1 for task in resultTasks if task.startTime <= 8.0)
        self.assertEqual(
            numberOfEarlyTasks,
            len(tasks),
            "Not all tasks are scheduled as early as possible",
        )

    def test_all_tasks_should_be_scheduled0(
        self,
    ):
        taskDuration = 0.25
        hoursRange = 5
        tasksCount = int(hoursRange / taskDuration)
        tasks = [
            Task(f"A{i}", "", "A", 1, None, taskDuration) for i in range(0, tasksCount)
        ]
        projects = [Project("A", "", 24 - hoursRange, 24)]

        resultTasks = scheduleTasks(tasks, projects, debug=True)
        self.assertAllTasksAreScheduled(tasksCount, resultTasks)

    def test_should_schedule_high_priority_tasks_earlier_then_short_tasks0(
        self,
    ):
        smallTaskDuration = 0.25
        hoursRange = 5
        smallTasksCount = int(hoursRange / smallTaskDuration)
        tasks = [
            Task(f"A{i}", "", "A", 1, None, smallTaskDuration)
            for i in range(0, smallTasksCount)
        ]
        tasks.append(Task("B1", "", "B", 2, None, 24 - hoursRange))
        projects = [Project("A", "", 0, 24), Project("B", "", 0, 24)]

        resultTasks = scheduleTasks(tasks, projects, debug=True)
        assertTaskStartTime(self, ("B1", 0.0), resultTasks)
        self.assertAllTasksAreScheduled(smallTasksCount + 1, resultTasks)

    def test_should_schedule_tasks_out_of_banned_ranges0(
        self,
    ):
        tasks = [Task("A1", "", "A", 4, None, 6), Task("A2", "", "A", 3, None, 6)]
        projects = [Project("A", "", 0, 24)]
        bannedRanges = [BannedRange("R1", 0.0, 8.0), BannedRange("R2", 16.0, 24.0)]

        resultTasks = scheduleTasks(tasks, projects, bannedRanges, debug=True)
        self.assertCountEqual([ScheduledTask("A1", 8.0)], resultTasks)

    def test_should_schedule_tasks_out_of_banned_ranges1(
        self,
    ):
        tasks2 = [Task(f"A{i}", "", "A", i + 1, None, 3) for i in range(1, 4)]
        tasks1 = [Task(f"A{i}", "", "A", 1, None, 3) for i in range(4, 7)]
        tasks = tasks2 + tasks1
        projects = [Project("A", "", 0, 24)]
        bannedRanges = [
            BannedRange("R1", 0.0, 3.0),
            BannedRange("R2", 6.0, 9.0),
            BannedRange("R2", 12.0, 15.0),
            BannedRange("R2", 18.0, 24.0),
        ]

        resultTasks = scheduleTasks(tasks, projects, bannedRanges, debug=True)
        self.assertAllTasksAreScheduled(3, resultTasks)
        assertTaskStartTime(self, ("A3", 3.0), resultTasks)
        assertTaskStartTime(self, ("A2", 9.0), resultTasks)
        assertTaskStartTime(self, ("A1", 15.0), resultTasks)

    def test_complex_case0(
        self,
    ):
        # 4 projects
        # 2 banned ranges
        # >10 tasks with different priorities
        defaultTasks = [
            Task(f"A1", "Odkurzyć", "A", 1, None, 0.5),
            Task(f"A2", "Duże zakupy", "A", 2, None, 1),
            Task(f"A3", "Wizyta internista", "A", 4, 12.0, 1),
            Task(f"A4", "Przygotować obiad na kolejne dni", "A", 2, None, 1),
        ]
        morningTasks = [
            Task(f"D1", "Medytacja", "D", 3, None, 0.25),
            Task(f"D2", "Spacer", "D", 2, None, 0.5),
        ]
        workTasks = [
            Task(f"B1", "Naprawić buga w feature A", "B", 4, None, 3),
            Task(f"B2", "Testy jednostkowe do feature A", "B", 3, None, 3),
            Task(f"B3", "Przeanalizować wymagania do feature X", "B", 1, None, 2),
        ]
        hobbyTasks = [
            Task(f"C1", "Bieganie", "C", 3, None, 1),
            Task(f"C2", "Czytanie", "C", 2, None, 0.5),
            Task(f"C3", "Pianino", "C", 1, None, 1),
        ]
        tasks = workTasks + hobbyTasks + defaultTasks + morningTasks
        projects = [
            Project("D", "morning", 8, 10),
            Project("A", "default", 0, 24),
            Project("B", "work", 9, 17),
            Project("C", "hobby", 17, 22),
        ]
        bannedRanges = [BannedRange("R1", 0.0, 8.0), BannedRange("R2", 22.0, 24.0)]
        # print(ScheduleTasksRequestDTOSchema().dumps(ScheduleTasksRequestDTO(tasks, projects, bannedRanges)))
        
        resultTasks = scheduleTasks(tasks, projects, bannedRanges, debug=True)
        self.assertAllTasksAreScheduled(len(tasks)-1, resultTasks)
        self.assertNotIn(ScheduledTask("B3", None), resultTasks)
        self.assertIn(ScheduledTask("B1", 9.0), resultTasks)
        self.assertIn(ScheduledTask("B2", 13.0), resultTasks)
        
        # print(ScheduleTasksResponseDTOSchema().dumps(ScheduleTasksResponseDTO(resultTasks, "1")))


def assertTaskStartTime(self, expect: Tuple[str, float], tasks: List[Task]):
    id, startTime = expect
    task = findTask(tasks, id)
    self.assertEqual(
        (task.id, task.startTime), (id, startTime), "Task id or time is wrong."
    )


def findTask(tasks: List[Task], id: str) -> Task:
    match = [task for task in tasks if task.id == id]
    if match:
        return match[0]
    else:
        raise LookupError(f"Task id {id} not found")


if __name__ == "__main__":
    unittest.main()
