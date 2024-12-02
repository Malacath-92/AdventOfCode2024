import aocd
import re
import math

import cli

sample_data = """\
3   4
4   3
2   5
1   3
3   9
3   3"""
data = sample_data if cli.sample else aocd.data

left_list, right_list = zip(
    *[[int(n) for n in re.sub(" +", " ", line).split()] for line in data.splitlines()]
)

left_list = sorted(left_list)
right_list = sorted(right_list)

distances = [abs(l - r) for (l, r) in zip(left_list, right_list)]
total_distance = sum(distances)

print(f"Problem 1: {total_distance}")

duplicate_numbers = [n for n in left_list if n in right_list]
similarities = [right_list.count(n) * n for n in duplicate_numbers]
total_similarity = sum(similarities)

print(f"Problem 2: {total_similarity}")

if cli.visualize:
    import pathlib
    import scipy.spatial
    import manim
    import numpy
    import random

    # Make up some random locations from input
    minimum_position = -math.floor(len(left_list) / 2)
    maximum_position = math.ceil(len(left_list) / 2)

    def random_point(loc_id):
        random.seed(loc_id)
        return (
            3.4
            * random.randrange(minimum_position, maximum_position)
            / maximum_position,
            4 * random.randrange(minimum_position, maximum_position) / maximum_position,
        )

    left_points = [random_point(id) for id in set(left_list)]
    right_points = [
        random_point(id) for id in right_list
    ]  # intentionally contains duplicates
    all_points = list(set(left_points + right_points))
    left_indices = [all_points.index(p) for p in left_points]
    right_indices = [all_points.index(p) for p in right_points]
    all_points = numpy.array(all_points)
    all_radii = [None] * len(all_points)

    # Note: These are not perfect radii, they are only guaranteed to not overlap
    triangulation = scipy.spatial.Delaunay(all_points)
    indices, neighbours = triangulation.vertex_neighbor_vertices
    for i, point in enumerate(all_points):
        ith_neighbours = [
            all_points[j] for j in neighbours[indices[i] : indices[i + 1]]
        ]
        ith_distances = [
            numpy.linalg.norm(point - neighbour_point)
            for neighbour_point in ith_neighbours
        ]
        nearest_neighbour = min(ith_distances)
        all_radii[i] = nearest_neighbour / 2 * random.randrange(800, 1000) / 1000

    class LocationsScene(manim.Scene):
        def __init__(self):
            super().__init__()

            self.left_circles = {}
            self.right_circles = {}

            self.left_dupes = set()
            self.right_dupes = {}

            def make_circle(point, radius, color, initial_offset):
                circle = manim.Circle(radius)
                circle.move_to((point + [initial_offset, 0]).tolist() + [0])
                circle.set_fill(color=color, opacity=0.8)
                circle.set_stroke(None, opacity=0.0)

                circle.generate_target()
                circle.target.set_fill(color=manim.GREEN, opacity=1.0)
                circle.target.move_to(point.tolist() + [0])

                return circle

            for i in left_indices:
                point, radius = all_points[i], all_radii[i]
                self.left_circles[i] = make_circle(point, radius, manim.PINK, -3.5)
                if i in right_indices:
                    self.left_dupes.add(i)

            for i in right_indices:
                point, radius = all_points[i], all_radii[i]
                self.right_circles[i] = make_circle(point, radius, manim.BLUE, 3.5)
                if i in left_indices:
                    if i not in self.right_dupes:
                        self.right_dupes[i] = []
                    self.right_dupes[i].append(self.right_circles[i])

        def construct(self):
            self.play(*self.create(self.left_circles))
            self.play(*self.create(self.right_circles))

            self.play(
                *self.fade_out_dupes(self.left_circles, self.left_dupes),
                *self.fade_out_dupes(self.right_circles, self.right_dupes),
            )

            self.play(
                *self.move_to_final(self.left_circles, self.left_dupes),
                *self.move_to_final(self.right_circles, self.right_dupes),
            )

            self.play(*self.explode_dupes())
            self.play(*self.fade_dupes())

            self.wait()

        def create(self, list):
            return [manim.Create(c) for c in list.values()]

        def fade_out_dupes(self, list, dupes):
            return [manim.FadeOut(c) for (i, c) in list.items() if i not in dupes]

        def move_to_final(self, list, dupes):
            return [manim.MoveToTarget(c) for (i, c) in list.items() if i in dupes]

        def explode_dupes(self):
            explode = []
            for i, dupes in self.right_dupes.items():
                point, radius = all_points[i], all_radii[i]
                initial_angle = random.randrange(0, 360) / 180 * math.pi
                for j, right_c in enumerate(dupes):
                    right_c.set_fill(color=manim.GREEN, opacity=0.5)
                    right_c.move_to(point.tolist() + [0])
                    right_c.move_to(point.tolist() + [0])

                    new_circle = manim.Circle(radius * 0.3)
                    angle = initial_angle + j * math.pi * 2 / (len(dupes) + 1)
                    offset = [
                        2.3 * radius * math.cos(angle),
                        2.3 * radius * math.sin(angle),
                    ]
                    new_circle.move_to((point + offset).tolist() + [0])
                    explode.append(manim.Transform(right_c, new_circle))

            return explode

        def fade_dupes(self):
            fade = []
            for i, dupes in self.right_dupes.items():
                point, radius = all_points[i], all_radii[i]
                for _, right_c in enumerate(dupes):
                    faded_circle = manim.Circle(radius)
                    faded_circle.move_to(point.tolist() + [0])
                    faded_circle.set_fill(color=manim.GREEN, opacity=0.0)
                    faded_circle.set_stroke(None, opacity=0.0)
                    fade.append(manim.Transform(right_c, faded_circle))
            return fade

    manim.config.output_file = pathlib.Path(__file__).stem
    if cli.sample:
        manim.config.output_file = f"{manim.config.output_file}_sample"
    LocationsScene().render()
