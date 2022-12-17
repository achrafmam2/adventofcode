from absl import app
from absl import flags
from typing import Sequence

import collections
import dataclasses
import functools
import re

FLAGS = flags.FLAGS
_INPUT_FILE = flags.DEFINE_string('input', None, 'Path to the input file.')


@dataclasses.dataclass(frozen=True)
class Valve():
  name: str
  rate: int
  neighbors: tuple[str, ...]


def parse(path: str) -> Sequence[Valve]:
  with open(path) as f:
    lines = f.read().splitlines()

  def parse_valve(l: str) -> Valve:
    regex = ('Valve ([A-Z]{2}) has flow rate=(\d+); ' +
             'tunnels? leads? to valves? (.+)')
    [(name, r, ns)] = re.findall(regex, l)

    return Valve(
        name=name,
        rate=int(r),
        neighbors=tuple(ns.split(', ')),
    )

  return [parse_valve(l) for l in lines]


def all_pairs_shortest_path(
    valves: Sequence[Valve]) -> dict[tuple[Valve, Valve], int]:
  dists = collections.defaultdict(lambda: len(valves) + 1)

  for v in valves:
    dists[(v, v)] = 0

  valve_by_name = {v.name: v for v in valves}
  for v in valves:
    for n in v.neighbors:
      u = valve_by_name[n]
      dists[(v, u)] = 1

  # Floys Warshall.
  for k in valves:
    for i in valves:
      for j in valves:
        dists[(i, j)] = min(dists[(i, j)], dists[(i, k)] + dists[(k, j)])

  return dists


def max_flow(
    valves: Sequence[Valve],
    start_valve_idx: int,
    available_time: int,
    num_agents: int,
) -> int:

  available_time += 1  # Add 1 because we open on the start valve.
  start_valve = valves[start_valve_idx]
  dists = all_pairs_shortest_path(valves)
  nonzero_rate_valves = [v for v in valves if v.rate > 0]
  valve_to_idx = {v: i for (i, v) in enumerate(valves)}

  @functools.cache
  def go(v: Valve, mask: int, rem_time: int, agent_idx: int) -> int:
    nonlocal nonzero_rate_valves, dists

    if rem_time <= 0:
      if agent_idx == 0:
        return 0  # Base case.
      # Switch to the next agent.
      return go(start_valve, mask, available_time, agent_idx - 1)

    rem_time -= 1  # 1 unit of time to open the valve.
    flow = v.rate * rem_time

    best = flow
    if agent_idx > 0:
      # Switch to the next agent.
      best = flow + go(start_valve, mask, available_time, agent_idx - 1)

    for vv in nonzero_rate_valves:
      idx = valve_to_idx[vv]
      if mask & (1 << idx):
        continue
      new_mask = mask | (1 << idx)
      new_rem_time = rem_time - dists[(v, vv)]
      best = max(best, flow + go(vv, new_mask, new_rem_time, agent_idx))

    return best

  return go(start_valve,
            mask=0,
            rem_time=available_time,
            agent_idx=num_agents - 1)


def main(argv):
  valves = parse(_INPUT_FILE.value)

  aa_idx = [i for (i, v) in enumerate(valves) if v.name == 'AA'][0]

  print(
      max_flow(valves, start_valve_idx=aa_idx, available_time=30, num_agents=1))

  # Part 2 takes around ~80 seconds.
  print(
      max_flow(valves, start_valve_idx=aa_idx, available_time=26, num_agents=2))


if __name__ == '__main__':
  app.run(main)
