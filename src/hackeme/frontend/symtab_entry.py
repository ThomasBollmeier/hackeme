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
        self._num_params = 0
        self._has_var_arg = False
        
    def inc_num_params(self):
        self._num_params += 1
        
    def get_num_params(self):
        return self._num_params
    
    def get_min_num_params(self):
        return self._num_params
    
    def get_max_num_params(self):
        if not self._has_var_arg:
            return self._num_params
        else:
            return None
        
    def set_var_arg_support(self):
        self._has_var_arg = True
        
        
class ParamEntry(SymtabEntry):
    
    def __init__(self, func_entry, name, type_catg = TypeCatg.UNKNOWN):
        SymtabEntry.__init__(self, name, Kind.PARAM, type_catg)
        self._func = func_entry
        self._param_nun = self._func.get_num_params()
        self._func.inc_num_params()
        
        
class VarArgEntry(ParamEntry):
    
    def __init__(self, func_entry, name):
        ParamEntry.__init__(self, func_entry, name, TypeCatg.LIST)
        self._func.set_var_arg_support()