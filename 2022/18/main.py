from absl import app
from absl import flags
from typing import Sequence

import collections

FLAGS = flags.FLAGS
_INPUT_FILE = flags.DEFINE_string('input', None, 'Path to the input file.')


class Point(collections.namedtuple('Point', 'x y z')):

  def __add__(self, other) -> 'Point':
    x, y, z = self
    a, b, c = other
    return Point(x + a, y + b, z + c)


Grid = set[Point]


def parse(path: str) -> Grid:

  def parse_point(s: str) -> Point:
    return Point(*map(int, s.split(',')))

  with open(path) as f:
    return set([parse_point(l) for l in f.read().splitlines()])


EDGES = (
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
)


def surface_area(grid: Grid) -> int:
  area = 0
  for p in grid:
    area += 6
    for e in EDGES:
      if (p + e) in grid:
        area -= 1
  return area


def external_surface_area(grid: Grid) -> int:
  xs = [p.x for p in grid]
  ys = [p.y for p in grid]
  zs = [p.z for p in grid]

  lower_bound = min(xs + ys + zs) - 1
  upper_bound = max(xs + ys + zs) + 1

  q = [Point(lower_bound, lower_bound, lower_bound)]
  seen = set()

  area = 0
  while q:
    u = q.pop()
    if u in seen:
      continue

    seen.add(u)
    for e in EDGES:
      v = u + e
      if v in grid:
        area += 1
        continue
      if all(e >= lower_bound and e <= upper_bound for e in v):
        q.append(v)
  return area


def main(argv):
  grid = parse(_INPUT_FILE.value)
  print(surface_area(grid))
  print(external_surface_area(grid))


if __name__ == '__main__':
  app.run(main)
