from .sequence_expr import *

label_counter = 0
def label() -> int:
   global label_counter
   label_counter += 1
   return label_counter

@dataclass
class LoopExpression(CompiledExpression):
    number : CompiledExpression
    body   : CompiledExpression

    def code_r(self, env: dict) -> str:
        lbl = label()
        return 'loadc 0\n' \
             f'loop_{lbl}:\n' \
                + self.condition.code_r(env) \
                + f'jumpz endloop_{lbl}\n' \
                + 'pop\n' \
             + f'do_{lbl}:\n' \
                + self.body.code_r(env) \
                + f'jump loop_{lbl}\n' \
             + f'endloop_{lbl}:\n'
