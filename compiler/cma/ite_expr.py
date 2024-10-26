from .while_expr import *

@dataclass
class ITEExpression(CompiledExpression):
    condition : CompiledExpression
    if_body   : CompiledExpression
    else_body : CompiledExpression

    def code_r(self, env: dict) -> str:
        return f'if_1:\n' \
                + self.condition.code_r(env) \
                + f'jumpz else_1\n' \
             + f'then_1:\n' \
                + self.if_body.code_r(env) \
                + f'jump endif_1\n' \
             + f'else_1:\n' \
                + self.else_body.code_r(env) \
             + f'endif_1:\n'
