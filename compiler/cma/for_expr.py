from .loop_expr import *

@dataclass
class ForExpression(CompiledExpression):
    start     : CompiledExpression
    condition : CompiledExpression
    change    : CompiledExpression
    body      : CompiledExpression

    def code_r(self, env: dict) -> str:
        lbl = label()
        # TODO: not working -> segfault
        return self.start.code_r(env) \
             +'loadc 0\n' \
             + f'for_{lbl}:\n' \
             + self.condition.code_r(env) \
             + f'jumpz endfor_{lbl}\n' \
             + 'pop\n' \
             + f'do_{lbl}:\n' \
             + self.body.code_r(env) \
             + self.change.code_r(env) \
             + f'jump for_{lbl}\n' \
             + f'endfor_{lbl}:\n'
