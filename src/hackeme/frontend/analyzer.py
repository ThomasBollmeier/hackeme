from .symbol_table import SymbolTable
from .symtab_entry import Kind, SymtabEntry, FuncEntry

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
        self._symtab.add(SymtabEntry(var_name, self._var_kind()))
        self._set_defining_scope(vardef)
        
    def _walk_fundef(self, fundef):
        fun_name = fundef.get_attr('name')
        self._symtab.add(FuncEntry(fun_name, self._var_kind()))
        self._set_defining_scope(fundef)
        for child in fundef.get_children():
            if child.name == "parameters":
                self._walk_params(child)
                
    def _walk_params(self, params):
        self._symtab = SymbolTable(self._symtab)
        for param in params.get_children():
            self._symtab.add(SymtabEntry(param.value, Kind.PARAM))
            self._set_defining_scope(param)
        self._symtab = self._symtab.get_parent()
        
    def _var_kind(self):
        if self._symtab.get_parent() is not None:
            return Kind.LOCAL_VAR
        else:
            return Kind.GLOBAL_VAR
        
    def _set_defining_scope(self, ast):
        ast.set_attr('scope', self._symtab.get_scope_id())

class Analyzer(object):
    
    def analyze(self, ast):
        Pass1().walk_root(ast)
        