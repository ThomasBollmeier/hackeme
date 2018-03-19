from .symbol_table import SymbolTable

class Pass1(object):
    
    def walk_root(self, ast):
        self._symtab = SymbolTable()
        for child in ast.get_children():
            if child.name == "vardef":
                self._walk_vardef(child)
            elif child.name == "fundef":
                pass
            else:
                pass
            
    def _walk_vardef(self, vardef):
        var_name = vardef.get_attr('name')
        value = None # <-- TDOD: evaluate
        self._symtab.add(var_name, SymbolTable.VAR, value)

class Analyzer(object):
    
    def analyze(self, ast):
        self._symbols = []