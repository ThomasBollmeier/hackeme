import sys
import unittest

sys.path.insert(0, "../src")

from hackeme.frontend import parse_analyze

class AnalyzerTest(unittest.TestCase):
    
    def test_ok(self):
        
        ast, errors, scope_mgr = parse_analyze(self._read_code("data/demo.hackeme"))
        
        self.assertTrue(ast)
        self.assertFalse(errors)
        
        print(ast.to_xml())
        
    def test_not_ok(self):
        
        ast, errors, scope_mgr = parse_analyze(self._read_code("data/demo_err.hackeme"))
        
        self.assertFalse(ast)
        self.assertTrue(errors)
        
        for error in errors:
            print(error)
            

    def _read_code(self, file_path):
        f = open(file_path)
        code = f.read()
        f.close()
        return code


if __name__ == "__main__":
    
    unittest.main()