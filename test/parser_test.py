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
        
        code = """
        (define my-answer 42) ; the answer to everything
        (if (#true)
            result
            (my-func first-arg result))
        (define (this-is-a-function a-param))
        (define (writeln words*))
        (define (even? n))
        '((this-is-a-function 23) 1 2 3 (4 5 (7 8 9)))
        """
        
        ast = self.parser.parse(code)
        
        self.assertTrue(ast)
        
        print(ast.to_xml())

        vardefs = ast.find_children_by_name('vardef')
        self.assertEqual(len(vardefs), 1)
        
        answer = int(vardefs[0].get_children()[0].value)
        self.assertEqual(answer, 42)
        
        fundefs = ast.find_children_by_name('fundef')
        self.assertEqual(len(fundefs), 3)
        

if __name__ == "__main__":
    
    unittest.main()