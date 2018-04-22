from .scope_manager import ScopeManager
from .symtab_entry import Kind, SymtabEntry, FuncEntry, \
    ParamEntry, VarArgEntry

class DefinitionFinder(object):

    def walk_ast(self, ast, scope, scope_mgr):
        self._scope = scope
        self._scope_mgr = scope_mgr
        self._curr_func = None
        ast.set_attr('x-scope', self._scope.get_scope_id())
        ast.walk(self)

    # Visitor implementation: enter_node, exit_node, visit_node    
    def enter_node(self, ast):
        if ast.name == "vardef":
            name = ast.get_attr('name')
            self._scope.add(SymtabEntry(name, self._var_kind()))
        elif ast.name == "fundef":
            name = ast.get_attr('name')
            self._curr_func = FuncEntry(name, self._var_kind())
            self._scope.add(self._curr_func)
            # a function definition creates a new scope
            self._scope = self._scope_mgr.new_scope(self._scope, name)
            ast.set_attr('x-scope', self._scope.get_scope_id())
    
    def exit_node(self, ast):
        if ast.name == "fundef":
            self._scope = self._scope.get_parent()
            self._curr_func = None
    
    def visit_node(self, ast):
        if ast.name == "parameter":
            self._scope.add(ParamEntry(self._curr_func, ast.value))
        elif ast.name == "var":
            self._scope.add(VarArgEntry(self._curr_func, ast.value))
    
    def _var_kind(self):
        if self._scope.get_parent() is not None:
            return Kind.LOCAL_VAR
        else:
            return Kind.GLOBAL_VAR
        
    
class IdentifierLookup(object):
    
    def walk_ast(self, ast, scope_mgr):
        self._scope_mgr = scope_mgr
        self._errors = []
        self._scope_stack = []
        ast.walk(self)
        return self._errors
        
    def enter_node(self, ast):
        scope = None
        if ast.has_attr('x-scope'):
            scope_id = ast.get_attr('x-scope')
            scope = self._scope_mgr.find_scope(scope_id)
        elif self._scope_stack:
            scope = self._scope_stack[-1]
        self._scope_stack.append(scope)
            
    def exit_node(self, ast):
        self._scope_stack.pop()
    
    def visit_node(self, ast):
        if ast.name == "IDENT":
            identifier = ast.value
            scope = self._scope_stack[-1]
            def_scope_id = scope.get_defining_scope(identifier)
            if def_scope_id is not None:
                ast.set_attr('x-from-scope', def_scope_id)
            else:
                error = "{}: '{}' is unknown".format(scope.get_full_name(), identifier)
                self._errors.append(error)
        

class Analyzer(object):
    
    def __init__(self):
        self._scope_mgr = ScopeManager()
        self._errors = []
    
    def analyze(self, ast):
        global_scope = self._scope_mgr.new_scope(name="global")
        DefinitionFinder().walk_ast(ast, global_scope, self._scope_mgr)
        self._errors = IdentifierLookup().walk_ast(ast, self._scope_mgr)
        if self._errors:
            return False
        return True
       
    def get_errors(self):
        return self._errors