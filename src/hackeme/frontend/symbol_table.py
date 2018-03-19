class SymbolTable(object):
    
    VAR = 1
    FUNC = 2
    
    def __init__(self, parent=None):
        self._parent = parent
        self._symbols = {}
        
    def add(self, name, kind, value):
        self._symbols[name] = (kind, value)