import pymysql
import re

##################################################### CRUD USER
def user_create(conn, user_name, email, city):  #create new user
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO users (user_name, email, city) VALUES (%s,%s,%s)', (user_name, email, city))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Unable to create user: {user_name}')

def find_user(conn, user_name):  #retrieve user's id using it's user name
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_user FROM users WHERE user_name = %s', (user_name))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def user_list(conn):  #list all users 
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_user, user_name, email, city FROM users WHERE is_activeu = 1')
        res = cursor.fetchall()
        users = tuple(x[0] for x in res)
        return users

def update_user_name(conn, id, new_user_name):  #update user info 
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE users SET user_name=%s WHERE id_user=%s', (new_user_name, id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Unable to update user name to {new_user_name}')

def update_user_email(conn, id, new_email):  #update user info
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE users SET email=%s WHERE id_user=%s', (new_email, id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Unable to update user email to {new_email}')

def update_user_city(conn, id, new_city):  #update user info
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE users SET city=%s WHERE id_user=%s', (new_city, id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Unable to update user city to {new_city}')

def update_user_active(conn, id, value):  #update user info
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE users SET is_activeu=%s WHERE id_user=%s', (value, id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Unable to update user active bool to {value}')

def delete_user(conn, id):  #logical user delete
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE users SET is_activeu=0 WHERE id_user=%s', (id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Unable to delete user {id}')

##################################################### CRUD BIRD
def bird_create(conn, bird_name):  #insert new bird
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO bird (bird_name) VALUES (%s)', (bird_name))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Unable to create bird: {bird_name}')

def find_bird(conn, bird_name):  #find bird id using it's name
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_bird FROM bird WHERE bird_name = %s AND is_activeb = 1', (bird_name))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def update_bird(conn, id, new_bird_name):  #update bird name (only when mistakes were made)
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE bird SET bird_name=%s WHERE id_bird=%s', (new_bird_name, id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Unable to update bird name to {new_bird_name}')

def delete_bird(conn, id):  #logical delete for birds (which may be unnecessary)
    with conn.cursor() as cursor:
        cursor.execute('UPDATE bird SET is_activeb=0 WHERE id_bird=%s', (id))

##################################################### LIKES
def user_likes_bird(conn, id_user, id_bird):  #insert new bird
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO user_bird (id_user, id_bird) VALUES (%s,%s)', (id_user, id_bird))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'User {id_user} is unable to like bird {id_bird}')

def user_dislikes_bird(conn, id_user, id_bird):
    with conn.cursor() as cursor:
        cursor.execute('UPDATE user_bird SET is_activeub = 0 WHERE id_user=%s AND id_bird=%s', (id_user, id_bird))

##################################################### CRUD POST
def find_mention(subs, s):
    check_end = 1
    while check_end:
        if s[-1] == " ":
            s = s[:-1]
        else:
            check_end = 0
    mentions = []
    splt = s.split(" ")
    print(s)
    for i in splt:
        if i[0] == subs:
            mentions.append(i[1:])
    return mentions

def post_create(conn, id_user, title, content=None, url=None):  #create new post
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO post (title, content, url, id_user) VALUES (%s,%s,%s,%s)', (title, content, url, id_user))

            user_search = find_mention('#', content) 
            if len(user_search) > 0:
                for i in user_search:
                    id_mention = find_user(conn, i)
                    id_post = find_post_title(conn, title)
                    post_mention_user(conn, id_post, id_mention)

            bird_search = find_mention('@', content) 
            if len(bird_search) > 0:
                for i in bird_search:
                    id_mention = find_bird(conn, i)
                    id_post = find_post_title(conn, title)
                    post_mention_bird(conn, id_post, id_mention)

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Unable to create post')

def post_mention_user(conn, id_post, id_mentioned_user):  #post mentions user
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO user_mention (id_post, id_user) VALUES (%s,%s)', (id_post, id_mentioned_user))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Mentioning user failed')

def post_mention_bird(conn, id_post, id_mentioned_bird):  #post mentions bird
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO bird_mention (id_post, id_bird) VALUES (%s,%s)', (id_post, id_mentioned_bird))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Mentioning bird failed')

def find_post_title(conn, title):  #find one post using it's title
    with conn.cursor() as cursor:
        cursor.execute('SELECT content, url, id_user FROM post WHERE title = %s AND is_activep = 1', (title))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def user_post_list(conn, id_user):  #list all posts a specific user wrote
    with conn.cursor() as cursor:
        cursor.execute('SELECT title, content, url FROM post WHERE id_user = %s AND is_activep = 1', (id_user))
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def delete_post(conn, id):  #logical delete for post
    with conn.cursor() as cursor:
        cursor.execute('UPDATE post SET is_activep=0 WHERE id_post=%s', (id))

##################################################### VIEWS
def view_create(conn, user, post, browser, ip, device):  #User viewed post
    with conn.cursor() as cursor:
        try:
            cursor.execute('''INSERT INTO views (id_user, id_post, browser, ip, device) 
                              VALUES (%s,%s,%s,%s,%s)''', (user, post, browser, ip, device))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Unable to create view from user {user}')

def find_view_user(conn, id_user):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM views WHERE id_user = %s', (id_user))
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def find_info_view(conn, id_user, id_post):  
    with conn.cursor() as cursor:
        cursor.execute('SELECT browser, ip, device FROM views WHERE id_user = %s AND id_post = %s', (id_user, id_post))
        res = cursor.fetchall()
        infos = tuple(x[0] for x in res)
        return infos

def find_users_viewed_post(conn, id_post):
    with conn.cursor() as cursor:
        cursor.execute('SELECT user_name FROM users INNER JOIN views USING (id_user) WHERE views.id_post = %s AND user.is_activeu = 1', (id_post))
        res = cursor.fetchall()
        users = tuple(x[0] for x in res)
        return users