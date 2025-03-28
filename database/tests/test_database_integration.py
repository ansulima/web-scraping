import unittest
import mysql.connector
from pathlib import Path


class TestDatabaseIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sua_senha",
            database="ans_database"
        )
        cls.execute_sql_file("migrations/01_create_tables.sql")

    @classmethod
    def execute_sql_file(cls, relative_path):
        file_path = Path(__file__).parent.parent / relative_path
        with open(file_path, 'r') as file:
            sql_commands = file.read().split(';')
            cursor = cls.conn.cursor()
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
            cls.conn.commit()

    def test_tables_creation(self):
        cursor = self.conn.cursor()
        cursor.execute("SHOW TABLES LIKE 'operadoras_ativas'")
        self.assertIsNotNone(cursor.fetchone())

        cursor.execute("SHOW TABLES LIKE 'demonstracoes_contabeis'")
        self.assertIsNotNone(cursor.fetchone())

    @classmethod
    def tearDownClass(cls):
        cursor = cls.conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS demonstracoes_contabeis")
        cursor.execute("DROP TABLE IF EXISTS operadoras_ativas")
        cls.conn.close()


if __name__ == '__main__':
    unittest.main()