from fastapi import FastAPI, status
from fastapi import HTTPException
from database import Base, engine
import schemas as schemas
import models
from sqlalchemy.orm import Session



Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
def root():
    return "todo"

@app.post('/todo', status_code = status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDo):
    session = Session(bind=engine,expire_on_commit=False)

    tododb = models.ToDo(task=todo.task)

    session.add(tododb)
    session.commit()

    id = tododb.id

    session.close()

    return f"created todo item with id {id}"

@app.get('/todo/{id}')
def read_todo(id:int):
    session = Session(bind=engine,expire_on_commit=False)
    todo = session.query(models.ToDo).get(id)

    session.close()
    if not todo:
        raise HTTPException(status_code = 401, detail=f"todo item with id {id} not found")
    return todo

@app.delete('/todo/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_todo(id:int):
    session = Session(bind=engine,expire_on_commit=False)

    todo = session.query(models.ToDo).get(id)

    if todo:
        session.delete(todo)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code = 404, detail = f"todo item with id {id} not found")
    return None

@app.put('/todo/{id}')
def update_todo(id:int, task:str):
    session = Session(bind=engine, expire_on_commit=False)

    todo = session.query(models.ToDo).get(id)

    if todo:
        todo.task = task
        session.commit()

    session.close()

    if not todo:
        return HTTPException(status_code = 404, detail = f"todo item with this id {id} not found")
    
    return todo

@app.get('/todo')
def read_list():
    session = Session(bind=engine, expire_on_commit=False)

    todo_list = session.query(models.ToDo).all()

    session.close()

    return todo_list