from datastructures import Variable, Rule, Expression
from datastructures import variables, facts_raw, rules
from datastructures import forward_chain, query, why
from helper import find_var
import re

class Parser(object):

    def parse(self, input):
        # Regex patterns for recognizing commands
        match_teach = re.match(r'[T/t]each (.*?) (->|=) (.*)', input)
        match_list = re.match(r'list', input, re.I)
        match_learn = re.match(r'learn', input, re.I)
        match_query = re.match(r'[Q/q]uery (.*)', input)
        match_why = re.match(r'[W/w]hy (.*)', input)
        match_demon = re.match(r'Summon', input, re.I)
        match_exit = re.match(r'exit', input, re.I)

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
                    flag = False
                    for i,var, in enumerate(variables):
                        if var.name == lhs:
                            flag = True
                            var.truth_value = True
                            variables[i] = var
                            facts_raw.append(var)
                            break
                    if not flag: print 'Variable doesn\'t exist'
                # Asserting false
                elif rhs.lower() == 'false':
                    flag = False
                    for i,var, in enumerate(variables):
                        if var.name == lhs:
                            flag = True
                            var.truth_value = False
                            variables[i] = var
                            facts_raw.append(var)
                            break
                    if not flag: print 'Variable doesn\'t exist'
                else:
                    print 'Unrecognized RHS'
            
            # New Rule
            elif operator == '->':
                new_rule = Rule(Expression(lhs), find_var(variables,rhs))
                rules.append(new_rule)


        elif match_list:
            print 'Variables:'
            for variable in variables:
                print '\t{}'.format(variable)

            print 'Facts:'
            for fact in facts_raw:
                if fact.truth_value is True:
                    print '\t{}'.format(fact.name)

            print 'Rules:'
            for rule in rules:
                print '\t{}'.format(rule)

        elif match_learn:
            forward_chain(rules, facts_raw)

        elif match_query:
            exp = match_query.group(1)
            expr = Expression(exp)
            expr_truth_value = query(expr)
            print expr_truth_value

        elif match_why:
            exp = match_why.group(1)
            expr = Expression(exp)
            why_tuple = why(expr)
            # print why_tuple[0]
            # print why_tuple[1]

        elif match_demon:
            pentagram = """MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMds+:--------:+sdNMMMMMMMMMMM
MMMMMMMMms:-+sdNMMMMMMMMNdy+--omMMMMMMMM
MMMMMMh:` /mMMMMMMMMMMMMMMMMm+ `-yMMMMMM
MMMMd--hN``--sNMMMMMMMMMMNy:..`md:.hMMMM
MMM+`yMMMy hd+./hMMMMMMh/.+dd sMMMh`/MMM
MM:.mMMMMM:.NMMh/.+dd+./hMMM--MMMMMm--NM
M+`mMMMMMMN`+MMMMm-  .dMMMMo mMMMMMMN.:M
d yMMMMMMMMy dNy:.omNs--sNm oMMMMMMMMh h
/`MMMMMMMMMM.`.+dMMMMMMm+.``NMMMMMMMMM-:
.:MMMMMMMd+./`oMMMMMMMMMMs /.+dMMMMMMM/`
.:MMMMmo.:yNMs dMMMMMMMMm`oMNy:.omMMMM/`
/`MNy:.omMMMMM--MMMMMMMM:.MMMMMNs--sNM.:
d -` :++++++++: /++++++/ :++++++++:  : h
M+ yddddddddddd+ yddddy /dddddddddddy`/M
MM/.mMMMMMMMMMMM.-MMMM/.NMMMMMMMMMMm.:NM
MMMo`sMMMMMMMMMMd sMMy hMMMMMMMMMMy`+MMM
MMMMd--hMMMMMMMMM+`mN`/MMMMMMMMMh--hMMMM
MMMMMMh:.omMMMMMMN.:/`NMMMMMMms.:hMMMMMM
MMMMMMMMNs:./shmMMh  yMMNds/.:smMMMMMMMM
MMMMMMMMMMMMdy+/---``---:+sdMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"""
            print pentagram
            print '-Copyright: http://www.retrojunkie.com/asciiart/myth/pentagrm.htm \n'
            musk_quote = """With artifical intellegence we are summoning the demon. You know all those stories where there's the guy with the pentagram and the holy water, and it's like yeah, he's sure he can control the demon. Doesn't work out. - Elon Musk"""
            print musk_quote + '\n'
            
        elif match_exit:
            print "Thanks for using SkynetBot! Please come again!"
            exit()
            
        else:
            print 'Unrecognized LHS'
