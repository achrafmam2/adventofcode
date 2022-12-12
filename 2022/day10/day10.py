from absl import app
from absl import flags
from typing import Sequence, Callable

import dataclasses
import enum
import numpy as np

FLAGS = flags.FLAGS
_INPUT_FILE = flags.DEFINE_string('input', None, 'Path to the input file.')


class Opcode(enum.StrEnum):
  NOOP = 'noop'
  ADDX = 'addx'


@dataclasses.dataclass(frozen=True)
class Instruction():
  opcode: Opcode
  argv: tuple[str, ...] = ()


# Represents the state of the VM.
# In this problem it is a simple variable.
State = int

CallbackFn = Callable[[State], None]


def simulate(
    instructions: Sequence[Instruction],
    state: State,
    callbacks: Sequence[CallbackFn] = (),
) -> State:
  """Simulates the input instructions.

  Argv:
    instructions: the instructions to simulate.
    state: the initial state of the VM.
    callbacks: callbacks that are called at the beginning of each cycle.
  """

  Args = tuple[str, ...]

  def addx(state: State, argv: Args) -> State:
    [x] = argv
    return state + int(x)

  def noop(state: State, argv: Args) -> State:
    assert (not argv)
    return state

  handlers = {
      Opcode.ADDX: addx,
      Opcode.NOOP: noop,
  }

  simulation_cycles = {
      Opcode.ADDX: 2,
      Opcode.NOOP: 1,
  }

  for i in instructions:
    num_cycles = simulation_cycles[i.opcode]
    for _ in range(num_cycles):
      for callback in callbacks:
        callback(state)
    handler = handlers[i.opcode]
    state = handler(state, i.argv)

  return state


def parse(path: str) -> Sequence[Instruction]:
  with open(path) as f:
    lines = f.read().splitlines()

  def parse_instruction(s: str) -> Instruction:
    match s.split():
      case ['noop']:
        return Instruction(Opcode.NOOP)
      case ['addx', x]:
        return Instruction(Opcode.ADDX, argv=(x,))

  return [parse_instruction(l) for l in lines]


def main(argv):
  instructions = parse(_INPUT_FILE.value)

  cpu_counter, signal_strength = 0, 0

  def debug_fn(s: State):
    nonlocal cpu_counter, signal_strength
    cpu_counter += 1
    if ((cpu_counter - 20) % 40 == 0):
      signal_strength += cpu_counter * s

  WINDOW_HEIGHT = 6
  WINDOW_WIDTH = 40
  crt = np.zeros([WINDOW_HEIGHT, WINDOW_WIDTH], dtype=bool)
  crt_counter = 0

  def draw(s: State):
    nonlocal crt, crt_counter

    row = crt_counter // WINDOW_WIDTH
    col = crt_counter % WINDOW_WIDTH
    if s - 1 <= col <= s + 1:
      # If the CRT is drawing where the sprite is, then a a pixel is emitted.
      # The location of the 3 pixel wide sprite is represented by the state of
      # the VM (e.g., indexes [state -1, state, state + 1]).
      crt[row, col] = True
    crt_counter += 1

  simulate(instructions, state=State(1), callbacks=[debug_fn, draw])

  # Part 1.
  print(signal_strength)

  # Part 2.
  for i in range(WINDOW_HEIGHT):
    for j in range(WINDOW_WIDTH):
      print('#' if crt[i, j] else '.', end='')
    print()


if __name__ == '__main__':
  app.run(main)
