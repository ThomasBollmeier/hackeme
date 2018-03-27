class SymbolTable(object):
    
    _next_id = 1
    _sym_tabs = {}
    
    @staticmethod
    def find(id_):
        return SymbolTable._sym_tabs[id_]
    
    def __init__(self, parent=None):
        self._id = SymbolTable._next_id
        SymbolTable._next_id += 1
        SymbolTable._sym_tabs[self._id] = self
        
        self._parent = parent
        self._symbols = {}
        
    def get_scope_id(self):
        return self._id
        
    def get_parent(self):
        return self._parent
        
    def add(self, entry):
        self._symbols[entry.get_name()] = entry
        
    def get_entry(self, name):
        symtab = self
        while symtab:
            if name in symtab._symbols:
                return symtab._symbols[name]
            symtab = symtab._parent
        return None
    
    def get_defining_scope(self, name):
        symtab = self
        while symtab:
            if name in symtab._symbols:
                return symtab.get_scope_id()
            symtab = symtab._parent
        return None