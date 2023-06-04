from itertools import product
from scipy.stats import dirichlet, multinomial

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


words = [
    "banana",
    "kiwi",
    "lemon",
    "strawberry",
    "tomato",
    "chicken",
    "piggy",
    "sheep",
    "crocodile",
    "zebra",
]


def add_svg_xticks(bar_chart):
    """Adds svg symbols instead of standard x-ticks to a BarChart."""
    for i, word in enumerate(words):
        symbol = create_word_token(word)
        symbol.next_to(bar_chart[0][i], DOWN, buff=0.3, aligned_edge=DOWN)
        bar_chart.add(symbol)


def create_histogram(probabilities, labels, **kwargs):
    """Creates a histogram with probabilities and labels."""
    return BarChart(
        values=probabilities,
        bar_names=labels,
        y_axis_config={"font_size": 36},
        x_axis_config={"font_size": 36},
        y_length=4,
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


def create_word_token(word):
    """Creates a word token."""
    symbol = SVGMobject(f"icons/{word}.svg", height=0.4)
    fix_svg(symbol)
    return symbol


def create_topic_symbol(row, value):
    """Creates a topic symbol."""
    if value == 0:
        symbol = Square(side_length=0.5, color=BLUE)
    else:
        symbol = Square(side_length=0.5, color=ORANGE)
    symbol.next_to(row, RIGHT, buff=0.05)
    row.add(symbol)
    return symbol


class TopicGenerationSimulation(Scene):
    alphas_topics = [10, 20]
    alphas_words_topic1 = [5, 10, 8, 3, 10]
    alphas_words_topic2 = [10, 3, 8, 9, 5]

    def construct(self):
        # create empty histograms
        topic_distribution = create_histogram([0, 0.0], labels, y_range=[0, 0.8, 0.2])
        word_distribution = create_histogram(
            10 * [0],
            labels=None,
            bar_colors=5 * ["#003f5c"] + 5 * ["#ffa600"],
            y_range=(0, 0.5, 0.1),
        )
        add_svg_xticks(word_distribution)

        # create arrows
        arrow_topic = Line(ORIGIN, DOWN * 0.8).add_tip().set_color(BLUE)
        arrow_word = Line(ORIGIN, DOWN * 0.8).add_tip().set_color(BLUE)

        # align objects
        topic_distribution.to_edge(DOWN + LEFT)
        word_distribution.to_edge(DOWN + RIGHT)
        word_distribution.move_to(topic_distribution, UP, UP)

        row = VGroup(Tex(r"doc 1:"))
        row.to_edge(UP + LEFT, buff=0.1)

        # initialize view
        self.add(topic_distribution, word_distribution, row)
        # self.add(topic_distribution, word_distribution)
        # return
        # animate
        # for doc in range(5):
        # draw probabilities

        for doc_index in range(3):
            topic_prob = dirichlet(self.alphas_topics).rvs(1)[0]
            word_prob = np.concatenate(
                [
                    dirichlet(self.alphas_words_topic1).rvs(1)[0],
                    dirichlet(self.alphas_words_topic2).rvs(1)[0],
                ],
            )
            if doc_index > 0:
                self.play(FadeOut(arrow_topic), FadeOut(arrow_word))
            self.play(topic_distribution.animate.change_bar_values(topic_prob))
            self.play(word_distribution.animate.change_bar_values(word_prob))
            # else:
            #     topic_distribution.change_bar_values(topic_prob)
            #     word_distribution.change_bar_values(word_prob)
            #     # self.add(topic_distribution, word_distribution)

            self.play(Wait(1))

            for word_index in range(5):
                topic = np.argmax(multinomial.rvs(1, topic_prob))
                word = (
                    np.argmax(
                        multinomial.rvs(1, word_prob[5 * topic : 5 * (topic + 1)])
                    )
                    + 5 * topic
                )
                topic_symbol = create_topic_symbol(row, topic)

                if doc_index != 0 and word_index == 0:
                    # self.play(FadeOut(arrow_topic), FadeOut(arrow_word))
                    new_row = VGroup(Tex(f"doc {doc_index+1}: "))
                    new_row.next_to(row, DOWN, buff=0.1, aligned_edge=LEFT)
                    self.add(new_row)
                    row = new_row
                    topic_symbol = create_topic_symbol(row, topic)

                if word_index == 0:
                    arrow_topic.next_to(topic_distribution[0][topic], UP, buff=0.1)
                    arrow_word.next_to(
                        word_distribution[0][word],
                        UP,
                        buff=0.1,
                    )
                    self.play(
                        FadeIn(topic_symbol),
                        FadeIn(arrow_topic),
                    )
                    self.play(FadeIn(arrow_word))
                else:
                    self.play(
                        FadeIn(topic_symbol),
                        arrow_topic.animate.next_to(
                            topic_distribution[0][topic], UP, buff=0.1
                        ),
                    )
                    self.play(
                        arrow_word.animate.next_to(
                            word_distribution[0][word],
                            UP,
                            buff=0.1,
                        ),
                    )

                word_symbol = create_word_token(words[word])
                word_symbol.next_to(
                    word_distribution[0][word], DOWN, buff=0.3, aligned_edge=DOWN
                )

                self.play(word_symbol.animate.move_to(topic_symbol.get_center()))
                self.play(FadeOut(topic_symbol), run_time=0.5)

        #     for word_index in range(6):
        #         topic, word = draw_topic_and_word()
        #         topic_symbol = create_topic_symbol(row, topic)

        #         if word_index == 0:
        #             arrow_topic.next_to(topic_distribution[0][topic], UP, buff=0.1)
        #             self.play(
        #                 FadeIn(topic_symbol),
        #                 FadeIn(arrow_topic),
        #             )
        #         else:
        #             self.play(
        #                 arrow_topic.animate.next_to(
        #                     topic_distribution[0][topic],
        #                     UP,
        #                     buff=0.1,
        #                 ),
        #                 run_time=0.25,
        #             )
        #             self.play(FadeIn(topic_symbol), run_time=0.5)
        return
        for doc_index, word_index in product(np.arange(3), np.arange(6)):
            topic = np.argmax(multinomial.rvs(1, topic_prob))
            word = (
                np.argmax(multinomial.rvs(1, [word_prob_1, word_prob_2][topic]))
                + 5 * topic
            )
            if doc_index > 0 and word_index == 0:
                self.play(FadeOut(arrow_topic), FadeOut(arrow_word))
            if word_index == 0:
                self.play(
                    topic_distribution[0].animate.change_bar_values(
                        probabilities[doc_index]
                    )
                )
                self.play(
                    word_distribution[0].animate.change_bar_values(
                        sum(word_probabilities[doc_index].values(), []),
                    ),
                )
            if doc_index != 0 and word_index == 0:
                new_row = VGroup(Tex(f"doc {doc_index+1}: "))
                new_row.next_to(row, DOWN, buff=0.1, aligned_edge=LEFT)
                self.add(new_row)
                row = new_row
            value = np.random.choice([0, 1], p=probabilities[doc_index])
            topic_symbol = create_topic_symbol(row, value)
            row.add(topic_symbol)
            if word_index == 0:
                arrow_topic.next_to(topic_distribution[0][value], UP, buff=0.1)
                self.play(
                    FadeIn(topic_symbol),
                    FadeIn(arrow_topic),
                )
            else:
                self.play(
                    arrow_topic.animate.next_to(
                        topic_distribution[0][value],
                        UP,
                        buff=0.1,
                    ),
                    run_time=0.25,
                )
                self.play(FadeIn(topic_symbol), run_time=0.5)
            topics = list(word_probabilities[doc_index].keys())
            topic = topics[value]
            value = np.random.choice(
                np.arange(5), p=word_probabilities[doc_index][topic]
            )
            word_symbol = create_word_token(value, topic)
            word_symbol.move_to(topic_symbol.get_center())
            bar = word_distribution[0][0][value + 5 * topics.index(topic)]
            if word_index == 0:
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
