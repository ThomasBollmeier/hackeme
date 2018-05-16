from .parser import make_parser
from .analyzer import Analyzer

def parse_analyze(source):
    """
    (str) -> (AST, [str])
    
    Parse and analyze source
    
    @param source: Hackeme code
    @return (AST, error_list, scope_manager) 
    """
    parser = make_parser()
    ast = parser.parse(source)
    
    if  ast:
        analyzer = Analyzer()
        ok = analyzer.analyze(ast)
        if ok:
            return (ast, [], analyzer.get_scope_manager())
        else:
            return (None, analyzer.get_errors(), None)
    else:
        return (None, [parser.error()], None)