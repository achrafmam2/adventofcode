import copy
import dataclasses
import more_itertools
import re

from absl import app
from absl import flags
from typing import Sequence

FLAGS = flags.FLAGS
_INPUT_FILE = flags.DEFINE_string('input', None, 'Path to the input file.')


@dataclasses.dataclass(frozen=True)
class Cmd():
  qty: int
  frm: int
  to: int


Stacks = list[list[str]]


def parse(path: str) -> (Stacks, Sequence[Cmd]):
  with open(path) as f:
    lines = f.read().splitlines()

  [cargo_lines, cmd_lines] = more_itertools.split_at(lines, lambda l: not l)

  num_stacks = sum(d != ' ' for d in cargo_lines[-1])
  stacks = [[] for _ in range(num_stacks)]
  for l in cargo_lines[:-1]:
    for i in range(num_stacks):
      if (ch := l[4 * i + 1]) and (not ch.isspace()):
        stacks[i].append(ch)
  stacks = [list(reversed(s)) for s in stacks]

  cmds = []
  for l in cmd_lines:
    m = re.match(r"move (\d+) from (\d+) to (\d+)", l)
    qty, frm, to = m.groups()
    cmds.append(Cmd(qty=int(qty), frm=int(frm) - 1, to=int(to) - 1))

  return (stacks, cmds)


def move_crates(
    stacks: Stacks,
    cmds: Sequence[Cmd],
    *,
    legacy_crate_mover: bool = False,
) -> Stacks:
  xs = copy.deepcopy(stacks)
  for c in cmds:
    n, frm, to = c.qty, c.frm, c.to

    ys = xs[frm][-n:]
    if legacy_crate_mover:
      ys = reversed(ys)
    del xs[frm][-n:]

    xs[to].extend(ys)
  return xs


def tops(stacks: Stacks) -> str:
  return ''.join(s[-1] for s in stacks)


def main(argv):
  stacks, cmds = parse(_INPUT_FILE.value)

  s = move_crates(stacks, cmds, legacy_crate_mover=True)
  print(tops(s))

  s = move_crates(stacks, cmds)
  print(tops(s))


if __name__ == '__main__':
  app.run(main)
