from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TodoItem(BaseModel):
    title: str
    is_completed: bool = False

@app.get("/todos")
async def get_all_todos(db: Session = Depends(get_db)):
    # Replaces the ghost list! Grabs every single row from the Postgres table.
    todos = db.query(models.Todo).all()
    return{"Total_Tasks": len(todos), "Tasks": todos}

@app.post("/todos")
async def create_todo(new_task: TodoItem, db: Session = Depends(get_db)):
    # 1. Convert the Pydantic data into the SQLAlchemy blueprint
    db_task = models.Todo(title = new_task.title, is_completed = new_task.is_completed)

    # 2. Put it in the waiting room
    db.add(db_task)
    # 3. Push it permanently to the Postgres database
    db.commit()
    # 4. Refresh to grab the auto-generated ID from Postgres
    db.refresh(db_task)

    return{"Message": "Task successfully createdin Postgres!", "Tasks":db_task}

@app.put("/todos/{task_id}")
async def update_todo(task_id: int, updated_task: TodoItem, db: Session = Depends(get_db)):
    # 1. Search Postgres for the exact ID (Replaces the 'for' loop)
    db_task = db.query(models.Todo).filter(models.Todo.id == task_id).first()
    # 2. If it doesn't exist, return error
    if db_task is None:
        return{"Error": "Task Not Found"}
    # 3. Overwrite the data
    db_task.title = updated_task.title
    db_task.is_completed = updated_task.is_completed
    # 4. Save the changes to the database
    db.commit()
    db.refresh(db_task)
    

@app.delete("/todos/{task_id}")
async def delete_todo(task_id: int, db: Session = Depends(get_db)):
    # 1. Search Postgres for the exact ID
    db_task = db.query(models.Todo).filter(models.Todo.id == task_id).first()
    # 2. Destroy the row in the database
    db.delete(db_task)
    db.commit()