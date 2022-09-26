from unittest.mock import MagicMock, Mock, patch
from sqlite3 import Cursor
from sqlite3 import Connection

import unittest

import src.main.utils.FileOperationsUtil
from src.main.utils.DBOUtil import *
from src.main.utils.FileOperationsUtil import convertToBinaryData

class testDBOUtil(unittest.TestCase):

    def test_sqliteConnect_successful(self):
        connectionString = "test/connection/string"
        sqlite3.connect = MagicMock(return_value='connection succeeded')

        dbc = sqliteConnect(connectionString)
        sqlite3.connect.assert_called_with(connectionString)
        self.assertEqual(dbc,'connection succeeded')

    def test_sqliteConnect_fail(self):
        connectionString = "test/connection/string"

        sqlite3.connect = MagicMock(side_effect=sqlite3.Error("connection failed"))

        dbc = sqliteConnect(connectionString)
        sqlite3.connect.assert_called_with(connectionString)
        self.assertEqual(dbc.args[0], 'connection failed')

    def test_createTables(self):
        conn = MagicMock(Connection)
        cursor = MagicMock(Cursor)

        conn.cursor.return_value = cursor
        cursor.execute.return_value = cursor

        createTables(conn)

        cursor.execute.assert_called()

    def test_insertFile(self):
        testFilePath = "test"
        testMimeType = "text/plain"
        testInboundFileName = "path/to/test/file.txt"

        conn = MagicMock(Connection)
        cursor = MagicMock(Cursor)

        conn.cursor.return_value = cursor
        cursor.execute.return_value = cursor
        conn.commit.return_value = conn

        with patch.object(src.main.utils.DBOUtil, 'convertToBinaryData', return_value="data") as mock_method:
            with patch.object(src.main.utils.DBOUtil, 'sqliteConnect', return_value=conn) as mock_conn:
                insertFile(conn, testFilePath, testMimeType, testInboundFileName)

        cursor.execute.assert_called()
        conn.commit.assert_called()

    def test_retrieveFile(self):
        testFilePath = "test/test/"
        testWorkingDir = "/test/dir/"

        resultTuple = None

        conn = MagicMock(Connection)
        cursor = MagicMock(Cursor)

        conn.cursor.return_value = cursor
        cursor.execute.return_value = cursor
        cursor.fetchone.return_value = ['correctKeys', 'correctValues']

        with patch.object(src.main.utils.DBOUtil, 'writeTofile', return_value="mocked function call") as mock_write, \
                patch.object(src.main.utils.DBOUtil, 'guess_extension', return_values="mocked_values") as mock_guess, \
                    patch.object(src.main.utils.DBOUtil, 'sqliteConnect', return_value=conn) as mock_conn:
                        resultTuple = retrieveFile(conn, testFilePath, testWorkingDir)

        cursor.execute.assert_called()
        cursor.fetchone.assert_called()
        self.assertEqual(resultTuple, ('correctValues', 'correctValues'))

    def test_deleteFile(self):
        testFilePath = "test/test/"
        testWorkingDir = "/test/dir/"

        conn = MagicMock(Connection)
        cursor = MagicMock(Cursor)

        conn.cursor.return_value = cursor
        cursor.execute.return_value = cursor
        cursor.fetchone.return_value = ['correctKeys', 'correctValues']
        conn.commit.return_value = conn

        with patch.object(src.main.utils.DBOUtil, 'removeFile', return_value="mocked function call") as mock_write, \
                patch.object(src.main.utils.DBOUtil, 'guess_extension', return_values="mocked_values") as mock_guess, \
                    patch.object(src.main.utils.DBOUtil, 'sqliteConnect', return_value=conn) as mock_conn:
                        deleteFile(conn, testFilePath, testWorkingDir)

        cursor.execute.assert_called()
        cursor.fetchone.assert_called()
        conn.commit.assert_called()