from itertools import product
import scipy.stats

from manim import *

probabilities = {0: [0.4, 0.6], 1: [0.3, 0.7], 2: [0.6, 0.4]}
labels = np.array(["food", "animals"])

word_probabilities = {
    0: {
        labels[0]: [0.2, 0.1, 0.3, 0.15, 0.25],
        labels[1]: [0.1, 0.15, 0.3, 0.25, 0.2],
    },
    1: {
        labels[0]: [0.15, 0.05, 0.35, 0.25, 0.2],
        labels[1]: [0.1, 0.25, 0.1, 0.3, 0.25],
    },
    2: {
        labels[0]: [0.1, 0.15, 0.3, 0.25, 0.2],
        labels[1]: [0.2, 0.1, 0.3, 0.15, 0.25],
    },
}


words = {
    labels[0]: ["banana.svg", "kiwi.svg", "lemon.svg", "strawberry.svg", "tomato.svg"],
    labels[1]: ["chicken.svg", "piggy.svg", "sheep.svg", "crocodile.svg", "zebra.svg"],
}


def create_histogram(probabilities, labels, **kwargs):
    """Creates a histogram with probabilities and labels."""
    return BarChart(
        values=probabilities,
        bar_names=labels,
        y_axis_config={"font_size": 36},
        y_length=3,
        x_length=5,
        **kwargs,
    )

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
    symbol.next_to(row, RIGHT, buff=0.05)
    return symbol

def add_svg_xticks(histogram):
    for i, svg in enumerate(sum(words.values(), [])):
        symbol = SVGMobject("icons/" + svg, width=0.4)
        symbol.next_to(histogram[0][i], DOWN, buff=0.3, aligned_edge=DOWN)
        histogram.add(symbol)

class TopicGenerationSimulation(Scene):

    alphas_topics = [10, 20]
    alphas_words_topic1 = [5,10,8,3,10]
    alphas_words_topic2 = [10,3,8,9,5]

    def construct(self):
        # create empty histograms
        histogram_topic = create_histogram([0,0.0], labels, y_range=[0, 0.6, 0.2])
        histogram_words = create_histogram(
            10*[0],
            labels=None,
            bar_colors=5 * ["#003f5c"] + 5 * ["#ffa600"],
            y_range = (0, 0.3, 0.1),
        )
        add_svg_xticks(histogram_words)

        # create arrows
        arrow_topic = Line(ORIGIN, DOWN * 0.8).add_tip().set_color(BLUE)
        arrow_word = Line(ORIGIN, DOWN * 0.8).add_tip().set_color(BLUE)

        # align objects
        histogram_topic.to_edge(DOWN + LEFT)
        histogram_words.to_edge(DOWN + RIGHT)
        histogram_words.move_to(histogram_topic, UP, UP)

        row = VGroup(Tex(r"doc 1:"))
        row.to_edge(UP + LEFT, buff=0.1)

        # initialize view
        self.add(histogram_topic, histogram_words, row)
        return
        # animate
        for i in range(5):
            topic_p = scipy.stats.dirichlet(self.alphas_topics).rvs(1)[0]

            word_p1 = scipy.stats.dirichlet(self.alphas_words_topic1).rvs(1)[0]
            word_p2 = scipy.stats.dirichlet(self.alphas_words_topic2).rvs(1)[0]

            word_p = np.concatenate((word_p1, word_p2))
            self.play(histogram_topic.animate.change_bar_values(topic_p))
            self.play(histogram_words.animate.change_bar_values(word_p))


        return
        for doc, word in product(np.arange(3), np.arange(6)):
            if doc > 0 and word == 0:
                self.play(FadeOut(arrow_topic), FadeOut(arrow_word))
            if word == 0:
                self.play(
                    histogram_topic[0].animate.change_bar_values(probabilities[doc])
                )
                self.play(
                    histogram_words[0].animate.change_bar_values(
                        sum(word_probabilities[doc].values(), []),
                    ),
                )
            if doc != 0 and word == 0:
                new_row = VGroup(Tex(f"doc {doc+1}: "))
                new_row.next_to(row, DOWN, buff=0.1, aligned_edge=LEFT)
                self.add(new_row)
                row = new_row
            value = np.random.choice([0, 1], p=probabilities[doc])
            topic_symbol = create_topic_symbol(row, value)
            row.add(topic_symbol)
            if word == 0:
                arrow_topic.next_to(histogram_topic[0][0][value], UP, buff=0.1)
                self.play(
                    FadeIn(topic_symbol),
                    FadeIn(arrow_topic),
                )
            else:
                self.play(
                    arrow_topic.animate.next_to(
                        histogram_topic[0][0][value], UP, buff=0.1,
                    ),
                    run_time=0.25,
                )
                self.play(FadeIn(topic_symbol), run_time=0.5)
            topics = list(word_probabilities[doc].keys())
            topic = topics[value]
            value = np.random.choice(np.arange(5), p=word_probabilities[doc][topic])
            word_symbol = create_word_token(value, topic)
            word_symbol.move_to(topic_symbol.get_center())
            bar = histogram_words[0][0][value + 5 * topics.index(topic)]
            if word == 0:
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
