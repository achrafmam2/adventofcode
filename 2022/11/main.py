from absl import app
from absl import flags
from typing import Sequence, Callable, Union

import copy
import dataclasses
import heapq
import math
import functools
import more_itertools
import operator
import re

FLAGS = flags.FLAGS
_INPUT_FILE = flags.DEFINE_string('input', None, 'Path to the input file.')


class ModedInt():
  """A moded int allows simple modular arithmetic (e.g, `+`, `*`) on big integers.

  Operations on a `ModedInt` are themselves `ModedInt`s. To get the result of computation
  as a Python int, use the builtin modulo operator `%`.

  >>> m = (ModedInt(5) * 6) * ModedInt(2) # (5 * 6) * 2 = 60
  >>> m % 6
  0
  """

  def __init__(self, x: int):
    self._x = lambda mod: x % mod

  def __add__(self, other):
    if isinstance(other, int):
      other = ModedInt(other)

    md = ModedInt(0)
    md._x = functools.lru_cache()(lambda mod:
                                  (self._x(mod) + other._x(mod)) % mod)
    return md

  def __mul__(self, other):
    if isinstance(other, int):
      other = ModedInt(other)

    md = ModedInt(0)
    md._x = functools.lru_cache()(lambda mod:
                                  (self._x(mod) * other._x(mod)) % mod)
    return md

  def __mod__(self, mod):
    assert isinstance(mod, int)
    return self._x(mod)


IntLike = Union[int, ModedInt]
OperationFn = Callable[[IntLike], IntLike]
TestFn = Callable[[IntLike], int]


@dataclasses.dataclass
class Monkey():
  items: list[IntLike]
  opfn: OperationFn
  testfn: TestFn
  num_items_inspected: int = 0


def parse(path: str) -> Sequence[Monkey]:
  with open(path) as f:
    lines = f.read().splitlines()

  is_empty_line = lambda s: s == ''
  grps = more_itertools.split_at(lines, is_empty_line)

  def parse_items(s: str) -> list[IntLike]:
    return [ModedInt(int(e)) for e in s.split(', ')]

  def make_operation_fn(expr: str) -> OperationFn:

    def fn(old: IntLike) -> int:
      nonlocal expr
      return eval(expr)

    return fn

  def make_test_fn(mod: int, m0: int, m1: int) -> TestFn:
    """Returns a function that returns m0 if the input is divible by mod otherwise m1."""

    def fn(v: IntLike) -> int:
      nonlocal mod, m0, m1
      if (v % mod) == 0:
        return m0
      return m1

    return fn

  def parse_monkey_specs(lines: str) -> Monkey:
    TEMPLATE = r'''Monkey \d+:
  Starting items: (.*)
  Operation: new = (.*)
  Test: divisible by (\d+)
    If true: throw to monkey (\d+)
    If false: throw to monkey (\d+)'''

    m = re.fullmatch(TEMPLATE, '\n'.join(lines))
    assert m
    return Monkey(items=parse_items(m[1]),
                  opfn=make_operation_fn(m[2]),
                  testfn=make_test_fn(int(m[3]), int(m[4]), int(m[5])))

  return [parse_monkey_specs(grp) for grp in grps]


def simulate_turn(monkeys: list[Monkey], turn_idx: int) -> list[Monkey]:
  ms = copy.copy(monkeys)

  m = ms[turn_idx]
  for itm in m.items:
    itm = m.opfn(itm)
    to = m.testfn(itm)
    ms[to].items.append(itm)

  m.num_items_inspected += len(m.items)
  m.items = []

  return ms


def simulate_round(monkeys: list[Monkey]) -> list[Monkey]:
  for i in range(len(monkeys)):
    monkeys = simulate_turn(monkeys, i)
  return monkeys


def main(argv):
  monkeys = parse(_INPUT_FILE.value)

  for _ in range(10000):
    monkeys = simulate_round(monkeys)

  num_itms_insepected_key = operator.attrgetter('num_items_inspected')
  print(math.prod(heapq.nlargest(2, map(num_itms_insepected_key, monkeys))))


if __name__ == '__main__':
  app.run(main)
