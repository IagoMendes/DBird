import io
import json
import logging
import os
import os.path
import re
import subprocess
import unittest
import pymysql
import time

from dbird import *

class TestProjeto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global config
        cls.connection = pymysql.connect(
            host=config['HOST'],
            user=config['USER'],
            password=config['PASS'],
            database='dbird'
        )

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def setUp(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('START TRANSACTION')

    def tearDown(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('ROLLBACK')

############################################################### TESTING USER
    def test_user_create(self):
        conn = self.__class__.connection
    
        user_name = 'Test'
        email = 'test@email.com'
        city = 'Sydney'

        user_create(conn, user_name, email, city)

        # Checks if user was created
        id = find_user(conn, user_name)
        self.assertIsNotNone(id)

        # Searches for inexistent user
        id = find_user(conn, 'jorg')
        self.assertIsNone(id)

    def test_delete_user(self):
        conn = self.__class__.connection
        user_create(conn, 'Liu', "jojo@email.com", "Cidade")
        id = find_user(conn, 'Liu')

        res = user_list(conn)
        self.assertCountEqual(res, (id,))

        delete_user(conn, id)

        res = user_list(conn)
        self.assertFalse(res)

    #@unittest.skip('Em desenvolvimento.')
    def test_update_user(self):
        conn = self.__class__.connection

        user_create(conn, 'eu', 'eu@eu.email', 'la')
        id = find_user(conn, 'eu')

        new_email = "new@email.com"
        new_city = "sao paulo"
        new_name = "NewName"
        # Tries to update user info
        try:
            update_user_city(conn, id, new_city)
            update_user_email(conn, id, new_email)
            update_user_name(conn, id, new_name)
        except ValueError:
            self.fail('Error updating user')
            pass

        # Confirms updates
        new_id = find_user(conn, 'NewName')
        self.assertEqual(id, new_id)

        data = describe_user(conn, id)
        self.assertEqual(new_name, data[0])
        self.assertEqual(new_email, data[1])
        self.assertEqual(new_city, data[2])

############################################################### TESTING BIRD
    def test_bird_create(self):
        conn = self.__class__.connection
    
        bird_name = 'Cacatua'

        bird_create(conn, bird_name)

        # Checks if bird was created
        id = find_bird(conn, bird_name)
        self.assertIsNotNone(id)

        # Searches for inexistent bird
        id = find_bird(conn, 'Rolinha')
        self.assertIsNone(id)

    def test_update_bird(self):
        conn = self.__class__.connection

        bird_create(conn, 'Cacatua')

        id = find_bird(conn, 'Cacatua')

        new_name = "Pomba"
        
        # Tries to update user info
        try:
            update_bird(conn, id, new_name)
        except ValueError:
            self.fail('Error updating bird')
            pass

        # Confirms updates
        new_id = find_bird(conn, 'Pomba')
        self.assertEqual(id, new_id)

    def test_bird_delete(self):
        conn = self.__class__.connection

        bird_name = 'Cacatua'

        bird_create(conn, bird_name)

        # Checks if bird was created
        id = find_bird(conn, bird_name)
        self.assertIsNotNone(id)

        # Deletes bird
        delete_bird(conn, id)

        # Checks if bird was deleted
        id = find_bird(conn, bird_name)
        self.assertIsNone(id)

############################################################### TESTING POST AND MENTIONS
    def test_post(self):
        conn = self.__class__.connection

        user_create(conn, 'eu', 'eu@eu.email', 'la')
        id_write = find_user(conn, 'eu')

        post_create(conn, id_write, 'New Post', 'Look at that pretty bird')
        post = find_post(conn, id_write, 'New Post')
        data = user_post_list(conn, id_write)
        self.assertEqual('New Post', data[0])
        self.assertEqual('Look at that pretty bird', data[1])
        self.assertEqual(None, data[2])

        delete_post(conn, post)
        post = find_post(conn, id_write, 'New Post')
        self.assertIsNone(post)

    def test_mention_user(self):
        conn = self.__class__.connection

        user_create(conn, 'eu', 'eu@eu.email', 'la')
        id_write = find_user(conn, 'eu')

        user_create(conn, 'jorg', 'jorg@email', 'here')
        id_ment = find_user(conn, 'jorg')

        post_create(conn, id_write, 'New Post', 'Look at that pretty bird')
        post = find_post(conn, id_write, 'New Post')

        post_mention_user(conn, post, id_ment)

        res = find_mentioned_posts_user(conn, id_ment)
        self.assertCountEqual(res, (post,))

    def test_mention_bird(self):
        conn = self.__class__.connection

        user_create(conn, 'eu', 'eu@eu.email', 'la')
        id_write = find_user(conn, 'eu')

        bird_create(conn, 'Cacatua')
        id_ment = find_bird(conn, 'Cacatua')

        post_create(conn, id_write, 'New Post', 'Look at that pretty bird')
        post = find_post(conn, id_write, 'New Post')

        post_mention_bird(conn, post, id_ment)
        
        res = find_mentioned_posts_bird(conn, id_ment)
        self.assertCountEqual(res, (post,))

    def full_mention_test(self):
        conn = self.__class__.connection

        user_create(conn, 'eu', 'eu@eu.email', 'la')
        id_write = find_user(conn, 'eu')

        user_create(conn, 'jorg', 'jorg@email', 'here')
        id_ment_user = find_user(conn, 'jorg')

        bird_create(conn, 'Cacatua')
        id_ment_bird = find_bird(conn, 'Cacatua')

        post_create(conn, id_write, 'New Post', 'Look at that pretty #Cacatua @jorg')
        post = find_post(conn, id_write, 'New Post')

        res = find_mentioned_posts_bird(conn, id_ment_bird)
        self.assertCountEqual(res, (post,))

        res = find_mentioned_posts_user(conn, id_ment_user)
        self.assertCountEqual(res, (post,))

############################################################### TESTING VIEW
    def test_view_create(self):
        conn = self.__class__.connection

        user_create(conn, 'eu', 'eu@eu.email', 'la')
        id_user = find_user(conn, 'eu')

        post_create(conn, id_user, 'New Post', 'Look at that pretty')
        post = find_post(conn, id_user, 'New Post')

        view_create(conn, id_user, post, 'Chrome', '192.168.0.1', 'iPhone', "2015-4-13 15:43:11")
        data = find_info_view(conn, id_user, post)
        self.assertEqual('Chrome', data[0])
        self.assertEqual('192.168.0.1', data[1])
        self.assertEqual('iPhone', data[2])

        res = find_view_user(conn, id_user)
        self.assertCountEqual(res, (post,))

        res = find_users_viewed_post(conn, post)
        self.assertCountEqual(res, (id_user,))


############################################################### TESTING LIKE
    def test_like(self):
        conn = self.__class__.connection
    
        bird_name = 'Cacatua'
        bird_create(conn, bird_name)

        user_create(conn, 'Jorg', 'email@jorg', 'landiafin')

        id_bird = find_bird(conn, bird_name)
        id_user = find_user(conn, 'Jorg')

        user_likes_bird(conn, id_user, id_bird)

        active = find_like(conn, id_user, id_bird)
        self.assertEqual(active, 1)

        user_dislikes_bird(conn, id_user, id_bird)
        active = find_like(conn, id_user, id_bird)
        self.assertEqual(active, 0)

############################################################### TESTING FASE 2

    def test_order(self):
        conn = self.__class__.connection
        user_create(conn, 'Jorg', 'email@jorg', 'landiafin')
        id_user = find_user(conn, 'Jorg')

        post_create(conn, id_user, 'New Post', 'Look at that pretty')
        time.sleep(5)
        post_create(conn, id_user, 'New Post2', 'Look at that pretty')
        time.sleep(5)
        post_create(conn, id_user, 'New Post3', 'Look at that pretty')
        time.sleep(5)
        post_create(conn, id_user, 'New Post4', 'Look at that pretty')
        time.sleep(5)
        post_create(conn, id_user, 'New Post5', 'Look at that pretty')

        posts = order_post(conn, id_user)
        
        self.assertEqual(posts[0][0], 'New Post5')
        self.assertEqual(posts[1][0], 'New Post4')
        self.assertEqual(posts[2][0], 'New Post3')
        self.assertEqual(posts[3][0], 'New Post2')
        self.assertEqual(posts[4][0], 'New Post')



############################################################### TESTING ALL

    @unittest.skip('Em desenvolvimento.')
    def test_all(self):
        conn = self.__class__.connection
        user_create(conn, 'vc', 'vc@vc.email', 'al')
        user_create(conn, 'ele', 'el@el.email', 'lal')

        bird_create(conn, 'arara')
        bird_create(conn, 'papagaio')

        post_create(conn, find_user(conn, 'vc'), 'Posterino', '@eu, vc por aqui')
        post_create(conn, find_user(conn, 'ele'), 'Posteroni', '#arara @vc')

        post = find_post(conn, find_user(conn, 'vc'), 'Posteroni')

        res1 = find_mentioned_posts_user(conn, find_user(conn, 'ele'))
        self.assertCountEqual(res1, (post,))

        res2 = find_mentioned_posts_bird(conn, find_bird(conn, 'arara'))
        self.assertCountEqual(res2, (post,))

        delete_user(conn, find_user(conn, 'vc'))
        delete_user(conn, find_user(conn, 'ele'))

        res3 = user_list(conn)
        self.assertFalse(res3)

        res4 = find_mentioned_posts_user(conn, find_user(conn, 'ele'))
        self.assertFalse(res4)

        delete_bird(conn, find_bird(conn, 'arara'))

        res5 = find_mentioned_posts_bird(conn, find_bird(conn, 'arara'))
        self.assertFalse(res5)

def run_sql_script(filename):
    global config
    with open(filename, 'rb') as f:
        subprocess.run(
            [
                config['MYSQL'], 
                '-u', config['USER'], 
                '-p' + config['PASS'], 
                '-h', config['HOST']
            ], 
            stdin=f
        )

def setUpModule():
    filenames = [entry for entry in os.listdir() 
        if os.path.isfile(entry) and re.match(r'.*_\d{3}\.sql', entry)]
    for filename in filenames:
        run_sql_script(filename)

def tearDownModule():
    run_sql_script('tear_down.sql')

if __name__ == '__main__':
    global config
    with open('config_tests.json', 'r') as f:
        config = json.load(f)
    logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)
    unittest.main(verbosity=2)
