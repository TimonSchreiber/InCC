from compiler.mama.enviroment import label
from compiler.mama.enviroment import lookup
from syntaxtree.syntaxtree import *

binary_operators = {
    '+'  : 'add',
    '-'  : 'sub',
    '*'  : 'mul',
    '/'  : 'div',
    '<'  : 'le',
    '>'  : 'gr',
    '<=' : 'leq',
    '>=' : 'geq',
    '='  : 'eq',
    '!=' : 'neq'
}

unary_operators = {
    '-' : 'neg'
}

def code_b(expr: Expression, rho: dict, kp: int) -> list[tuple[str | int]]:
    match expr:
        case SelfEvaluatingExpression(value):
            return [
                ('loadc', value)
            ]
        case BinaryOperatorExpression(e1, e2, op):
            return [
                *code_b(e1, rho, kp + 0),
                *code_b(e2, rho, kp + 1),
                (binary_operators[op])
            ]
        case UnaryOperatorExpression(e, op):
            return [
                *code_b(e, rho, kp),
                (unary_operators[op])
            ]
        case ITEExpression(if_expr, then_body, else_body):
            nr = label()
            l_if = f'if_{nr}'
            l_then = f'then_{nr}'
            l_else = f'else_{nr}'
            l_endif = f'endif_{nr}'

            return [
                ('label', l_if),
                *code_b(if_expr, rho, kp),
                ('jumpz', l_else),
                ('label', l_then),
                *code_b(then_body, rho, kp),
                ('jump', l_endif),
                ('label', l_else),
                *code_b(else_body, rho, kp),
                ('label', l_endif)
            ]
        # case LetExpression(vars, body):
        #     rho2 = {'..': rho}
        #     variables = []
        #     size = len(vars)
        #     for i in range(size):
        #         var, val = vars[i]
        #         rho2[var] = {'scope': 'local', 'addr' : kp + i + 1, 'size' : 8}
        #         variables += code_v(val, rho2, kp+i)
        #     return variables + code_b(body, rho2, kp+size) + [('slide', size)]
        # case LetRecExpression(vars, body):
        #     rho2 = {'..': rho}
        #     variables = []
        #     size = len(vars)
        #     for i in range
        #     for i in range(size):
        #         var, val = vars[i]
        #         rho2[var] = {'scope': 'local', 'addr' : kp + i + 1, 'size' : 8}
        #         variables += code_v(val, rho2, kp+i) + [('rewrite', size-i)] # TODO: size-i richtig?
        #     return variables + code_b(body, rho2, kp+size) + [('slide', size)]
        case VariableExpression(_) | CallExpression(_) | LetExpression(_) | LetRecExpression(_):
            '''
            mark A
            for i in range(m):
                code_v(formals[m-1-i], rho, kp+3+i)
            code_v(f, rho, kp+3+m)
            apply
            A;
            '''
            return [
                *code_v(expr, rho, kp),
                ('getbasic')
            ]
        case None:
            return [
                ('loadc', 0)
            ]
        case _:
            raise Exception(f'code_b uninplemented for {expr}')

def code_v(expr: Expression, rho: dict, kp: int) -> list[str]:
    match expr:
        case VariableExpression(name):
            return [
                getvar(name, rho, kp)
            ]
        case ITEExpression(if_expr, then_body, else_body):
            nr = label()
            l_if = f'if_{nr}'
            l_then = f'then_{nr}'
            l_else = f'else_{nr}'
            l_endif = f'endif_{nr}'

            return [
                ('label', l_if),
                *code_b(if_expr, rho, kp),
                ('jumpz', l_else),
                ('label', l_then),
                *code_v(then_body, rho, kp),
                ('jump', l_endif),
                ('label', l_else),
                *code_v(else_body, rho, kp),
                ('label', l_endif)
            ]
        case LetExpression(vars, body):
            rho2 = {'..': rho}
            variables = []
            size = len(vars)
            for i in range(size):
                var, val = vars[i]
                rho2[var] = {'scope': 'local', 'addr' : kp + i + 1, 'size' : 8}
                variables += code_v(val, rho2, kp+i)
            return [
                *variables,
                *code_v(body, rho2, kp+size),
                ('slide', size)
            ]
        case LetRecExpression(vars, body):
            rho2 = {'..': rho}
            size = len(vars)
            variables = [('alloc', size)]
            for i in range(size):
                var, val = vars[i]
                rho2[var] = {'scope': 'local', 'addr' : kp + i + 1, 'size' : 8}
                variables += code_v(val, rho2, kp+size) + [('rewrite', size-i)] # TODO: size-i richtig?
            return [
                *variables,
                *code_v(body, rho2, kp+size),
                ('slide', size)
            ]
        case LambdaExpression(vars, body):
            nr = label()
            l_lambda = f'lambda_{nr}'
            l_endlambda = f'endlambda_{nr}'

            free_vars = list(free(expr))
            size = len(free_vars)

            arguments = sum([code_v(VariableExpression(free_vars[i]), rho, kp + i) for i in range(size)], [])
            print("arguments: ", arguments)

            rho2 = {'..': rho}
            rho2 |= {
                free_vars[i] : {
                    'addr': i, 'scope': 'global',  'size': 8
                    } for i in range(size)
                }
            rho2 |= {
                vars[i] : {
                    'addr': -i, 'scope': 'local',  'size': 8
                    } for i in range(len(vars))
                }

            return [
                *arguments,
                ('mkvec', size),
                ('mkfunval', l_lambda),
                ('jump', l_endlambda),
                ('label', l_lambda),
                *code_v(body, rho2, 0),
                ('popenv'),
                ('label', l_endlambda)
            ]

        case CallExpression(name, args):
            nr = label()
            l_return = f'return_{nr}'

            size = len(args)
            arguments = sum([code_v(args[size - 1 - i], rho, kp + 3 + i) for i in range(size)], [])

            return [
                ('mark', l_return),
                *arguments,
                *code_v(name, rho, kp + 3 + size),
                ('apply'),
                ('label', l_return)
            ]
        case SelfEvaluatingExpression(_) | BinaryOperatorExpression(_) | UnaryOperatorExpression(_):
            return [
                *code_b(expr, rho, kp),
                ('mkbasic')
            ]
        case None:
            return [
                ('loadc', 0)
            ]
        case _:
            raise Exception(f'code_v uninplemented for {expr}')

def getvar(name: str, rho: dict, kp: int) -> tuple[str, int]:
    match lookup(rho, name):
        case {'addr' : j, 'scope' : 'local', 'size' : _}:
            return ('pushloc', kp-j)
        case {'addr' : j, 'scope' : 'global', 'size' : _}:
            return ('pushglob', j)
        case _:
            raise Exception(f'variable {name} not defined in {rho}')

def free(expr: Expression) -> set[str]:
    match expr:
        case SelfEvaluatingExpression(value):
            return set()
        case BinaryOperatorExpression(e1, e2, _):
            return free(e1) | free(e2)
        case UnaryOperatorExpression(e, _):
            return free(e)
        case VariableExpression(name):
            return {name}
        case AssignmentExpression(var, e):
            return {var} | free(e)
        case ITEExpression(if_expr, then_body, else_body):
            return free(if_expr) | free(then_body) | free(else_body)
        case LetExpression(vars, body) | LetRecExpression(vars, body):
            return free(body) - {v for (v,_) in vars}
        case LambdaExpression(vars, body):
            return free(body) - {x for x in vars}
        case CallExpression(name, args):
            return free(name) | {x for arg in args for x in free(arg)}
        case None:
            return set()
        case _:
            Exception

'''
    Lambda:
    - frei
    entry, next = next(lambda_label)
    ...

    Call:
    A = next(call_label)
    ...

    Let: ...

    LetRec: *in zwei schleifen; erst namen anlegen, dann zuweisen
'''

'''
    identisch zu code_b() aber am ende wird 'mkbasic' aufgerufen

    basic zellen sind immmer 16 byte groß
        mov rdi, 16
        call malloc     # malloc hinzufuegen
        push rax


    -
        pop rdx
        mov qword [rdx], 'B'
        pop rax
        mov [rdx+8], rax
        push rdx
'''