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
        self._arities = []
        
    def create_arity(self):
        arity = FuncArity()
        self._arities.append(arity)
        return arity
    
    def find_matching_arity(self, num_args):
        for arity in self._arities:
            if num_args < arity.get_min_num_params():
                continue
            max_num_params = arity.get_max_num_params()
            if max_num_params is not None and num_args > max_num_params:
                continue
            return arity
        return None
        
        
class FuncArity(object):
    
    def __init__(self):
        
        self._num_params = 0
        self._has_var_arg = False
        
    def inc_num_params(self):
        self._num_params += 1
        
    def get_num_params(self):
        return self._num_params
    
    def get_min_num_params(self):
        if not self._has_var_arg:
            return self._num_params
        else:
            return self._num_params - 1
    
    def get_max_num_params(self):
        if not self._has_var_arg:
            return self._num_params
        else:
            return None
        
    def has_var_arg(self):
        return self._has_var_arg
        
    def set_var_arg_support(self):
        self._has_var_arg = True
        
        
class ParamEntry(SymtabEntry):
    
    def __init__(self, arity, name, type_catg = TypeCatg.UNKNOWN):
        SymtabEntry.__init__(self, name, Kind.PARAM, type_catg)
        self._arity = arity
        self._param_num = self._arity.get_num_params()
        self._arity.inc_num_params()
        
        
class VarArgEntry(ParamEntry):
    
    def __init__(self, arity, name):
        ParamEntry.__init__(self, arity, name, TypeCatg.LIST)
        self._arity.set_var_arg_support()