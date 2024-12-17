import aocd
import re
import abc
from tqdm import tqdm as progress

import cli

sample_data = """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""
data = sample_data if cli.sample else aocd.data

[registers, program] = data.split("\n\n")


class Machine:
    def __init__(self, registers: list[str]):
        for register in registers:
            (reg, val) = re.match(r"Register (\w): (\d+)", register).groups()
            match reg:
                case "A":
                    self.ram = int(val)
                case "B":
                    self.rbm = int(val)
                case "C":
                    self.rcm = int(val)

        self.out = []


class Program:
    def __init__(self, octal_code: str):
        self.octals = list(map(int, octal_code.split(",")))
        self.instruction_pointer = 0

    def reset(self):
        self.instruction_pointer = 0

    def octal_source(self) -> str:
        return ",".join(map(str, self.octals))

    def eop(self) -> bool:
        return self.instruction_pointer >= len(self.octals)

    def octal(self, off: int) -> int:
        return self.octals[self.instruction_pointer + off]

    def jump(self, ptr: int) -> None:
        self.instruction_pointer = ptr

    def advance(self, steps: int) -> int:
        self.instruction_pointer += steps
        return self.instruction_pointer


class Instruction(abc.ABC):
    @abc.abstractmethod
    def disasm(self, prog: Program, mach: Machine) -> str:
        pass

    @abc.abstractmethod
    def execute(self, prog: Program, mach: Machine) -> None:
        pass

    def combo(self, operand: int, mach: Machine) -> int:
        if operand <= 3:
            return operand
        match operand:
            case 4:
                return mach.ram
            case 5:
                return mach.rbm
            case 6:
                return mach.rcm
        raise "Bruv..."

    def combo_str(self, operand: int, mach: Machine) -> str:
        if operand <= 3:
            return str(operand)
        match operand:
            case 4:
                return "ram"
            case 5:
                return "rbm"
            case 6:
                return "rcm"
        return "err"


class ADivide(Instruction):
    def disasm(self, prog: Program, mach: Machine) -> str:
        return f"div ram ram {self.combo_str(prog.octal(1), mach)}"

    def execute(self, prog: Program, mach: Machine) -> None:
        mach.ram = mach.ram // (2 ** self.combo(prog.octal(1), mach))
        prog.advance(2)


class BDivide(Instruction):
    def disasm(self, prog: Program, mach: Machine) -> str:
        return f"div rbm ram {self.combo_str(prog.octal(1), mach)}"

    def execute(self, prog: Program, mach: Machine) -> None:
        mach.rbm = mach.ram // (2 ** self.combo(prog.octal(1), mach))
        prog.advance(2)


class CDivide(Instruction):
    def disasm(self, prog: Program, mach: Machine) -> str:
        return f"div rcm ram {self.combo_str(prog.octal(1), mach)}"

    def execute(self, prog: Program, mach: Machine) -> None:
        mach.rcm = mach.ram // (2 ** self.combo(prog.octal(1), mach))
        prog.advance(2)


class BitwiseXOR(Instruction):
    def disasm(self, prog: Program, mach: Machine) -> str:
        return f"bxl rbm rcm"

    def execute(self, prog: Program, mach: Machine) -> None:
        mach.rbm = mach.rbm ^ mach.rcm
        prog.advance(2)


class BitwiseXOR_Op(Instruction):
    def disasm(self, prog: Program, mach: Machine) -> str:
        return f"bxl rbm {prog.octal(1)}"

    def execute(self, prog: Program, mach: Machine) -> None:
        mach.rbm = mach.rbm ^ prog.octal(1)
        prog.advance(2)


class Modulo(Instruction):
    def disasm(self, prog: Program, mach: Machine) -> str:
        return f"bst rbm {self.combo_str(prog.octal(1), mach)}"

    def execute(self, prog: Program, mach: Machine) -> None:
        mach.rbm = self.combo(prog.octal(1), mach) % 8
        prog.advance(2)


class JumpNotZero(Instruction):
    def disasm(self, prog: Program, mach: Machine) -> str:
        return f"bst rbm {self.combo_str(prog.octal(1), mach)}"

    def execute(self, prog: Program, mach: Machine) -> None:
        if mach.ram == 0:
            prog.advance(2)
        else:
            prog.jump(prog.octal(1))


class Output(Instruction):
    def disasm(self, prog: Program, mach: Machine) -> str:
        return f"out {self.combo_str(prog.octal(1), mach)} # {self.gen_out(prog, mach)}"

    def execute(self, prog: Program, mach: Machine) -> None:
        mach.out.append(self.gen_out(prog, mach))
        prog.advance(2)

    def gen_out(self, prog: Program, mach: Machine) -> str:
        return str(self.combo(prog.octal(1), mach) % 8)


instructions: dict[int, Instruction] = {
    0: ADivide(),
    6: BDivide(),
    7: CDivide(),
    4: BitwiseXOR(),
    1: BitwiseXOR_Op(),
    2: Modulo(),
    3: JumpNotZero(),
    5: Output(),
}


################################################################################################
# Problem 1
def execute(program: Program, machine: Machine, generate_disasm: bool = False):
    full_disasm = [] if generate_disasm else None
    while not program.eop():
        inst = instructions[program.octal(0)]

        if generate_disasm:
            disasm = inst.disasm(program, machine)
            full_disasm.append(disasm)

        inst.execute(program, machine)

    return machine.out, full_disasm


machine = Machine(registers.splitlines())
program = Program(program.removeprefix("Program: "))
out, disasm = execute(program, machine, generate_disasm=True)

print("Disasm:\n\t" + "\n\t".join(disasm))
print("Output:\n\t" + ",".join(out))

################################################################################################
# Problem 2

# Observations to make this solution make sense:
# - each out instruction happens after taking off the three right-most bits of RAM (one octal)
# - for each octal the output value of that octal is not affected by any octals to the right of it
# - so we can find chains of octals by starting from the left-most octal


def solve_for_specific_ram(ram: int):
    machine = Machine(registers.splitlines())
    machine.ram = ram

    program.reset()
    out, _ = execute(program, machine)
    return out


possible_values: list[int] = [0]
for op in progress(list(reversed(program.octals))):
    new_values = []
    for base_ram in possible_values:
        # shift to make space for fresh octals
        base_ram <<= 3

        # get a list of the eight possible values to extend this potential solution
        extended_rams = list(map(lambda j: base_ram | j, range(0, 8)))

        # compute these eight programs and see what eight outputs they add
        output_map = list(
            map(lambda o: int(solve_for_specific_ram(o)[0]), extended_rams)
        )

        # for each one that has the desired output add it to the list of potential solutions
        indices = [i for i, o in enumerate(output_map) if o == op]
        for j in indices:
            new_values.append(base_ram | j)

    possible_values = new_values

# we have a set of solutions now, the problem asks for the smallest
print(f"Problem 2: {min(possible_values)}")
