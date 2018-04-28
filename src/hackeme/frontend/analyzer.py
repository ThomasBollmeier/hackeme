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
        
        
class AstWalker(object):
    
    def __init__(self, scope_mgr):
        self._scope_mgr = scope_mgr
        self._scope_stack = []
        
    def push_scope(self, ast):
        scope = None
        if ast.has_attr('x-scope'):
            scope_id = ast.get_attr('x-scope')
            scope = self._scope_mgr.find_scope(scope_id)
        elif self._scope_stack:
            scope = self._scope_stack[-1]
        self._scope_stack.append(scope)

    def pop_scope(self):
        self._scope_stack.pop()
        
    
class IdentifierLookup(AstWalker):
    
    def __init__(self, scope_mgr):
        AstWalker.__init__(self, scope_mgr)
    
    def walk_ast(self, ast):
        self._errors = []
        ast.walk(self)
        return self._errors
        
    def enter_node(self, ast):
        self.push_scope(ast)
            
    def exit_node(self, ast):
        self.pop_scope()
    
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
                
                
class CallChecker(AstWalker):
    
    def __init__(self, scope_mgr):
        AstWalker.__init__(self, scope_mgr)
    
    def walk_ast(self, ast):
        self._call_stack = []
        self._errors = []
        ast.walk(self)
        return self._errors
        
    def enter_node(self, ast):
        self.push_scope(ast)
        if ast.name == "call":
            self._check_call(ast)
            
    def exit_node(self, ast):
        self.pop_scope()
        
    def visit_node(self, ast):
        pass
    
    def _check_call(self, ast):
        callee, args = ast.get_children()
        fn = callee.get_children()[0]
        if fn.name == "IDENT" and fn.has_attr('x-from-scope'):
            func_name = fn.value
            scope = self._scope_stack[-1]
            func_entry = scope.get_entry(func_name)
            if isinstance(func_entry, FuncEntry):
                self._check_arguments(args, func_entry, scope)
            else:
                error = "{}: '{}' is not a function".format(scope.get_full_name(), func_name)
                self._errors.append(error)
                
    def _check_arguments(self, args, func_entry, scope):
        num_args = len(args.get_children())
        min_num_params = func_entry.get_min_num_params()
        if min_num_params > num_args:
            error = "{}: '{}' requires at least {} arguments".format(
                scope.get_full_name(), func_entry.get_name(), min_num_params)
            self._errors.append(error)
        else:
            max_num_params = func_entry.get_max_num_params()
            if max_num_params is not None and max_num_params < num_args:
                error = "{}: '{}' must not be called with more than {} arguments".format(
                    scope.get_full_name(), func_entry.get_name(), max_num_params)
                self._errors.append(error)
                
                
class TailPositionFinder(object):
    
    def walk_ast(self, ast):
        ast.walk(self)
    
    def enter_node(self, ast):
        if ast.name == "fundef":
            self._set_tail_pos_info(ast)
            
    def exit_node(self, ast):
        pass
        
    def visit_node(self, ast):
        pass
    
    def _set_tail_pos_info(self, fundef):
        func_name = fundef.get_attr("name")
        body = fundef.find_children_by_name("body")[0]
        last_expr = body.get_children()[-1]
        self._set_tail_pos_info_in_expr(last_expr, func_name)
        
    def _set_tail_pos_info_in_expr(self, expr, func_name):
        if expr.name == "if_expr":
            self._set_tail_pos_info_in_if(expr, func_name)
        elif expr.name == "cond":
            self._set_tail_pos_info_in_cond(expr, func_name)
        else:
            expr.set_attr('x-tail-pos-of', func_name)
                
    def _set_tail_pos_info_in_if(self, if_expr, func_name):
        children = if_expr.get_children()
        consequent = children[1].get_children()[0]
        alternate = children[2].get_children()[0]
        self._set_tail_pos_in_expr(consequent, func_name)
        self._set_tail_pos_in_expr(alternate, func_name)
        
    def _set_tail_pos_info_in_cond(self, cond_expr, func_name):
        for branch in cond_expr.get_children():
            consequent = branch.get_children()[1]
            self._set_tail_pos_info_in_expr(consequent, func_name)
        

class Analyzer(object):
    
    def __init__(self):
        self._scope_mgr = ScopeManager()
        self._errors = []
    
    def analyze(self, ast):
        global_scope = self._scope_mgr.new_scope(name="global")
        DefinitionFinder().walk_ast(ast, global_scope, self._scope_mgr)
        TailPositionFinder().walk_ast(ast)
        self._errors = IdentifierLookup(self._scope_mgr).walk_ast(ast)
        self._errors += CallChecker(self._scope_mgr).walk_ast(ast)
        if self._errors:
            return False
        return True
       
    def get_errors(self):
        return self._errors