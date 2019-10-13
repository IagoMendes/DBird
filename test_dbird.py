import io
import json
import logging
import os
import os.path
import re
import subprocess
import unittest
import pymysql

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

############################################################### TESTING POST


############################################################### TESTING VIEW


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

############################################################### TESTING MENTION



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
        if os.path.isfile(entry) and re.match(r'script.sql', entry)]
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
