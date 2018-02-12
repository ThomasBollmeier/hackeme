from komparse.grammar import Grammar
from komparse.translators import *
from komparse.parser import Parser
from komparse.ast import Ast

class HackemeGrammar(Grammar):
    
    def __init__(self):
        
        Grammar.__init__(self)
        
        self.g = self
        
        self._init_tokens()
        self._init_rules()
        
    def _init_tokens(self):
        
        self.add_token('NUMBER', '\d+')
    
    def _init_rules(self):
        
        self.rule('start',
                  OneOf(TokenType('NUMBER')),
                  is_root=True)
        self.set_ast_transform('start', self._start)
        
    def _start(self, ast):
        ret = Ast('hackeme')
        child = ast.get_children()[0]
        child.id = ''
        ret.add_child(child)
        return ret
    
if __name__ == "__main__":
    
    code = "42"
    
    parser = Parser(HackemeGrammar())
    
    ast = parser.parse(code)
    if ast:
        print(ast.to_xml())
    else:
        print(parser.error())