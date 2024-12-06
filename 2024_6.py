import aocd

import cli

sample_data = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
data = sample_data if cli.sample else aocd.data

floor = data.splitlines()
width = len(floor[0])
height = len(floor)

pos_in_range_map = {
    (-1, 0): lambda x: x[0] >= 0,
    (+1, 0): lambda x: x[0] < width,
    (0, -1): lambda x: x[1] >= 0,
    (0, +1): lambda x: x[1] < height,
}

start_pos = data.replace("\n", "").find("^")
start_pos = (start_pos % width, start_pos // width)


def find_next_obstruction(floor, pos, dir):
    pos_in_range = pos_in_range_map[dir]

    next_pos = [pos[0] + dir[0], pos[1] + dir[1]]
    while pos_in_range(next_pos) and floor[next_pos[1]][next_pos[0]] != "#":
        next_pos[0] += dir[0]
        next_pos[1] += dir[1]

    if pos_in_range(next_pos):
        next_pos = [next_pos[0] - dir[0], next_pos[1] - dir[1]]
        return {"pos": next_pos, "symbol": "#"}
    else:
        return {"pos": next_pos, "symbol": "~"}


path = []
pos = start_pos
dir = (0, -1)
while pos_in_range_map[dir](pos):
    path += [(pos, dir)]

    pos = (pos[0] + dir[0], pos[1] + dir[1])
    (x, y) = pos
    if not pos_in_range_map[dir](pos):
        break
    elif floor[y][x] == "#":
        pos = (pos[0] - dir[0], pos[1] - dir[1])
        dir = (-dir[1], dir[0])

visited = set(map(lambda x: tuple(x[0]), path))
print(f"Problem 1: {len(visited)}")


def next_obstructed_path():
    for i, ((ox, oy), odir) in enumerate(path):
        print(f"Testing position number {i}")

        def loop_path():
            pos = (ox, oy)
            dir = odir
            loop_visited = [[None] * width for _ in range(height)]
            loop_path = []
            while pos_in_range_map[dir](pos):
                loop_path += [pos]

                (x, y) = pos
                if vis := loop_visited[y][x]:
                    if dir in vis:
                        return loop_path
                    vis.append(dir)
                else:
                    loop_visited[y][x] = [dir]

                pos = (pos[0] + dir[0], pos[1] + dir[1])
                (x, y) = pos
                if not pos_in_range_map[dir](pos):
                    break
                elif floor[y][x] == "#" or (x, y) == (ox + odir[0], oy + odir[1]):
                    pos = (pos[0] - dir[0], pos[1] - dir[1])
                    dir = (-dir[1], dir[0])
            return None

        if p := loop_path():
            yield ((ox, oy), p)


if not cli.visualize:
    obstructed_paths = list(next_obstructed_path())
    print(f"Problem 2: {len(obstructed_paths)}")


if cli.visualize:
    import manim
    import pathlib
    import itertools

    obstacle_positions = [
        (x, y)
        for (x, y) in itertools.product(range(0, width), range(0, height))
        if floor[y][x] == "#"
    ]

    def reduce_path(path):
        reduced_path = []
        curr_pos = path[0][0]
        curr_dir = path[0][1]
        for pos, dir in path:
            if curr_dir != dir:
                reduced_path += [(curr_pos, pos)]
                curr_pos = pos
                curr_dir = dir
        reduced_path += [(curr_pos, path[-1][0])]
        return reduced_path

    reduced_path = reduce_path(path)

    class FloorScene(manim.Scene):
        def __init__(self):
            super().__init__()

            self.obstacles = []
            for x, y in obstacle_positions:
                square = manim.Square(side_length=1)
                square.set_x(x).set_y(y)
                self.obstacles.append(square)
            self.floor = manim.Group(*self.obstacles)

            self.path_lines = []
            for from_pos, to_pos in reduced_path:
                line = manim.Line(from_pos, to_pos)
                line.set_stroke(width=0.3)
                self.path_lines.append(line)
            self.path = manim.Group(*self.path_lines)

            first_obstructed_path = next_obstructed_path()

            self.added_obstacle = manim.Square(side_length=1)
            self.added_obstacle.set_x(first_obstructed_path[0][0])
            self.added_obstacle.set_y(first_obstructed_path[0][1])

            self.obstructed_path_lines = []
            for from_pos, to_pos in reduce_path(first_obstructed_path[1]):
                line = manim.Line(from_pos, to_pos)
                line.set_stroke(width=0.3)
                self.obstructed_path_lines.append(line)
            self.obstructed_path = manim.Group(*self.obstructed_path_lines)

            self.whole_floor = manim.Group(
                self.floor, self.path, self.added_obstacle, self.obstructed_path
            )

        def construct(self):
            self.add(self.floor)
            self.add(self.path)

            self.add()

        def zoom_in_on_point(self, point):
            self.whole_floor.target.scale(0.1)
            self.whole_floor.target.move_to(point)

    manim.config.pixel_width = width
    manim.config.pixel_height = height
    manim.config.frame_width = width
    manim.config.frame_height = height
    manim.config.output_file = pathlib.Path(__file__).stem
    if cli.sample:
        manim.config.output_file = f"{manim.config.output_file}_sample"
    FloorScene().render()
