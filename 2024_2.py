import aocd
import collections
import itertools

import cli

sample_data = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
data = sample_data if cli.sample else aocd.data

reports = [[int(n) for n in l.split()] for l in data.splitlines()]


def is_report_safe(report, with_dampener=False):
    def sliding_window(iterable, n):
        iterator = iter(iterable)
        window = collections.deque(itertools.islice(iterator, n - 1), maxlen=n)
        for x in iterator:
            window.append(x)
            yield tuple(window)

    def try_dampen(i):
        # strip off left level
        left_stripped = report.copy()
        del left_stripped[i]
        if is_report_safe(left_stripped):
            return i

        # strip off right level
        right_stripped = report.copy()
        del right_stripped[i + 1]
        if is_report_safe(right_stripped):
            return i + 1

        # strip off first level
        first_stripped = report.copy()
        del first_stripped[0]
        if is_report_safe(first_stripped):
            return 0

        # strip off second level
        second_stripped = report.copy()
        del second_stripped[1]
        if is_report_safe(second_stripped):
            return 1

        return False

    last_diff = 0
    for i, [lhs, rhs] in enumerate(sliding_window(report, 2)):
        diff = rhs - lhs
        if abs(diff) < 1 or abs(diff) > 3:
            return try_dampen(i) if with_dampener else False
        if last_diff != 0 and last_diff / diff < 0:
            return try_dampen(i) if with_dampener else False
        last_diff = diff

    return True


report_safeties = [is_report_safe(report) for report in reports]
safe_reports = [report for i, report in enumerate(reports) if report_safeties[i]]
print(f"Problem 1: {len(safe_reports)}")

dampened_report_safeties = [is_report_safe(report, True) for report in reports]
dampened_safe_reports = [
    report for i, report in enumerate(reports) if dampened_report_safeties[i]
]
print(f"Problem 2: {len(dampened_safe_reports)}")

if cli.visualize:
    import manim
    import numpy
    import pathlib
    import random

    def to_manim(pt):
        return pt.tolist() + [0]

    if cli.sample:
        grid_width = 3
        grid_height = 3
        unsafe_grid_width = 2
        unsafe_grid_height = 2
    else:
        grid_width = 16
        grid_height = 10
        unsafe_grid_width = 10
        unsafe_grid_height = 8

        # Take only N elements, from front and back
        reduced_number_reports = grid_width * grid_height
        reports = (
            reports[: reduced_number_reports // 2]
            + reports[-reduced_number_reports // 2 :]
        )
        random.shuffle(reports)
        report_safeties = [is_report_safe(report) for report in reports]
        dampened_report_safeties = [is_report_safe(report, True) for report in reports]

    report_lengths = [len(report) for report in reports]
    report_ranges = [(min(report), max(report)) for report in reports]

    class ReportsScene(manim.Scene):
        def __init__(self):
            super().__init__()

            canvas_min = numpy.array([-4 * 16 / 9, -4])
            canvas_max = numpy.array([+4 * 16 / 9, +4])
            canvas_size = canvas_max - canvas_min
            axis_config = {"tick_size": 0.1 if cli.sample else 0.03}
            vertex_dot_radius = 0.06 if cli.sample else 0.005

            self.axes = [
                manim.Axes(
                    x_range=[0, report_length - 1],
                    y_range=[report_range[0] - 1, report_range[1] + 1],
                    x_length=canvas_size[0] / grid_width / 1.2,
                    y_length=canvas_size[1] / grid_height / 1.2,
                    tips=False,
                    axis_config=axis_config,
                )
                for report_length, report_range in zip(report_lengths, report_ranges)
            ]
            for i, axis in enumerate(self.axes):
                x = i % grid_width + 0.5
                y = i // grid_width + (1 if cli.sample else 0.5)
                axis.move_to(
                    to_manim(
                        canvas_min + (canvas_size * [x, y]) / (grid_width, grid_height)
                    )
                )

            self.unsafe_axes = {
                i: manim.Axes(
                    x_range=[0, report_length - 1],
                    y_range=[report_range[0] - 1, report_range[1] + 1],
                    x_length=canvas_size[0] / unsafe_grid_width / 1.2,
                    y_length=canvas_size[1] / unsafe_grid_height / 1.2,
                    tips=False,
                    axis_config=axis_config,
                )
                for i, (report_length, report_range) in enumerate(
                    zip(report_lengths, report_ranges)
                )
                if report_safeties[i] == False
            }
            for i, unsafe_axis in enumerate(self.unsafe_axes.values()):
                x = i % unsafe_grid_width + 0.5
                y = i // unsafe_grid_width + 0.5
                unsafe_axis.move_to(
                    to_manim(
                        canvas_min
                        + (canvas_size * [x, y])
                        / (unsafe_grid_width, unsafe_grid_height)
                    )
                )

            self.plots = []
            self.unsafe_plots = {}
            for i, axis in enumerate(self.axes):
                report = reports[i]

                x_values = range(report_lengths[i])
                y_values = report
                plot = axis.plot_line_graph(
                    x_values,
                    y_values,
                    line_color=manim.BLUE,
                    vertex_dot_radius=vertex_dot_radius,
                )
                self.plots.append(plot)

                if not report_safeties[i]:
                    unsafe_plot = self.unsafe_axes[i].plot_line_graph(
                        x_values,
                        y_values,
                        line_color=manim.RED,
                        vertex_dot_radius=vertex_dot_radius,
                    )

                    if not isinstance(dampened_report_safeties[i], bool):
                        x_values = list(x_values)
                        y_values = report.copy()
                        del x_values[dampened_report_safeties[i]]
                        del y_values[dampened_report_safeties[i]]
                        fixed_plot = self.unsafe_axes[i].plot_line_graph(
                            x_values,
                            y_values,
                            line_color=manim.GREEN,
                            vertex_dot_radius=vertex_dot_radius,
                        )
                    else:
                        fixed_plot = None

                    self.unsafe_plots[i] = {"broken": unsafe_plot, "fixed": fixed_plot}

        def construct(self):
            self.play(*self.create())
            self.play(*self.do_plots())

            self.play(*self.highlight_plots())

            self.play(*self.fade_safe_plots(), *self.reorganize_unsafe_plots())

            self.play(*self.highlight_problem_points())

            self.play(*self.transform_to_fixed_reports())

            self.wait()

        def create(self):
            return [manim.Create(axis) for axis in self.axes]

        def do_plots(self):
            return [manim.Create(plot) for plot in self.plots]

        def highlight_plots(self):
            return [
                manim.FadeToColor(
                    plot, color=manim.GREEN if report_safeties[i] else manim.RED
                )
                for i, plot in enumerate(self.plots)
            ]

        def fade_safe_plots(self):
            return [
                manim.AnimationGroup(manim.FadeOut(axis), manim.FadeOut(plot))
                for i, (axis, plot) in enumerate(zip(self.axes, self.plots))
                if report_safeties[i]
            ]

        def reorganize_unsafe_plots(self):
            return [
                manim.AnimationGroup(
                    manim.Transform(axis, self.unsafe_axes[i]),
                    manim.Transform(plot, self.unsafe_plots[i]["broken"]),
                )
                for i, (axis, plot) in enumerate(zip(self.axes, self.plots))
                if report_safeties[i] == False
            ]

        def highlight_problem_points(self):
            def get_problem_point(i, axis):
                removed_point = dampened_report_safeties[i]
                problem_point = axis.coords_to_point(
                    removed_point, reports[i][removed_point]
                )
                return problem_point

            return [
                manim.Flash(get_problem_point(i, axis))
                for i, axis in self.unsafe_axes.items()
                if not isinstance(dampened_report_safeties[i], bool)
            ]

        def transform_to_fixed_reports(self):
            return [
                manim.Transform(self.plots[i], unsafe_plot["fixed"])
                for i, unsafe_plot in self.unsafe_plots.items()
                if not isinstance(dampened_report_safeties[i], bool)
            ]

    manim.config.output_file = pathlib.Path(__file__).stem
    if cli.sample:
        manim.config.output_file = f"{manim.config.output_file}_sample"
    ReportsScene().render()
