from datastructures import *

A = Variable("A", "string A", True)
B = Variable("B", "string B", True)
C = Variable("C", "string C", False)

variables.append(A)
variables.append(B)
variables.append(C)

facts_raw.append(A)
facts_raw.append(B)

exp = Expression('A & B')
rule = Rule(exp, C)
print rule

rules.append(rule)

truth = query(Expression('A & C'))

#truth = exp.soft_evaluate()

print str(truth)