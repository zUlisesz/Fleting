"""Galería de gradientes lineales, radiales y angulares de Flet."""

import math

import flet as ft


def gradient_gallery() -> ft.Row:
    """Muestra distintas configuraciones de los tres tipos de gradiente."""

    examples: list[tuple[str, ft.Gradient]] = [
        (
            "Linear · horizontal",
            ft.LinearGradient(
                begin=ft.Alignment.CENTER_LEFT,
                end=ft.Alignment.CENTER_RIGHT,
                colors=["#2563EB", "#7C3AED"],
            ),
        ),
        (
            "Linear · vertical",
            ft.LinearGradient(
                begin=ft.Alignment.TOP_CENTER,
                end=ft.Alignment.BOTTOM_CENTER,
                colors=["#F97316", "#DB2777"],
            ),
        ),
        (
            "Linear · multicolor",
            ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=["#06B6D4", "#22C55E", "#EAB308"],
                stops=[0.0, 0.45, 1.0],
            ),
        ),
        (
            "Linear · sunset",
            ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=["#FDE68A", "#FB7185", "#7C3AED"],
            ),
        ),
        (
            "Linear · ocean",
            ft.LinearGradient(
                begin=ft.Alignment.TOP_CENTER,
                end=ft.Alignment.BOTTOM_CENTER,
                colors=["#A5F3FC", "#0891B2", "#164E63"],
            ),
        ),
        (
            "Linear · forest",
            ft.LinearGradient(
                begin=ft.Alignment.CENTER_LEFT,
                end=ft.Alignment.CENTER_RIGHT,
                colors=["#D9F99D", "#65A30D", "#14532D"],
            ),
        ),
        (
            "Linear · rose gold",
            ft.LinearGradient(
                begin=ft.Alignment.BOTTOM_LEFT,
                end=ft.Alignment.TOP_RIGHT,
                colors=["#9F1239", "#FDA4AF", "#FDE68A"],
                stops=[0.0, 0.55, 1.0],
            ),
        ),
        (
            "Neon · purple blue",
            ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=["#D946EF", "#7C3AED", "#2563EB", "#22D3EE"],
                stops=[0.0, 0.32, 0.7, 1.0],
            ),
        ),
        (
            "Neon · cyan green",
            ft.LinearGradient(
                begin=ft.Alignment.CENTER_LEFT,
                end=ft.Alignment.CENTER_RIGHT,
                colors=["#00F5FF", "#00FFB3", "#A3FF12"],
            ),
        ),
        (
            "Neon · yellow red",
            ft.LinearGradient(
                begin=ft.Alignment.TOP_CENTER,
                end=ft.Alignment.BOTTOM_CENTER,
                colors=["#F9FF00", "#FF8A00", "#FF1744"],
            ),
        ),
        (
            "Neon · galaxy",
            ft.LinearGradient(
                begin=ft.Alignment.BOTTOM_LEFT,
                end=ft.Alignment.TOP_RIGHT,
                colors=["#090026", "#4C1D95", "#E040FB", "#00D9FF"],
                stops=[0.0, 0.38, 0.72, 1.0],
            ),
        ),
        (
            "Radial · centered",
            ft.RadialGradient(
                center=ft.Alignment.CENTER,
                radius=0.8,
                colors=["#FDE68A", "#F97316", "#9A3412"],
                stops=[0.0, 0.45, 1.0],
            ),
        ),
        (
            "Radial · offset",
            ft.RadialGradient(
                center=ft.Alignment(-0.5, -0.5),
                radius=1.1,
                colors=["#F0ABFC", "#A855F7", "#312E81"],
            ),
        ),
        (
            "Radial · focal",
            ft.RadialGradient(
                center=ft.Alignment.CENTER,
                focal=ft.Alignment(-0.4, -0.3),
                focal_radius=0.1,
                radius=0.85,
                colors=["#FFFFFF", "#38BDF8", "#0C4A6E"],
            ),
        ),
        (
            "Radial · lavender",
            ft.RadialGradient(
                center=ft.Alignment.CENTER,
                radius=0.9,
                colors=["#F5D0FE", "#C084FC", "#6D28D9"],
            ),
        ),
        (
            "Radial · ember",
            ft.RadialGradient(
                center=ft.Alignment(0.4, 0.3),
                radius=1.0,
                colors=["#FEF08A", "#F97316", "#7F1D1D"],
            ),
        ),
        (
            "Radial · mint",
            ft.RadialGradient(
                center=ft.Alignment(-0.3, -0.4),
                radius=0.95,
                colors=["#ECFDF5", "#5EEAD4", "#0F766E"],
            ),
        ),
        (
            "Radial · midnight",
            ft.RadialGradient(
                center=ft.Alignment.CENTER,
                radius=0.85,
                colors=["#818CF8", "#4338CA", "#0F172A"],
                stops=[0.0, 0.5, 1.0],
            ),
        ),
        (
            "Neon · violet pulse",
            ft.RadialGradient(
                center=ft.Alignment.CENTER,
                radius=0.9,
                colors=["#F0ABFC", "#A21CAF", "#3B0764", "#090026"],
                stops=[0.0, 0.28, 0.65, 1.0],
            ),
        ),
        (
            "Neon · electric lagoon",
            ft.RadialGradient(
                center=ft.Alignment(-0.35, -0.35),
                radius=1.1,
                colors=["#CCFFF6", "#00F5D4", "#008CFF", "#071B4D"],
                stops=[0.0, 0.3, 0.68, 1.0],
            ),
        ),
        (
            "Neon · solar flare",
            ft.RadialGradient(
                center=ft.Alignment(0.2, -0.2),
                radius=1.0,
                colors=["#FFFFFF", "#F9FF00", "#FF5A00", "#7F001D"],
                stops=[0.0, 0.2, 0.55, 1.0],
            ),
        ),
        (
            "Neon · nebula",
            ft.RadialGradient(
                center=ft.Alignment(-0.2, 0.2),
                radius=1.0,
                colors=["#FF67F0", "#6D28D9", "#1D4ED8", "#08071C"],
                stops=[0.0, 0.3, 0.7, 1.0],
            ),
        ),
        (
            "Sweep · spectrum",
            ft.SweepGradient(
                center=ft.Alignment.CENTER,
                colors=["#EF4444", "#FACC15", "#22C55E", "#3B82F6", "#A855F7", "#EF4444"],
                stops=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            ),
        ),
        (
            "Sweep · rotated",
            ft.SweepGradient(
                center=ft.Alignment.CENTER,
                rotation=math.pi / 4,
                colors=["#0F172A", "#2DD4BF", "#F8FAFC", "#0F172A"],
                stops=[0.0, 0.35, 0.7, 1.0],
            ),
        ),
        (
            "Sweep · half turn",
            ft.SweepGradient(
                center=ft.Alignment.CENTER,
                start_angle=0.0,
                end_angle=math.pi,
                colors=["#FB7185", "#FBBF24", "#7C3AED"],
                stops=[0.0, 0.5, 1.0],
            ),
        ),
        (
            "Sweep · citrus",
            ft.SweepGradient(
                center=ft.Alignment.CENTER,
                colors=["#F97316", "#FACC15", "#84CC16", "#F97316"],
            ),
        ),
        (
            "Sweep · lagoon",
            ft.SweepGradient(
                center=ft.Alignment.CENTER,
                colors=["#0F766E", "#67E8F9", "#2563EB", "#0F766E"],
            ),
        ),
        (
            "Sweep · berry",
            ft.SweepGradient(
                center=ft.Alignment.CENTER,
                colors=["#881337", "#F472B6", "#A855F7", "#881337"],
            ),
        ),
        (
            "Sweep · copper",
            ft.SweepGradient(
                center=ft.Alignment.CENTER,
                rotation=math.pi / 3,
                colors=["#78350F", "#FBBF24", "#FED7AA", "#78350F"],
            ),
        ),
        (
            "Neon · ultraviolet",
            ft.SweepGradient(
                center=ft.Alignment.CENTER,
                colors=["#6D28D9", "#F000FF", "#00D9FF", "#2563EB", "#6D28D9"],
            ),
        ),
        (
            "Neon · acid green",
            ft.SweepGradient(
                center=ft.Alignment.CENTER,
                colors=["#00F5FF", "#00FF85", "#D8FF00", "#00F5FF"],
            ),
        ),
        (
            "Neon · molten",
            ft.SweepGradient(
                center=ft.Alignment.CENTER,
                colors=["#FF1744", "#FF6D00", "#F9FF00", "#FF1744"],
            ),
        ),
        (
            "Neon · cosmic wheel",
            ft.SweepGradient(
                center=ft.Alignment.CENTER,
                rotation=math.pi / 4,
                colors=["#090026", "#A855F7", "#00D9FF", "#F000FF", "#090026"],
                stops=[0.0, 0.22, 0.5, 0.78, 1.0],
            ),
        ),
    ]

    return ft.Row(
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        run_spacing=20,
        controls=[
            ft.Container(
                width=240,
                height=220,
                gradient=gradient,
                border_radius=18,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                alignment=ft.Alignment.BOTTOM_CENTER,
                content=ft.Container(
                    width=240,
                    padding=12,
                    bgcolor=ft.Colors.with_opacity(0.75, ft.Colors.BLACK),
                    content=ft.Text(
                        label,
                        color=ft.Colors.WHITE,
                        size=15,
                        weight=ft.FontWeight.W_600,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ),
            )
            for label, gradient in examples
        ],
    )


def main(page: ft.Page) -> None:
    """Abre la galería como una aplicación independiente."""

    page.title = "Flet Gradients"
    page.bgcolor = "#111827"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 24
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(
        ft.Text("Flet gradients", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        gradient_gallery(),
    )


if __name__ == "__main__":
    ft.run(main)
