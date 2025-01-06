from compiler.enviroment import lookup, label, new_addr

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

def code_l(expr: Expression, env: dict) -> list[str]:
    match expr:
        case VariableExpression(name) if lookup(env, name, 'scope') == 'global':
            return [
                ('loadc', lookup(env, name, 'addr'))
            ]
        case VariableExpression(name):
            return [
                ('loadrc', lookup(env, name, 'addr'))
            ]
        case _:
            raise Exception(f'code_l uninplemented for {expr}')

def code_r(expr: Expression, env: dict) -> list[str]:
    match expr:
        case SelfEvaluatingExpression(value):
            return [
                ('loadc', value)
            ]
        case BinaryOperatorExpression(e1, e2, op):
            return [
                *code_r(e1, env),
                *code_r(e2, env),
                (binary_operators[op])
            ]
        case UnaryOperatorExpression(e, op):
            return [
                *code_r(e, env),
                (unary_operators[op])
            ]
        case VariableExpression(_):
            return [
                *code_l(expr, env),
                ('load')
            ]
        case AssignmentExpression(var, e):
            if var not in env:
                env[var] = {'addr': new_addr(8), 'scope': 'global', 'size': 8}
            var = VariableExpression(var)
            return [
                *code_r(e, env),
                *code_l(var, env),
                ('store')
            ]
        case SequenceExpression(seq):
            return [
                x
                for e in seq
                for x in (code_r(e, env) + ['pop'])
            ][:-1]
        case LoopExpression(e, body):
            nr = label()
            l_loop = f'loop_{nr}'
            l_endloop = f'endloop_{nr}'
            return [
                ('loadc', 0),
                *code_r(e, env),
                ('label', l_loop),
                ('dup'),
                ('jumpz', l_endloop),
                ('dec'),
                ('swap'),
                ('pop'),
                *code_r(body, env),
                ('swap'),
                ('jump', l_loop),
                ('label', l_endloop),
                ('pop')
            ]
        case WhileExpression(condition, body):
            nr = label()
            l_while = f'while_{nr}'
            l_do = f'do_{nr}'
            l_endwhile = f'endwhile_{nr}'
            return [
                ('loadc', 0),
                ('label', l_while),
                *code_r(condition, env),
                ('jumpz', l_endwhile),
                ('pop'),
                ('label', l_do),
                *code_r(body, env),
                ('jump', l_while),
                ('label', l_endwhile)
            ]
        case ITEExpression(if_expr, then_body, else_body):
            nr = label()
            l_if = f'if_{nr}'
            l_then = f'then_{nr}'
            l_else = f'else_{nr}'
            l_endif = f'endif_{nr}'
            return [
                ('label', l_if),
                *code_r(if_expr, env),
                ('jumpz', l_else),
                ('label', l_then),
                *code_r(then_body, env),
                ('jump', l_endif),
                ('label', l_else),
                *code_r(else_body, env),
                ('label', l_endif)
            ]
        case ProcedureExpression(vars, locals, body):
            nr = label()
            l_proc = f'proc_{nr}'
            l_endproc = f'endproc_{nr}'

            env2 = {'..' : env}
            env2 |= {
                vars[i] : {
                    'addr': -(16+i*8), 'scope': 'args',  'size': 8
                    } for i in range(len(vars))
                }
            env2 |= {
                locals[i] : {
                    'addr': (8+i*8), 'scope': 'local', 'size': 8
                    } for i in range(len(locals))
                }

            return [
                ('jump', l_endproc),
                ('label', l_proc),
                ('enter'),
                ('alloc', 8 * len(locals)),
                *code_r(body, env2),
                ('loadrc', -16),
                ('store'),
                ('pop'),
                ('ret'),
                ('label', l_endproc),
                ('loadc', l_proc) # TODO: used to be loadrc l_proc
            ]
        case CallExpression(name, args):
            arguments = sum([code_r(e, env) for e in args[::-1]], [])
            return [
                *arguments,
                ('mark'),
                *code_r(name, env),
                ('call'),
                ('pop'),
                ('slide', 8 * len(args) - 8, 8)
            ]
        case None:
            return [
                ('loadc', 0)
            ]
        case _:
            raise Exception(f'code_r uninplemented for {expr}')
