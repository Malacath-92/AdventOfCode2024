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

        def loop_path():
            pos = (ox, oy)
            dir = odir
            loop_visited = [[None] * width for _ in range(height)]
            loop_path = []
            while pos_in_range_map[dir](pos):
                loop_path += [(pos, dir)]

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

    def to_manim(point):
        return (point[0], point[1], 0)

    def reduce_path(path, extend):
        reduced_path = []
        curr_pos = path[0][0]
        curr_dir = path[0][1]
        for pos, dir in path:
            if curr_dir != dir:
                reduced_path += [(curr_pos, pos)]
                curr_pos = pos
                curr_dir = dir
        (last_pos, last_dir) = path[-1]
        if extend:
            final_pos = (last_pos[0] + last_dir[0] * 3, last_pos[1] + last_dir[1] * 3)
        else:
            final_pos = (last_pos[0], last_pos[1])
        reduced_path += [(curr_pos, final_pos)]
        return reduced_path

    def make_path_points(path):
        path_points = []
        for from_pos, to_pos in path:
            path_points.append(to_manim(from_pos))
        path_points.append(to_manim(to_pos))
        return path_points

    reduced_path = reduce_path(path, extend=True)
    obstructed_path_gen = next_obstructed_path()

    class ObstructedPath:
        def __init__(self):
            obstructed_path = obstructed_path_gen.__next__()

            self.obstacle = manim.Square(side_length=1)
            self.obstacle.set_opacity(0.95)
            self.obstacle.set_x(obstructed_path[0][0] + obstructed_path[1][0][1][0])
            self.obstacle.set_y(obstructed_path[0][1] + obstructed_path[1][0][1][1])
            self.obstacle.set_fill(color=manim.random_color())
            self.obstacle.set_stroke(width=0)

            self.path = manim.VMobject().set_points_as_corners(
                make_path_points(reduce_path(obstructed_path[1], extend=False))
            )
            self.path.set_stroke(width=15, opacity=0.5)
            self.path.set_color(self.obstacle.color)
            self.path_dashed = manim.DashedVMobject(self.path, num_dashes=180)

            self.original_path = obstructed_path[1]

        def length(self):
            return len(self.original_path)

        def appear_obstacles(self):
            return manim.AnimationGroup(
                manim.Flash(self.obstacle),
                manim.Create(self.obstacle),
            )

        def draw_paths(self):
            return manim.Create(self.path)

        def disappear(self):
            return manim.AnimationGroup(
                manim.Uncreate(self.obstacle),
                manim.Uncreate(self.path),
            )

        def mobjects(self):
            return [
                self.obstacle,
                self.path,
                self.path_dashed,
            ]

    class FloorScene(manim.Scene):
        def __init__(self):
            super().__init__()

            self.obstacles = []
            for x, y in obstacle_positions:
                square = manim.Square(side_length=1)
                square.set_x(x).set_y(y)
                square.set_opacity(1.0)
                square.set_fill(color=manim.LIGHT_GRAY)
                square.set_stroke(width=0)
                self.obstacles.append(square)
            self.floor = manim.Group(*self.obstacles)

            self.path = manim.VMobject().set_points_as_corners(
                make_path_points(reduced_path)
            )
            self.path.set_stroke(width=15)
            self.path.set_color(manim.RED_E)

            num_viz = 6 if cli.sample else 150
            self.obstructed_paths = [ObstructedPath() for _ in range(0, num_viz)]
            self.longest_obstructed_path = max(
                self.obstructed_paths, key=ObstructedPath.length
            )

            self.whole_floor = manim.Group(
                self.floor,
                self.path,
                *[o for p in self.obstructed_paths for o in p.mobjects()],
            )
            self.whole_floor.align_on_border(manim.LEFT, 0)
            self.whole_floor.align_on_border(manim.DOWN, 0)

        def construct(self):
            if cli.sample:
                self.play(
                    manim.AnimationGroup(
                        [manim.Write(o) for o in self.obstacles],
                        lag_ratio=0.1,
                    ),
                )
            else:
                self.add(self.floor)

            self.play(manim.Create(self.path), run_time=4, rate_func=manim.linear)
            self.wait()

            self.play(
                manim.Uncreate(self.path),
                run_time=1,
                rate_func=manim.linear,
            )
            self.wait()

            self.play(
                manim.AnimationGroup(
                    map(ObstructedPath.appear_obstacles, self.obstructed_paths),
                    lag_ratio=0.1,
                )
            )
            self.wait()

            self.play(
                manim.AnimationGroup(
                    map(ObstructedPath.draw_paths, self.obstructed_paths), lag_ratio=0.1
                )
            )
            self.wait()

            self.play(
                manim.AnimationGroup(
                    *[
                        o.disappear()
                        for o in self.obstructed_paths
                        if o != self.longest_obstructed_path
                    ],
                    lag_ratio=0.1,
                )
            )
            self.wait()

    manim.config.pixel_width = 1500
    manim.config.pixel_height = 1500
    manim.config.frame_width = width
    manim.config.frame_height = height
    manim.config.background_color = manim.LIGHT_PINK
    manim.config.output_file = pathlib.Path(__file__).stem
    if cli.sample:
        manim.config.output_file = f"{manim.config.output_file}_sample"
    FloorScene().render()
