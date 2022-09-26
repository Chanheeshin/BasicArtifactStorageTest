import unittest
import src.main.controllers.DataStoreController
from src.main.controllers.DataStoreController import createResource
from src.main.controllers.DataStoreController import retrieveResource
from src.main.controllers.DataStoreController import deleteResource
from unittest.mock import MagicMock, patch
from src.main.models.responseModel import responseModel

class testDataStoreController(unittest.TestCase):

    def test_createResource(self):
        req = MagicMock()
        req.headers = {"Content-Type":"text/plain"}
        req.get_data.return_value = "testdata"

        with patch("src.main.controllers.DataStoreController.request", req), \
            patch.object(src.main.controllers.DataStoreController, 'writeTofile', return_value=True), \
                patch.object(src.main.controllers.DataStoreController, 'insertFile', return_value=True), \
                    patch.object(src.main.controllers.DataStoreController, 'removeFile', return_value=True):
                        test = createResource("/test/path/file")

        assert test.status == '200 OK'

    def test_retrieveResource(self):
        req = MagicMock()
        req.headers = {"Content-Type":"text/plain"}
        req.get_data.return_value = "testdata"

        res = MagicMock(responseModel)
        res.return_value = "returned response"

        with patch("src.main.controllers.DataStoreController.request", req), \
            patch.object(src.main.controllers.DataStoreController, 'retrieveFile', return_value=("text/plain", "testdata")), \
                patch("src.main.controllers.DataStoreController.responseModel", res):
                    test = retrieveResource("/test/path/file")

        assert test == 'returned response'

    def test_deleteResource(self):
        req = MagicMock()
        req.headers = {"Content-Type":"text/plain"}
        req.get_data.return_value = "testdata"

        res = MagicMock(responseModel)
        res.return_value = "returned response"

        with patch("src.main.controllers.DataStoreController.request", req), \
            patch.object(src.main.controllers.DataStoreController, 'deleteFile', return_value=("text/plain", "testdata")), \
                patch("src.main.controllers.DataStoreController.responseModel", res):
                    test = deleteResource("/test/path/file")

        assert test.status == '200 OK'
