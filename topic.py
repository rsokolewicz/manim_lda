from manim import *

probabilities = 0.4, 0.6
labels = np.array(["food", "animals"])

word_probabilities = {
    labels[0]: [0.2, 0.1, 0.3, 0.15, 0.25],
    labels[1]: [0.1, 0.15, 0.3, 0.25, 0.2],
}

words = {
    labels[0]: ["banana.svg", "kiwi.svg", "lemon.svg", "strawberry.svg", "tomato.svg"],
    labels[1]: ["chicken.svg", "piggy.svg", "sheep.svg", "crocodile.svg", "zebra.svg"],
}


def create_histogram(probabilities, labels, **kwargs):
    """Creates a histogram with probabilities and labels."""
    histogram = VGroup()
    chart = BarChart(
        values=probabilities,
        bar_names=labels,
        y_axis_config={"font_size": 36},
        y_length=3,
        x_length=5,
        **kwargs,
    )

    histogram.add(chart)
    histogram.to_edge(DL)
    return histogram


def fix_svg(svgmobject):
    """Fixes missing attributes when loading svg."""
    attrs = [
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


def create_word_token(value, topic):
    """Creates a word token."""
    symbol = SVGMobject(f"icons/{words[topic][value]}", height=0.4)
    fix_svg(symbol)
    return symbol


def create_topic_symbol(row, value):
    """Creates a topic symbol."""
    if value == 0:
        symbol = Square(side_length=0.5, color=BLUE)
    else:
        symbol = Square(side_length=0.5, color=ORANGE)
    symbol.next_to(row, RIGHT, buff=0.0)
    return symbol


class TopicGenerationSimulation(Scene):
    def construct(self):
        histogram_topic = create_histogram(probabilities, labels)
        histogram_words = create_histogram(
            sum(word_probabilities.values(), []),
            labels=None,
            bar_colors=5 * ["#003f5c"] + 5 * ["#ffa600"],
        )

        histogram_words.to_edge(DOWN + RIGHT)
        for i, symbol in enumerate(sum(words.values(), [])):
            symbol = SVGMobject("icons/" + symbol, width=0.4)
            symbol.next_to(histogram_words[0][0][i], DOWN, buff=0.1)
            histogram_words.add(symbol)
        arrow_topic = Line(ORIGIN, DOWN * 0.8).add_tip().set_color(BLUE)
        arrow_word = Line(ORIGIN, DOWN * 0.8).add_tip().set_color(BLUE)

        row = VGroup(Tex(r"doc 1:"))
        row.to_edge(UP + LEFT, buff=0)
        self.add(histogram_topic, histogram_words, row)
        for i in range(10):
            value = np.random.choice([0, 1], p=probabilities)
            topic_symbol = create_topic_symbol(row, value)
            row.add(topic_symbol)
            row.to_edge(UP + LEFT, buff=0)
            if i == 0:
                arrow_topic.next_to(histogram_topic[0][0][value], UP, buff=0.1)
                self.play(
                    FadeIn(topic_symbol),
                    FadeIn(arrow_topic),
                )
            else:
                self.play(
                    arrow_topic.animate.next_to(
                        histogram_topic[0][0][value], UP, buff=0.1
                    ),
                    run_time=0.25,
                )
                self.play(FadeIn(topic_symbol), run_time=0.5)
            topics = list(word_probabilities.keys())
            topic = topics[value]
            value = np.random.choice(np.arange(5), p=word_probabilities[topic])
            word_symbol = create_word_token(value, topic)
            word_symbol.move_to(topic_symbol.get_center())
            bar = histogram_words[0][0][value + 5 * topics.index(topic)]
            if i == 0:
                arrow_word.next_to(
                    bar,
                    UP,
                    buff=0.1,
                )
                self.play(FadeIn(arrow_word))
            else:
                self.play(
                    arrow_word.animate.next_to(
                        bar,
                        UP,
                        buff=0.1,
                    ),
                    run_time=0.25,
                )
            self.play(FadeIn(word_symbol), FadeOut(topic_symbol), run_time=0.5)
