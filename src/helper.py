################# HELPER FUNCTIONS ##########################

_and = '&'
_or = '|'
_not = '!'
_inclusive_not = '@'

    
def find_var(var_list, var_name):
    for variable in var_list:
        if variable.name == var_name:
            return variable
    return None
        
def is_valid_op(char):
    allowed_ops = [_and, _or, _not, '(', ')']
    return char in allowed_ops

def is_var(var_list, char):
    return  find_var(var_list, char) is not None

def negate_op(operator):
    if operator == _and:
        return _or
    elif operator == _or:
        return _and

def is_left_assoc(op):
    """
    Returns a bool indicating if an oepration is left associative
    """
    return op == _and or op == _or

def has_less_precedence(op1, op2):
    """ 
    Returns a bool indicating if op1 has less precedence than op2
    """
    # order of precedence: not, and, or
    if (op1 == _not) or (op1 == _inclusive_not):
        return False
    elif op1 == _and:
        if op2 == _not or op2 == _inclusive_not:
            return True
        if op2 == _or:
            return False
    elif op1 == _or:
        return True