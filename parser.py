from lark import Lark, Transformer
from infer import *

with open("grammar.lark") as f:
  grammar = f.read()

parser = Lark(grammar)

class ToTree(Transformer):
  def block(self, args):
    return Block(args[:-1], args[-1])
  def var_decl(self, args):
    return VarDecl(*args)
  def return_stmt(self, args):
    return args[0]
  def var(self, args):
    return Name(args[0])
  def func_call(self, args):
    p, args = args
    return FuncCall(p, args.children)
  def func_expr(self, args):
    params, body = args[0]
    return FuncExpr(params, body)
  def func_body(self, args):
    params = []
    body = args[0]
    if len(args) == 2:
      params, body = args
      params = params.children
    return params, body
  def table(self, args):
    fields = []
    if args:
      fields = args[0]
    new = {}
    for f in fields:
      n, v = f.children
      new[n] = v
    return Table(new)
  def or_expr(self, args):
    return BinaryExpr(args[0], "or", args[1])
  def and_expr(self, args):
    return BinaryExpr(args[0], "and", args[1])
  def eq_expr(self, args):
    return BinaryExpr(*args)
  def rel_expr(self, args):
    return BinaryExpr(*args)
  def add_expr(self, args):
    return BinaryExpr(*args)
  def mul_expr(self, args):
    return BinaryExpr(*args)
  def pow_expr(self, args):
    return BinaryExpr(*args)
  def unary_expr(self, args):
    return UnaryExpr(*args)
  def NAME(self, token):
    return token.value
  def NUMBER(self, token):
    return NumberLiteral(token.value)
  def STRING(self, token):
    return StringLiteral(token.value)


code = """

local add = function(x)
  return x + 1
end

return add("123")

"""

tree = parser.parse(code)
expr = ToTree().transform(tree)
result = infer({}, expr)
if isinstance(result, str):
  print(f"ERROR: {result}")
else:
  _, type = result
  print(f"TYPE: {type}")
