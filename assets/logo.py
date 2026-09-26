"""The logo: the real fly nervous system as a halftone, seen from the front, over the wordmark.

    pip install uharfbuzz fonttools
    python assets/logo.py        # writes assets/logo-light.svg and assets/logo-dark.svg

Each dot is one cell of a hex grid laid over the 140,638 neurons whose cell bodies have a known
position, with its area following how many neurons fall in the cell. Where most of them belong to
the optic lobes the dot is red: the optic lobes sit right behind the fly's red eyes. The wordmark is
Newsreader Italic (SIL Open Font License), fetched once and turned into outlines, so the SVG needs
no font to display.
"""
from __future__ import annotations

import os
import urllib.request
from pathlib import Path

import numpy as np

OUT = Path(__file__).parent
DATA = Path(os.environ.get("FLY_DATA", Path.home() / "fly-data")) / "brain.npz"   # as brainfly.data
FONT_URL = "https://github.com/google/fonts/raw/main/ofl/newsreader/Newsreader-Italic%5Bopsz,wght%5D.ttf"
FONT = Path.home() / ".cache" / "brainfly" / "Newsreader-Italic[opsz,wght].ttf"
THEMES = {"light": ("#1f2328", "#b8322a"), "dark": ("#e6edf3", "#e5533f")}   # ink, eye red
OPTIC = ["ol_intrinsic", "ol_sensory", "visual_projection", "visual_centrifugal"]


def halftone(cols: int = 40, gamma: float = 0.55, ref_pct: float = 85, min_r: float = 0.16):
    """Dot centres and radii in units of the grid pitch, and whether each dot is optic lobe."""
    z = np.load(DATA)
    pos, known = z["positions"], ~np.isnan(z["positions"]).any(1)
    x, y = pos[known, 0].astype(float), pos[known, 1].astype(float)
    optic = np.isin(z["superclass"][known], OPTIC)
    pitch = (x.max() - x.min()) / cols
    row = np.round((y - y.min()) / (pitch * np.sqrt(3) / 2)).astype(int)
    col = np.round((x - x.min() - (row % 2) * pitch / 2) / pitch).astype(int)
    cells, inv, count = np.unique(row * 10_000 + col, return_inverse=True, return_counts=True)
    red = np.bincount(inv, weights=optic) / count > 0.5
    rad = 0.5 * np.clip(count / np.percentile(count, ref_pct), 0, 1) ** gamma
    r, c = cells // 10_000, cells % 10_000
    keep = rad >= min_r
    occupied = set(zip(r[keep], c[keep]))
    for i in np.flatnonzero(keep):   # drop specks with fewer than two occupied hex neighbours
        d = r[i] % 2   # odd rows sit half a pitch to the right
        near = [(r[i], c[i] - 1), (r[i], c[i] + 1), (r[i] - 1, c[i] - 1 + d), (r[i] - 1, c[i] + d),
                (r[i] + 1, c[i] - 1 + d), (r[i] + 1, c[i] + d)]
        keep[i] = sum(n in occupied for n in near) >= 2
    return c[keep] + (r[keep] % 2) / 2, r[keep] * np.sqrt(3) / 2, rad[keep], red[keep]


def wordmark(text: str, size: float = 100, axes: dict | None = None):
    """Outline path of `text`, shaped with its kerning and ligatures, and its ink bounds."""
    import uharfbuzz as hb
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont
    from fontTools.varLib.instancer import instantiateVariableFont

    if not FONT.exists():
        FONT.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(FONT_URL, FONT)
    axes = axes or {"opsz": 72, "wght": 600}
    font = hb.Font(hb.Face(hb.Blob.from_file_path(str(FONT))))
    font.set_variations(axes)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    tt = instantiateVariableFont(TTFont(FONT), axes)
    glyphs, order, s = tt.getGlyphSet(), tt.getGlyphOrder(), size / tt["head"].unitsPerEm
    x, paths, bounds = 0, [], BoundsPen(glyphs)
    for info, p in zip(buf.glyph_infos, buf.glyph_positions):
        g = glyphs[order[info.codepoint]]
        t = (s, 0, 0, -s, (x + p.x_offset) * s, -p.y_offset * s)
        pen = SVGPathPen(glyphs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        g.draw(TransformPen(pen, t))
        g.draw(TransformPen(bounds, t))
        paths.append(pen.getCommands())
        x += p.x_advance
    return " ".join(paths), bounds.bounds


def logo(theme: str, dots, word, width: float = 1000, word_share: float = 0.78, gap: float = 0.09) -> str:
    ink, eye = THEMES[theme]
    cx, cy, rad, red = dots
    pad = rad.max()
    s = width / (cx.max() - cx.min() + 2 * pad)
    fill = {True: [], False: []}
    for x, y, r, is_red in zip(cx, cy, rad, red):
        fill[bool(is_red)].append(f'<circle cx="{(x - cx.min() + pad) * s:.1f}" cy="{(y - cy.min() + pad) * s:.1f}" r="{r * s:.2f}"/>')
    mark_h = (cy.max() - cy.min() + 2 * pad) * s
    path, (bx0, by0, bx1, by1) = word
    k = word_share * width / (bx1 - bx0)
    tx, ty = (width - (bx1 - bx0) * k) / 2 - bx0 * k, mark_h + gap * width - by0 * k
    height = ty + by1 * k
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}" role="img" aria-labelledby="t">'
            f'<title id="t">brainfly</title>'
            f'<g fill="{ink}">{"".join(fill[False])}</g><g fill="{eye}">{"".join(fill[True])}</g>'
            f'<path fill="{ink}" transform="translate({tx:.1f} {ty:.1f}) scale({k:.4f})" d="{path}"/></svg>')


if __name__ == "__main__":
    dots, word = halftone(), wordmark("brainfly")
    for theme in THEMES:
        path = OUT / f"logo-{theme}.svg"
        path.write_text(logo(theme, dots, word))
        print(f"{path} ({path.stat().st_size / 1e3:.0f} kB, {len(dots[0])} dots)")
