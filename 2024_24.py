import aocd
from typing import DefaultDict
from tqdm import tqdm as progress

import cli


sample_data = """\
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""
data = sample_data if cli.sample else aocd.data

[initials_str, gates_str] = data.split("\n\n")
initials = {}
for l in initials_str.splitlines():
    [name, value] = l.split(":")
    initials[name] = True if value.strip() == "1" else False


class Gate:
    def __init__(self, setup: str):
        [inputs_str, output_str] = setup.split("->")
        inputs_str = inputs_str.split()

        self.lhs = inputs_str[0].strip()
        self.rhs = inputs_str[2].strip()
        self.operation = inputs_str[1].strip()
        self.output = output_str.strip()

    def exec(self, values: dict[str, bool]) -> bool:
        if self.lhs not in values:
            values[self.lhs] = gates[self.lhs].exec(values)
        if self.rhs not in values:
            values[self.rhs] = gates[self.rhs].exec(values)

        lhs = values[self.lhs]
        rhs = values[self.rhs]

        match self.operation:
            case "AND":
                return lhs and rhs
            case "OR":
                return lhs or rhs
            case "XOR":
                return lhs != rhs

        raise "Bruh..."


gates = {gate.output: gate for gate in map(Gate, gates_str.splitlines())}

################################################################################################
# Problem 1
values = initials.copy()
z_names = list(reversed(sorted(filter(lambda x: x[0] == "z", gates.keys()))))
for z in z_names:
    values[z] = gates[z].exec(values)
z_combo = "".join(map(lambda x: "1" if x else "0", map(values.get, z_names)))
z_value = int(z_combo, 2)
print(f"Problem 1: {z_value}")


################################################################################################
# Problem 2
# print(f"Problem 1: {",".join(sorted(find_maximum_network()))}")
