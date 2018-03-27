class TypeCatg:
    SIMPLE = 1
    STRUCT = 2
    LIST = 3
    FUNCTION = 4
    UNKNOWN = 99
    
    
class Kind:
    GLOBAL_VAR = 1
    LOCAL_VAR = 2
    PARAM = 3
    
    
class SymtabEntry(object):
    
    def __init__(self, name, kind, type_catg = TypeCatg.UNKNOWN):
        self._name = name
        self._kind = kind
        self._type_catg = type_catg
        
    def get_name(self):
        return self._name
    
    def get_kind(self):
        return self._kind
    
    def get_type_catg(self):
        return self._type_catg
    
        
class SimpleEntry(SymtabEntry):
    
    def __init__(self, name, kind):
        SymtabEntry.__init__(self, name, kind, TypeCatg.SIMPLE)
        

class FuncEntry(SymtabEntry):
    
    def __init__(self, name, kind):
        SymtabEntry.__init__(self, name, kind, TypeCatg.FUNCTION)
