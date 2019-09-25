import subprocess
import unittest
import pymysql

connection = pymysql.connect(
    host='localhost',
    user='megadados',
    password='megadados2019',
    database='dbird')

# class TestCase(unittest.TestCase):
#     def test_insert(self):
#         with connection.cursor() as cursor:
#             sql = "INSERT INTO users (id_user, user_name, email, city)"
#             cursor.execute(sql)
#         pass

#     @classmethod
#     def setUpClass(TestCase):
#         with open("script.sql", "rb") as f:
#             res = subprocess.run("mysql -u root -proot".split(), stdin=f)
#             print(res)
    
with connection.cursor() as cursor:
    sql = """INSERT INTO users (user_name, email, city) VALUES
            ('jorgen_smorgen', 'liu.liu@liu.liu', 'benis')"""
    cursor.execute(sql)
    cursor.execute("COMMIT")

if __name__ == "__main__":
    unittest.main()
