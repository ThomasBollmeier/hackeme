import sys
import unittest

sys.path.insert(0, "../src")

from hackeme.frontend.parser import make_parser
from hackeme.frontend.analyzer import Analyzer

class AnalyzerTest(unittest.TestCase):
    
    def setUp(self):
        
        self.parser = make_parser()
        self.analyzer = Analyzer()
        
    def tearDown(self):
        
        self.parser = None
        self.analyzer = None
    
    def test_ok(self):

        f = open("demo.hackeme")
        code = f.read()
        f.close()
       
        ast = self.parser.parse(code)
        self.assertTrue(ast)
        
        if self.analyzer.analyze(ast):
            print(ast.to_xml())
        else:
            errors = self.analyzer.get_errors()
            for error in errors:
                print(error)
                
    def test_err(self):

        f = open("demo_err.hackeme")
        code = f.read()
        f.close()
        
        ast = self.parser.parse(code)
        self.assertTrue(ast)
        
        result = self.analyzer.analyze(ast)
        self.assertFalse(result)
       
        errors = self.analyzer.get_errors()
        self.assertEqual(len(errors), 4)
        
        for error in errors:
            print(error)
            
        

if __name__ == "__main__":
    
    unittest.main()