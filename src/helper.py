################# HELPER FUNCTIONS ##########################

_and = '&'
_or = '|'
_not = '!'

    
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