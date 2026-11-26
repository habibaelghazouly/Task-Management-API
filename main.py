from fastapi import FastAPI , HTTPException
from dataclasses import asdict

from models import Task
from schemas import TaskCreate, TaskUpdate, TaskResponse

dataset: dict[int, Task] = {}
dataset = {
    1: Task(
        task_id=1,
        title="Study FastAPI",
        priority="high",
        description="Complete assignment"
    ),

    2: Task(
        task_id=2,
        title="Study SQL",
        priority="medium",
        description="No description"
    )
}


app = FastAPI() 

@app.get("/")
def root():
    return {"message":" Welcome to the Task Management API!"}


@app.post("/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate):

    task_data = task.model_dump()

    task_id = max(dataset.keys(), default=0) + 1
    new_task = Task(task_id=task_id, **task_data)

    dataset[task_id] = new_task

    return TaskResponse(**asdict(new_task))


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks():

   return [
        TaskResponse(**asdict(task))
        for task in dataset.values()
    ]


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    if task_id not in dataset:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    del dataset[task_id]

    return {"message": "Task deleted successfully"}


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, update: TaskUpdate):

    if task_id not in dataset:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    update_data = update.model_dump(exclude_unset=True)
    
    existing_task = dataset[task_id]
    existing_data = asdict(existing_task)
    existing_data.update(update_data)

    new_task = Task(**existing_data)
    dataset[task_id] = new_task

    return TaskResponse(**asdict(new_task))