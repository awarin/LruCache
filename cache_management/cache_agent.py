''' Exposes CacheAgent class '''
from threading import Lock
from cache_management.document import Document

class CacheAgent():
    ''' In memory cache management
        This class implements an LRU caching system
        It uses a doubly linked list and a dictionnay '''

    def __init__(self, max_size=10):
        self.dict = {}

        self.head = None
        self.tail = None

        self.size = max_size

        self.lock = Lock()

    def get_all_keys(self):
        ''' Returns all keys in cache '''
        return list(self.dict.keys())

    def get_document(self, key):
        ''' Tries to get a value by key within the local dictionnary
            If not found, returns None '''
        if key in self.dict:
            with self.lock:
                doc = self.dict[key]
                self.remove_document_refs(doc)
                self.set_head_refs(doc)
                return doc

        return None

    def set_document(self, key, value):
        ''' Adds the document to the local dictionnary
            If already existing, the value will be overriden '''
        #check if value not already in document
        with self.lock:
            if key in self.dict:
                #update document
                updated = self.dict[key]
                #remove it
                self.remove_document_refs(updated)
                self.set_head_refs(updated)
                updated.add_new_value(value)

            else:
                doc = Document(key, value)
                if len(self.dict) == self.size:
                    self.remove_tail_document()

                self.set_head_refs(doc)
                self.dict[doc.key] = doc

    def remove_document_refs(self, doc):
        ''' Removes the document references in the lists '''
        if doc.previous is None:
            #document was the head
            self.head = doc.next
        else:
            doc.previous.next = doc.next

        if doc.next is None:
            #document was the tail
            self.tail = doc.previous
        else:
            doc.next.previous = doc.previous

    def set_head_refs(self, doc):
        ''' Set the document as the head of the list '''
        doc.next = self.head
        if self.head != None:
            self.head.previous = doc

        self.head = doc

        if self.tail is None:
            self.tail = doc

    def remove_tail_document(self):
        ''' Deletes the last document references.
            Also removes it from the local dictionnary '''
        doc = self.tail
        self.remove_document_refs(doc)
        del self.dict[doc.key]
