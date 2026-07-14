from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
fake_todo_db = []
class TodoItem(BaseModel):
    id: int
    title: str
    is_completed: bool = False

@app.get("/todos")
async def get_all_todos():
    return{"Total_Tasks": len(fake_todo_db), "Tasks": fake_todo_db}

@app.post("/todos")
async def create_todo(new_task: TodoItem):
    task_dict = new_task.dict()
    fake_todo_db.append(task_dict)
    return{"Message": "Task successfully created!", "Tasks":task_dict}

@app.put("/todos/{task_id}")
async def update_todo(task_id: int, updated_task: TodoItem):
    for i in range(len(fake_todo_db)):
        if fake_todo_db[i]["id"] == task_id:
            fake_todo_db[i] = updated_task.dict()
            return{"Message": f"Task {task_id} updated!","Task": fake_todo_db[i]}
    return{"Error": "Task not found"}

@app.delete("/todos/{task_id}")
async def delete_todo(task_id: int):
    for i in range(len(fake_todo_db)):
        if fake_todo_db[i]["id"] == task_id:
            del fake_todo_db[i]
            return{"Message": f"Task{task_id} completey deleted!"}
    return{"Error": "Task Not Found"}
