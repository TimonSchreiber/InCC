from dataclasses import dataclass

operators = {'+': 'add',
             '-': 'sub',
             '*': 'mul',
             '/': 'div'}

class CompiledExpression:
    def code(self, env):
        return self.code_r(env) + 'pop' + '\n'

    def code_l(self, env):
        raise Exception("code_l uninplemented")

    def code_r(self, env):
        raise Exception("code_r uninplemented")

# @dataclass
# class ProgramExpression(CompiledExpression) :
#     e: CompiledExpression

#     def code_r(self, env):
#         return self.e.code_r(env)

@dataclass
class SelfEvaluatingExpression(CompiledExpression):
    id : CompiledExpression

    def code_r(self,env):
        return f'loadc {self.id}' + '\n'

@dataclass
class BinaryOperatorExpression(CompiledExpression):
    e1: CompiledExpression
    op: str
    e2: CompiledExpression

    def code_r(self,env):
        return self.e1.code_r(env) + self.e2.code_r(env) + operators[self.op]+ '\n'
