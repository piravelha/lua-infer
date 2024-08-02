from helper import *

def infer(env: Context, expr: Tree) -> tuple[Substitution, Type] | str:
  match expr:
    case StringLiteral(_):
      return Substitution(), PrimitiveType("string")
    case NumberLiteral(_):
      return Substitution(), PrimitiveType("number")
    case Name(n):
      if n not in env:
        return f"Unbound variable: {n}"
      return Substitution(), env[n]
    case UnaryExpr(op, e):
      match op:
        case "-":
          r = infer(env, e)
          if isinstance(r, str):
            return r
          s1, t1 = r
          s2 = unify(t1, PrimitiveType("number"))
          if isinstance(s2, str):
            return s2
          return s2(s1), s2(t1)
        case "#":
          r = infer(env, e)
          if isinstance(r, str):
            return r
          s1, t1 = r
          s2 = unify(t1, PrimitiveType("string"))
          if isinstance(s2, str):
            return s2
          return s2(s1), s2(t1)
        case _: assert False
    case BinaryExpr(l, op, r):
      match op:
        case op if op in "+-*/^%":
          res = infer(env, l)
          if isinstance(res, str):
            return res
          s1, t1 = res
          res = infer(env, r)
          if isinstance(res, str):
            return res
          s2, t2 = res
          s3 = unify(t1, PrimitiveType("number"))
          if isinstance(s3, str):
            return s3
          s4 = unify(t2, PrimitiveType("number"))
          if isinstance(s4, str):
            return s4
          return s4(s3(s2(s1))), PrimitiveType("number")
        case "..":
          res = infer(env, l)
          if isinstance(res, str):
            return res
          s1, t1 = res
          res = infer(env, r)
          if isinstance(res, str):
            return res
          s2, t2 = res
          s3 = unify(t1, PrimitiveType("string"))
          if isinstance(s3, str):
            return s3
          s4 = unify(t2, PrimitiveType("string"))
          if isinstance(s4, str):
            return s4
          return s4(s3(s2(s1))), PrimitiveType("string")
        case op if op in ["<", ">", "<=", ">="]:
          res = infer(env, l)
          if isinstance(res, str):
            return res
          s1, t1 = res
          res = infer(env, r)
          if isinstance(res, str):
            return res
          s2, t2 = res
          s3 = unify(t1, PrimitiveType("number"))
          if isinstance(s3, str):
            return s3
          s4 = unify(t2, PrimitiveType("number"))
          if isinstance(s4, str):
            return s4
          return s4(s3(s2(s1))), PrimitiveType("boolean")
        case op if op in ["==", "~="]:
          res = infer(env, l)
          if isinstance(res, str):
            return res
          s1, t1 = res
          res = infer(env, r)
          if isinstance(res, str):
            return res
          s2, t2 = res
          s3 = unify(t1, t2)
          if isinstance(s3, str):
            return s3
          return s3(s2(s1)), PrimitiveType("boolean")
        case op if op in ["and", "or"]:
          res = infer(env, l)
          if isinstance(res, str):
            return res
          s1, t1 = res
          res = infer(env, r)
          if isinstance(res, str):
            return res
          s2, t2 = res
          s3 = unify(t1, PrimitiveType("boolean"))
          if isinstance(s3, str):
            return s3
          s4 = unify(t2, PrimitiveType("boolean"))
          if isinstance(s4, str):
            return s4
          return s4(s3(s2(s1))), PrimitiveType("boolean")
    case Table(fields):
      new = {}
      s = Substitution()
      for k, v in fields.items():
        r = infer(env, v)
        if isinstance(r, str):
          return r
        s1, t1 = r
        s = s1(s)
        new[k] = t1
      return s, TableType(new)
    case FuncExpr(ps, b):
      env = env.copy()
      vars = []
      for p in ps:
        v = TypeVar()
        env[p] = v
        vars.append(v)
      r = infer(env, b)
      if isinstance(r, str):
        return r
      s1, t1 = r
      params = [s1(p) for p in vars]
      return s1, FuncType(params, t1)
    case FuncCall(f, xs):
      r = infer(env, f)
      if isinstance(r, str):
        return r
      s1, t1 = r
      args = []
      for x in xs:
        r = infer(env, x)
        if isinstance(r, str):
          return r
        s2, t2 = r
        args.append(t2)
        s1 = s2(s1)
      if not isinstance(t1, FuncType):
        return f"Attempting to call non-function type: '{t1}'"
      for a, b in zip(t1.params, args):
        s3 = unify(a, b)
        if isinstance(s3, str):
          return s3
        s1 = s3(s1)
      return s1, s1(t1.ret)
    case VarDecl(n, v):
      r = infer(env, v)
      if isinstance(r, str):
        return r
      s1, t1 = r
      env[n] = t1
      return s1, PrimitiveType("nil")
    case Block(stmts, last):
      s1 = Substitution()
      for s in stmts:
        r = infer(env, s)
        if isinstance(r, str):
          return r
        s2, t2 = r
        s1 = s2(s1)
      r = infer(env, last)
      if isinstance(r, str):
        return r
      s3, t3 = r
      return s3(s1), t3
  print(expr)
  assert False
