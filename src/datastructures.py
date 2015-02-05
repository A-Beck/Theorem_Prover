# A file that defines the custom data structs used in our assignment

variables = []
facts = []
rules = []

class Variable(object):
    
    """ Class that represents the basic state of a variable """
    
    def __init__(self, name="", str_val="", bool_val=False):
        """ object state includes string value and truth value """
        self.name = name
        self.string_value = str_val
        self.truth_value = bool_val

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.name == other.name)
        
    def __str__(self):
        """ so str() operator can be used """
        return '{} = "{}"'.format(self.name, self.string_value)
