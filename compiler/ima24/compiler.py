from compiler.enviroment import label, lookup, new_addr
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
        case VariableExpression() | AssignmentExpression():
            return [
                *code_v(expr, rho, kp),
                ('getbasic')
            ]
        case None:
            return [
                ('loadc', 0)
            ]
        case _:
            raise Exception(f'code_b unimplemented for {expr}')


def code_v(expr: Expression, rho: dict, kp: int) -> list[tuple[str | int]]:
    match expr:
        case VariableExpression(name):
            return [
                getvar(name, rho, kp)
            ]
        case AssignmentExpression(var, e):
            if var not in rho:
                rho[var] = {'addr': new_addr(8), 'scope': 'global', 'size': 8}
            var = VariableExpression(var)
            return [
                *code_b(var, rho, kp),
                *code_v(e, rho, kp + 1),
                ('store')
            ]
        case None:
            return [
                *code_b(expr, rho, kp)
            ]
        case SelfEvaluatingExpression(e):
            return code_b(expr, rho, kp)
        case _:
            raise Exception(f'code_v unimplemented for {expr}')


def getvar(name: str, rho: dict, kp: int) -> tuple[str, int]:
    scope = lookup(rho, name, 'scope')
    match scope:
        case 'local':
            val = lookup(rho, name, 'addr')
            return ('pushloc', val)
            # return ('pushloc', kp-j)
        case 'global':
            val = lookup(rho, name, 'addr')
            return ('pushglob', val)
            # return ('pushglob', j)
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
