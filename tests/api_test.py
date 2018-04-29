""" Test api responses """
import unittest
import json
import sys
import mock
from cache_server import app
from cache_management.cache_agent import CacheAgent, Document

class ApiTest(unittest.TestCase):
    """ Test cache routes """
    @mock.patch.object(CacheAgent, 'get_all_keys')
    def test_should_retrieve_documents(self, mock_get_keys):
        """ Should get list of keys """
        with app.test_client() as client:
            mock_get_keys.return_value = ["key-a", "key-b"]
            response = client.get('/documents')
            mock_get_keys.assert_called()
            response_json = json.loads(response.get_data().decode(sys.getdefaultencoding()))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response_json), 2)

    @mock.patch.object(CacheAgent, 'get_document')
    def test_should_retrieve_document(self, mock_get_document):
        """ Should get list of keys """
        with app.test_client() as client:
            mock_get_document.return_value = Document("key", "value")
            response = client.get('/document/key')
            mock_get_document.assert_called_with("key")
            response_json = json.loads(response.get_data().decode(sys.getdefaultencoding()))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_json["key"], "key")
            self.assertEqual(response_json["value"], "value")

    @mock.patch.object(CacheAgent, 'get_document')
    def test_retrieve_document_not_existing(self, mock_get_document):
        """ document does not exist """
        with app.test_client() as client:
            mock_get_document.return_value = None
            response = client.get('/document/key')
            mock_get_document.assert_called_with("key")
            response_json = json.loads(response.get_data().decode(sys.getdefaultencoding()))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_json["status"], "error")
            self.assertEqual(response_json["message"], "cannot find the document")

    def test_insert_doc_incorrect_request(self):
        """ document does not exist """
        with app.test_client() as client:
            response = client.post('/document')
            response_json = json.loads(response.get_data().decode(sys.getdefaultencoding()))
            self.assertEqual(response.status_code, 422)
            self.assertEqual(response_json["status"], "error")
            self.assertEqual(response_json["message"], "Incorrect request. key or value missing")

    def test_insert_doc_valid_request(self):
        """ document does not exist """
        with app.test_client() as client:
            response = client.post('/document', data=json.dumps({"key": "key", "value": "value"}), content_type="application/json")
            response_json = json.loads(response.get_data().decode(sys.getdefaultencoding()))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_json["success"], "true")
