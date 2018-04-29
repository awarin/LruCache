""" test document class model """
import unittest
from cache_management.document import Document

class DocumentTest(unittest.TestCase):
    """ Test document class model """
    def test_should_init_document(self):
        """ Should create a new document """
        doc = Document("key-a", "value-a")
        self.assertEqual(doc.value[0], "value-a")
        self.assertEqual(doc.get_last_value(), "value-a")

    def test_should_update(self):
        """ Should update a ndocument """
        doc = Document("key-a", "value-a")
        doc.add_new_value("new-value")

        self.assertEqual(doc.get_last_value(), "new-value")
        self.assertEqual(len(doc.get_all_values()), 2)
