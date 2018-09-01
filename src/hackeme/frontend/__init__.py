from .hackeme_parser import HackemeParser
from .analyzer import Analyzer

def make_parser():
    """
    () -> HackemeParser

    Create a syntax parser for the Hackeme language
    """
    return HackemeParser()

def make_analyzer():
    """
    () -> Analyzer

    Create an analyzer
    """
    return Analyzer()

def parse_analyze(source):
    """
    (str) -> (AST, [str], ScopeManager)
    
    Parse and analyze source
    
    @param source: Hackeme code
    @return (AST, error_list, scope_manager) 
    """
    parser = HackemeParser()
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