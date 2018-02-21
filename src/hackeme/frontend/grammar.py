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
        
        self.add_token('LIST_BEGIN', "'\(")
        self.add_token('LPAR', '\(')
        self.add_token('RPAR', '\)')
        self.add_token('PLUS', '\+')
        self.add_token('MINUS', '\-')
        
        self.add_token('IDENT', '[a-z][a-z0-9]*(-[a-z0-9]+)*[!?]?')
        self.add_token('VARARG', '[a-z][a-z0-9]*(-[a-z0-9]+)*\*')
        self.add_token('NUMBER', '\d+')
        self.add_token('BOOLEAN', '#t(rue)?|#f(alse)?')
        
    def _init_rules(self):
        
        self.rule('start',
                  Many(
                    OneOf(
                     Rule('definition'),
                     Rule('expr'))),
                  is_root=True)
        self.set_ast_transform('start', self._start)
        
        self.rule('definition',
                  OneOf(
                    Rule('vardef'),
                    Rule('fundef')))
        self.set_ast_transform('definition', lambda ast: ast.get_children()[0])
        
        self.rule('vardef',
                  Sequence(
                    TokenType('LPAR'),
                    TokenType('DEFINE'),
                    TokenType('IDENT', 'name'),
                    Rule('expr', 'value'),
                    TokenType('RPAR')))
        self.set_ast_transform('vardef', self._vardef)

        self.rule('fundef',
                  Sequence(
                    TokenType('LPAR'),
                    TokenType('DEFINE'),
                    TokenType('LPAR'),
                    TokenType('IDENT', 'name'),
                    Many(TokenType('IDENT', 'param')),
                    Optional(TokenType('VARARG', 'vararg')),
                    TokenType('RPAR'),
                    Many(
                        Rule('definition', 'localdef')),
                    OneOrMore(
                        Rule('expr', 'body')),
                    TokenType('RPAR')))
        self.set_ast_transform('fundef', self._fundef)
                
        self.rule('expr',
                  OneOf(
                    Rule('no_list'),
                    Rule('list')))
        self.set_ast_transform('expr', lambda ast: ast.get_children()[0])
        
        self.rule('no_list',
                  OneOf(
                    Rule('if_expr'),
                    Rule('call'),
                    TokenType('IDENT'),
                    TokenType('NUMBER'),
                    Rule('boolean')))
        self.set_ast_transform('no_list', lambda ast: ast.get_children()[0])
 
        self.rule('if_expr',
                  Sequence(
                    TokenType('LPAR'),
                    TokenType('IF'),
                    Rule('expr', 'test'),
                    Rule('expr', 'consequent'),
                    Rule('expr', 'alternate'),
                    TokenType('RPAR')))
        self.set_ast_transform('if_expr', self._if_expr)
 
        self.rule('call',
                  Sequence(
                    TokenType('LPAR'),
                    OneOf(
                        TokenType('IDENT', 'callee'),
                        Rule('call', 'callee'),
                        Rule('operator', 'callee')),
                    Many(Rule('expr', 'arg')),
                    TokenType('RPAR')))
        self.set_ast_transform('call', self._call)
        
        self.rule('operator',
                  OneOf(
                    TokenType('PLUS'),
                    TokenType('MINUS')))
        self.set_ast_transform('operator', self._operator)
 
        self.rule('boolean', TokenType('BOOLEAN'))
        self.set_ast_transform('boolean', self._boolean)
        
        self.rule('list',
                  Sequence(
                    TokenType('LIST_BEGIN'),
                    OneOrMore(
                        Rule('list_item', 'li')),
                    TokenType('RPAR')))
        self.set_ast_transform('list', self._list)
        
        self.rule('list_item',
                  OneOf(
                    Sequence(
                      TokenType('LPAR'),
                      OneOrMore(
                          Rule('list_item', 'li')),
                      TokenType('RPAR')),
                    Rule('no_list', 'single')))
        self.set_ast_transform('list_item', self._list_item)
        
    # AST transformations:
    
    def _start(self, ast):
        ret = Ast('hackeme')
        for child in ast.get_children():
            child.id = ''
            ret.add_child(child)
        return ret
    
    def _vardef(self, ast):
        ret = Ast('vardef')
        name_node = ast.find_children_by_id('name')[0]
        ret.set_attr('name', name_node.value)
        ret.add_children_by_id(ast, 'value')
        return ret
    
    def _fundef(self, ast):
        ret = Ast('fundef')
        name_node = ast.find_children_by_id('name')[0]
        ret.set_attr('name', name_node.value)
        params = Ast('parameters')
        ret.add_child(params)
        param_nodes = ast.find_children_by_id('param')
        for param_node in param_nodes:
            params.add_child(Ast('parameter', param_node.value))
        vararg = ast.find_children_by_id('vararg')
        if vararg:
            vararg = vararg[0]
            params.add_child(Ast('var', vararg.value[:-1]))
        localdefs = Ast('localdefs')
        ret.add_child(localdefs)
        localdefs.add_children_by_id(ast, 'localdef')
        body = Ast('body')
        ret.add_child(body)
        body.add_children_by_id(ast, 'body')
        return ret
    
    def _if_expr(self, ast):
        ret = Ast('if_expr')
        test = Ast('test')
        ret.add_child(test)
        test.add_children_by_id(ast, 'test')
        consequent = Ast('consequent')
        ret.add_child(consequent)
        consequent.add_children_by_id(ast, 'consequent')
        alternate = Ast('alternate')
        ret.add_child(alternate)
        alternate.add_children_by_id(ast, 'alternate')
        return ret
    
    def _call(self, ast):
        ret = Ast('call')
        callee = Ast('callee')
        ret.add_child(callee)
        callee.add_children_by_id(ast, 'callee')
        args = Ast('arguments')
        ret.add_child(args)
        args.add_children_by_id(ast, 'arg')
        return ret
    
    def _operator(self, ast):
        ret = Ast('operator')
        op = ast.get_children()[0].value
        ret.set_attr('value', op)
        return ret
    
    def _boolean(self, ast):
        child = ast.get_children()[0]
        if child.value == '#t' or child.value == '#true':
            return Ast('TRUE')
        else:
            return Ast('FALSE')
        
    def _list(self, ast):
        ret = Ast('list')
        ret.add_children_by_id(ast, 'li')
        return ret
    
    def _list_item(self, ast):
        children = ast.find_children_by_id('single')
        if children:
            ret = children[0]
            ret.id = ''
            return ret
        else:
            ret = Ast('list')
            ret.add_children_by_id(ast, 'li')
            return ret
    
