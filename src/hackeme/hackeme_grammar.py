from komparse.grammar import Grammar
from komparse.translators import *
from komparse.parser import Parser
from komparse.ast import Ast

class HackemeGrammar(Grammar):
    
    def __init__(self):
        
        Grammar.__init__(self)
        
        self._init_tokens()
        self._init_rules()
        
    def _init_tokens(self):

        self.add_keyword('define')
        self.add_keyword('if')
        
        self.add_token('LPAR', '\(')
        self.add_token('RPAR', '\)')
        
        self.add_token('IDENT', '[a-z][a-z0-9]*(-[a-z0-9]+)*')
        self.add_token('NUMBER', '\d+')
        
    def _init_rules(self):
        
        self.rule('start',
                  Many(
                    OneOf(
                     Rule('special_form'),
                     Rule('expr'))),
                  is_root=True)
        
        self.rule('special_form',
                  OneOf(
                    Rule('definition'),
                    Rule('if_expr')))
        
        self.rule('definition',
                  OneOf(
                    Rule('vardef'),
                    Rule('fundef')))
        
        self.rule('vardef',
                  Sequence(
                    TokenType('LPAR'),
                    TokenType('DEFINE'),
                    TokenType('IDENT', 'name'),
                    Rule('expr', 'value'),
                    TokenType('RPAR')))

        self.rule('fundef',
                  Sequence(
                    TokenType('LPAR'),
                    TokenType('DEFINE'),
                    TokenType('LPAR'),
                    TokenType('IDENT', 'name'),
                    Many(TokenType('IDENT', 'param')),
                    TokenType('RPAR'),
                    TokenType('RPAR')))
        
        self.rule('if_expr',
                  Sequence(
                    TokenType('LPAR'),
                    TokenType('IF'),
                    TokenType('RPAR')))
        
        self.rule('expr',
                  OneOf(
                    Rule('if_expr'),
                    Rule('call'),
                    TokenType('IDENT'),
                    TokenType('NUMBER')))

        self.rule('call',
                  Sequence(
                    TokenType('LPAR'),
                    OneOf(
                        TokenType('IDENT', 'callee'),
                        Rule('call', 'callee')),
                    Many(Rule('expr', 'arg')),
                    TokenType('RPAR')))
        
        
if __name__ == "__main__":
    
    code = """
    (define my-answer 42)
    (define (this-is-a-function a-param))
    (this-is-a-function 23 some-arg)
    """
    
    parser = Parser(HackemeGrammar())
    
    ast = parser.parse(code)
    if ast:
        print(ast.to_xml())
    else:
        print(parser.error())