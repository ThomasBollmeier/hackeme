class SymbolTable(object):
    
    def __init__(self, parent=None):
        self._parent = parent
        self._symbols = {}
        
    def add(self, entry):
        self._symbols[entry.get_name()] = entry
        
    def get_entry(self, name):
        symtab = self
        while symtab:
            if name in symtab._symbols:
                return symtab._symbols[name]
            symtab = symtab._parent
        return None