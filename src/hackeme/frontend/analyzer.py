from .scope_manager import ScopeManager
from .symtab_entry import Kind, SymtabEntry, FuncEntry

class Pass1(object):
    
    def walk_root(self, scope, scope_mgr, ast):
        
        self._scope = scope
        self._scope_mgr = scope_mgr
        
        for child in ast.get_children():
            if child.name == "vardef":
                self._walk_vardef(child)
            elif child.name == "fundef":
                self._walk_fundef(child)
            else:
                pass
            
    def _walk_vardef(self, vardef):
        var_name = vardef.get_attr('name')
        self._scope.add(SymtabEntry(var_name, self._var_kind()))
        self._set_defining_scope(vardef)
        
    def _walk_fundef(self, fundef):
        
        fun_name = fundef.get_attr('name')
        
        self._scope.add(FuncEntry(fun_name, self._var_kind()))
        self._set_defining_scope(fundef)
        self._scope = self._scope_mgr.new_scope(self._scope)
        
        for child in fundef.get_children():
            if child.name == "parameters":
                self._walk_params(child)
            elif child.name == "localdefs":
                self._walk_localdefs(child)
        
        self._scope = self._scope.get_parent()
                
    def _walk_params(self, params):
        for param in params.get_children():
            self._scope.add(SymtabEntry(param.value, Kind.PARAM))
            self._set_defining_scope(param)
            
    def _walk_localdefs(self, localdefs):
        for child in localdefs.get_children():
            if child.name == "vardef":
                self._walk_vardef(child)
            elif child.name == "fundef":
                self._walk_fundef(child)
        
    def _var_kind(self):
        if self._scope.get_parent() is not None:
            return Kind.LOCAL_VAR
        else:
            return Kind.GLOBAL_VAR
        
    def _set_defining_scope(self, ast):
        ast.set_attr('scope', self._scope.get_scope_id())

class Analyzer(object):
    
    def __init__(self):
        self._scope_mgr = ScopeManager()
    
    def analyze(self, ast):
        
        global_scope = self._scope_mgr.new_scope()
        
        Pass1().walk_root(global_scope, self._scope_mgr, ast)
        