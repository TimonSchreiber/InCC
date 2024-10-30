from .ite_expr import *

@dataclass
class ProcedureExpression(CompiledExpression):
    vars   : list[str]
    locals : list[str]
    body   : CompiledExpression

    def code_r(self, env: dict) -> str:
        lbl = label()

        p_env = {'..' : env}

        p_env |= {self.vars[i] : {'addr': -(16+i*8), 'scope': 'args',  'size': 8} for i in range(len(self.vars))}   # offset 2 values in - direction
        p_env |= {self.locals[i] : {'addr': (8+i*8), 'scope': 'local', 'size': 8} for i in range(len(self.locals))} # offset 1 value in + direction

        return f'jump endproc_{lbl}\n' \
             + f'proc_{lbl}:\n' \
             + f'enter\n' \
             + f'alloc {8 * len(self.locals)}\n' \
             + self.body.code_r(p_env) \
             + f'loadrc -16\n' \
             + f'store\n' \
             + f'pop\n' \
             + f'ret\n' \
             + f'endproc_{lbl}:\n' \
             + f'loadc proc_{lbl}\n'

@dataclass
class CallExpression(CompiledExpression):
    name : CompiledExpression
    args : list[CompiledExpression]

    def code_r(self, env: dict) -> str:
        values = ''.join([expr.code_r(env) for expr in self.args[::-1]])
        return values \
             + f'mark\n' \
             + self.name.code_r(env) \
             + f'call\n' \
             + f'pop\n' \
             + f'slide {8 * len(self.args) - 8} {8}\n'
