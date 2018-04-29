''' Module documents exposes a Document model '''

class Document():
    ''' Model to store document in cache memory '''
    def __init__(self, key, init_value):
        self.value = [init_value]
        self.key = key
        self.previous = None
        self.next = None

    def add_new_value(self, new_value):
        ''' Adds to the end of the value list a new value for the document '''
        self.value.append(new_value)

    def get_last_value(self):
        ''' Returned last know document value '''
        return self.value[-1]

    def get_all_values(self):
        ''' Returns a list of values for the document '''
        return list(self.value)
