import sys

sys.path.append("../src")

from hackeme.frontend.parser import make_parser

if __name__ == "__main__":
    
    code = """
    (define my-answer 42) ; the answer to everything
    (if (#true)
        result
        (my-func first-arg result))
    (define (this-is-a-function a-param))
    (this-is-a-function 23)
    '(1 2 3 (4 5 (7 8 9)))
    """
    
    parser = make_parser()
    
    ast = parser.parse(code)
    if ast:
        print(ast.to_xml())
    else:
        print(parser.error())