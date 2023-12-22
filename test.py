from model.schedule import scheduleTasks
from model.type import Project, Task


task1 = Task("A1", "", "A", 4, None, 8.5)
task2 = Task("B1", "", "B", 3, None, 7.5)
task3 = Task("B2", "", "B", 2, None, 8)
task4 = Task("C1", "", "C", 1, None, 8)
tasks = [task1, task2, task3, task4]

projectA = Project("A", "", 0, 24)
projectB = Project("B", "", 0, 24)
projectC = Project("C", "", 8, 24)
projects = [projectA, projectB, projectC]

scheduleTasks(tasks, projects)