"""Higher-level visual components for quantum-network figures.

Each component takes the canvas + a small set of anchor coordinates and emits
the SVG for that motif. Components do not know about each other; figures
compose them.

Conventions
-----------
* x, y are top-left unless otherwise documented.
* `cx` and `cy` mean centre.
* Components return useful derived anchors (e.g. fibre-exit point) so the
  figure can hook subsequent geometry off them.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .svglib import Canvas


# ===========================================================================
# Node containers (silhouettes)
# ===========================================================================


@dataclass
class ChandelierAnchors:
    """Anchor points returned by `chandelier()`."""

    cx: float
    top_y: float
    bottom_y: float  # fibre-exit y at the chandelier base


def chandelier(
    canvas: Canvas,
    cx: float,
    top_y: float,
    bottom_y: float,
    top_width: float,
    bottom_width: float,
    *,
    stages: list[tuple[float, str]] | None = None,
    cls: str = "vessel-A",
    plate_cls: str = "plate",
    tag_cls: str = "plate-tag",
) -> ChandelierAnchors:
    """Draw a stepped-trapezoid dilution-fridge silhouette.

    The chandelier tapers linearly from `top_width` (at `top_y`) to
    `bottom_width` (at `bottom_y`). If `stages` is given, each entry is
    ``(plate_y, label)`` — a plate hairline is drawn at that y across the
    interior, and the label is placed inside the segment **below** the
    hairline (because each plate cools the stage below it).

    Returns ChandelierAnchors with the fibre-exit point at the base.
    """
    if stages is None:
        stages = []

    height = bottom_y - top_y
    # Convex stepped polygon. We pick N intermediate steps proportional to
    # stages so the silhouette visibly narrows at each plate.
    # Simpler approach: 4-step trapezoid with stages placed proportionally.
    # The path follows: top edge, stepped right side, bottom edge, stepped
    # left side.
    step_count = max(len(stages), 1)
    # Each step narrows by (top_width - bottom_width) / step_count
    narrow_per_step = (top_width - bottom_width) / step_count
    step_h = height / (step_count + 1)

    # Build the polygon
    pts: list[tuple[float, float]] = []
    # Top edge
    pts.append((cx - top_width / 2, top_y))
    pts.append((cx + top_width / 2, top_y))
    # Right side stepping down
    cur_w = top_width
    cur_y = top_y
    for i in range(step_count):
        next_y = cur_y + step_h
        # Vertical segment to next step
        pts.append((cx + cur_w / 2, next_y - 3))
        cur_w -= narrow_per_step
        # Step inward
        pts.append((cx + cur_w / 2, next_y))
        cur_y = next_y
    # Drop to bottom
    pts.append((cx + cur_w / 2, bottom_y))
    pts.append((cx - cur_w / 2, bottom_y))
    # Left side stepping UP — must mirror the right side. The right loop ended
    # at cur_y = last step y (67.5 px above bottom_y on the worked example),
    # so without resetting we'd kick off the left loop one step too high and
    # the *last* step on the left would land within a few px of top_y — an
    # extra spurious step right at the top corner.
    cur_y = bottom_y
    for i in range(step_count):
        next_y = cur_y - step_h
        pts.append((cx - cur_w / 2, next_y + 3))
        cur_w += narrow_per_step
        pts.append((cx - cur_w / 2, next_y))
        cur_y = next_y
    # Close to top-left
    pts.append((cx - top_width / 2, top_y))

    d = "M " + " L ".join(f"{x},{y}" for x, y in pts) + " Z"
    canvas.path(d, cls=cls, name="chandelier")

    # Plate hairlines + tags
    for plate_y, label in stages:
        # Plate width at this y, linearly interpolated.
        t = (plate_y - top_y) / height
        w = top_width + t * (bottom_width - top_width)
        canvas.line(
            cx - w / 2 + 2,
            plate_y,
            cx + w / 2 - 2,
            plate_y,
            cls=plate_cls,
            name=f"plate@{plate_y}",
        )
        # Tag sits just below the plate hairline (where the cold stage is),
        # tucked into the left edge of the vessel. Small + low-contrast so it
        # doesn't compete with the qubits / side labels.
        canvas.text(
            cx - w / 2 + 5,
            plate_y + 8,
            label,
            cls=tag_cls,
            anchor="start",
            font_size=7,
            name=f"plate-tag@{plate_y}",
        )

    return ChandelierAnchors(cx=cx, top_y=top_y, bottom_y=bottom_y)


@dataclass
class ChamberAnchors:
    cx: float
    top_y: float
    bottom_y: float  # fibre/UV-exit at the chamber base


def vacuum_chamber(
    canvas: Canvas,
    cx: float,
    top_y: float,
    bottom_y: float,
    width: float,
    *,
    cls: str = "vessel-B",
    viewport_cls: str = "viewport",
    viewport_rows: tuple[float, ...] = (),
    rx: float = 12,
) -> ChamberAnchors:
    """Capsule-style vacuum chamber with optional viewports on each side."""
    h = bottom_y - top_y
    canvas.rect(cx - width / 2, top_y, width, h, cls=cls, rx=rx, name="chamber")
    for vy in viewport_rows:
        canvas.circle(cx - width / 2, vy, 4, cls=viewport_cls, name=f"viewport-L@{vy}")
        canvas.circle(cx + width / 2, vy, 4, cls=viewport_cls, name=f"viewport-R@{vy}")
    return ChamberAnchors(cx=cx, top_y=top_y, bottom_y=bottom_y)


def node_outline(
    canvas: Canvas,
    cx: float,
    top_y: float,
    bottom_y: float,
    width: float,
    *,
    cls: str = "nodeB-bdy",
    rx: float = 8,
    name: str = "node-outline",
) -> None:
    """Dashed node-boundary rectangle (used to wrap chamber + QFC bench)."""
    h = bottom_y - top_y
    canvas.rect(cx - width / 2, top_y, width, h, cls=cls, rx=rx, name=name)


# ===========================================================================
# Qubit columns + SWAP marker
# ===========================================================================


def qubit_column(
    canvas: Canvas,
    cx: float,
    qubits: list[tuple[float, str, str, str]],
    *,
    side_anchor: str = "start",
    side_offset: float = 20,
    radius: float = 11,
) -> None:
    """Stack of qubits along a vertical line.

    Each qubit is ``(y, role_class, glyph, side_label)``:
        role_class - "data" | "comm" | "memory"
        glyph      - text drawn inside the circle (can contain <tspan>)
        side_label - text drawn to the side at `side_offset` from cx

    side_anchor decides which side the labels appear on ("start" = right of
    the column, "end" = left of the column).
    """
    for y, role_cls, glyph, side_label in qubits:
        canvas.circle(cx, y, radius, cls=role_cls, name=f"qubit@{cx},{y}")
        # text-anchor:middle centres the *whole* glyph including any
        # subscript tspan, which leaves the main letter biased to the left.
        # Nudge x rightwards so the main letter sits over the circle centre.
        tx = cx + 2.5 if "<tspan" in glyph else cx
        canvas.text(
            tx,
            y + 2,
            glyph,
            cls="qbit-in",
            font_size=9,
            anchor="middle",
            raw=True,
            name=f"qbit-in@{cx},{y}",
        )
        if side_label:
            lx = cx + side_offset if side_anchor == "start" else cx - side_offset
            canvas.text(
                lx,
                y + 3,
                side_label,
                cls="qbit-side",
                font_size=9,
                anchor=side_anchor,
                name=f"qbit-side@{cx},{y}",
            )


def swap_arrow(canvas: Canvas, cx: float, y_top: float, y_bottom: float) -> None:
    """Vertical dashed line with outward-pointing arrowheads — represents
    an on-chip SWAP gate between two adjacent qubits on the same column.
    """
    # Dashed line between the arrowheads
    canvas.line(cx, y_top + 4, cx, y_bottom - 4, cls="swap-link", name=f"swap@{cx}")
    # Up-arrow at top
    canvas.path(
        f"M {cx-4} {y_top+4} L {cx+4} {y_top+4} L {cx} {y_top-2} Z",
        style="fill:#9b87c4",
        name=f"swap-arr-up@{cx}",
    )
    # Down-arrow at bottom
    canvas.path(
        f"M {cx-4} {y_bottom-4} L {cx+4} {y_bottom-4} L {cx} {y_bottom+2} Z",
        style="fill:#9b87c4",
        name=f"swap-arr-down@{cx}",
    )


# ===========================================================================
# Transducer block (M2O / QFC) with stacked frequency-conversion text
# ===========================================================================


def transducer_block(
    canvas: Canvas,
    cx: float,
    top_y: float,
    width: float,
    height: float,
    *,
    title: str,
    line_in: str,
    line_out: str,
    cls: str,
) -> None:
    """Rectangle with title, input line, bidirectional diamond, output line."""
    canvas.rect(cx - width / 2, top_y, width, height, cls=cls, rx=3, name=title)
    canvas.text(cx, top_y + 12, title, cls="blk-ttl", font_size=10, name=f"{title}-title")
    canvas.text(cx, top_y + 24, line_in, cls="blk-line", font_size=8, name=f"{title}-in")
    # Elongated vertical diamond — conversion is bidirectional and the flow is
    # vertical (microwave ↔ telecom, UV ↔ telecom). Tall and narrow so it
    # reads as an axis indicator rather than a square widget.
    ax = cx
    ay = top_y + 35
    canvas.path(
        f"M {ax} {ay-7} L {ax+2.5} {ay} L {ax} {ay+7} L {ax-2.5} {ay} Z",
        style="fill:#6a7280",
        name=f"{title}-arrow",
    )
    # line_out sits just below the diamond. Caller picks a `height` tight to
    # this layout (about 55 px) so the box doesn't have dead space at the base.
    canvas.text(cx, ay + 14, line_out, cls="blk-line", font_size=8, name=f"{title}-out")


# ===========================================================================
# QR repeater (wide rectangle containing QFC | γ | L | C | R | γ | QFC)
# ===========================================================================


def qr_node(
    canvas: Canvas,
    cx: float,
    axis_y: float,
    *,
    label: str,
    width: float = 140,
    height: float = 36,
    qbit_gap: float = 22,
) -> dict[str, float]:
    """Repeater node with two comm qubits flanking a central memory.

    Returns a dict of anchor positions:
        left_edge, right_edge, l_x, c_x, r_x
    """
    rect_top = axis_y - height / 2
    canvas.rect(cx - width / 2, rect_top, width, height, cls="repeater", rx=4, name=label)
    canvas.text(cx, rect_top - 4, label, cls="lbl", font_size=10, name=f"{label}-title")

    l_x = cx - qbit_gap
    r_x = cx + qbit_gap

    n = label.split("-")[-1]
    # Layout left → right inside the QR rectangle:
    #   [ QFC ] —— (photon) | L (comm) | C (memory) | R (comm) | (photon) —— [ QFC ]
    # Left half — QFC then photon-then-L
    canvas.rect(l_x - 39, axis_y - 9, 18, 18, cls="qfc-blk", rx=2, name=f"{label}-qfc-L")
    canvas.text(l_x - 30, axis_y + 4, "QFC", cls="mini", font_size=8.5, name=f"{label}-qfc-L-txt")
    canvas.circle(l_x - 14, axis_y, 4, cls="photon", name=f"{label}-γ-L")
    canvas.circle(l_x, axis_y, 9, cls="comm", name=f"{label}-L")
    canvas.text(
        l_x + 1.5, axis_y + 1, f'L<tspan baseline-shift="sub" font-size="70%">{n}</tspan>',
        cls="qbit-in", font_size=9, raw=True, name=f"{label}-L-in",
    )
    # Centre memory
    canvas.circle(cx, axis_y, 9, cls="memory", name=f"{label}-C")
    canvas.text(
        cx + 1.5, axis_y + 1, f'C<tspan baseline-shift="sub" font-size="70%">{n}</tspan>',
        cls="qbit-in", font_size=9, raw=True, name=f"{label}-C-in",
    )
    # Right half — R-then-photon then QFC
    canvas.circle(r_x, axis_y, 9, cls="comm", name=f"{label}-R")
    canvas.text(
        r_x + 1.5, axis_y + 1, f'R<tspan baseline-shift="sub" font-size="70%">{n}</tspan>',
        cls="qbit-in", font_size=9, raw=True, name=f"{label}-R-in",
    )
    canvas.circle(r_x + 14, axis_y, 4, cls="photon", name=f"{label}-γ-R")
    canvas.rect(r_x + 21, axis_y - 9, 18, 18, cls="qfc-blk", rx=2, name=f"{label}-qfc-R")
    canvas.text(r_x + 30, axis_y + 4, "QFC", cls="mini", font_size=8.5, name=f"{label}-qfc-R-txt")

    # Internal fibre stubs: drawn LAST so they paint over the QFC's inner
    # border stroke. The stub starts exactly at the QFC's outer face (no
    # overlap into the QFC body) and ends at the comm qubit's outer edge.
    # Uses `fiber--stub` (full opacity, thicker) so the short ~12 px segment
    # stays visible — the main axis fibre is at 55 % opacity for distance
    # cueing, but that washes out the small internal stub.
    canvas.line(l_x - 21, axis_y, l_x - 9, axis_y, cls="fiber--stub", name=f"{label}-stub-L")
    canvas.line(r_x + 9, axis_y, r_x + 21, axis_y, cls="fiber--stub", name=f"{label}-stub-R")

    return dict(
        left_edge=cx - width / 2,
        right_edge=cx + width / 2,
        l_x=l_x,
        c_x=cx,
        r_x=r_x,
    )


# ===========================================================================
# Elbow fibre path
# ===========================================================================


def elbow_path(
    canvas: Canvas,
    start_x: float,
    start_y: float,
    end_x: float,
    end_y: float,
    *,
    radius: float = 35,
    cls: str = "fiber--quantum",
    name: str = "elbow",
) -> None:
    """L-shape fibre with a rounded corner.

    Goes vertical from (start_x, start_y) down to near end_y, then curves to
    horizontal and runs to end_x at end_y.
    """
    direction = 1 if end_x > start_x else -1
    corner_y = end_y - radius
    sweep_end_x = start_x + direction * radius
    d = (
        f"M {start_x} {start_y} "
        f"V {corner_y} "
        f"Q {start_x} {end_y} {sweep_end_x} {end_y} "
        f"H {end_x}"
    )
    canvas.path(d, cls=cls, name=name)


# ===========================================================================
# Midpoint BSM marker (QuISP BSA icon)
# ===========================================================================


def midpoint_bsm(
    canvas: Canvas,
    cx: float,
    cy: float,
    *,
    size: float = 26,
    label: str = "",
    label_pos: str = "above",
    symbol: str = "quisp-bsa-white",
) -> None:
    """Drop a QuISP BSA glyph centred on (cx, cy).

    `symbol`: which BSA variant — `quisp-bsa` (original, transparent bg) or
              `quisp-bsa-white` (rotated 180°, white-fill background).
    `label_pos`: "above" (default — works for icons on a horizontal axis),
                 "right" / "left" (works for icons on a vertical fibre).
    """
    canvas.use(
        f"#{symbol}",
        cx - size / 2,
        cy - size / 2,
        size,
        size,
        name=f"bsm-{label}",
    )
    if not label:
        return
    if label_pos == "above":
        canvas.text(
            cx, cy - size / 2 - 4, label, cls="lbl",
            font_size=10, anchor="middle",
            name=f"bsm-label-{label}",
        )
    elif label_pos == "right":
        canvas.text(
            cx + size / 2 + 8, cy + 3, label, cls="lbl",
            font_size=10, anchor="start",
            name=f"bsm-label-{label}",
        )
    elif label_pos == "left":
        canvas.text(
            cx - size / 2 - 8, cy + 3, label, cls="lbl",
            font_size=10, anchor="end",
            name=f"bsm-label-{label}",
        )


# ===========================================================================
# Hop bracket strip beneath the photonic axis
# ===========================================================================


def hop_brackets(
    canvas: Canvas,
    y: float,
    boundaries: list[float],
    labels: list[str],
    *,
    tick_h: float = 4,
) -> None:
    """Hop-segment brackets along a horizontal line."""
    for i in range(len(boundaries) - 1):
        x0, x1 = boundaries[i], boundaries[i + 1]
        canvas.line(x0, y, x1, y, cls="midline", name=f"hop-line-{i}")
        canvas.text(
            (x0 + x1) / 2,
            y + 16,
            labels[i],
            cls="hop",
            font_size=10.5,
            anchor="middle",
            name=f"hop-label-{i}",
        )
    for x in boundaries:
        canvas.line(
            x,
            y - tick_h,
            x,
            y + tick_h,
            style="stroke:#aab0ba;stroke-width:1",
            name=f"hop-tick@{x}",
        )


# ===========================================================================
# Legend row
# ===========================================================================


def legend_row(
    canvas: Canvas,
    base_y: float,
    items: list[dict],
    *,
    start_x: float = 30,
    end_x: float = 970,
    gap: float = 12,  # retained for API compatibility, unused
    font_size: float = 8.5,
) -> None:
    """Lay out legend items in equal-width slots between `start_x` and `end_x`.

    The old auto-spacing tried to estimate text width from the label length —
    which kept under-counting and letting labels eat into the next icon. This
    version assigns each item a fixed slot and draws icon+label flush-left in
    its slot, so the only constraint is that the slot is wide enough for the
    longest label. Pick `start_x` / `end_x` accordingly.

    Each item is one of:
        {"kind": "rect",    "cls": "...", "label": "..."}
        {"kind": "circle",  "cls": "...", "label": "...", "r": 6}
        {"kind": "photons", "sizes": [7,4,2], "label": "..."}
    """
    del gap  # legacy
    n = len(items)
    slot_w = (end_x - start_x) / n
    for i, it in enumerate(items):
        slot_x = start_x + slot_w * i
        if it["kind"] == "rect":
            canvas.rect(
                slot_x, base_y - 6, 18, 11, cls=it["cls"], rx=2,
                name=f"legend-{it['label']}",
            )
            canvas.text(
                slot_x + 24, base_y + 3, it["label"],
                cls="mini", font_size=font_size, anchor="start",
                name=f"legend-txt-{it['label']}",
            )
        elif it["kind"] == "circle":
            r = it.get("r", 6)
            canvas.circle(slot_x + r, base_y, r, cls=it["cls"], name=f"legend-{it['label']}")
            canvas.text(
                slot_x + r * 2 + 6, base_y + 3, it["label"],
                cls="mini", font_size=font_size, anchor="start",
                name=f"legend-txt-{it['label']}",
            )
        elif it["kind"] == "photons":
            cur = slot_x
            for r in it["sizes"]:
                canvas.circle(cur + r, base_y, r, cls="photon")
                cur += r * 2 + 1
            canvas.text(
                cur + 6, base_y + 3, it["label"],
                cls="mini", font_size=font_size, anchor="start",
                name=f"legend-txt-{it['label']}",
            )
