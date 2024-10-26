from .comparison_expr import *
from .enviroment import new_addr

@dataclass
class VariableExpression(CompiledExpression):
    name : str

    def code_l(self, env: dict) -> str:
        return f'loadc {env[self.name]["addr"]}\n'

    def code_r(self, env: dict) -> str:
        return f'loadc {env[self.name]["addr"]}\n' \
                'load\n'

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
