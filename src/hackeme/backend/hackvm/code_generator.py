from hackeme.backend.code_generator import CodeGenerator as BaseCodeGenerator
from .type_codes import TypeCodes

class CodeGenerator(BaseCodeGenerator):
    
    def __init__(self, ast, scope_manager, output):
        BaseCodeGenerator.__init__(self, ast, scope_manager, output)
    
    def gen_list(self, lst):
        elements = lst.get_children()[:]
        elements.reverse()
        
        
    def _gen_list_pair(self, expr):
        self._writeln("push constant 4")
        self._writeln("call Memory.alloc 1")
        self._writeln("pop pointer 0")
        # Set type info:
        self._writeln("push constant {}".format(TypeCodes.LIST))
        self._writeln("pop this 0")
        # Set ref counter:
        self._writeln("push constant 0")
        self._writeln("pop this 1")
        # Set content (car):
        segment, idx = self._get_segment_idx(expr)
        self._writeln("push {} {}".format(segment, idx))
        self._writeln("pop this 2")
        # Set pointer to next (cdr) = nil:
        self._writeln("push constant 0")
        self._writeln("pop this 3")
        # set result
        self._writeln("push pointer 0")
        
    def _writeln(self, s):
        self._output.writeln(s)
        
    def _get_segment_idx(self, expr):
        return "constant", 0 # todo 
        