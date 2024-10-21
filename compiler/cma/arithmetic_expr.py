from dataclasses import dataclass

binary_operators = {
    '+': 'add',
    '-': 'sub',
    '*': 'mul',
    '/': 'div'
}

unary_operators = {
    '-': 'uminus'
}

class CompiledExpression:
    def code(self, env: dict) -> str:
        return self.code_r(env) + 'pop' + '\n'

    def code_l(self, env: dict) -> str:
        raise Exception("code_l uninplemented")

    def code_r(self, env: dict) -> str:
        raise Exception("code_r uninplemented")

@dataclass
class SelfEvaluatingExpression(CompiledExpression):
    id : CompiledExpression

    def code_r(self, env: dict) -> str:
        return f'loadc {self.id}' + '\n'

@dataclass
class BinaryOperatorExpression(CompiledExpression):
    e1: CompiledExpression
    op: str
    e2: CompiledExpression

    def code_r(self, env: dict) -> str:
        return self.e1.code_r(env) \
             + self.e2.code_r(env) \
             + binary_operators[self.op] + '\n'

@dataclass
class UnaryOperatorExpression(CompiledExpression):
    op: str
    e1: CompiledExpression

    def code_r(self, env: dict) -> str:
        return self.e1.code_r(env) \
             + unary_operators[self.op] + '\n'

@dataclass
class ParenthesisExpression(CompiledExpression):
    e1: CompiledExpression

    def code_r(self, env: dict) -> str:
        return self.e1.code_r(env)
