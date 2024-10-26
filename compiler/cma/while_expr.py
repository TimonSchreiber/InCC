from .for_expr import *

@dataclass
class WhileExpression(CompiledExpression):
    condition : CompiledExpression
    body      : CompiledExpression

    def code_r(self, env: dict) -> str:
        return ''
