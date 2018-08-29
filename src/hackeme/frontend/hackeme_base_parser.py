from komparse import Parser, Grammar, Sequence, OneOf, \
    Optional, OneOrMore, Many


class _Grammar(Grammar):
    
    def __init__(self):
        Grammar.__init__(self, case_sensitive=True)
        self._init_tokens()
        self._init_rules()
    
    def _init_tokens(self):
        self.add_comment(';', '\n')
        self.add_comment('#|', '|#')
        self.add_string('"', '"', '\\', 'STRING')
        self.add_token('LIST_BEGIN', '\'\(')
        self.add_token('LPAR', '\(')
        self.add_token('RPAR', '\)')
        self.add_token('LSQBR', '\[')
        self.add_token('RSQBR', '\]')
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
        self.add_keyword('define')
        self.add_keyword('if')
        self.add_keyword('cond')
    
    def _init_rules(self):
        self.rule('start', Many(self._oneof_1()), is_root=True)
        self.rule('definition', self._oneof_2())
        self.rule('vardef', self._seq_1())
        self.rule('fundef', self._seq_2())
        self.rule('expr', self._oneof_3())
        self.rule('no_list', self._oneof_4())
        self.rule('if_expr', self._seq_3())
        self.rule('cond_expr', self._seq_4())
        self.rule('cond_branch', self._seq_5())
        self.rule('call', self._seq_6())
        self.rule('operator', self._oneof_6())
        self.rule('boolean', self.BOOLEAN())
        self.rule('list', self._seq_7())
        self.rule('list_item', self._oneof_7())
    
    def _seq_1(self):
        return Sequence(
            self.LPAR(),
            self.DEFINE(),
            self.IDENT('name'),
            self.expr('value'),
            self.RPAR())
    
    def _seq_2(self):
        return Sequence(
            self.LPAR(),
            self.DEFINE(),
            self.LPAR(),
            self.IDENT('name'),
            Many(self.IDENT('param')),
            Optional(self.VARARG('vararg')),
            self.RPAR(),
            Many(self.definition('localdef')),
            OneOrMore(self.expr('body')),
            self.RPAR())
    
    def _seq_3(self):
        return Sequence(
            self.LPAR(),
            self.IF(),
            self.expr('test'),
            self.expr('consequent'),
            self.expr('alternate'),
            self.RPAR())
    
    def _seq_4(self):
        return Sequence(
            self.LPAR(),
            self.COND(),
            OneOrMore(self.cond_branch('branch')),
            self.RPAR())
    
    def _seq_5(self):
        return Sequence(
            self.LSQBR(),
            self.expr('test'),
            self.expr('consequent'),
            self.RSQBR())
    
    def _seq_6(self):
        return Sequence(
            self.LPAR(),
            self._oneof_5(),
            Many(self.expr('arg')),
            self.RPAR())
    
    def _seq_7(self):
        return Sequence(
            self.LIST_BEGIN(),
            OneOrMore(self.list_item('li')),
            self.RPAR())
    
    def _seq_8(self):
        return Sequence(
            self.LPAR(),
            OneOrMore(self.list_item('li')),
            self.RPAR())
    
    def _oneof_1(self):
        return OneOf(
            self.definition(),
            self.expr())
    
    def _oneof_2(self):
        return OneOf(
            self.vardef(),
            self.fundef())
    
    def _oneof_3(self):
        return OneOf(
            self.no_list(),
            self.list())
    
    def _oneof_4(self):
        return OneOf(
            self.if_expr(),
            self.cond_expr(),
            self.call(),
            self.IDENT(),
            self.NUMBER(),
            self.boolean(),
            self.STRING())
    
    def _oneof_5(self):
        return OneOf(
            self.IDENT('callee'),
            self.call('callee'),
            self.operator('callee'))
    
    def _oneof_6(self):
        return OneOf(
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
            self.LE())
    
    def _oneof_7(self):
        return OneOf(
            self._seq_8(),
            self.no_list('single'))
    
    
class HackemeBaseParser(Parser):
    
    def __init__(self):
        Parser.__init__(self, _Grammar())
        
    
