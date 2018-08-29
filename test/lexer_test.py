import sys
import unittest

sys.path.insert(0, "../src")

from hackeme.frontend.hackeme_parser import HackemeParser
from komparse.scanner import Scanner
from komparse.char_stream import StringStream

class LexerTest(unittest.TestCase):
    
    def setUp(self):
        
        self.grammar = HackemeParser()._grammar
        
    def tearDown(self):
        
        self.grammar = None
    
    def test_ok(self):
        
        f = open("data/demo.hackeme")
        code = f.read()
        f.close()
                
        scanner = Scanner(StringStream(code), self.grammar)
        
        while scanner.has_next():
            token = scanner.advance()
            print(token)
            

if __name__ == "__main__":
    
    unittest.main()