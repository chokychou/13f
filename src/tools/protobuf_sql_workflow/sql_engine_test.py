import unittest
import psycopg2
from unittest.mock import patch
from src.tools.protobuf_sql_workflow.sql_engine import connect_to_db, execute_query, close_connection

class DBUtilsTest(unittest.TestCase):

    test_host = "test_host"
    test_db = "test_db"
    test_user = "test_user"
    test_password = "test_password"
    test_port = "5432"

    @patch("psycopg2.connect")
    def test_connect_to_db(self, mock_connect):
        conn = connect_to_db(self.test_host, self.test_db, self.test_user, self.test_password, self.test_port)
        mock_connect.assert_called_once_with(host=self.test_host, database=self.test_db, user=self.test_user, password=self.test_password, port=self.test_port)
        self.assertEqual(conn, mock_connect.return_value)

    @patch("psycopg2.connect")
    def test_connect_to_db_error(self, mock_connect):
        mock_connect.side_effect = psycopg2.Error("Test error")
        conn = connect_to_db(self.test_host, self.test_db, self.test_user, self.test_password, self.test_port)
        self.assertIsNone(conn)

    @patch("psycopg2.connect")
    def test_execute_query(self, mock_connect):
        conn = mock_connect.return_value
        cursor = conn.cursor.return_value
        execute_query(conn, "SELECT * FROM users")
        cursor.execute.assert_called_once_with("SELECT * FROM users")
        conn.commit.assert_called_once()

    @patch("psycopg2.connect")
    def test_close_connection(self, mock_connect):
        conn = mock_connect.return_value
        close_connection(conn)
        conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
