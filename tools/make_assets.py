"""Собирает графику для README: assets/hero.svg и кнопки контактов.

Запуск: uv run --no-project --with fonttools python tools/make_assets.py
Шрифты скачиваются автоматически в .build/fonts и в репозиторий не попадают.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import icons  # noqa: E402
from svg_text import cap_height, text_path  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

W = 520
H = 220
PAD = 36

NICK = "axstiz"
HELLO = "Привет, я Матвей"
SUB = "AI-инженер · студент УрФУ · Екатеринбург"
STATUS = "Открыт к работе: Junior+ / стажировка в AI"

STYLE = """
.card{fill:#f7f8fb;stroke:#e4e7ef}
.pill{fill:#f0edff;stroke:#ddd6ff}
.hair{stroke:#e4e7ef}
.title{fill:#0b0d14}
.muted{fill:#5c6377}
.nick{fill:#6d3fe0}
.status{fill:#15803d}
.dot{fill:#15803d}
.halo{fill:none;stroke:#15803d}
.bar{fill:#7a4dff}
@media (prefers-color-scheme: dark){
  .card{fill:#12141c;stroke:#262a38}
  .pill{fill:#1b1730;stroke:#312a52}
  .hair{stroke:#262a38}
  .title{fill:#eef0f6}
  .muted{fill:#9aa3b8}
  .nick{fill:#b18cff}
  .status{fill:#4ade80}
  .dot{fill:#4ade80}
  .halo{stroke:#4ade80}
  .bar{fill:#b18cff}
}
.status{animation:ax-blink 3.6s ease-in-out infinite}
@keyframes ax-blink{0%,100%{opacity:1}50%{opacity:.12}}
.halo{transform-box:fill-box;transform-origin:center;animation:ax-halo 2.4s ease-out infinite}
@keyframes ax-halo{0%{transform:scale(.45);opacity:.55}70%,100%{transform:scale(1.5);opacity:0}}
.nick,.title,.muted{animation:ax-in .7s cubic-bezier(.2,.9,.3,1.1) both}
.status,.dot,.halo{animation-delay:.25s}
@keyframes ax-in{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion: reduce){
  .status,.halo,.nick,.title,.muted{animation:none!important;opacity:1!important;transform:none!important}
  .halo{opacity:0!important}
}
"""


def build_hero() -> None:
    nick, nick_w = text_path("Orbitron", 700, NICK, 44, x=PAD, y=64, letter_spacing=0.6)
    hello, hello_w = text_path("Inter", 600, HELLO, 26, x=PAD, y=100)
    sub, sub_w = text_path("Inter", 400, SUB, 15, x=PAD, y=126, letter_spacing=0.1)

    # текст центрируется по высоте заглавных, а не по геометрическому центру:
    # визуальный центр строки выше базовой линии, на 4.5px для этого размера
    pill_h = 40
    pill_y = H - 70
    pill_mid = pill_y + pill_h / 2
    stat, stat_w = text_path(
        "Inter", 500, STATUS, 16, x=PAD + 36, y=pill_mid + cap_height("Inter", 500, 16) / 2
    )

    dot_x, dot_y = PAD + 15, pill_mid
    pill_w = PAD + 36 + stat_w + 20

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{NICK}. {HELLO}. {SUB}. {STATUS}.">
<title>{NICK} — {HELLO}</title>
<style>{STYLE}</style>
<rect class="card" x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="18" stroke-width="1.5"/>
<rect class="bar" x="0" y="34" width="3" height="{H - 68}" rx="1.5"/>
<path class="nick" d="{nick}"/>
<path class="title" d="{hello}"/>
<path class="muted" d="{sub}"/>
<line class="hair" x1="{PAD}" y1="146" x2="{W - PAD}" y2="146" stroke-width="1"/>
<rect class="pill" x="{PAD}" y="{pill_y}" width="{pill_w:.0f}" height="{pill_h}" rx="{pill_h / 2}" stroke-width="1.5"/>
<circle class="halo" cx="{dot_x}" cy="{dot_y}" r="7" stroke-width="1.5"/>
<circle class="dot" cx="{dot_x}" cy="{dot_y}" r="5"/>
<path class="status" d="{stat}"/>
</svg>
"""
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "hero.svg").write_text(svg, encoding="utf-8")
    print(
        f"hero.svg      {len(svg):>6} байт   "
        f"ник={nick_w:.0f} привет={hello_w:.0f} подпись={sub_w:.0f} "
        f"статус={stat_w:.0f} пилюля={pill_w:.0f} (доступно {W - 2 * PAD})"
    )


BUTTONS = [
    ("telegram", "Telegram", icons.TELEGRAM),
    ("email", "litsummer@mail.ru", icons.ENVELOPE),
    ("github", "GitHub", icons.GITHUB),
    ("gitverse", "Gitverse", icons.GIT),
]

BTN_STYLE = """
.bg{fill:#f7f8fb;stroke:#e4e7ef}
.label{fill:#0b0d14}
.icon{fill:#5c6377}
@media (prefers-color-scheme: dark){
  .bg{fill:#12141c;stroke:#262a38}
  .label{fill:#eef0f6}
  .icon{fill:#9aa3b8}
}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
"""


def build_buttons() -> None:
    bh, icon_sz, gap, pad = 40, 17, 10, 15
    scale = icon_sz / 24
    for slug, label, icon_d in BUTTONS:
        _, tw = text_path("Inter", 500, label, 14)
        w = pad + icon_sz + gap + tw + pad
        # evenodd превращает внутренний контур конверта в вырез «сложки»
        rule = ' fill-rule="evenodd"' if slug == "email" else ""
        icon = (
            f'<g class="icon" transform="translate({pad:.1f},{bh / 2 - icon_sz / 2:.2f}) '
            f'scale({scale:.4f})"><path{rule} d="{icon_d}"/></g>'
        )
        # верх заглавных на одной высоте у всех четырёх
        label_y = bh / 2 + cap_height("Inter", 500, 14) / 2
        text, _ = text_path("Inter", 500, label, 14, x=pad + icon_sz + gap, y=label_y)
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{bh}" viewBox="0 0 {w:.0f} {bh}" role="img" aria-label="{label}">
<style>{BTN_STYLE}</style>
<rect class="bg" x="0.75" y="0.75" width="{w - 1.5:.0f}" height="{bh - 1.5}" rx="10" stroke-width="1.5"/>
{icon}
<path class="label" d="{text}"/>
</svg>
"""
        (ASSETS / f"btn-{slug}.svg").write_text(svg, encoding="utf-8")
        print(f"btn-{slug}.svg  {len(svg):>5} байт  {w:.0f}x{bh}  «{label}»")


if __name__ == "__main__":
    build_hero()
    print()
    build_buttons()
