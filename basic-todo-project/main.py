from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

TODOS = []


class TodoSchema(BaseModel):
    id: int
    title: str
    is_important: Optional[bool] = False

    @classmethod
    def get_todos(cls):
        return TODOS

    @classmethod
    def get_todo_by_id(cls, id):
        todo = next(filter(lambda x: x.id == id, TODOS), None)
        if todo:
            return todo
        else:
            return {'message': 'Todo not found'}

    @classmethod
    def add_todo(cls, todo):  # cls is the class TodoSchema itself. Similar to self in a class method
        old_todo = next(filter(lambda x: x.id == todo.id, TODOS), None)  # next returns the first item in the iterable. If no item is found, it returns None
        if old_todo:
            return {'message': 'Todo already exists'}
        else:
            TODOS.append(todo)
            return {'message': 'Todo added successfully'}

    @classmethod
    def delete_todo_by_id(cls, id):
        todo = cls.get_todo_by_id(id)
        if isinstance(todo, dict):
            return todo
        TODOS.remove(todo)
        return {'message': 'Todo deleted successfully'}

    @classmethod
    def update_todo_by_id(cls, id, todo):
        new_todo = cls.get_todo_by_id(id)
        if isinstance(new_todo, dict):
            return new_todo
        new_todo.title = todo.title
        new_todo.is_important = todo.is_important
        return {'message': 'Todo updated successfully', 'todo': new_todo}


@app.get("/todos")
async def get_todos():
    return TodoSchema.get_todos()


@app.get("/todos/{id}")
async def get_todo_by_id(id: int):
    return TodoSchema.get_todo_by_id(id)


@app.post("/todos")
async def add_todo(todo: TodoSchema):
    return TodoSchema.add_todo(todo)


@app.delete("/todos/{id}")
async def delete_todo_by_id(id: int):
    return TodoSchema.delete_todo_by_id(id)


@app.put("/todos/{id}")
async def update_todo_by_id(id: int, todo: TodoSchema):
    return TodoSchema.update_todo_by_id(id, todo)
