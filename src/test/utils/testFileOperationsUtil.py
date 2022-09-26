import unittest
from unittest.mock import MagicMock, Mock, patch, mock_open
from src.main.utils.FileOperationsUtil import *
import src.main.utils.FileOperationsUtil

class testFileOperationsUtil(unittest.TestCase):

    @patch('os.path.exists')
    @patch('os.remove')
    def test_removeFile(self, mock_exists, mock_remove):
        testFileName = "test/file.txt"
        mock_exists.return_value=True
        mock_remove.return_value=True
        removeFile(testFileName)

        mock_exists.assert_called()
        mock_remove.assert_called()

    def test_convertToBinaryData(self):
        testPath = "path/to/open"
        with patch('builtins.open', new_callable=mock_open()) as m:
            temp = convertToBinaryData(testPath)
            m.assert_called_with(testPath, 'rb')

        assert temp is not None

    def test_writeToFile(self):
        testData = "test"
        testPath = "path/to/open"
        with patch('builtins.open', new_callable=mock_open()) as m:
            temp = writeTofile(testData, testPath)
            m.assert_called_with(testPath, 'wb')

    def test_isBinary(self):
        testMimeType = "text"
        testSubType = "plain"
        assert isBinary(testMimeType, testSubType) is False

    def test_isBinaryTrue(self):
        testMimeType = "image"
        testSubType = "png"
        assert isBinary(testMimeType, testSubType) is True

