from komparse.grammar import Grammar as BaseGrammar
from komparse.translators import *
from komparse.parser import Parser
from komparse.ast import Ast

class Grammar(BaseGrammar):
    
    def __init__(self):
        
        BaseGrammar.__init__(self)
        
        self._init_tokens()
        self._init_rules()
        
    def _init_tokens(self):
        
        self.add_comment(';', '\n')
        self.add_comment('#|', '|#')

        self.add_keyword('define')
        self.add_keyword('if')
        
        self.add_token('LPAR', '\(')
        self.add_token('RPAR', '\)')
        
        self.add_token('IDENT', '[a-z][a-z0-9]*(-[a-z0-9]+)*')
        self.add_token('NUMBER', '\d+')
        self.add_token('BOOLEAN', '#t(rue)?|#f(alse)?')
        
    def _init_rules(self):
        
        self.rule('start',
                  Many(
                    OneOf(
                     Rule('definition'),
                     Rule('expr'))),
                  is_root=True)
        
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
        
        self.rule('expr',
                  OneOf(
                    Rule('if_expr'),
                    Rule('call'),
                    TokenType('IDENT'),
                    TokenType('NUMBER'),
                    TokenType('BOOLEAN')))
 
        self.rule('if_expr',
                  Sequence(
                    TokenType('LPAR'),
                    TokenType('IF'),
                    TokenType('LPAR'),
                    Rule('expr', 'test'),
                    TokenType('RPAR'),
                    Rule('expr', 'consequent'),
                    Rule('expr', 'alternate'),
                    TokenType('RPAR')))
 
        self.rule('call',
                  Sequence(
                    TokenType('LPAR'),
                    OneOf(
                        TokenType('IDENT', 'callee'),
                        Rule('call', 'callee')),
                    Many(Rule('expr', 'arg')),
                    TokenType('RPAR')))
        
