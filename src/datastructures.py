# A file that defines the custom data structs used in our assignment

class Variable(object):
    
    """ Class that represents the basic state of a variable """
    
    def __init__(self, str_val="", bool_val=False):
        """ object state includes string value and truth value """
        self.string_value = str_val
        self.truth_value = bool_val
        
    def __str__(self):
        """ so str() operator can be used """
        return self.string_value
