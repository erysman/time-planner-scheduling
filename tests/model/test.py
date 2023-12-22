from src.model import scheduleTasks, Task, Project
import unittest


class TestCalculations(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.a = 10

    def test_should_skip_task_with_lowest_priority(self):
        task1 = Task("A1", "", "A", 4, None, 8.5)
        task2 = Task("B1", "", "B", 3, None, 7.5)
        task3 = Task("B2", "", "B", 2, None, 8)
        task4 = Task("C1", "", "C", 1, None, 8)
        tasks = [task1, task2, task3, task4]

        projectA = Project("A", "", 0, 24)
        projectB = Project("B", "", 0, 24)
        projectC = Project("C", "", 8, 24)
        projects = [projectA, projectB, projectC]

        resultTasks = scheduleTasks(tasks, projects)
        self.assertEqual((resultTasks[0].id, resultTasks[0].startTime), ("A1", 0), "Task id or time is wrong.")
        self.assertEqual((resultTasks[1].id, resultTasks[1].startTime), ("B1", 8.5), "Task id or time is wrong.")
        self.assertEqual((resultTasks[2].id, resultTasks[2].startTime), ("B2", 16.0), "Task id or time is wrong.")
        self.assertEqual((resultTasks[3].id, resultTasks[3].startTime), ("C1", None), "Task id or time is wrong.")


if __name__ == "__main__":
    unittest.main()
