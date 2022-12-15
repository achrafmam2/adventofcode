from absl import app
from absl import flags
from typing import Sequence, Iterable

import collections
import intervals as I
import functools
import operator
import re

FLAGS = flags.FLAGS
_INPUT_FILE = flags.DEFINE_string('input', None, 'Path to the input file.')
_VERBOSE = flags.DEFINE_bool('verbose', False,
                             'Include extra information during execution.')


class Point(collections.namedtuple('Point', 'x y')):

  def __add__(self, other) -> 'Point':
    x, y = self
    a, b = other
    return Point(x + a, y + b)


def dist(p0: Point, p1: Point) -> int:
  x, y = p0
  a, b = p1
  return abs(x - a) + abs(y - b)


Sensors = Sequence[Point]
Beacons = Sequence[Point]


def parse(path: str) -> tuple[Sensors, Beacons]:
  with open(path) as f:
    lines = f.read().splitlines()

  def parse_line(l: str) -> tuple[Point, Point]:
    regex = r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)'
    [(x, y, a, b)] = re.findall(regex, l)
    return (Point(int(x), int(y)), Point(int(a), int(b)))

  # This converts a list of pairs to two lists.
  # Example:
  #   >>> xs = [('1','a'),('2','b')]
  #   >>> list(zip(*xs))
  #   [('1', '2'), ('a', 'b')]

  sensors, beacons = zip(*[parse_line(l) for l in lines])
  return (sensors, beacons)


def nobeacon_interval(
    *,
    sensor: Point,
    beacon: Point,
    yline: int,
) -> I.Interval:
  """Returns an interval where no beacon can possibly exist."""
  x, _ = sensor
  rad = dist(sensor, beacon) - dist(sensor, Point(x, yline))
  if rad < 0:
    return I.open(x, x)
  return I.closed(x - rad, x + rad)


def merge_intervals(intervals: Iterable[I.Interval]) -> I.Interval:
  return functools.reduce(operator.__or__, intervals)


def interval_len(i: I.Interval) -> int:
  length = 0
  for j in i:
    width = j.upper - j.lower + 1
    if not j.left:
      width -= 1
    if not j.right:
      width -= 1
    length += width
  return length


def singleton(i: I.Interval) -> int:
  """Returns the only point in the input interval.

  The funtion fails if the interval does not contain exactly one point.
  """
  l, r = i.lower, i.upper
  if not i.left:
    l += 1
  if not i.right:
    r -= 1

  assert l == r
  return l


def main(argv):
  sensors, beacons = parse(_INPUT_FILE.value)

  # Part 1.
  yline = 2000000
  intervals = [
      nobeacon_interval(sensor=s, beacon=b, yline=yline)
      for (s, b) in zip(sensors, beacons)
  ]
  u = merge_intervals(intervals)
  for (x, y) in beacons:
    if y == yline:
      u -= I.closed(x, x)

  print(interval_len(u))

  # Part 2.
  n = 4000000
  for y in range(n + 1):
    if _VERBOSE.value and (y % 10000 == 0):
      print('Iteration ', y)

    intervals = [
        nobeacon_interval(sensor=s, beacon=b, yline=y)
        for (s, b) in zip(sensors, beacons)
    ]

    u = merge_intervals(intervals)
    u &= I.closed(0, n)  # Clip to [0, n].

    if u != I.closed(0, n):
      # Get the singleton point not covered by the interval u.
      u = ~u & I.closed(0, n)
      x = singleton(u)
      print(x * n + y)
      break


if __name__ == '__main__':
  app.run(main)
