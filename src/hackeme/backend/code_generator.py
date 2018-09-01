class CodeGenerator(object):
    
    def __init__(self, ast, scope_manager, output):
        self._ast = ast
        self._scope_mgr = scope_manager
        self._output = output
        
    def gen_expr(self, ast):
        if ast.name == "list":
            self.gen_list(ast)
            
    def gen_list(self, lst):
        raise NotImplementedError
        
        