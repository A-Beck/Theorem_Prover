# A file that defines the custom data structs used in our assignment
from helper import *
from collections import deque

variables = []
facts_raw = []
rules = []

_and = '&'
_or = '|'
_not = '!'
_inclusive_not = '@'

class Variable(object):
    
    """ Class that represents the basic state of a variable """
    
    def __init__(self, name="", str_val="", bool_val=False, bool_val_soft=False):
        """ object state includes string value and truth value """
        self.name = name
        self.string_value = str_val
        self.truth_value = bool_val
        self.truth_value_soft = bool_val_soft

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
        return str(self.expression) + " -> " + self.variable.name
    
    def __repr__(self):
        return str(self)
    
    def evaluate(self):
        pass
    
    def validate(self):
        """ validates that all variables """

        
class Expression(object):
    
    def __init__(self, string):
        self.expr_str = string
        self.token_list = self.tokenize()

    def __str__(self):
        return str(self.expr_str)
        
    def tokenize(self):
        """ Parses a string into token list """
        operators = ['(',')', _and, _or, _not]
        array = list() # hold the tokens
        aggregator = "" # accumulates the characters in a variable string
        for char in self.expr_str:
            if char in operators:
                #if an operator, add current variable and the op
                if aggregator != "":
                    array.append(aggregator)
                    aggregator = ""
                array.append(char)
            elif char == " ":
                # if a space, stop aggregating and add the variable
                if aggregator != "":
                    array.append(aggregator)
                    aggregator = ""
            elif char.isalpha() or char == '_':
                # if A-Z, a-z, or _, add to current variable string
                aggregator = aggregator + char
            else:
                pass
        if aggregator != "":
            array.append(aggregator)    
        return array

    def evaluate(self):
        queue = get_RPN(self.token_list)
        root_node = build_tree(queue)
        return calc_tree(root_node)

    def soft_evaluate(self):
        queue = get_RPN(self.token_list)
        root_node = build_tree(queue)
        return calc_tree_soft(root_node)

    
class TreeNode(object):
    """ Class used to make abstract syntax tree for Expressions"""

    def __init__(self, value="", left=None, right=None, neg=False):
        self.value = value
        self.left = left
        self.right = right
        self.negate = neg
        
    def __str__(self):
        # expects v
        if not self.negate:
            return str(self.value)
        else:
            return "Not " + str(self.value)


def get_RPN(token_list):
    """ 
    Uses shunting-yard algo to get infix into RPN form
    Handles '!' outside a Parenthesis in a stateful way
    Returns None if malformed input
    Returns a queue of Variables in reverse polish notation if successful
    Most comments come from the wikipedia article on this algo
    """
    # initialize data structures : SY is stack based
    stack = list()  # stack holds operator and parenthesis
    queue = deque([])  # queue holds expression in RPN
    nm_stack = list()  # holds if expression is in negate mode or not
    nm_stack.append(False)  # start off in a state that is not negate mode
    
    # convienence array to easily check check char is an 'and' or 'or'
    operators = [_and, _or]
    
    def is_in_negate_mode():
        """ True if in negate mode, false otherwise"""
        l = len(nm_stack)
        if l > 0:
            return nm_stack[l-1]
        else:
            return False
    # Read a token
    for i in range(0, len(token_list)):  
        token = token_list[i]
        # if current token is a variable, append it to output queue
        if is_var(variables, token):
            var = find_var(variables, token)
            # if in negate mode, apply demorgan
            if is_in_negate_mode(): 
                queue.append('!')
            queue.append(var)
        # manage nots based on negate mode
        elif is_valid_op(token):
            if token == _not:
                next_token = token_list[i+1]
                if is_in_negate_mode():
                    if  next_token == '(':
                        nm_stack.append(False)
                    else:
                        queue.append(token)
                else:
                    if next_token == '(':
                        nm_stack.append(True)
                    else: 
                        queue.append(token)
            # if token is an operator (o1)
            elif token in operators:
                # while there is an operator token on top of the stack (o2), and either:
                #    o1 is left associative and its precedence is <= o2
                #    o1 is right associative and it precedence is < o2
                while len(stack) > 0 and stack[len(stack) -1] in operators:
                        # pop o2 and append to output queue
                        op = stack.pop()
                        queue.append(op)
                # then push o1 onto the stack
                # if in negate mode, apply demorgan first       
                if is_in_negate_mode(): 
                    stack.append(negate_op(token))
                else: 
                    stack.append(token)
            # If the token is a left parenthesis, then push it onto the stack.
            elif token == '(':
                stack.append(token)
                # if negate mode was not altered by previous token
                # maintain negate mode from outer scope
                if (i-1 >= 0) and token_list[i-1] != '!':
                    nm_stack.append(is_in_negate_mode())
            # if the token is a right parenthesis:
            elif token == ')':
                paren_matched = False
                # Until the token at the top of the stack is a left parenthesis, 
                # pop operators off the stack onto the output queue.
                while len(stack) > 0:
                    item = stack.pop()
                    if item == '(':
                        paren_matched = True
                        if len(nm_stack) > 1:
                            nm_stack.pop()
                        break
                    else:
                        queue.append(item)
                # If the stack runs out without finding a left parenthesis, 
                # then there are mismatched parentheses
                if not paren_matched:
                    return None
            else:
                #TODO: failure mode here, token matches nothing we can identify
                return None
    # When there are no more tokens to read
    # While there are still operator tokens in the stack
    while (len(stack) > 0):
        top = stack.pop()
        # If the operator token on the top of the stack is a parenthesis, 
        # then there are mismatched parentheses
        if top == '(' or top == ')':
            return None
        # Pop the operator onto the output queue
        else:
            queue.append(top)
    # if there are two negatives right after eachother, they cancel eachother
    for i in range(0,len(queue)-1):
        if queue[i] == '!' and queue[i+1] == '!':
            queue[i] = ''
            queue[i+1] = '' 
    return queue
           

def build_tree(queue):
    """ 
    Uses queue built in get_RPN method to build a tree ...
    Head node is returned in success
    None is returned in failure 
    """
    operators = [_and, _or]
    
    stack = list()
    while len(queue) > 0:
        item = queue.popleft();
        if item == '':
            pass
        elif type(item) is Variable:
            stack.append(TreeNode(value=item))
        elif item == _not:
            if len(queue) > 0: 
                item2 = queue.popleft()
            else:
                return None
            stack.append(TreeNode(value=item2, neg=True))
        elif item in operators:
            right=stack.pop()
            left= stack.pop()
            stack.append(TreeNode(value=item, right=right, left=left, neg=False))
    return stack.pop()
        
    
## gets a truth value given an expression Node
def calc_tree(node):
    # if leaf, it is a Variable
    if node.right is None and node.left is None:
        if node.negate:
            return not node.value.truth_value
        else:
            return node.value.truth_value
    elif node.value == _and:
        return calc_tree(node.right) and calc_tree(node.left)
    elif node.value == _or:
        return calc_tree(node.right) or calc_tree(node.left)

## gets a truth value given an expression Node
def calc_tree_soft(node):
    # if leaf, it is a Variable
    if node.right is None and node.left is None:
        if node.negate:
            return not node.value.truth_value_soft
        else:
            return node.value.truth_value_soft
    elif node.value == _and:
        return calc_tree_soft(node.right) and calc_tree_soft(node.left)
    elif node.value == _or:
        return calc_tree_soft(node.right) or calc_tree_soft(node.left)


def print_inorder(node):
    if node is not None:
        if node.left is not None:
            print_inorder(node.left)
        print node
        if node.right is not None:
            print_inorder(node.right)


def forward_chain(rules, facts):
    flag = True
    while(flag):
        flag = False
        for rule in rules:
            expr = rule.expression
            # var must exist in variables, add check
            var = rule.variable
            expr_truth_value = expr.evaluate()

            if expr_truth_value and (var not in facts):
                facts.append(var)
                flag = True


def query_for_fact(var, rule_dict):
    """
     var is variable obj
     returns nothing, but updates soft truth values in var objs
    """
    if var in facts_raw:
        var.truth_value_soft = True
    else:
        rule_exists = False
        for rule in rule_dict.keys():
            if rule.variable == var and rule_dict[rule] is False:
                rule_exists = True
                rule_dict[rule] = True
                expr = rule.expression
                for item in expr.token_list:
                    if item not in [_and, _not, _or, '(', ')']:
                        # it is a var
                        new_var = find_var(variables, item)
                        query_for_fact(new_var, rule_dict)
                truth = expr.soft_evaluate()
                var.truth_value_soft = truth
                break
        if rule_exists is False:
            var.truth_value_soft = False


def query(expression):
    rule_dict = {}
    for rule in rules:
        rule_dict[rule] = False
    for item in expression.token_list:
        if item not in [_and, _not, _or, '(', ')']:
            # it is a var
            var = find_var(variables, item)
            query_for_fact(var, rule_dict)
    result = expression.soft_evaluate()
    return result

##################################

def get_RPN_2(token_list):
    """ 
    Uses shunting-yard algo to get infix into RPN form
    Handles '!' outside a Parenthesis in a stateful way
    Returns None if malformed input
    Returns a queue of Variables in reverse polish notation if successful
    """
    # initialize data structures : SY is stack based
    stack = list()  # stack holds operator and parenthesis
    queue = deque([])  # queue holds expression in RPN
    
    # convienence array to easily check check char is an 'and' or 'or'
    operators = [_and, _or, _not]
    
    #Read a token
    for i in range(0, len(token_list)): 
        #print str(queue)
        token = token_list[i]
        # if current token is a variable, append it to output queue
        if is_var(variables, token):
            var = find_var(variables, token)
            queue.append(var)
        # if token is an operator (o1)
        elif token in operators:
            # determine type of not used
            if token == _not:
                next_token = token_list[i+1]
                if next_token == '(':
                    token = _inclusive_not
            # while there is an operator token on top of the stack (o2), and either:
            # o1 is left associative and its precedence is <= o2, or
            # o1 is right associative and it precedence is < o2
            while (len(stack) > 0) and (stack[len(stack) -1] in operators) and \
                    ((is_left_assoc(token) and has_less_precedence(token, stack[len(stack) -1])) or \
                    ((not is_left_assoc(token)) and has_less_precedence(token, stack[len(stack) -1]))):
                    # pop o2 and append to output queue
                    op = stack.pop()
                    queue.append(op)
            # then push o1 onto the stack    
            stack.append(token)
        # If the token is a left parenthesis, then push it onto the stack.
        elif token == '(':
            stack.append(token)
        # if the token is a right parenthesis:
        elif token == ')':
            paren_matched = False
            # Until the token at the top of the stack is a left parenthesis, 
            # pop operators off the stack onto the output queue.
            while len(stack) > 0:
                item = stack.pop()
                if item == '(':
                    paren_matched = True
                    break
                else:
                    queue.append(item)
            # If the stack runs out without finding a left parenthesis, 
            # then there are mismatched parentheses
            if not paren_matched:
                print 'mismatched parenthesis'
                return None
        else:
            #TODO: failure mode here, token matches nothing we can identify
            print "Invalid token: " + token
            return None
    # When there are no more tokens to read
    # While there are still operator tokens in the stack
    while (len(stack) > 0):
        top = stack.pop()
        # If the operator token on the top of the stack is a parenthesis, 
        if top == '(' or top == ')':
             # then there are mismatched parentheses
            print 'mismatched parenthesis'
            return None
        # Pop the operator onto the output queue
        else:
            queue.append(top)
    return queue
        

def build_tree_2(queue):
    """ 
    Uses queue built in get_RPN method to build a tree ...
    Head node is returned in success
    None is returned in failure 
    """
    operators = [_and, _or]
    
    stack = list()
    while len(queue) > 0:
        item = queue.popleft();
        if item == '':
            pass
        elif type(item) is Variable:
            stack.append(TreeNode(value=item))
        elif item == _inclusive_not:
            right=stack.pop()
            stack.append(TreeNode(value=item, right=right, left=None, neg=False))
        elif item == _not:
            last_node = stack.pop()
            last_node.negate = not last_node.negate
            stack.append(last_node)
        elif item in operators:
            right=stack.pop()
            left= stack.pop()
            stack.append(TreeNode(value=item, right=right, left=left, neg=False))
    return stack.pop()


## gets a truth value given an expression Node
def calc_tree_2(node):
    # if leaf, it is a Variable
    if node.right is None and node.left is None:
        if node.negate:
            return not node.value.truth_value
        else:
            return node.value.truth_value
    elif node.value == _inclusive_not:
        if node.negate:
            return calc_tree_2(node.right)
        else:
            return not calc_tree_2(node.right)
    elif node.value == _and:
        return calc_tree_2(node.right) and calc_tree_2(node.left)
    elif node.value == _or:
        return calc_tree_2(node.right) or calc_tree_2(node.left)
    
    
def calc_tree_soft_2(node):
    # if leaf, it is a Variable
    if node.right is None and node.left is None:
        if node.negate:
            return not node.value.truth_value_soft
        else:
            return node.value.truth_value_soft
    elif node.value == _inclusive_not:
        if node.negate:
            return calc_tree_soft_2(node.right)
        else:
            return not calc_tree_soft_2(node.right)
    elif node.value == _and:
        return calc_tree_soft_2(node.right) and calc_tree_soft_2(node.left)
    elif node.value == _or:
        return calc_tree_soft_2(node.right) or calc_tree_soft_2(node.left)