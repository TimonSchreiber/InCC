from .assignment_expr import *

@dataclass
class SequenceExpression(CompiledExpression):
    seq : list[CompiledExpression]

    def code_r(self, env: dict) -> str:
        return 'pop\n'.join(map(lambda e: e.code_r(env), self.seq))
