from .comparison_expr import *
from .enviroment import getitem, new_addr

@dataclass
class VariableExpression(CompiledExpression):
    name : str

    def code_l(self, env: dict) -> str:
        load = 'loadc' if getitem(env, self.name)['scope'] == 'global' else 'loadrc'
        return f'{load} {getitem(env, self.name)["addr"]}\n'

    def code_r(self, env: dict) -> str:
        # load = 'loadc' if getitem(env, self.name)['scope'] == 'global' else 'loadrc'
        # return f'{load} {getitem(env, self.name)["addr"]}\n' \
        return self.code_l(env) \
             + 'load\n'

@dataclass
class AssignmentExpression(CompiledExpression):
    var  : str
    expr : CompiledExpression

    def code_r(self, env: dict) -> str:
        if self.var not in env:
            env[self.var] = {'addr': new_addr(8), 'scope': 'global', 'size': 8}
        var = VariableExpression(self.var)
        return self.expr.code_r(env) \
             + var.code_l(env) \
             + 'store\n'
