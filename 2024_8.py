import aocd
import re
import itertools

import cli

sample_data = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
data = sample_data if cli.sample else aocd.data
flat_data = "".join(data.splitlines())

city = data.splitlines()
width = len(city[0])
height = len(city)
flat_idx_to_coords = lambda i: (i % width, i // width)
is_in_range = lambda p: p[0] >= 0 and p[1] >= 0 and p[0] < width and p[1] < height

antenna_types = set(re.findall(r"[^\.]", flat_data))
antenna_positions = {
    antenna_type: list(
        map(
            lambda x: flat_idx_to_coords(x.regs[0][0]),
            re.finditer(antenna_type, flat_data),
        )
    )
    for antenna_type in antenna_types
}

anti_nodes = [[set() for _ in range(width)] for _ in range(height)]

for antenna_type, positions in antenna_positions.items():
    pairwise_positions = itertools.product(positions, positions)
    for l, r in pairwise_positions:
        if l == r:
            continue

        d = (l[0] - r[0], l[1] - r[1])
        anti_node_l = (l[0] + d[0], l[1] + d[1])
        if is_in_range(anti_node_l):
            anti_nodes[anti_node_l[1]][anti_node_l[0]].add(antenna_type)
        anti_node_r = (r[0] - d[0], r[1] - d[1])
        if is_in_range(anti_node_r):
            anti_nodes[anti_node_r[1]][anti_node_r[0]].add(antenna_type)

anti_nodes_flat = list(itertools.chain.from_iterable(anti_nodes))
num_positions_with_anti_nodes = len(anti_nodes_flat) - anti_nodes_flat.count(set())
print(f"Problem 1: {num_positions_with_anti_nodes}")


real_anti_nodes = [[set() for _ in range(width)] for _ in range(height)]


def get_anti_nodes(l, r):
    d = (l[0] - r[0], l[1] - r[1])
    while d[0] % 2 == 0 and d[1] % 2 == 0:
        d = (d[0] // 2, d[1] // 2)

    anti_nodes = []

    anti_node_l = l
    while is_in_range(anti_node_l):
        anti_nodes.append(anti_node_l)
        anti_node_l = (anti_node_l[0] + d[0], anti_node_l[1] + d[1])

    anti_node_r = (l[0] - d[0], l[1] - d[1])
    while is_in_range(anti_node_r):
        anti_nodes.append(anti_node_r)
        anti_node_r = (anti_node_r[0] - d[0], anti_node_r[1] - d[1])

    return anti_nodes


for antenna_type, positions in antenna_positions.items():
    pairwise_positions = itertools.product(positions, positions)
    for l, r in pairwise_positions:
        if l == r:
            continue

        anti_nodes = get_anti_nodes(l, r)
        for x, y in anti_nodes:
            real_anti_nodes[y][x].add(antenna_type)

real_anti_nodes_flat = list(itertools.chain.from_iterable(real_anti_nodes))
num_positions_with_real_anti_nodes = len(
    real_anti_nodes_flat
) - real_anti_nodes_flat.count(set())
print(f"Problem 2: {num_positions_with_real_anti_nodes}")

if cli.visualize:
    import math
    import manim
    import pathlib

    colors = {
        antenna_type: manim.random_bright_color() for antenna_type in antenna_types
    }

    def align(mobject: manim.Mobject):
        return mobject.shift(manim.DOWN * height // 2).shift(manim.LEFT * width // 2)

    class Antenna:
        def __init__(self, antenna_type, position):
            self.antenna_type = antenna_type
            self.position = position
            self.color = colors[antenna_type]

            (x, y) = position

            self.tower = manim.Circle(0.25)
            self.tower.set_x(x).set_y(height - y)
            self.tower.set_opacity(1.0)
            self.tower.set_color(self.color)
            self.tower.set_stroke(color=manim.WHITE)
            align(self.tower)

            self.target_circles = [
                align(
                    manim.Circle(width * math.sqrt(2))
                    .set_stroke(color=self.color)
                    .set_x(x)
                    .set_y(height - y)
                )
                for _ in range(0, 6)
            ]

        def tower_mobject(self):
            return self.tower

        def show_tower(self):
            return manim.Write(self.tower)

        def new_circles(self):
            (x, y) = self.position
            self.circles = [
                align(
                    manim.Circle(0.0)
                    .set_stroke(color=self.color)
                    .set_x(x)
                    .set_y(height - y)
                )
                for _ in range(0, 10)
            ]
            return self.circles

        def show_signal(self):
            return manim.AnimationGroup(
                *[
                    manim.Transform(c, tc)
                    for c, tc in zip(self.circles, self.target_circles)
                ],
                lag_ratio=0.25,
            )

    class AntiNode:
        def __init__(self, position):
            (x, y) = position

            self.square = manim.Square(side_length=0.0)
            self.square.set_x(x).set_y(height - y)
            self.square.set_opacity(0.25)
            self.square.set_color(manim.RED_B)
            self.square.set_stroke(opacity=0.0)
            align(self.square)

            self.target_square = manim.Square(side_length=1.0)
            self.target_square.set_x(x).set_y(height - y)
            self.target_square.set_opacity(0.25)
            self.target_square.set_color(manim.RED_B)
            self.target_square.set_stroke(opacity=0.0)
            align(self.target_square)

        def square_mobject(self):
            return self.square

        def appear(self):
            return manim.AnimationGroup(
                manim.Flash(self.square),
                manim.Transform(self.square, self.target_square),
                lag_ratio=0.25,
            )

    class CityScene(manim.Scene):
        def __init__(self):
            super().__init__()

            self.antennas = [
                Antenna(t, p) for t, ps in antenna_positions.items() for p in ps
            ]

            first_antennas = antenna_positions["A"][:2]
            self.first_antennas = [
                a for a in self.antennas if a.position in first_antennas
            ]

            first_anti_nodes = get_anti_nodes(*first_antennas)
            other_anti_nodes = [
                (x, y)
                for (x, y) in itertools.product(range(0, width), range(0, height))
                if real_anti_nodes[y][x] != set() and (x, y) not in first_anti_nodes
            ]

            self.first_anti_nodes = list(map(AntiNode, first_anti_nodes))
            self.other_anti_nodes = list(map(AntiNode, other_anti_nodes))

        def construct(self):
            self.play(
                manim.AnimationGroup(
                    [a.show_tower() for a in self.antennas],
                    lag_ratio=0.1 if cli.sample else 0.01,
                )
            )
            self.wait()

            self.add(
                *self.first_antennas[0].new_circles(),
                *self.first_antennas[1].new_circles(),
                *[a.square_mobject() for a in self.first_anti_nodes],
            )
            self.play(
                self.first_antennas[0].show_signal(),
                self.first_antennas[1].show_signal(),
                *[a.appear() for a in self.first_anti_nodes],
                run_time=3.5,
            )
            self.wait()

            self.add(
                *[c for a in self.antennas for c in a.new_circles()],
                *[a.square_mobject() for a in self.other_anti_nodes],
            )
            self.play(
                *[a.show_signal() for a in self.antennas],
                *[a.appear() for a in self.other_anti_nodes],
                run_time=5.5,
            )
            self.wait()

    manim.config.pixel_width = 1500
    manim.config.pixel_height = 1500
    manim.config.frame_width = width
    manim.config.frame_height = height
    manim.config.output_file = pathlib.Path(__file__).stem
    if cli.sample:
        manim.config.output_file = f"{manim.config.output_file}_sample"
    CityScene().render()
