from datastructures import Variable
from datastructures import variables, facts_raw, rules
import re

class Parser(object):

    def parse(self, input):
        # Regex patterns for recognizing commands
        match_teach = re.match(r'[T/t]each (.*?) (->|=) (.*)', input)
        match_list = re.match(r'list', input, re.I)
        match_learn = re.match(r'learn', input, re.I)
        match_query = re.match(r'[Q/q]uery (.*)', input)
        match_why = re.match(r'[W/w]hy (.*)', input)


        if match_teach:            
            lhs = match_teach.group(1)
            operator = match_teach.group(2)
            rhs = match_teach.group(3)

            # New variable or assertion
            if operator == '=':
                # New variable
                if rhs.startswith('"') and rhs.endswith('"'):
                    rhs_stripped = rhs[1:-1]
                    new_var = Variable(lhs, rhs_stripped)
                    if new_var not in variables:
                        variables.append(new_var)
                    else:
                        print 'Variable {} already exists'.format(new_var.name)
                # Asserting true
                elif rhs.lower() == 'true':
                    for i,var, in enumerate(variables):
                        if var.name == lhs:
                            var.truth_value = True
                            variables[i] = var
                            facts_raw.append(var)
                        else:
                            print 'Variable doesn\'t exist'
                # Asserting false
                elif rhs.lower() == 'false':
                    for i, var in enumerate(variables):
                        if var.name == lhs:
                            var.truth_value = False
                            variables[i] = var
                            if var in facts_raw:
                                facts_raw.remove(var)
                        else:
                            print 'Variable doesn\'t exist'
                else:
                    print 'Unrecognized RHS'
            
            # New Rule
            elif operator == '->':
                print 'New rule'

        elif match_list:
            print 'Variables:'
            for variable in variables:
                print '\t{}'.format(variable)

            print 'Facts:'
            for fact in facts_raw:
                print '\t{}'.format(fact.name)

            print 'Rules:'

        elif match_learn:
            print 'Learning...'

        elif match_query:
            print 'Querying...'
            exp = match_query.group(1)

        elif match_why:
            print 'Explaining why...'
            exp = match_why.group(1)

        else:
            print 'Unrecognized LHS'
