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
  def __init__(self, stmts: list[Stmt], last: Stmt):
    self.stmts = stmts
    self.last = last

class StringLiteral:
  def __init__(self, value: str):
    self.value = value

class NumberLiteral:
  def __init__(self, value: str):
    self.value = value

class Name:
  def __init__(self, name: str):
    self.name = name

class UnaryExpr:
  def __init__(self, op: str, expr: Expr):
    self.op = op
    self.expr = expr

class BinaryExpr:
  def __init__(self, left: Expr, op: str, right: Expr):
    self.left = left
    self.op = op
    self.right = right

class Table:
  def __init__(self, fields: dict[str, Expr]):
    self.fields = fields

class FuncExpr:
  def __init__(self, params: list[Name], body: Block):
    self.params = params
    self.body = body

class FuncCall:
  def __init__(self, func: Expr, args: list[Expr]):
    self.func = func
    self.args = args

class MethodCall:
  def __init__(self, obj: Expr, met: str, args: list[Expr]):
    self.obj = obj
    self.met = met
    self.args = args

class IndexExpr:
  def __init__(self, obj: Expr, index: Expr):
    self.obj = obj
    self.index = index

class PropExpr:
  def __init__(self, obj: Expr, prop: Name):
    self.obj = obj
    self.prop = prop

class IfStmt:
  def __init__(self, cond: Expr, body: Block):
    self.cond = cond
    self.body = body

class LocalFuncDecl:
  def __init__(self, name: Name, params: list[Name], body: Block):
    self.name = name
    self.params = params
    self.body = body

class FuncDecl:
  def __init__(self, name: Name, params: list[Name], body: Block):
    self.name = name
    self.params = params
    self.body = body

class VarDecl:
  def __init__(self, name: Name, value: Expr):
    self.name = name
    self.value = value
