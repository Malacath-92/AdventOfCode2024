import aocd
import re
import abc

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
        return f"out {self.combo_str(prog.octal(1), mach)}"

    def execute(self, prog: Program, mach: Machine) -> None:
        mach.out.append(str(self.combo(prog.octal(1), mach) % 8))
        prog.advance(2)


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
