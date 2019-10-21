from fastapi import FastAPI
from functools import partial
from pydantic import BaseModel
import pymysql
import re
from dbird import *

app = FastAPI()

def run_db_query(conn, query, args=None):
    with conn.cursor() as cursor:
        print('Executando query:')
        cursor.execute(query, args)
        for result in cursor:
            print(result)

conn = pymysql.connect(
    host='localhost',
    user='megadados',
    password='megadados2019',
    database='dbird'
    )

db = partial(run_db_query, conn)

class User(BaseModel):
    user_name: str
    email: str
    city: str

class Bird(BaseModel):
    bird_name: str

class Post(BaseModel):
    title: str
    content: str
    url: str


@app.get("/users")
def read_users():
    try:
        return user_list(conn)
    except:
        return "Unable to list users"

@app.post("/users")
def create_user(user: User):
    try:
        user_create(conn, user.user_name, user.email, user.city)
        conn.commit()
        return "User created"
    except:
        return "Unable to create user"

# @app.put("/users")
# def update user(user: User):


@app.delete("/users")
def user_delete(user: User):
    try:
        user_id = find_user(conn, user.user_name)
        if user_id:
            delete_user(conn, user_id)
            conn.commit()
            return "User deleted"
        else:
            return "No such user"
    except:
        return "Unable to remove user"


@app.get("/bird")
def read_birds():
    try:
        return bird_list(conn)
    except:
        return "Unable to list birds"

@app.post("/bird")
def create_bird(bird: Bird):
    try:
        bird_create(conn, bird.bird_name)
        conn.commit()
        return "Bird created"
    except:
        return "Unable to create bird"

# @app.put("/bird")
# def bird_update(bird_name: str, new_bird_name: str):
#     try:
#         bird_id = find_bird(conn, bird_name)
#         if bird_id:
#             update_bird(conn, bird_id, new_bird_name)
#             return "Bird name updated"
#         else:
#             return "No such bird"
#     except:
#         return "Unable to update bird"

@app.delete("/bird")
def bird_delete(bird: Bird):
    try:
        bird_id = find_bird(conn, bird.bird_name)
        if bird_id:
            delete_bird(conn, bird_id)
            conn.commit()
            return "Bird deleted"
        else:
            return "No such bird"
    except:
        return "Unable to remove bird"

@app.get("/users/post")
def read_user_posts(user: User):
    try:
        user_id = find_user(conn, user.user_name)
        if user_id:
            return user_post_list(conn, user_id)
        else:
            return "No such user"
    except:
        return "Unable to list posts"

@app.post("/users/post")
def create_post(user_name: str, title: str, content: str, url: str):
    try:
        user_id = find_user(conn, user_name)
        if user_id:
            post_create(conn, user_id, title, content, url)
            conn.commit()
            return "Post created"
        else:
            return "No such user"
    except:
        return "Unable to create post"

@app.delete("/users/post")
def post_delete(bird: Bird):
    try:
        bird_id = find_bird(conn, bird.bird_name)
        if bird_id:
            delete_bird(conn, bird_id)
            conn.commit()
            return "Bird deleted"
        else:
            return "No such bird"
    except:
        return "Unable to remove bird"