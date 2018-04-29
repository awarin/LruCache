''' Tests the implementation of the cache agent '''

import unittest
from cache_management.cache_agent import CacheAgent
from cache_management.document import Document

class TestEmptyCacheAgent(unittest.TestCase):
    """ Test empty cache agent implementation """
    def setUp(self):
        self.cache = CacheAgent(3)

    def test_get_all_keys_should_return(self):
        """ Should return all keys """
        self.cache.dict = {
            "key-a": "value",
            "key-b": "value",
            "key-c": "value"
        }

        keys = self.cache.get_all_keys()
        self.assertEqual(len(keys), 3)
        self.assertTrue("key-a" in keys)

    def test_get_document_not_found(self):
        """ Should return none """
        doc = self.cache.get_document("non-existing-key")
        self.assertEqual(doc, None)

    def test_get_document_one_doc(self):
        """ Should return the document """
        doc_in_cache = Document("key-a", "value")
        self.cache.dict = {
            doc_in_cache.key: doc_in_cache
        }
        self.cache.tail = doc_in_cache
        self.cache.head = doc_in_cache

        doc = self.cache.get_document(doc_in_cache.key)

        self.assertEqual(doc.key, doc_in_cache.key)
        self.assertEqual(self.cache.tail.key, doc_in_cache.key)
        self.assertEqual(self.cache.head.key, doc_in_cache.key)

class TestFullCacheAgent(unittest.TestCase):
    """ Test full cache agent implementation """
    def setUp(self):
        self.cache = CacheAgent(3)
        doc_a = Document("key-a", "value-a")
        doc_b = Document("key-b", "value-b")
        doc_c = Document("key-c", "value-c")

        # order for the list is A ==> B ==> C
        doc_a.next = doc_b
        doc_b.previous = doc_a
        doc_b.next = doc_c
        doc_c.previous = doc_b

        # fill dictionnary
        self.cache.dict = {
            doc_a.key: doc_a,
            doc_b.key: doc_b,
            doc_c.key: doc_c,
        }

        self.cache.tail = doc_c
        self.cache.head = doc_a

    def test_get_document_three_doc(self):
        """ Should return the document
            Setup a cache state where 3 documents are in memory """

        doc_retrieved = self.cache.get_document("key-c")

        self.assertEqual(doc_retrieved.get_last_value(), "value-c")
        self.assertEqual(self.cache.head.key, "key-c")
        self.assertEqual(self.cache.head.next.key, "key-a")
        self.assertEqual(self.cache.head.next.next.key, "key-b")

        self.assertEqual(self.cache.tail.key, "key-b")
        self.assertEqual(self.cache.tail.previous.previous.key, "key-c")

    def test_set_document_should_free(self):
        """ Should remove key-c (tail) document """

        self.cache.set_document("key-d", "value-d")
        self.assertTrue("key-d" in self.cache.dict)
        self.assertTrue("key-c" not in self.cache.dict)
        self.assertEqual(len(self.cache.dict), 3)

    def test_set_document_update(self):
        """ Should add new version of doc-b and set key-b as head """

        self.cache.set_document("key-b", "second-value-b")
        self.assertTrue("key-b" in self.cache.dict)

        doc_b = self.cache.dict["key-b"]
        self.assertEqual(len(doc_b.get_all_values()), 2)
        self.assertEqual(len(self.cache.dict), 3)
        self.assertEqual(doc_b.get_last_value(), "second-value-b")
        self.assertEqual(doc_b.get_all_values()[0], "value-b")

        self.assertEqual(self.cache.head.key, "key-b")
