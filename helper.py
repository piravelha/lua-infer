from models import *
from typing import overload

class Substitution:
  __match_args__ = ("raw",)
  def __init__(self, raw: dict[str, Type] = {}):
    self.raw = raw

  @overload
  def __call__(self, t: Type) -> Type: ...
  @overload
  def __call__(self, t: 'Substitution') -> 'Substitution': ...
  def __call__(self, t):
    match t:
      case TypeVar(n):
        if n in self.raw:
          return self.raw[n]
        return t
      case PrimitiveType(n):
        return t
      case FuncType(ps, b):
        ps = [self(p) for p in ps]
        return FuncType(ps, self(b))
      case TableType(fields):
        return TableType({
          k: self(v)
          for k, v in fields.items()
        })
      case RecursiveType(n, b):
        return RecursiveType(n, self(b))
      case Substitution(raw):
        return Substitution(self.raw | {
          k: self(v)
          for k, v in raw.items()
        })

Context: TypeAlias = dict[str, Type]

def unify(t1: Type, t2: Type) -> Substitution | str:
  match (t1, t2):
    case (TypeVar(n1), TypeVar(n2)) if n1 == n2:
      return Substitution()
    case (_, TypeVar(n2)):
      return Substitution({n2: t1})
    case (TypeVar(_), _):
      return unify(t2, t1)
    case (PrimitiveType(n1), PrimitiveType(n2)) if n1 == n2:
      return Substitution()
    case (FuncType(ps1, b1), FuncType(ps2, b2)):
      if len(ps1) != len(ps2):
        return f"Function types have a different amount of parameters: '{t1}' and '{t2}'"
      s = {}
      for p1, p2 in zip(ps1, ps2):
        r = unify(p1, p2)
        if isinstance(r, str):
          return r
        s |= r.raw
      r = unify(b1, b2)
      if isinstance(r, str):
        return r
      s |= r.raw
      return Substitution(s)
    case (TableType(fs1), TableType(fs2)):
      if len(fs1) != len(fs2):
        return f"Table types have a different amount of fields: '{t1}' and '{t2}'"
      s = {}
      for k1, v1 in fs1.items():
        if k1 not in fs2:
          return f"Key '{k1}' missing on type '{fs2}'"
        v2 = fs2[k1]
        r = unify(v1, v2)
        if isinstance(r, str):
          return r
        s |= r.raw
      return Substitution(s)
    case (RecursiveType(n1, b1), RecursiveType(n2, b2)):
      if n1 != n2:
        return f"Recursive types have different recursive variable: '{t1}', '{t2}'"
      return unify(b1, b2)
    case _, _:
      return f"Types dont unify: '{t1}', '{t2}'"


