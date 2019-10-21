from functools import partial
import io
import json
from fastapi import FastAPI
import os
import os.path
import subprocess
import pymysql
from pydantic import BaseModel
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


@app.post("/users")
def create_user(user: User):
    try:
        user_create(conn, user.user_name, user.email, user.city)
        conn.commit()
        return "User created"
    except:
        return "Unable to create user"

@app.get("/users")
def read_users():
    try:
        return user_list(conn)
    except:
        return "Unable to list users"

@app.put("/users")
def update_user(user_name: str, new_user_name: str, new_user_email: str, new_user_city: str):
    try:
        user_id = find_user(conn, user_name)
        if user_id:
            update_user_name(conn, user_id, new_user_name)
            update_user_email(conn, user_id, new_user_email)
            update_user_city(conn, user_id, new_user_city)
            conn.commit()
            return "User updated"
        else:
            return "No such user"
    except:
        return "Unable to update"

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





@app.post("/bird")
def create_bird(bird: Bird):
    try:
        bird_create(conn, bird.bird_name)
        conn.commit()
        return "Bird created"
    except:
        return "Unable to create bird"

@app.get("/bird")
def read_birds():
    try:
        return bird_list(conn)
    except:
        return "Unable to list birds"

@app.put("/bird")
def bird_update(bird_name: str, new_bird_name: str):
    try:
        bird_id = find_bird(conn, bird_name)
        if bird_id:
            update_bird(conn, bird_id, new_bird_name)
            conn.commit()
            return "Bird name updated"
        else:
            return "No such bird"
    except:
        return "Unable to update bird"

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

@app.delete("/users/post")
def post_delete(user_name:str, title: str):
    try:
        user_id = find_user(conn, user_name)
        if user_id:
            post_id = find_post(conn, user_id, title)
            if post_id:
                delete_post(conn, post)
                conn.commit()
                return "Post deleted"
            else:
                return "No such post"
        else:
            return "No such user"
    except:
        return "Unable to remove post"