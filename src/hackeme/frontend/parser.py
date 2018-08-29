from komparse.ast import Ast
from .hackeme_parser import HackemeParser

def make_parser():
    return _HackemeParser()

class _HackemeParser(HackemeParser):
    
    def __init__(self):
        HackemeParser.__init__(self)
        
    def parse(self, source):
        ast = HackemeParser.parse(self, source)
        if ast:
            arity_grouping = ArityGrouping()
            ast.walk(arity_grouping)
            return arity_grouping.get_grouped_ast()
        else:
            return None
    
    
class ArityGrouping(object):
    """
    Group arities into function definition node
    """
    def __init__(self):
        self._ast = None
        self._node_stack = []
        self._func_stack = []
        
    def get_grouped_ast(self):
        return self._ast
    
    def enter_node(self, node):
        
        if node.has_attr('root'):
        
            self._ast = node.copy()
            self._node_stack.append(self._ast)
            self._func_stack = [{}]
            
        elif node.name == 'fundef':
            
            arity = Ast("arity")
            
            func_name = node.get_attr('name')
            funcs = self._func_stack[-1]
            if func_name not in funcs:
                func_node = node.copy()
                funcs[func_name] = func_node
                self._add_to_parent(func_node)
            else:
                func_node = funcs[func_name]
                
            func_node.add_child(arity)
            self._node_stack.append(arity)
            
            self._func_stack.append({})
                
        else:
            self._node_stack.append(node.copy())
            
    def exit_node(self, node):
        child = self._node_stack.pop()
        if node.name != "fundef":
            self._add_to_parent(child)
        else:
            self._func_stack.pop()
        
    def visit_node(self, node):
        self._add_to_parent(node.copy())
            
    def _add_to_parent(self, node):
        if self._node_stack:
            parent = self._node_stack[-1]
            parent.add_child(node)
    
    
    
    