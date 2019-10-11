import pymysql

connection = pymysql.connect(
    host = 'localhost',
    user = 'megadados',
    password = 'megadados2019',
    database = 'dbird'
)
##################################################### CRUD USER
def user_create(conn, user_name, email, city):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO users (user_name, email, city) VALUES (%s,%s,%s)', (user_name, email, city))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Unable to create user: {user_name}')

def find_user(conn, user_name):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_user FROM users WHERE user_name = %s', (user_name))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def user_list(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_user, user_name, email, city FROM users')
        res = cursor.fetchall()
        perigos = tuple(x[0] for x in res)
        return perigos

def update_user_name(conn, id, new_user_name):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE users SET user_name=%s WHERE id_user=%s', (new_user_name, id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Unable to update user name to {new_user_name}')

def update_user_email(conn, id, new_email):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE users SET email=%s WHERE id_user=%s', (new_email, id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Unable to update user email to {new_email}')

def update_user_city(conn, id, new_city):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE users SET city=%s WHERE id_user=%s', (new_city, id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Unable to update user city to {new_city}')

def update_user_active(conn, id, value):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE users SET is_activeu=%s WHERE id_user=%s', (value, id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Unable to update user active bool to {value}')

def delete_user(conn, id):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE users SET is_activeu=0 WHERE id_user=%s', (id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Unable to delete user {id}')

##################################################### CRUD BIRD
def bird_create(conn, bird_name):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO bird (bird_name) VALUES (%s)', (bird_name))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Unable to create bird: {bird_name}')

def find_bird(conn, bird_name):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_bird FROM bird WHERE bird_name = %s', (bird_name))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def update_bird(conn, id, new_bird_name):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE bird SET bird_name=%s WHERE id_bird=%s', (new_bird_name, id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Unable to update bird name to {new_bird_name}')

def delete_bird(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM bird WHERE id_bird=%s', (id))

##################################################### CRUD POST
def post_create(conn, id_user, title, content = None, url = None):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO post (title, content, url, id_user) VALUES (%s,%s,%s,%s)', (title, content, url, id_user))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Unable to create post')

def find_post_title(conn, title):
    with conn.cursor() as cursor:
        cursor.execute('SELECT content, url, id_user FROM post WHERE title = %s', (title))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def user_post_list(conn, id_user):
    with conn.cursor() as cursor:
        cursor.execute('SELECT title, content, url FROM post WHERE id_user = %s', (id_user))
        res = cursor.fetchall()
        perigos = tuple(x[0] for x in res)
        return perigos
