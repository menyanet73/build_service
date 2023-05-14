import asyncio
from typing import Dict, List

from fastapi import FastAPI, HTTPException, status

from models import Build, GetTasksRequest
from utils import get_builds_from_file, get_task_graph, get_tasks_from_file

app = FastAPI()


builds_from_file = []
tasks_from_file = []
task_graph = None


@app.on_event("startup")
async def startup_event():
    global builds_from_file, tasks_from_file, task_graph
    builds_from_file, tasks_from_file = await asyncio.gather(
        get_builds_from_file(), get_tasks_from_file())
    task_graph = get_task_graph(tasks=tasks_from_file)


@app.post("/get_tasks/")
async def get_tasks(request_data: Dict[str, str] | None = None):
    if request_data is None or request_data == {}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='Request body must contain "build" field')

    serializer = GetTasksRequest(**request_data)
    build_name = serializer.build


    build_list: List[Build]= [build for build in builds_from_file \
        if build.name == build_name]
    if len(build_list) < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Build {build_name} not found')

    build = build_list[0]
    if len(build.tasks) == 0:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail='Build has no tasks')

    sorted_tasks = task_graph.get_task_sequence(task_names=build.tasks)

    return sorted_tasks
