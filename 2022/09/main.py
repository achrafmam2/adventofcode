from absl import app
from absl import flags
from collections import namedtuple
from typing import Sequence

import dataclasses
import enum

FLAGS = flags.FLAGS
_INPUT_FILE = flags.DEFINE_string('input', None, 'Path to the input file.')


class Direction(enum.StrEnum):
  Up = 'U'
  Down = 'D'
  Left = 'L'
  Right = 'R'


@dataclasses.dataclass(frozen=True)
class Cmd():
  direction: Direction
  count: int


class Point(namedtuple('Point', 'x y')):

  def __add__(self, other: 'Point') -> 'Point':
    return Point(self.x + other.x, self.y + other.y)


def l0_dist(p1: Point, p2: Point) -> int:
  return max(abs(p1.x - p2.x), abs(p1.y - p2.y))


def l1_dist(p1: Point, p2: Point) -> int:
  return abs(p1.x - p2.x) + abs(p1.y - p2.y)


# A chain is a sequence of knots.
# The head of the chain is the first element of the sequence
# and the tail of the chain is the last element of the sequence.
Chain = Sequence[Point]


def move(chain: Chain, delta: Point) -> Chain:
  ch = list(chain)
  ch[0] += delta

  for i in range(1, len(chain)):
    prev, cur = ch[i - 1], ch[i]

    if l0_dist(prev, cur) <= 1:
      continue

    dxdy = Point(0, 0)
    best = 10000  # A high value.
    for dx in [-1, 0, 1]:
      for dy in [-1, 0, 1]:
        dist = l1_dist(prev, cur + Point(dx, dy))
        if dist < best:
          dxdy = Point(dx, dy)
          best = dist
    ch[i] += dxdy

  return ch


def simulate(chain: Chain, cmds: Sequence[Cmd]) -> int:
  deltas = {
      Direction.Up: Point(1, 0),
      Direction.Down: Point(-1, 0),
      Direction.Right: Point(0, 1),
      Direction.Left: Point(0, -1),
  }

  visited = {chain[-1]}
  for cmd in cmds:
    d, n = cmd.direction, cmd.count
    for _ in range(n):
      delta = deltas[d]
      chain = move(chain, delta)
      visited.add(chain[-1])
  return len(visited)


def parse(path: str) -> Sequence[Cmd]:
  with open(path) as f:
    lines = f.read().splitlines()

  def parse_line(l: str) -> Cmd:
    c, n = l.split(' ')
    return Cmd(direction=Direction(c), count=int(n))

  return list(map(parse_line, lines))


def main(argv):
  cmds = parse(_INPUT_FILE.value)

  chain2 = (Point(0, 0),) * 2
  print(simulate(chain2, cmds))

  chain10 = (Point(0, 0),) * 10
  print(simulate(chain10, cmds))


if __name__ == '__main__':
  app.run(main)
