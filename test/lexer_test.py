import sys
import unittest

sys.path.insert(0, "../src")

from hackeme.frontend.parser import make_parser

class LexerTest(unittest.TestCase):
    
    def setUp(self):
        
        self.lexer = make_parser()._scanner
        
    def tearDown(self):
        
        self.lexer = None
    
    def test_ok(self):
        
        f = open("demo.hackeme")
        code = f.read()
        f.close()
                
        stream = self.lexer.find_tokens(code)
        
        while stream.has_next():
            token = stream.advance()
            print(token)
            

if __name__ == "__main__":
    
    unittest.main()