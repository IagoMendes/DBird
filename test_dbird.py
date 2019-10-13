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

        # Tenta mudar nome para algum nome já existente.
        try:
            update_user_city(conn, id, "sao paulo")
            update_user_email(conn, id, "new@email.com")
            update_user_name(conn, id, "NewName")
        except ValueError as e:
            self.fail('Error updating user')
            pass

        # Verifica se mudou.
        id_novo = find_user(conn, 'NewName')
        self.assertEqual(id, id_novo)

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
