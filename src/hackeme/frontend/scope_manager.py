from .symbol_table import SymbolTable

class ScopeManager(object):
    
    def __init__(self):
        self._next_id = 1
        self._scopes = {}
    
    def new_scope(self, parent=None):
        scope = SymbolTable(self._next_id, parent)
        self._scopes[self._next_id] = scope
        self._next_id += 1
        return scope
    
    def find_scope(self, id_):
        return self._scopes[id_]