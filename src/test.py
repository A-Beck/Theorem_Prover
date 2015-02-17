from datastructures import *
import unittest


class Test(unittest.TestCase):

    def setUp(self):

        #set up variables

        var1 = Variable('S', 'Sam likes Ice Cream')
        var2 = Variable('V', 'Sam eats Ice Cream')
        var3 = Variable('A', 'Sam is fat')
        var4 = Variable('B', 'Sam dies')
        var5 = Variable('C', 'Sam is skinny')
        var6 = Variable('D', 'Sam lives')
        var7 = Variable('E', 'Sam is vegan')

        variables.extend([
            var1,
            var2,
            var3,
            var4,
            var5,
            var6,
            var7
        ])

        var1.truth_value = True
        facts_raw.append(var1)

        var3.truth_value = True
        facts_raw.append(var3)

        var4.truth_value = False
        facts_raw.append(var4)

        # set up expressions

        self.exp1 = Expression('S&V')  # True 
        self.exp2 = Expression('!(B)')  # True
        self.exp3 = Expression('!(!(S|V)&(!B))')  # not (not (True and True) and ( not False)) --> True
	self.exp4 = Expression('B|!A')  # (False or  not True) --> False
       	self.exp5 = Expression('! (S&A) | (!A|B)')  # not (true and true) or (not true or false)) --> false 

	 # set up rules

        rule1 = Rule(Expression('S'), var2)
        rules.append(rule1)

        rule2 = Rule(self.exp2, var6)
        rules.append(rule2)

    def test_query(self):
        self.assertTrue(query(self.exp1))
        self.assertTrue(query(self.exp2))
        self.assertTrue(query(self.exp3))
	self.assertFalse(query(self.exp4))
	self.assertFalse(query(self.exp5))	

    def test_forward_chain(self):
        pass

    def test_why(self):
        """Print line testing why()"""
        why(Expression('A'))   # simplest case (true)
	print '\n'
	why(Expression('!A'))  # A simple not case (false)
	print '\n'
	why(self.exp1)  # simple (true) 'and' expression
	print '\n'
	why(Expression('!S&V'))   # simple (false) 'and' and not expression
	print '\n'
	why(Expression('B|A'))   # simple (true) 'or' expression
	print '\n'
	why(self.exp4)   # simple (false) 'or' and 'not' expression
	print '\n'
	why(self.exp3)  # complex (true) expression with 'ands' and 'nots' and 'ors'
	print '\n'
	why(self.exp5)  # complex (false) expression with all operators		


if __name__ == '__main__':
    unittest.main()
