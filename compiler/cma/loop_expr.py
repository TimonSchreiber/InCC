from .sequence_expr import *

@dataclass
class LoopExpression(CompiledExpression):
    number : CompiledExpression
    body   : CompiledExpression

    def code_r(self, env: dict) -> str:
        return ''
