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

        self.exp1 = Expression('S&V')
        self.exp2 = Expression('!(B)')
        self.exp3 = Expression('!(!(S|V)&(!B))')
        # not (not (True and True) and ( not False)) --> True

        # set up rules

        rule1 = Rule(Expression('S'), var2)
        rules.append(rule1)

        rule2 = Rule(self.exp2, var6)
        rules.append(rule2)

    def test_query(self):
        self.assertTrue(query(self.exp1))
        self.assertTrue(query(self.exp2))
        self.assertTrue(query(self.exp3))

    def test_forward_chain(self):
        pass

    def test_why(self):
        """Print line testing why()"""
        why(Expression('A'))  # simplest case
	print '\n'
	why(Expression('!A')) # A slightly more complex case
	print '\n'
	why(self.exp1)	# simple expression test
	print '\n'
	why(self.exp3)
	print '\n'
		


if __name__ == '__main__':
    unittest.main()
