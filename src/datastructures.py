# A file that defines the custom data structs used in our assignment
from helper import *

variables = []
facts_raw = []
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
    
    
class Rule(object):
    
    def __init__(self, exp, var):
        self.expression = exp  # Expression Object
        self.variable = var    # Variable object
        
    def __str__(self):
        return self.expression + " -> " + variable.name
    
    def evaluate(self):
        pass
    
    def validate(self):
        """ validates that all variables """

        
class Expression(object):
    
    def __init__(self, string):
        self.expr_str = string
        self.token_list = self.tokenize()
        
    def tokenize(self):
        temp_string = "".join(self.expr_str.split())
        l = []
        for char in temp_string:
            l.append(char)
        return l


class TreeNode(object):

    def __init__(self, value="", left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def get_token(token_list, expected):
    if token_list[0] == expected:
        del token_list[0]
        return True
    else:
        return False

def get_variable(token_list):
    x = token_list[0]
    x_var = find_var(variables, x)
    if type(x_var) != Variable:
        return None
    del token_list[0]
    return TreeNode(x_var, None, None)

def print_inorder(node):
    if node is not None:
        print_inorder(node.left)
        print node.value
        print_inorder(node.right)






