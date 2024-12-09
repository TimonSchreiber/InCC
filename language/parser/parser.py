from ply.yacc import yacc

from language.lexer.tokens import *
from syntaxtree.syntaxtree import *

precedence = [
    ['left', 'EXTEND'],
    ['left', 'STRUCT'],
    ['left', 'COMMA'],
    ['left', 'ARROW'],
    ['left', 'IN'],
    ['left', 'THEN'],
    ['left', 'ELSE'],
    ['left', 'DO'],
    ['right', 'ASSIGN'],
    ['left', 'EQUALS', 'NOT_EQUALS'],
    ['left', 'OR', 'NOR'],
    ['left', 'AND', 'NAND'],
    ['left', 'XOR', 'NEQ', 'EQ', 'IMPL'],
    ['left', 'LESS_THEN', 'GREATER_THEN', 'LESS_EQUALS', 'GREATER_EQUALS'],
    ['left', 'PLUS', 'MINUS'],
    ['left', 'TIMES', 'DIVIDE'],
    ['right', 'UMINUS'],
    ['right', 'LPAREN'],
    ['left', 'SEPARATOR'],
    ['left', 'DOT'],
]

def p_expression_single_value(p):
    '''expression : NUMBER
                  | FLOAT
                  | CHAR
                  | STRING'''
    p[0] = SelfEvaluatingExpression(p[1])

def p_expression_list_non_empty(p):
    'expression : LIST LPAREN expression_list RPAREN'
    p[0] = ListExpression(p[3])

def p_expression_list_empty(p):
    'expression : LIST LPAREN RPAREN'
    p[0] = ListExpression(None)

def p_expression_array_non_empty(p):
    '''expression : LBRACKET expression_list RBRACKET
                  | ARRAY LPAREN expression_list RPAREN'''
    p[0] = ArrayExpression(p[2]) if len(p) == 4 else ArrayExpression(p[3])

def p_expression_array_empty(p):
    '''expression : LBRACKET RBRACKET
                  | ARRAY LPAREN RPAREN'''
    p[0] = ArrayExpression([])

def p_expression_array_access(p):
    'expression : IDENTIFIER LBRACKET expression RBRACKET'
    p[0] = ArrayAccessExpression(p[1], p[3])

def p_expression_unary(p):
    '''expression : MINUS expression %prec UMINUS
                  | NOT expression %prec UMINUS'''
    p[0] = UnaryOperatorExpression(p[2], p[1])

def p_expression_binary(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression LESS_THEN expression
                  | expression GREATER_THEN expression
                  | expression LESS_EQUALS expression
                  | expression GREATER_EQUALS expression
                  | expression EQUALS expression
                  | expression NOT_EQUALS expression
                  | expression AND expression
                  | expression NAND expression
                  | expression OR expression
                  | expression NOR expression
                  | expression XOR expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression IMPL expression'''
    p[0] = BinaryOperatorExpression(p[1], p[3], p[2])

def p_expression_parenthesis(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_boolean_value(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = BooleanValueExpression(p[1])

def p_expression_id(p):
    'expression : IDENTIFIER'
    p[0] = VariableExpression(p[1])

def p_expression_assign(p):
    'expression : IDENTIFIER ASSIGN expression'
    p[0] = AssignmentExpression(p[1], p[3])

def p_expression_sequences(p):
    'expression : BEGIN body END'
    p[0] = SequenceExpression(p[2])

def p_bodyn(p):
    '''body : expression
            | body SEPARATOR expression'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

def p_expression_loop(p):
    'expression : LOOP expression DO expression'
    p[0] = LoopExpression(p[2], p[4])

def p_expression_for(p):
    'expression : FOR expression SEPARATOR expression SEPARATOR expression DO expression'
    p[0] = ForExpression(p[2], p[4], p[6], p[8])

def p_expression_while(p):
    'expression : WHILE expression DO expression'
    p[0] = WhileExpression(p[2], p[4])

def p_expression_it(p):
    'expression : IF expression THEN expression'
    p[0] = ITEExpression(p[2], p[4], None)

def p_expression_ite(p):
    'expression : IF expression THEN expression ELSE expression'
    p[0] = ITEExpression(p[2], p[4], p[6])

def p_identifier_list(p):
    '''identifier_list : IDENTIFIER
                       | IDENTIFIER COMMA identifier_list'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

def p_expression_lock(p):
    'expression : LOCK identifier_list IN expression'
    p[0] = LockExpression(p[2], p[4])

def p_assign_list(p):
    '''assign_list : IDENTIFIER ASSIGN expression
                   | assign_list COMMA IDENTIFIER ASSIGN expression'''
    p[0] = [(p[1], p[3])] if len(p) == 4 else p[1] + [(p[3], p[5])]

def p_expression_let(p):
    'expression : LET assign_list IN expression'
    p[0] = LetExpression(p[2], p[4])

def p_expression_letrec(p):
    'expression : LETREC assign_list IN expression'
    p[0] = LetRecExpression(p[2], p[4])


def p_expression_list(p):
    '''expression_list : expression
                       | expression COMMA expression_list'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

def p_expression_n_lambda(p):
    'expression : LAMBDA identifier_list ARROW expression'
    p[0] = LambdaExpression(p[2], p[4])

def p_expression_0_lambda(p):
    'expression : LAMBDA ARROW expression'
    p[0] = LambdaExpression([], p[3])

def p_expression_call_n_args(p):
    'expression : expression LPAREN expression_list RPAREN'
    p[0] = CallExpression(p[1], p[3])

def p_expression_call_0_args(p):
    'expression : expression LPAREN RPAREN'
    p[0] = CallExpression(p[1], [])

def p_dots(p):
    '''dots : DOT
            | dots DOT'''
    p[0] = 1 if len(p) == 2 else p[1] + 1

def p_struct_body(p):
    '''struct_body : IDENTIFIER ASSIGN expression
                   | struct_body SEPARATOR IDENTIFIER ASSIGN expression'''
    p[0] = [(p[1], p[3])] if len(p) == 4 else p[1] + [(p[3], p[5])]

def p_expression_struct(p):
    'expression : STRUCT BEGIN struct_body END'
    p[0] = StructExpression(p[3])

def p_expression_struct_member_access(p):
    'expression : expression dots IDENTIFIER'
    p[0] = StructMemberAccessExpression(p[1], p[2], p[3])

def p_expression_dots_id(p):
    'expression : dots IDENTIFIER'
    p[0] = DotVariableExpression(p[1], p[2])

def p_struct_extend_expression(p):
    'expression : EXTEND expression BEGIN struct_body END'
    p[0] = StructExtendExpression(p[2], p[4])

def p_expression_nm_proc(p):
    'expression : PROC LPAREN identifier_list RPAREN identifier_list ARROW expression'
    p[0] = ProcedureExpression(p[3], p[5], p[7])

def p_expression_0m_proc(p):
    'expression : PROC LPAREN RPAREN identifier_list ARROW expression'
    p[0] = ProcedureExpression([], p[4], p[6])

def p_expression_n0_proc(p):
    'expression : PROC LPAREN identifier_list RPAREN ARROW expression'
    p[0] = ProcedureExpression(p[3], [], p[6])

def p_expression_00_proc(p):
    'expression : PROC LPAREN RPAREN ARROW expression'
    p[0] = ProcedureExpression([], [], p[5])

def p_error(p):
    print(f'Syntax error at {p.value}')

parser = yacc(start='expression')
