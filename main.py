from dotenv import load_dotenv
import os

load_dotenv(r"C:\Users\Zzz\PycharmProjects\hello\.env")
database_name = os.getenv("DATABASE_NAME")
app_name = os.getenv("APP_NAME")

from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

def init_db():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

class User(BaseModel):
    name: str
    age: int

@app.post("/users")
def create_user(user: User):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (user.name, user.age))
    conn.commit()
    conn.close()
    return {"message": f"Пользователь {user.name} создан!"}

@app.get("/users")
def get_users():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

@app.delete("/users/{id}")
def delete_user(id: int):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": f"Пользователь {id} удалён!"}

@app.put ("/users/{id}")
def update_user(id: int, user: User):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ? WHERE id = ?", (user.name, id))
    conn.commit()
    conn.close()
    return {"message": f"Пользователь {id} обновлён!"}

