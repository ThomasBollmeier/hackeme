class CodeGenerator(object):
    
    def __init__(self, ast, scope_manager):
        self._ast = ast
        self._scope_mgr = scope_manager