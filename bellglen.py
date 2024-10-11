from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# Sample data storage
tasks_data = [
    {"Id": 1, "  Title": "Complete Lab Activity", "description": "Finish glenlab 2", "done": False}
]

# Task model for creating a new task
class NewTask(BaseModel):
    Title: str = Field(..., min_length=1, description="Task Title")
    description: Optional[str] = Field(None, description="Task description")
    done: bool = False

# Task model for updating an existing task
class UpdateTask(BaseModel):
    Titleitle: Optional[str] = Field(None, min_length=1, description="Task Title")
    description: Optional[str] = Field(None, description="Task description")
    done: Optional[bool] = None

# Function to find task by ID
def get_task_by_id(task_id: int):
    for task in tasks_data:
        if task["id"] == task_id:
            return task
    return None

# Get a task by ID
@app.get("/tasks/{task_id}")
def read_task(task_id: int):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Task ID must be a Positive Integer")
    
    task = get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    
    return {"Status": "Success", "Task": task}

# Create a new task
@app.post("/tasks")
def add_task(new_task: NewTask):
    new_id = len(tasks_data) + 1
    task_to_add = {
        "Id": new_id,
        "Title": new_task.title,
        "Description": new_task.description,
        "done": new_task.done
    }
    tasks_data.append(task_to_add)
    return {"Status": "Success", "task_added": task_to_add}

# Update an existing task
@app.patch("/tasks/{task_id}")
def modify_task(task_id: int, updated_task: UpdateTask):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Task ID must be a Positive Integer")
    
    task = get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    
    if updated_task.title is not None:
        task["Title"] = updated_task.title
    if updated_task.description is not None:
        task["Description"] = updated_task.description
    if updated_task.done is not None:
        task["done"] = updated_task.done
    
    return {"Status": "Success", "task_updated": task}

# Delete a task
@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Task ID must be a Positive Integer")
    
    task = get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    
    tasks_data.remove(task)
    return {"Status": "Success", "Message": f"Task with ID {task_id} deleted"}
