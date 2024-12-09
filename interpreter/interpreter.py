import operator

from interpreter.enviroment import Enviroment
from syntaxtree.syntaxtree import *

binary_operators = {
    '+'    : operator.add,
    '-'    : operator.sub,
    '*'    : operator.mul,
    '/'    : operator.truediv,
    '<'    : operator.lt,
    '>'    : operator.gt,
    '<='   : operator.le,
    '>='   : operator.ge,
    '='    : operator.eq,
    '!='   : operator.ne,
    'and'  : operator.and_,
    'or'   : operator.or_,
    'eq'   : operator.eq,
    'xor'  : operator.xor,
    'neq'  : operator.xor,
    'nand' : lambda a,b: not (a and b),
    'nor'  : lambda a,b: not (a or b),
    'impl' : lambda a,b: (not a) | b
}

unary_operators = {
    '-'   : operator.neg,
    'NOT' : operator.not_
}

boolean_values = {
    'TRUE'  : True,
    'FALSE' : False
}

def eval(expr: Expression, env: Enviroment) -> any:
    match expr:
        case SelfEvaluatingExpression(value):
            return value
        case ListExpression(lst):
            return (eval(lst[0], env), eval(lst[1], env)) if lst else None
        case ArrayExpression(arr):
            return [eval(elem, env) for elem in arr]
        case ArrayAccessExpression(arr, index):
            return env[arr][eval(index, env)]
        case BinaryOperatorExpression(e1, e2, op):
            return binary_operators[op](eval(e1, env), eval(e2, env))
        case UnaryOperatorExpression(e, op):
            return unary_operators[op](eval(e, env))
        case VariableExpression(var):
            return env[var]
        case AssignmentExpression(var, e):
            value = eval(e, env)
            env[var] = value
            return value
        case BooleanValueExpression(b):
            return boolean_values[b.upper()]
        case SequenceExpression(seq):
            for e in seq:
                res = eval(e, env)
            return res
        case LoopExpression(e, body):
            loops = eval(e, env)
            res = None
            for _ in range(int(loops)):
                res = eval(body, env)
            return res
        case ForExpression(start, condition, change, body):
            eval(start, env)
            res = None
            while eval(condition, env):
                res = eval(body, env)
                eval(change, env)
            return res
        case WhileExpression(condition, body):
            res = None
            while eval(condition, env):
                res = eval(body, env)
            return res
        case ITEExpression(if_expr, then_body, else_body):
            if eval(if_expr, env):
                return eval(then_body, env)
            else:
                return eval(else_body, env)
        case LockExpression(vars, body):
            env.lock_variables(vars)
            res = eval(body, env)
            env.unlock_variables(vars)
            return res
        case LetExpression(vars, body) | LetRecExpression(vars, body):
            env2 = Enviroment()
            env2.set_parent(env)
            for (var, expr) in vars:
                val = eval(expr, env2)
                dict.__setitem__(env2, var, val)
            res = eval(body, env2)
            return res
        case LambdaExpression(vars, body):
            def fun(*values):
                if len(values) != len(vars):
                    raise Exception(f'wrong number of arguments: is {len(values)}, but should be {len(vars)}')
                env1 = Enviroment()
                env1.set_parent(env)
                env1 |= {vars[i]: values[i] for i in range(len(values))}
                res = eval(body, env1)
                return res
            return fun
        case CallExpression(name, args):
            fun = eval(name, env)
            vals = [eval(arg, env) for arg in args]
            return fun(*vals)
        case DotVariableExpression(dots, name):
            return env.get_item(dots, name)
        case StructExpression(body):
            env2 = Enviroment()
            env2.set_parent(env)  # set env (local scope) as the parent of this struct
            # env1.add_root(env)  # set env (local scope) as the parent of this struct
            for (id, e) in body:
                val = eval(e, env2)
                dict.__setitem__(env2, id, val)  # add value to this level of dict
            env2.remove_root()  # remove the root from env1
            return env2
        case StructExtendExpression(s_expr, body):
            # TODO: are StructExpression and StructExtendExpression not the same?
            struct = eval(s_expr, env)
            env2 = Enviroment()
            env2.set_parent(struct)  # set the parent of this struct
            env2.add_root(env)  # add env (local scope) as the root of this struct
            for (id, e) in body:
                val = eval(e, env2)
                dict.__setitem__(env2, id, val)  # add value to this level of dict
            env2.remove_root()  # remove the root from env1
            return env2
        case StructMemberAccessExpression(e, dots, id):
            struct: Enviroment = eval(e, env)
            val = struct.get_item(dots, id)
            return val
        case ProcedureExpression(vars, locals, body):
            def fun(*values):
                if len(values) != len(vars):
                    raise Exception(f'wrong number of arguments: is {len(values)}, but should be {len(vars)}')
                env2 = Enviroment()
                root = env.get_root()
                env2.set_parent(root)
                env2 |= {vars[i]: values[i] for i in range(len(values))}
                env2 |= {locals[i]: None for i in range(len(locals))}

                lst = body.seq if body is SequenceExpression else [body]
                for e in lst:
                    if e is AssignmentExpression:
                        var, expr = e
                        if env2.__contains__(var):
                            res = eval(expr, env2)
                        else:
                            # TODO: this should add the varibale as a new global variable
                            # TODO: is 'env' the root env???
                            # res, env = expr.eval(env)
                            raise Exception(f'Not allowed to create new variables')
                    else:
                        res= eval(e, env2)

                return res
            return fun
        case None:
            return None
        case _:
            raise Exception('eval unimplemented')
