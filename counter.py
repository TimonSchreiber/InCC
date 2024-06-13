counter = '''
{ counter := acc -> {x -> { acc := acc + x}}
; counter := x -> y -> x := x + y
; c := counter(0)
; a1 := c(1)
; a2 := c(1)
; a3 := c(1)
; a4 := c(2)
; a5 := c(3)
}'''

if __name__ == '__main__':
    from ply.lex import lex
    from ply.yacc import yacc

    from language.lexer.lambda_expr import *
    from language.parser.lambda_expr import *
    from language.parser.code_generation import set_generator_module, check_generator_module

    from interpreter import lambda_expr
    from interpreter.enviroment import Enviroment
    from language.parser.lambda_expr import precedence

    set_generator_module(lambda_expr)
    check_generator_module(used_procedures_and_classes)

    lexer = lex()
    parser = yacc(start='expression')
    env = Enviroment()

    result = parser.parse(input=counter, lexer=lexer)
    print(counter, "\n", result.eval(env))

    # for p in precedence:
    #     print(*p)