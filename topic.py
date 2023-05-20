from manim import *
from copy import deepcopy

HOME2 = "icons"

probabilities = 0.4, 0.6
labels = np.array(["food", "animals"])

def get_histogram(probabilities, labels):
    """Creates a histogram with probabilities and labels."""
    histogram = VGroup()
    chart = BarChart(
        values=probabilities,
        bar_names=labels,
        y_axis_config={"font_size": 36},
        y_length=6,
        x_length=10,
    )
    bar_chart_labels = chart.get_bar_labels(font_size=48)

    histogram.add(chart, bar_chart_labels)
    histogram.to_edge(DL)
    return histogram

def fix_svg(svgmobject):
    """fixes missing attributes when loading svg"""
    attrs =[
            "fill_rgbas",
            "stroke_rgbas",
            "background_stroke_rgbas",
            "stroke_width",
            "background_stroke_width",
            "sheen_direction",
            "sheen_factor",
        ]
    for attr in attrs:
        if getattr(svgmobject, attr) is None:
            setattr(svgmobject, attr, 0)


def add_value_to_row(row, value):
    new_row = deepcopy(row)
    if value == 0:
        symbol = SVGMobject(f"{HOME2}/green_tick.svg")
    else:
        symbol = SVGMobject(f"{HOME2}/cross.svg")
    fix_svg(symbol)

    symbol.next_to(new_row, RIGHT)
    new_row.add(symbol)
    return new_row


class TopicGenerationSimulation(Scene):
    def construct(self):
        def update(row):
            value = np.random.choice([0,1], p=probabilities)
            new_row = add_value_to_row(row, value)
            row.become(new_row)
            arrow.next_to(histogram[0][0][value], UP, buff=0.1)

        histogram = get_histogram(probabilities, labels)
        arrow = Line(ORIGIN, DOWN * 0.8).add_tip().set_color(BLUE)

        row = VGroup()
        self.add(histogram, row, arrow)
        for i in range(3):
            self.play(UpdateFromFunc(row, update))
