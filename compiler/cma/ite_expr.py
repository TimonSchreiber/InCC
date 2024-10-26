from .while_expr import *

@dataclass
class ITEExpression(CompiledExpression):
    condition : CompiledExpression
    if_body   : CompiledExpression
    else_body : CompiledExpression

    def code_r(self, env: dict) -> str:
        lbl = label()
        if self.else_body is None:  # TODO: not the best solution
            self.else_body = SelfEvaluatingExpression(0)
        return f'if_{lbl}:\n' \
                + self.condition.code_r(env) \
                + f'jumpz else_{lbl}\n' \
             + f'then_{lbl}:\n' \
                + self.if_body.code_r(env) \
                + f'jump endif_{lbl}\n' \
             + f'else_{lbl}:\n' \
                + self.else_body.code_r(env) \
             + f'endif_{lbl}:\n'
