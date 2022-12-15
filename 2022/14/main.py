from absl import app
from absl import flags
from typing import Any, Callable, Sequence

import collections
import copy
import numpy as np
import itertools
import operator

FLAGS = flags.FLAGS
_INPUT_FILE = flags.DEFINE_string('input', None, 'Path to the input file.')

Point = collections.namedtuple('Point', 'x y')
getx = operator.attrgetter('x')
gety = operator.attrgetter('y')
is_point = lambda obj: isinstance(obj, Point)

VOID = 0
ROCK = 1
SOURCE = 2
SAND = 3


def tree_map(
    f: Callable[[Any], Any],
    tree: Any,
    is_leaf: Callable[[Any], bool],
) -> Any:
  """Maps over hierarchichal sequences."""
  if is_leaf(tree):
    return f(tree)
  return [tree_map(f, subtree, is_leaf) for subtree in tree]


def tree_flatten(tree: Any, is_leaf: Callable[[Any], bool]) -> Any:
  """Flattens a hierarchichal sequence."""
  if is_leaf(tree):
    yield tree
  else:
    for subtree in tree:
      yield from tree_flatten(subtree, is_leaf)


def normalize_points(points) -> Sequence[Sequence[Point]]:
  minx = min(map(getx, tree_flatten(points, is_point)))
  miny = min(map(gety, tree_flatten(points, is_point)))

  return tree_map(lambda p: Point(p.x - minx, p.y - miny), points, is_point)


Grid = np.ndarray


def parse(path: str) -> Grid:
  with open(path) as f:
    lines = f.read().splitlines()

  def read_point(l: str) -> Point:
    [x, y] = l.split(',')
    return Point(int(x), int(y))

  def read_points(l: str) -> Sequence[Point]:
    return [read_point(s) for s in l.split(' -> ')]

  points = [read_points(l) for l in lines]
  points = points + [Point(500, 0)]  # Add the SOURCE.
  points = normalize_points(points)

  width = max(map(getx, tree_flatten(points, is_point))) + 1
  height = max(map(gety, tree_flatten(points, is_point))) + 1

  mp = np.full([height, width], VOID, dtype=np.int32)
  for ps in points[:-1]:
    for (a, b) in zip(ps, ps[1:]):
      if a.x == b.x:
        [l, r] = sorted([a.y, b.y])
        for k in range(l, r + 1):
          mp[k, a.x] = 1
      else:
        [l, r] = sorted([a.x, b.x])
        for k in range(l, r + 1):
          mp[a.y, k] = 1
  [srcx, srcy] = points[-1]
  mp[srcy, srcx] = SOURCE

  return mp


def simulate_sand_unit(grid: Grid, p: Point) -> Point:
  """Returns where the unit sand `p` will fall."""
  n, m = grid.shape
  x, y = p

  while True:
    if y + 1 >= n:
      return Point(x, y + 1)
    elif grid[y + 1, x] == VOID:
      y += 1
    elif x - 1 < 0:
      return Point(x - 1, y + 1)
    elif grid[y + 1, x - 1] == VOID:
      x -= 1
      y += 1
    elif x + 1 >= m:
      return Point(x + 1, y + 1)
    elif grid[y + 1, x + 1] == VOID:
      x += 1
      y += 1
    else:
      return Point(x, y)


def simulate_sand(grid: Grid, add_floor: bool = False) -> Grid:
  grid = copy.copy(grid)

  if add_floor:
    n, m = grid.shape
    mp = np.full([n + 2, m + 2 * n], VOID, dtype=np.int32)
    mp[:n, n:n + m] = grid
    mp[n + 1, :] = np.full([1, m + 2 * n], ROCK, dtype=np.int32)
    grid = mp

  n, m = grid.shape
  src = Point(0, 0)
  for i in range(n):
    for j in range(m):
      if grid[i, j] == SOURCE:
        src = Point(j, i)

  while True:
    p = simulate_sand_unit(grid, src)
    if p.x < 0 or p.x >= m or p.y >= n:
      # Out of bound.
      break
    grid[p.y, p.x] = SAND
    if p == src:
      # No new sand unit can come out.
      break

  return grid


def num_sand_units(grid: np.ndarray) -> int:
  return np.sum(np.where(grid == SAND, 1, 0))


def main(argv):
  grid = parse(_INPUT_FILE.value)

  print(num_sand_units(simulate_sand(grid)))
  print(num_sand_units(simulate_sand(grid, add_floor=True)))


if __name__ == '__main__':
  app.run(main)
