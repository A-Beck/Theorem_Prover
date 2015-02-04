import re

class Parser:

    def parse(self, input):
        match_teach = re.match(r'[T/t]each (.*?) (->|=) (.*)', input)
        match_list = re.match(r'list', input, re.I)
        match_learn = re.match(r'learn', input, re.I)
        match_query = re.match(r'[Q/q]uery', input)

        if match_teach:
            print 'Teaching...'
            
            lhs = match_teach.group(1)
            operator = match_teach.group(2)
            rhs = match_teach.group(3)

            print 'LHS: ' + lhs
            print 'Operator: ' + operator
            print 'RHS: ' + rhs

            if operator == '=':
                if rhs.startswith('"') and rhs.endswith('"'):
                    rhs_stripped = rhs[1:-1]
                    print 'Definition: ' + rhs_stripped
                elif rhs.lower() == 'true':
                    print 'Boolean Value: ' + rhs.lower()
                elif rhs.lower() == 'false':
                    print 'Boolean Value: ' + rhs.lower()
                else:
                    print 'Unrecognized RHS' 

        elif match_list:
            print 'Listing...'
        elif match_learn:
            print 'Learning...'
        elif match_query:
            print 'Querying...'
        else:
            print 'Unrecognized LHS'
