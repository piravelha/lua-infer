from typing import TypeAlias, Union

Expr: TypeAlias = Union[
  'StringLiteral',
  'NumberLiteral',
  'Name',
  'UnaryExpr',
  'BinaryExpr',
  'Table',
  'FuncExpr',
  'FuncCall',
  'MethodCall',
  'IndexExpr',
  'PropExpr',
]

Stmt: TypeAlias = Union[
  'FuncCall',
  'IfStmt',
  'LocalFuncDecl',
  'FuncDecl',
  'VarDecl',
]

class Block:
  __match_args__ = ("stmts", "last")
  def __init__(self, stmts: list[Stmt], last: Stmt):
    self.stmts = stmts
    self.last = last

class StringLiteral:
  __match_args__ = ("value",)
  def __init__(self, value: str):
    self.value = value

class NumberLiteral:
  __match_args__ = ("value",)
  def __init__(self, value: str):
    self.value = value

class Name:
  __match_args__ = ("name",)
  def __init__(self, name: str):
    self.name = name

class UnaryExpr:
  __match_args__ = ("op", "expr")
  def __init__(self, op: str, expr: Expr):
    self.op = op
    self.expr = expr

class BinaryExpr:
  __match_args__ = ("left", "op", "right")
  def __init__(self, left: Expr, op: str, right: Expr):
    self.left = left
    self.op = op
    self.right = right

class Table:
  __match_args__ = ("fields",)
  def __init__(self, fields: dict[str, Expr]):
    self.fields = fields

class FuncExpr:
  __match_args__ = ("params", "body")
  def __init__(self, params: list[Name], body: Block):
    self.params = params
    self.body = body

class FuncCall:
  __match_args__ = ("func", "args")
  def __init__(self, func: Expr, args: list[Expr]):
    self.func = func
    self.args = args

class MethodCall:
  __match_args__ = ("obj", "met", "args")
  def __init__(self, obj: Expr, met: str, args: list[Expr]):
    self.obj = obj
    self.met = met
    self.args = args

class IndexExpr:
  __match_args__ = ("obj", "index")
  def __init__(self, obj: Expr, index: Expr):
    self.obj = obj
    self.index = index

class PropExpr:
  __match_args__ = ("obj", "prop")
  def __init__(self, obj: Expr, prop: Name):
    self.obj = obj
    self.prop = prop

class IfStmt:
  __match_args__ = ("cond", "body")
  def __init__(self, cond: Expr, body: Block):
    self.cond = cond
    self.body = body

class LocalFuncDecl:
  __match_args__ = ("name", "params", "body")
  def __init__(self, name: Name, params: list[Name], body: Block):
    self.name = name
    self.params = params
    self.body = body

class FuncDecl:
  __match_args__ = ("name", "params", "body")
  def __init__(self, name: Name, params: list[Name], body: Block):
    self.name = name
    self.params = params
    self.body = body

class VarDecl:
  __match_args__ = ("name", "value")
  def __init__(self, name: Name, value: Expr):
    self.name = name
    self.value = value

Type: TypeAlias = Union[
  'TypeVar',
  'PrimitiveType',
  'FuncType',
  'TableType',
]

class TypeVar:
  __match_args__ = ("name",)
  iota = 0
  def __init__(self, name: str | None = None):
    if not name:
      TypeVar.iota += 1
      name = f"t{TypeVar.iota}"
    self.name = name

class PrimitiveType:
  __match_args__ = ("name",)
  def __init__(self, name: str):
    self.name = name

class FuncType:
  __match_args__ = ("params", "ret")
  def __init__(self, params: list[Type], ret: Type):
    self.params = params
    self.ret = ret

class TableType:
  __match_args__ = ("fields",)
  def __init__(self, fields: dict[str, Type]):
    self.fields = fields

class RecursiveType:
  __match_args__ = ("name", "body")
  def __init__(self, name: str, body: Type):
    self.name = name
    self.body = body
