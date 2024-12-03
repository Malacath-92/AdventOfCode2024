import aocd
import re
from functools import reduce
from operator import mul

import cli

sample_data = (
    "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
)
data = sample_data if cli.sample else aocd.data

instructions = [map(int, inst) for inst in re.findall(r"mul\((\d+),(\d+)\)", data)]
multiplications = [reduce(mul, instruction) for instruction in instructions]
print(f"Problem 1: {sum(multiplications)}")

data = re.sub(r"(don't\(\)).*?(do\(\))", "", "".join(data.splitlines()))
data = data.split("don't")[0]
instructions = [map(int, inst) for inst in re.findall(r"mul\((\d+),(\d+)\)", data)]
multiplications = [reduce(mul, instruction) for instruction in instructions]
print(f"Problem 2: {sum(multiplications)}")

if cli.visualize:
    import manim
    import pathlib

    data = sample_data if cli.sample else aocd.data
    data = "".join(data.splitlines())
    if not cli.sample:
        data = data[: len(data) // 4]
    reduced_data = re.sub(r"(don't\(\)).*?(do\(\))", "", data).split("don't")[0]

    raw_data = data
    raw_reduced_data = reduced_data

    if not cli.sample:
        chunk_size = len(data) // 36
        data = "\n".join(
            [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]
        )
        chunk_size = len(data) // 36
        reduced_data = "\n".join(
            [
                reduced_data[i : i + chunk_size]
                for i in range(0, len(reduced_data), chunk_size)
            ]
        )

    dont_do_re = re.compile(
        r"(d\n?o\n?n\n?'\n?t\n?\(\n?\)\n?).*?(d\n?o\n?\(\n?\)\n?)", re.DOTALL
    )
    mul_re = re.compile(r"m\n?u\n?l\n?\(\n?(\d*\n?\d*)\n?,\n?(\d*\n?\d*)\n?\)")

    disabled_ranges = re.finditer(dont_do_re, data)
    mul_ranges = list(re.finditer(mul_re, reduced_data))
    raw_mul_ranges = list(re.finditer(mul_re, raw_reduced_data))

    class InstructionsScene(manim.Scene):
        def __init__(self):
            super().__init__()

            disabled_highlights = {
                f"[{disabled_range.regs[0][0]}:{disabled_range.regs[0][1]}]": manim.RED
                for disabled_range in disabled_ranges
            }

            mul_highlights = {
                f"[{mul_range.regs[0][0]}:{mul_range.regs[0][1]}]": manim.GREEN
                for mul_range in mul_ranges
            }
            bold_highlights = {
                f"[{mul_range.regs[1][0]}:{mul_range.regs[1][1]}]": manim.BOLD
                for mul_range in mul_ranges
            }
            bold_highlights.update(
                {
                    f"[{mul_range.regs[2][0]}:{mul_range.regs[2][1]}]": manim.BOLD
                    for mul_range in mul_ranges
                }
            )

            raw_mul_highlights = {
                f"[{raw_mul_range.regs[0][0]}:{raw_mul_range.regs[0][1]}]": manim.GREEN
                for raw_mul_range in raw_mul_ranges
            }
            raw_bold_highlights = {
                f"[{raw_mul_range.regs[1][0]}:{raw_mul_range.regs[1][1]}]": manim.BOLD
                for raw_mul_range in raw_mul_ranges
            }
            raw_bold_highlights.update(
                {
                    f"[{raw_mul_range.regs[2][0]}:{raw_mul_range.regs[2][1]}]": manim.BOLD
                    for raw_mul_range in raw_mul_ranges
                }
            )

            self.original_text = manim.Text(data)
            self.highlight_text = manim.Text(data, t2c=disabled_highlights)
            self.reduced_text = manim.Text(
                reduced_data, t2c=mul_highlights, t2w=bold_highlights
            )

            self.raw_reduced_text = manim.Text(
                raw_reduced_data, t2c=raw_mul_highlights, t2w=raw_bold_highlights
            )
            self.raw_reduced_text.scale(2.0)
            self.raw_reduced_text.align_on_border(manim.LEFT)
            self.raw_reduced_text.align_on_border(manim.DOWN)

            self.marker = manim.Arrow(start=manim.UP, end=manim.DOWN)
            self.marker.align_on_border(manim.LEFT)
            self.marker.align_on_border(manim.DOWN, 1.85)
            self.marker.generate_target()
            self.marker.target.align_on_border(manim.RIGHT)

            self.counter_visible = False

            def make_text():
                if self.counter_visible == False:
                    text = manim.Text("0")
                    text.scale(4.0)
                    text.align_on_border(manim.UP, 2)
                    return text

                text_x = self.original_text.get_x()
                text_w = self.original_text.width
                mark_x = self.marker.get_x()
                alpha = (mark_x - text_x + text_w / 2) / text_w
                pos = int(alpha * len(raw_reduced_data))
                sub_data = raw_reduced_data[:pos]
                sub_instructions = [
                    map(int, inst) for inst in re.findall(mul_re, sub_data)
                ]
                partial_solution = [
                    reduce(mul, instruction) for instruction in sub_instructions
                ]

                text = manim.Text(f"{sum(partial_solution)}")
                text.scale(4.0)
                text.align_on_border(manim.UP, 2)
                return text

            self.current_counter = manim.always_redraw(make_text)

            if cli.sample:
                self.original_text.scale(0.5)
                self.highlight_text.scale(0.5)
                self.reduced_text.scale(0.5)
            else:
                self.original_text.scale(0.25)
                self.highlight_text.scale(0.25)
                self.reduced_text.scale(0.25)

        def construct(self):
            self.play(manim.FadeIn(self.original_text))
            self.play(manim.Transform(self.original_text, self.highlight_text))
            self.play(manim.Transform(self.original_text, self.reduced_text))
            self.wait()

            self.play(
                manim.Transform(self.original_text, self.raw_reduced_text),
                manim.Write(self.current_counter),
                manim.Create(self.marker),
            )
            self.wait(duration=0.5)

            self.original_text.generate_target()
            self.original_text.target.align_on_border(manim.RIGHT)
            self.original_text.target.align_on_border(manim.DOWN)

            self.counter_visible = True

            run_time = 2 if cli.sample else 20
            self.play(
                manim.MoveToTarget(self.original_text),
                manim.MoveToTarget(self.marker),
                run_time=run_time,
                rate_func=manim.linear,
            )

            self.wait()

    manim.config.output_file = pathlib.Path(__file__).stem
    if cli.sample:
        manim.config.output_file = f"{manim.config.output_file}_sample"
    InstructionsScene().render()
