from absl import app
from absl import flags
from collections import namedtuple
from typing import Sequence

import collections
import numpy as np

FLAGS = flags.FLAGS
_INPUT_FILE = flags.DEFINE_string('input', None, 'Path to the input file.')


class Point(namedtuple('Point', 'x y')):

  def __add__(self, other: 'Point') -> 'Point':
    return Point(self.x + other.x, self.y + other.y)


Start = Point
Target = Point


def parse(path: str) -> tuple[np.ndarray, Start, Target]:
  with open(path) as f:
    lines = f.read().splitlines()

  def height(ch: str) -> int:
    if ch == 'S':
      return height('a')
    if ch == 'E':
      return height('z')
    return ord(ch) - ord('a')

  n, m = len(lines), len(lines[0])
  mp = np.zeros([n, m], dtype=np.int32)
  start, target = None, None
  for i in range(n):
    for j in range(m):
      ch = lines[i][j]
      mp[i, j] = height(ch)
      if ch == 'S':
        start = Point(i, j)
      elif ch == 'E':
        target = Point(i, j)

  assert start and target

  return mp, start, target


def bfs(heightmap: np.ndarray, start: Point) -> np.ndarray:

  def is_out_of_bound(p: Point) -> bool:
    nonlocal heightmap
    n, m = heightmap.shape
    x, y = p
    return (x < 0 or x >= n) or (y < 0 or y >= m)

  def is_valid_move(*, frm: Point, to: Point) -> bool:
    return heightmap[frm] <= heightmap[to] + 1

  MOVES = [Point(0, 1), Point(1, 0), Point(-1, 0), Point(0, -1)]

  q = collections.deque()
  seen = set()
  dists = np.full(heightmap.shape, np.inf)

  q.append(start)
  seen.add(start)
  dists[start] = 0
  while q:
    u = q.popleft()
    for mv in MOVES:
      v = u + mv
      if is_out_of_bound(v):
        continue
      if v in seen:
        continue
      if not is_valid_move(frm=u, to=v):
        continue
      q.append(v)
      seen.add(v)
      dists[v] = 1 + dists[u]

  return dists


def main(argv):
  heightmap, start, target = parse(_INPUT_FILE.value)

  # Shortest distance from the target to all other points in the map.
  # The operator `shortest distance (SD)` is commutative. That is `SD(a to b)`
  # is equal to `SD(b to a)`.
  dists = bfs(heightmap, target)

  # Part 1.
  # We look for the shortest path from `start` to `target`.
  print(dists[start])

  # Part 2.
  # We look for the shortest path from any 0 elevation point to `target`.
  best = np.inf
  with np.nditer(heightmap, flags=['multi_index']) as it:
    for h in it:
      if h == 0:
        best = min(best, dists[it.multi_index])
  print(best)


if __name__ == '__main__':
  app.run(main)
