from .while_expr import *

@dataclass
class ProcedureExpression(CompiledExpression):
    vars   : list[str]
    locals : list[str]
    body   : CompiledExpression

    def code_r(self, env: dict) -> str:
        lbl = label()
        p_env = {}
        p_env['..'] = env
        p_env |= {var : {'addr': new_addr(8), 'scope': 'args', 'size': 8} for var in self.vars}
        p_env |= {var : {'addr': new_addr(8), 'scope': 'local', 'size': 8} for var in self.locals}
        return ''

@dataclass
class CallExpression(CompiledExpression):
    name : str
    args : list[CompiledExpression]

    def code_r(self, env: dict) -> str:
        fun, env = self.name.eval(env)
        vals = [arg.eval(env)[0] for arg in self.args]
        return (fun(*vals), env)
