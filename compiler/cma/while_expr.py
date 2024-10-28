from .for_expr import *

@dataclass
class WhileExpression(CompiledExpression):
    condition : CompiledExpression
    body      : CompiledExpression

    def code_r(self, env: dict) -> str:
        lbl = label()
        # TODO: what does loadc 0 and pop do here?
        return 'loadc 0\n' \
             + f'while_{lbl}:\n' \
             + self.condition.code_r(env) \
             + f'jumpz endwhile_{lbl}\n' \
             + 'pop\n' \
             + f'do_{lbl}:\n' \
             + self.body.code_r(env) \
             + f'jump while_{lbl}\n' \
             + f'endwhile_{lbl}:\n'
