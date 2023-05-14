from typing import List

import yaml
from fastapi import HTTPException

from conf import BUILDS_YAML, TASKS_YAML
from models import Build, Task


class TaskGraph:
    def __init__(self):
        self.tasks = {}
        self.edges = {}

    def add_task(self, task: Task):
        self.tasks[task.name] = task
        self.edges[task.name] = set()

        if len(task.dependencies) > 0:
            [self._add_dependency(
                task_name=task.name, dependency_name=dependency) \
                    for dependency in task.dependencies]

    def _add_dependency(self, task_name, dependency_name):
        self.edges[task_name].add(dependency_name)

    def get_task_sequence(self, task_names: List[str] | None = None):
        if not task_names:
            task_names = self.tasks.keys()
        visited = set()
        stack = []
        for task_name in task_names:
            self._dfs(task_name, visited, stack)
        return stack[::-1]

    def _dfs(self, task_name, visited, stack):
        if task_name not in self.edges.keys():
            raise HTTPException(
                status_code=400,
                detail=f'Has no task {task_name} in tasks.yaml')

        if task_name in visited:
            return
        visited.add(task_name)
        for dependency_name in self.edges[task_name]:
            self._dfs(dependency_name, visited, stack)
        stack.append(task_name)


def get_task_graph(tasks: List[Task]) -> TaskGraph:
    task_graph = TaskGraph()
    [task_graph.add_task(task=task) for task in tasks]
    return task_graph


async def get_builds_from_file() -> List[Build]:
    with open(BUILDS_YAML) as file:
        builds = [Build(**build) for build in yaml.safe_load(file).get('builds')]
    return builds


async def get_tasks_from_file() -> List[Task]:
    with open(TASKS_YAML) as file:
        tasks = [Task(**task) for task in yaml.safe_load(file).get('tasks')]
    return tasks
