"""Превращает текст в SVG-контуры через шрифтовые глифы.

Нужен потому, что GitHub не даёт контролировать шрифт в markdown, а `<text>`
в SVG зависит от шрифтов машины. Контуры от такого не зависят.
"""

from __future__ import annotations

import functools
import urllib.request
from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FONT_DIR = Path(__file__).resolve().parent.parent / ".build" / "fonts"

SOURCES = {
    "Orbitron": "https://raw.githubusercontent.com/google/fonts/main/ofl/orbitron/Orbitron%5Bwght%5D.ttf",
    "Inter": "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz,wght%5D.ttf",
}


def _fetch(name: str) -> Path:
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    path = FONT_DIR / f"{name}.ttf"
    if not path.exists():
        with urllib.request.urlopen(SOURCES[name], timeout=120) as r:
            path.write_bytes(r.read())
    return path


def _ntos(v: float) -> str:
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


@functools.lru_cache(maxsize=32)
def load(family: str, weight: int) -> TTFont:
    font = TTFont(_fetch(family), recalcBBoxes=False, recalcTimestamp=False)
    if "fvar" in font:
        axes = {a.axisTag for a in font["fvar"].axes}
        loc = {"wght": weight}
        if "opsz" in axes:
            loc["opsz"] = 12
        font = instancer.instantiateVariableFont(font, loc, inplace=False, updateFontNames=False)
    return font


def metrics(family: str, weight: int) -> tuple[float, float, float]:
    """Возвращает (upem, ascent, descent) в единицах шрифта."""
    f = load(family, weight)
    upem = f["head"].unitsPerEm
    hhea = f["hhea"]
    return upem, hhea.ascender, hhea.descender


def advance(family: str, weight: int, s: str, size: float) -> float:
    f = load(family, weight)
    scale = size / f["head"].unitsPerEm
    cmap, hmtx = f.getBestCmap(), f["hmtx"]
    total = 0.0
    for ch in s:
        g = cmap.get(ord(ch)) or cmap[ord("?")]
        total += hmtx[g][0] * scale
    return total


def text_path(
    family: str,
    weight: int,
    s: str,
    size: float,
    x: float = 0.0,
    y: float = 0.0,
    letter_spacing: float = 0.0,
    anchor: str = "start",
) -> tuple[str, float]:
    """Возвращает (path-d, ширина) для строки с базовой линией в (x, y).

    anchor: start | middle | end. letter_spacing добавляется между символами,
    без хвостового пробела в конце.
    """
    f = load(family, weight)
    upem = f["head"].unitsPerEm
    scale = size / upem
    cmap, hmtx = f.getBestCmap(), f["hmtx"]
    glyphs = f.getGlyphSet()
    fallback = cmap[ord("?")]

    names = [cmap.get(ord(ch)) or fallback for ch in s]
    widths = [hmtx[g][0] * scale for g in names]
    total = sum(widths) + letter_spacing * max(0, len(names) - 1)

    if anchor == "middle":
        cursor = x - total / 2
    elif anchor == "end":
        cursor = x - total
    else:
        cursor = x

    pen = SVGPathPen(glyphs, ntos=_ntos)
    for i, g in enumerate(names):
        # ось Y в шрифте смотрит вверх, в SVG — вниз
        glyphs[g].draw(TransformPen(pen, Transform(scale, 0, 0, -scale, cursor, y)))
        cursor += widths[i]
        if i < len(names) - 1:
            cursor += letter_spacing

    return pen.getCommands(), total
