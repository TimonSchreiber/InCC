from .code_generation import gen
from .struct_expr import *
from ..lexer.proc_expr import tokens

used_procedures_and_classes |= {
    'ProcExpression'
}

def p_expression_nm_proc(p):
    'expression : PROC LPAREN identifier_list RPAREN identifier_list ARROW expression'
    p[0] = gen().ProcExpression(p[3], p[5], p[7])

def p_expression_0m_proc(p):
    'expression : PROC LPAREN RPAREN identifier_list ARROW expression'
    p[0] = gen().ProcExpression([], p[4], p[6])

def p_expression_n0_proc(p):
    'expression : PROC LPAREN identifier_list RPAREN ARROW expression'
    p[0] = gen().ProcExpression(p[3], [], p[6])

def p_expression_00_proc(p):
    'expression : PROC LPAREN RPAREN ARROW expression'
    p[0] = gen().ProcExpression([], [], p[5])
