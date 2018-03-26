from .symbol_table import SymbolTable
from .symtab_entry import VarEntry, FuncEntry

class Pass1(object):
    
    def walk_root(self, ast):
        self._symtab = SymbolTable()
        for child in ast.get_children():
            if child.name == "vardef":
                self._walk_vardef(child)
            elif child.name == "fundef":
                self._walk_fundef(child)
            else:
                pass
            
    def _walk_vardef(self, vardef):
        var_name = vardef.get_attr('name')
        self._symtab.add(VarEntry(var_name))
        
    def _walk_fundef(self, fundef):
        fun_name = fundef.get_attr('name')
        self._symtab.add(FuncEntry(fun_name))
        

class Analyzer(object):
    
    def analyze(self, ast):
        self._symbols = []