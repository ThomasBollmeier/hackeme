class SymbolTable(object):
    
    def __init__(self, id_, parent=None):
        self._id = id_
        self._parent = parent
        self._symbols = {}
        
    def get_scope_id(self):
        return self._id
        
    def get_parent(self):
        return self._parent
        
    def add(self, entry):
        self._symbols[entry.get_name()] = entry
        
    def get_entry(self, name, search_in_parents=True):
        if search_in_parents:
            symtab = self
            while symtab:
                if name in symtab._symbols:
                    return symtab._symbols[name]
                symtab = symtab._parent
            return None
        else:
            return (name in self._symbols) and self._symbols[name] or None
    
    def get_defining_scope(self, name):
        symtab = self
        while symtab:
            if name in symtab._symbols:
                return symtab.get_scope_id()
            symtab = symtab._parent
        return None