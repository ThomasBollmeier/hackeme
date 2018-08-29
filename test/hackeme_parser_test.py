import sys
import unittest
import os

srcdir = os.path.abspath(os.path.dirname(__file__))
srcdir += os.sep + ".." + os.sep + "src"
sys.path.insert(0, srcdir)

from hackeme.frontend.hackeme_parser import HackemeParser

class ParserTest(unittest.TestCase):
    
    def setUp(self):
        
        self.parser = HackemeParser()
        
    def tearDown(self):
        
        self.parser = None
    
    def test_ok(self):

        f = open("data/demo.hackeme")
        code = f.read()
        f.close()
       
        ast = self.parser.parse(code)
        
        print(self.parser.error())
        
        self.assertTrue(ast)
        
        print(ast.to_xml())

        vardefs = ast.find_children_by_name('vardef')
        self.assertEqual(len(vardefs), 4)
        
        answer = int(vardefs[0].get_children()[0].value)
        self.assertEqual(answer, 42)
        
        fundefs = ast.find_children_by_name('fundef')
        self.assertEqual(len(fundefs), 3)
        
    def test_arities(self):

        f = open("data/mult_arity.hackeme")
        code = f.read()
        f.close()
       
        ast = self.parser.parse(code)
        self.assertTrue(ast)
        
        print(ast.to_xml())

if __name__ == "__main__":
    
    unittest.main()