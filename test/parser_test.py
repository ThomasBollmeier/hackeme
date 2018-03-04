import sys
import unittest

sys.path.insert(0, "../src")

from hackeme.frontend.parser import make_parser

class ParserTest(unittest.TestCase):
    
    def setUp(self):
        
        self.parser = make_parser()
        
    def tearDown(self):
        
        self.parser = None
    
    def test_ok(self):

        f = open("demo.hackeme")
        code = f.read()
        f.close()
       
        ast = self.parser.parse(code)
        
        print(self.parser.error())
        
        self.assertTrue(ast)
        
        print(ast.to_xml())

        vardefs = ast.find_children_by_name('vardef')
        self.assertEqual(len(vardefs), 2)
        
        answer = int(vardefs[0].get_children()[0].value)
        self.assertEqual(answer, 42)
        
        fundefs = ast.find_children_by_name('fundef')
        self.assertEqual(len(fundefs), 3)
        

if __name__ == "__main__":
    
    unittest.main()