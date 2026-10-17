from pathlib import Path

from manim import *


config.pixel_width = 540
config.pixel_height = 960
config.frame_height = 8
config.frame_width = config.frame_height * config.pixel_width / config.pixel_height
config.frame_rate = 30

BACKGROUND = "#0B1220"
TEXT = "#F5F7FA"
MUTED = "#A9B6C8"
TEAL = "#24C8B5"
GOLD = "#FFB454"
PANEL = "#141F32"
DIVIDER = "#2B3A52"


def make_pie(center, denominator, highlighted, radius, color, second_color=None):
    slices = VGroup()
    for index in range(denominator):
        if second_color and highlighted[0] <= index < highlighted[1]:
            slice_color = second_color
            opacity = 0.95
        else:
            slice_color = color
            opacity = 0.95 if index < highlighted[0] else 0.12

        slices.add(
            Sector(
                radius=radius,
                angle=TAU / denominator,
                start_angle=PI / 2 + index * TAU / denominator,
                color=slice_color,
                fill_opacity=opacity,
                stroke_color=BACKGROUND,
                stroke_width=2,
            ).shift(center)
        )

    outline = Circle(
        radius=radius,
        color=TEXT,
        stroke_width=2,
    ).move_to(center)
    return VGroup(slices, outline)


class SomaFracoes(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND

        kicker = Text(
            "MATEMÁTICA • FRAÇÕES",
            color=TEAL,
            font_size=18,
            weight=BOLD,
        ).to_edge(UP, buff=0.42)
        title = Text(
            "Somar frações",
            color=TEXT,
            font_size=38,
            weight=BOLD,
        ).next_to(kicker, DOWN, buff=0.2)
        subtitle = Text(
            "com denominadores diferentes",
            color=MUTED,
            font_size=22,
        ).next_to(title, DOWN, buff=0.16)
        subtitle.scale_to_fit_width(config.frame_width - 0.45)

        divider = Line(
            LEFT * 1.65,
            RIGHT * 1.65,
            color=DIVIDER,
            stroke_width=2,
        ).next_to(subtitle, DOWN, buff=0.33)

        self.play(FadeIn(kicker, shift=DOWN * 0.12), Write(title), run_time=2)
        self.play(FadeIn(subtitle), Create(divider), run_time=1.5)
        self.wait(2)

        left_center = LEFT * 1.02 + DOWN * 0.12
        right_center = RIGHT * 1.02 + DOWN * 0.12
        radius = 0.62
        problem = MathTex(
            r"\frac{2}{4}+\frac{1}{3}=?",
            color=TEXT,
        ).scale(0.9).move_to(UP * 1.35)
        pie_2_4 = make_pie(left_center, 4, (2, 2), radius, TEAL)
        pie_1_3 = make_pie(right_center, 3, (1, 1), radius, GOLD)
        plus = MathTex("+", color=TEXT).scale(0.72).move_to(DOWN * 0.12)
        label_2_4 = MathTex(r"\frac{2}{4}", color=TEAL).scale(0.86)
        label_1_3 = MathTex(r"\frac{1}{3}", color=GOLD).scale(0.86)
        label_2_4.next_to(pie_2_4, DOWN, buff=0.13)
        label_1_3.next_to(pie_1_3, DOWN, buff=0.13)
        opening_caption = Text(
            "Duas pizzas. Dois tipos de fatia.",
            color=TEXT,
            font_size=20,
        ).scale_to_fit_width(config.frame_width - 0.45).move_to(DOWN * 2.15)

        self.play(Write(problem), run_time=1.8)
        self.play(
            FadeIn(pie_2_4),
            FadeIn(pie_1_3),
            Write(plus),
            Write(label_2_4),
            Write(label_1_3),
            run_time=2,
        )
        self.play(FadeIn(opening_caption, shift=UP * 0.12), run_time=1)
        self.wait(3.5)

        self.play(
            FadeOut(problem, pie_2_4, pie_1_3, plus, label_2_4, label_1_3, opening_caption),
            run_time=1.2,
        )

        mismatch_title = Text(
            "Tente juntar uma fatia de cada...",
            color=TEXT,
            font_size=24,
        ).scale_to_fit_width(config.frame_width - 0.4).move_to(UP * 1.35)
        quarter_center = LEFT * 0.9 + DOWN * 0.18
        third_center = RIGHT * 0.9 + DOWN * 0.18
        quarter_slice = Sector(
            radius=0.62,
            angle=PI / 2,
            start_angle=0,
            color=TEAL,
            fill_opacity=0.82,
            stroke_color=BACKGROUND,
            stroke_width=3,
        ).shift(quarter_center)
        third_slice = Sector(
            radius=0.62,
            angle=2 * PI / 3,
            start_angle=0,
            color=GOLD,
            fill_opacity=0.68,
            stroke_color=BACKGROUND,
            stroke_width=3,
        ).shift(third_center)
        quarter_label = MathTex(
            r"\frac{1}{4}=90^\circ",
            color=TEAL,
        ).scale(0.68).move_to(LEFT * 0.9 + DOWN * 1.18)
        third_label = MathTex(
            r"\frac{1}{3}=120^\circ",
            color=GOLD,
        ).scale(0.68).move_to(RIGHT * 0.9 + DOWN * 1.18)
        mismatch = MathTex(r"\ne", color=RED).scale(0.75).move_to(DOWN * 0.18)
        mismatch_caption = Text(
            "90° e 120° não se encaixam!\nAs fatias não têm o mesmo tamanho.",
            color=TEXT,
            font_size=19,
            line_spacing=0.9,
        ).scale_to_fit_width(config.frame_width - 0.45).move_to(DOWN * 2.35)

        self.play(Write(mismatch_title), run_time=1.5)
        self.play(
            FadeIn(quarter_slice),
            FadeIn(third_slice),
            run_time=2,
        )
        self.play(
            Write(quarter_label),
            Write(third_label),
            run_time=1.5,
        )
        self.play(Write(mismatch), FadeIn(mismatch_caption), run_time=1.5)
        self.wait(4)

        self.play(
            FadeOut(
                mismatch_title,
                quarter_slice,
                third_slice,
                quarter_label,
                third_label,
                mismatch,
                mismatch_caption,
            ),
            run_time=1,
        )

        solution_title = Text(
            "A solução: dividir em partes iguais",
            color=TEXT,
            font_size=23,
            weight=BOLD,
        ).scale_to_fit_width(config.frame_width - 0.4).move_to(UP * 1.35)
        pie_2_4 = make_pie(left_center, 4, (2, 2), radius, TEAL)
        pie_1_3 = make_pie(right_center, 3, (1, 1), radius, GOLD)
        original_label_a = MathTex(r"\frac{2}{4}", color=TEAL).scale(0.82)
        original_label_b = MathTex(r"\frac{1}{3}", color=GOLD).scale(0.82)
        original_label_a.next_to(pie_2_4, DOWN, buff=0.12)
        original_label_b.next_to(pie_1_3, DOWN, buff=0.12)
        mmc_label = Text(
            "MMC(4, 3) = 12",
            color=TEAL,
            font_size=27,
            weight=BOLD,
        ).move_to(DOWN * 1.85)

        self.play(Write(solution_title), run_time=1.5)
        self.play(
            FadeIn(pie_2_4),
            FadeIn(pie_1_3),
            Write(original_label_a),
            Write(original_label_b),
            run_time=1.8,
        )
        self.play(Write(mmc_label), run_time=1.4)
        self.wait(2)

        pie_6_12 = make_pie(left_center, 12, (6, 6), radius, TEAL)
        pie_4_12 = make_pie(right_center, 12, (4, 4), radius, GOLD)
        equivalent_a = MathTex(
            r"\frac{2}{4}=\frac{6}{12}",
            color=TEAL,
        ).scale(0.72).move_to(DOWN * 1.18 + LEFT * 0.98)
        equivalent_b = MathTex(
            r"\frac{1}{3}=\frac{4}{12}",
            color=GOLD,
        ).scale(0.72).move_to(DOWN * 1.18 + RIGHT * 0.98)
        equal_caption = Text(
            "Agora, cada pedacinho tem o mesmo tamanho.",
            color=TEXT,
            font_size=18,
        ).scale_to_fit_width(config.frame_width - 0.45).move_to(DOWN * 2.25)

        self.play(
            ReplacementTransform(pie_2_4, pie_6_12),
            ReplacementTransform(pie_1_3, pie_4_12),
            Transform(original_label_a, equivalent_a),
            Transform(original_label_b, equivalent_b),
            run_time=2.5,
        )
        self.play(Transform(mmc_label, equal_caption), run_time=1.5)
        self.wait(4)

        self.play(
            FadeOut(
                solution_title,
                pie_6_12,
                pie_4_12,
                original_label_a,
                original_label_b,
                mmc_label,
                divider,
            ),
            run_time=1.3,
        )

        result_center = UP * 0.48
        result_pie = make_pie(result_center, 12, (6, 10), 0.82, TEAL, GOLD)
        equation = MathTex(
            r"\frac{6}{12}+\frac{4}{12}=\frac{10}{12}",
            color=TEXT,
        ).scale_to_fit_width(config.frame_width - 0.35).scale(0.72)
        simplification = MathTex(
            r"\frac{10}{12}=\frac{5}{6}",
            color=TEAL,
        ).scale(0.82)
        equation.move_to(DOWN * 1.22)
        simplification.move_to(DOWN * 2.28)
        result_title = Text(
            "Agora podemos somar!",
            color=TEXT,
            font_size=29,
            weight=BOLD,
        ).scale_to_fit_width(config.frame_width - 0.4).move_to(UP * 1.55)

        self.play(Write(result_title), run_time=1.8)
        self.play(FadeIn(result_pie, scale=0.92), run_time=1.5)
        self.play(Write(equation), run_time=2)
        self.play(Write(simplification), run_time=1.5)

        takeaway = Text(
            "Some os numeradores; mantenha o denominador.",
            color=MUTED,
            font_size=18,
        ).scale_to_fit_width(config.frame_width - 0.5)
        takeaway.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(takeaway), run_time=1)
        self.wait(5)


if __name__ == "__main__":
    config.media_dir = str(Path(__file__).resolve().parent / "media")
    SomaFracoes().render()
