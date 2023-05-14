from typing import List
from pydantic import BaseModel



class Task(BaseModel):
    name: str
    dependencies: List[str]


class Build(BaseModel):
    name: str
    tasks: List[str]


class GetTasksRequest(BaseModel):
    build: str
