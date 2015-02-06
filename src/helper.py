################# HELPER FUNCTIONS ##########################
            
def find_var(var_list, var_name):
    for variable in var_list:
        if variable.name == var_name:
            return variable
    return None
        
def is_valid_op(char):
    allowed_ops = ['v', '^', '!', '(', ')']
    return char in allowed_ops

def check_rule_validity(var_list, lhs, rhs):
    rhs_var = find_var(var_list, rhs)
    if rhs_var is None:
        return False
    exp = "".join(lhs.split())
    for char in exp:
        val = (char.isalpha() and find_var(var_list, char)) or is_valid_op(char)
        if val is False:
            return False
        if val is None:
            return False
    return True