class SymtabEntry(object):
    
    VAR = 1
    FUNC = 2
    
    def __init__(self, name, kind):
        self._name = name
        self._kind = kind
        
    def get_name(self):
        return self._name
    
        
class VarEntry(SymtabEntry):
    
    def __init__(self, name):
        SymtabEntry.__init__(self, name, SymtabEntry.VAR)
        

class FuncEntry(SymtabEntry):
    
    def __init__(self, name):
        SymtabEntry.__init__(self, name, SymtabEntry.FUNC)
