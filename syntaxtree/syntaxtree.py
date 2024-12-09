from dataclasses import dataclass
from types import NoneType

def array2list(arr):
    return None if arr is None or len(arr) == 0 else (arr[0], ListExpression(arr[1:]))

def head(lst):
    return lst[0]

def tail(lst):
    return lst[1]

def cons(l1, l2):
    return (l1, l2)

@dataclass
class Expression:
    pass

@dataclass
class SelfEvaluatingExpression(Expression):
    value : any

@dataclass
class ListExpression(Expression):
    lst : NoneType | tuple[Expression, ...]
    def __init__(self, arr):
        self.lst = array2list(arr)

@dataclass
class ArrayExpression(Expression):
    arr : list[Expression]

@dataclass
class ArrayAccessExpression(Expression):
    arr   : list[Expression]
    index : Expression

@dataclass
class BooleanValueExpression(Expression):
    expr : str

@dataclass
class UnaryOperatorExpression(Expression):
    expr : Expression
    op   : str

@dataclass
class BinaryOperatorExpression(Expression):
    e1 : Expression
    e2 : Expression
    op : str

@dataclass
class VariableExpression(Expression):
    name : str

@dataclass
class AssignmentExpression(Expression):
    var  : str
    expr : Expression

@dataclass
class SequenceExpression(Expression):
    seq : list[Expression]

@dataclass
class LoopExpression(Expression):
    number : Expression
    body   : Expression

@dataclass
class ForExpression(Expression):
    start     : Expression
    condition : Expression
    change    : Expression
    body      : Expression

@dataclass
class WhileExpression(Expression):
    condition : Expression
    body      : list[Expression]

@dataclass
class ITEExpression(Expression):
    condition : Expression
    if_body   : Expression
    else_body : Expression

@dataclass
class LockExpression(Expression):
    vars : list[str]
    body : Expression

@dataclass
class LetExpression(Expression):
    vars : list[tuple[str, Expression]]
    body : Expression

@dataclass
class LetRecExpression(Expression):
    vars : list[tuple[str, Expression]]
    body : Expression

@dataclass
class LambdaExpression(Expression):
    vars : list[str]
    body : Expression

@dataclass
class CallExpression(Expression):
    name : Expression
    args : list[Expression]

@dataclass
class DotVariableExpression(Expression):
    dots : int
    name : str

@dataclass
class StructExpression(Expression):
    body : list[tuple[str, Expression]]

@dataclass
class StructExtendExpression(Expression):
    expr : Expression
    body : list[tuple[str, Expression]]

@dataclass
class StructMemberAccessExpression(Expression):
    expr : Expression
    dots : int
    id   : str

@dataclass
class ProcedureExpression(Expression):
    vars   : list[str]
    locals : list[str]
    body   : Expression
