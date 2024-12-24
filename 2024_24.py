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


def parse_input(data: str):
    [initials_str, gates_str] = data.split("\n\n")
    initials = {}
    for l in initials_str.splitlines():
        [name, value] = l.split(":")
        initials[name] = True if value.strip() == "1" else False

    gates = {gate.output: gate for gate in map(Gate, gates_str.splitlines())}
    return initials, gates


initials, gates = parse_input(data)

################################################################################################
# Problem 1
values = initials.copy()
z_names = list(reversed(sorted(filter(lambda x: x[0] == "z", gates.keys()))))
for z in z_names:
    values[z] = gates[z].exec(values)
z_combo = "".join(map(lambda x: "1" if x else "0", map(values.get, z_names)))
z_value = int(z_combo, 2)
print(f"Problem 1: {z_value}")


def find_output_bit(lhs: str, rhs: str, operation: str) -> str | None:
    inputs = tuple(sorted((lhs, rhs, operation)))
    for gate in gates.values():
        gate_inputs = tuple(sorted((gate.lhs, gate.rhs, gate.operation)))
        if gate_inputs == inputs:
            return gate.output

    return None


################################################################################################
# Problem 2
# We reproduce the whole logic of adding two numbers in binary and hope that the program was
# initially using the same algorithm. Then we fix the gates on the way...
#
#  See here for all details: https://en.wikipedia.org/wiki/Adder_(electronics)#Full_adder
#
# This function adds three bits and is just a sequence of operations that ends up in two output
# bits as the result:
#   - the sum bit, which is the result of adding the three bits
#   - the carry bit, which is the overflow that has to be carried to the next addition
#
# The tree bits we add are the ith bits of x and y (lhs and rhs in code) and the carry from the
# last three bit add.
#
# The actual addition happens as follows:
#   - lhs                XOR  rhs            ->  interim_sum
#   - lhs                AND  rhs            ->  interim_carry
#   - carry              AND  interim_sum    ->  interim_sum_carry
#   - carry              XOR  interim_sum    ->  out_sum
#   - interim_sum_carry  OR   interim_carry  ->  out_carry
def add_bits(
    lhs: str, rhs: str, carry: str, swapped_outputs: list[str]
) -> tuple[str | None, str | None]:

    # Note: When adding bits to swapped_outputs we don't actually pair them up
    #       as we don't care about the order in the end
    # Note: We assume all over the place that the program in question actually
    #       follows this implementation and bits are only swapped once, otherwise
    #       everything here is broken

    # find the output bits for these operations
    interim_sum = find_output_bit(lhs, rhs, "XOR")
    interim_carry = find_output_bit(lhs, rhs, "AND")

    # if either of these is None we are fucked ig, because this program can't add
    # two numbers without changing instructions
    if interim_sum is None or interim_carry is None:
        raise "Bruh..."

    if carry is None:
        # without a carry input we have to do no more work
        out_sum, out_carry = interim_sum, interim_carry
    else:
        interim_sum_carry = find_output_bit(carry, interim_sum, "AND")
        out_sum = find_output_bit(carry, interim_sum, "XOR")

        if interim_sum_carry is None:
            # for the program to be well-formed these two have to be None at
            # the same time, so we re-assign them together
            assert out_sum is None

            # can't find output bit, must be swapped
            interim_sum, interim_carry = interim_carry, interim_sum
            interim_sum_carry = find_output_bit(carry, interim_sum, "AND")
            out_sum = find_output_bit(carry, interim_sum, "XOR")

            swapped_outputs.append(interim_sum)
            swapped_outputs.append(interim_carry)

        # the intermediate results should not be written into a z-bit, those
        # should be reserved for final outputs
        if interim_sum[0] == "z":
            interim_sum, out_sum = out_sum, interim_sum
            swapped_outputs.append(interim_sum)
            swapped_outputs.append(out_sum)
        elif interim_carry[0] == "z":
            interim_carry, out_sum = out_sum, interim_carry
            swapped_outputs.append(interim_carry)
            swapped_outputs.append(out_sum)
        elif interim_sum_carry[0] == "z":
            interim_sum_carry, out_sum = out_sum, interim_sum_carry
            swapped_outputs.append(interim_sum_carry)
            swapped_outputs.append(out_sum)

        # we already swapped offending bits in this operation, so this next
        # bit has to be found, otherwise the program must be ill-formed
        out_carry = find_output_bit(interim_sum_carry, interim_carry, "OR")

    # make sure we are not writing the carry result into a z-bit, we should be
    # writing the sum result into a z-bit
    if out_carry[0] == "z":
        out_carry, out_sum = out_sum, out_carry
        swapped_outputs.append(out_carry)
        swapped_outputs.append(out_sum)

    return out_sum, out_carry


x_names = list(reversed(sorted(filter(lambda x: x[0] == "x", initials.keys()))))
y_names = list(reversed(sorted(filter(lambda x: x[0] == "x", initials.keys()))))
max_bits_xy = int(x_names[0][1:])
max_bits_z = int(z_names[0][1:])

in_carry = None
swapped_outputs = []
for i in range(max_bits_xy):
    # get the ith bits
    lhs = f"x{i:02d}"
    rhs = f"y{i:02d}"

    # add these two bits and carry bit from last add
    out_sum, out_carry = add_bits(lhs, rhs, in_carry, swapped_outputs)

    # pass carry to next iteration
    in_carry = out_carry

print(f"Problem 2: {','.join(sorted(swapped_outputs))}")
