from komparse.grammar import Grammar as BaseGrammar
from komparse.translators import OneOrMore, Many, Optional, Sequence, OneOf
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
        self.add_keyword('cond')
        
        self.add_token('LIST_BEGIN', "'\(")
        self.add_token('LPAR', '\(')
        self.add_token('RPAR', '\)')
        self.add_token('LSQB', '\[')
        self.add_token('RSQB', '\]')
        self.add_token('PLUS', '\+')
        self.add_token('MINUS', '\-')
        self.add_token('MULT', '\*')
        self.add_token('DIV', '/')
        self.add_token('MOD', '%')
        self.add_token('EQ', '=')
        self.add_token('NE', '<>')
        self.add_token('GT', '>')
        self.add_token('GE', '>=')
        self.add_token('LT', '<')
        self.add_token('LE', '<=')
        
        self.add_token('IDENT', '[a-z][a-z0-9]*(-[a-z0-9]+)*[!?]?')
        self.add_token('VARARG', '[a-z][a-z0-9]*(-[a-z0-9]+)*\*')
        self.add_token('NUMBER', '\d+')
        self.add_token('BOOLEAN', '#t(rue)?|#f(alse)?')
        self.add_token('STRING', r"\"([^\\\"]|\\\")*\"")
        
    def _init_rules(self):
        
        self.rule('start',
                  Many(
                    OneOf(
                     self.definition(),
                     self.expr())),
                  is_root=True)
        self.set_ast_transform('start', self._start)
        
        self.rule('definition',
                  OneOf(
                    self.vardef(),
                    self.fundef()))
        self.set_ast_transform('definition', lambda ast: ast.get_children()[0])
        
        self.rule('vardef',
                  Sequence(
                    self.LPAR(),
                    self.DEFINE(),
                    self.IDENT('name'),
                    self.expr('value'),
                    self.RPAR()))
        self.set_ast_transform('vardef', self._vardef)

        self.rule('fundef',
                  Sequence(
                    self.LPAR(),
                    self.DEFINE(),
                    self.LPAR(),
                    self.IDENT('name'),
                    Many(self.IDENT('param')),
                    Optional(self.VARARG('vararg')),
                    self.RPAR(),
                    Many(self.definition('localdef')),
                    OneOrMore(self.expr('body')),
                    self.RPAR()))
        self.set_ast_transform('fundef', self._fundef)
                
        self.rule('expr',
                  OneOf(
                    self.no_list(),
                    self.list()))
        self.set_ast_transform('expr', lambda ast: ast.get_children()[0])
        
        self.rule('no_list',
                  OneOf(
                    self.if_expr(),
                    self.cond_expr(),
                    self.call(),
                    self.IDENT(),
                    self.NUMBER(),
                    self.boolean(),
                    self.STRING()))
        self.set_ast_transform('no_list', lambda ast: ast.get_children()[0])
 
        self.rule('if_expr',
                  Sequence(
                    self.LPAR(),
                    self.IF(),
                    self.expr('test'),
                    self.expr('consequent'),
                    self.expr('alternate'),
                    self.RPAR()))
        self.set_ast_transform('if_expr', self._if_expr)
        
        self.rule('cond_expr',
                  Sequence(
                    self.LPAR(),
                    self.COND(),
                    OneOrMore(self.cond_branch('branch')),
                    self.RPAR()))
        self.set_ast_transform('cond_expr', self._cond_expr)
        
        self.rule('cond_branch',
                  Sequence(
                    self.LSQB(),
                    self.expr('test'),
                    self.expr('consequent'),
                    self.RSQB()))
        self.set_ast_transform('cond_branch', self._cond_branch)
 
        self.rule('call',
                  Sequence(
                    self.LPAR(),
                    OneOf(
                        self.IDENT('callee'),
                        self.call('callee'),
                        self.operator('callee')),
                    Many(self.expr('arg')),
                    self.RPAR()))
        self.set_ast_transform('call', self._call)
        
        self.rule('operator',
                  OneOf(
                    self.PLUS(),
                    self.MINUS(),
                    self.MULT(),
                    self.DIV(),
                    self.MOD(),
                    self.EQ(),
                    self.NE(),
                    self.GT(),
                    self.GE(),
                    self.LT(),
                    self.LE()))
        self.set_ast_transform('operator', self._operator)
 
        self.rule('boolean', self.BOOLEAN())
        self.set_ast_transform('boolean', self._boolean)
        
        self.rule('list',
                  Sequence(
                    self.LIST_BEGIN(),
                    OneOrMore(self.list_item('li')),
                    self.RPAR()))
        self.set_ast_transform('list', self._list)
        
        self.rule('list_item',
                  OneOf(
                    Sequence(
                      self.LPAR(),
                      OneOrMore(
                          self.list_item('li')),
                      self.RPAR()),
                    self.no_list('single')))
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
    
    def _cond_expr(self, ast):
        ret = Ast('cond')
        ret.add_children_by_id(ast, 'branch')
        return ret
    
    def _cond_branch(self, ast):
        ret = Ast('branch')
        test = Ast('test')
        ret.add_child(test)
        test.add_children_by_id(ast, 'test')
        consequent = Ast('consequent')
        ret.add_child(consequent)
        consequent.add_children_by_id(ast, 'consequent')
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
    
