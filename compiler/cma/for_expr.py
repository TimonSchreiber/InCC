from .loop_expr import *

@dataclass
class ForExpression(CompiledExpression):
    start     : CompiledExpression
    condition : CompiledExpression
    change    : CompiledExpression
    body      : CompiledExpression

    def code_r(self, env: dict) -> str:
        return ''
