"""Generate images/4hop-topology.svg.

Run from the repo root::

    python -m scripts.diagrams.topology_4hop

Layout: one source of truth for every named coordinate. Editing a constant
here propagates everywhere — M_n midpoints, 50 km labels, hop brackets, and
elbow path endpoints all derive from the QR centres.
"""

from __future__ import annotations

from pathlib import Path

from .svglib import Canvas, render_png
from . import quisp_icons as Q
from . import components as C


# ---------------------------------------------------------------------------
# LAYOUT — every figure-wide anchor lives here.
# ---------------------------------------------------------------------------

# Overall canvas
W, H = 1000, 580

# Node A (dilution fridge): column x, vessel extent
NODE_A_CX = 80
NODE_A_TOP = 20
NODE_A_BOT = 290
CHAND_TOP_W = 140
CHAND_BOT_W = 110

# Node B (UHV trap + room-temp QFC bench)
NODE_B_CX = 920
NODE_B_OUTLINE_TOP = 12
NODE_B_OUTLINE_BOT = 294
CHAMBER_TOP = 58
CHAMBER_BOT = 196
CHAMBER_W = 100

# Qubit column geometry (shared y-positions in both nodes)
Y_DQ = 78  # nudged up from 88 to give more room between DQ and MQ
Y_MQ = 118
Y_CQ = 165
Y_PHOTON_NEAR_CQ = 184
Y_FIBER_LINK_FROM = 176  # CQ bottom edge
Y_TRANSDUCER_TOP = 229  # centres the 55-tall block in the chandelier bottom
Y_TRANSDUCER_BOT = 284  # box (between last narrowing ~y=222 and base y=290)
TRANSDUCER_W = 80
TRANSDUCER_H = 55

# Horizontal photonic axis
AXIS_Y = 430

# Repeater positions. With the L-shape elbow adding ~177 px of non-horizontal
# distance to hops 1 and 4, the QR centres are chosen so all four hops have
# the same visual path length (~300 px).
QR_CENTRES = (200, 500, 800)
QR_WIDTH = 140
QBIT_GAP = 22  # spacing between L/C/R centres in each QR
# Outer face of the QFC block, measured from the QR centre. Inside qr_node the
# QFC rect sits at l_x - 39 = cx - QBIT_GAP - 39 = cx - 61. So a fibre that
# wants to *touch* the QFC's outer face should terminate at cx ± QR_QFC_FACE.
QR_QFC_FACE = QBIT_GAP + 39  # = 61

# M1/M4 sit at the visual midpoint between each node's fibre exit and the axis
Y_M1_M4 = 360

# Matter-photon interface — y where the conceptual line between the matter
# qubits (DQ, MQ, repeater memory C) and the photonic / network subsystem
# (CQ, transducers, photonic axis, repeater comm L/R, BSMs) sits. Midway
# between MQ (y=118) and CQ (y=165). Above this line: long-lived matter
# qubits holding compute state and stored entanglement. Below: the
# short-coherence photon-facing layer that gets reset every entanglement
# attempt, plus everything optical. NOT to be confused with an LOCC
# boundary — LOCC is a protocol class, not a spatial region. See the LOCC
# callout on /entanglement for that distinction.
INTERFACE_Y = 142

# Hop bracket strip
HOP_BRACKET_Y = 498

# Legend
LEGEND_Y = 550


# ---------------------------------------------------------------------------
# STYLES — single CSS block referenced by every component.
# ---------------------------------------------------------------------------

CSS = """
  .vessel-A   { fill: #fff8ef; stroke: #b8783c; stroke-width: 1.4; }
  .vessel-B   { fill: #f3f8fd; stroke: #5a83b3; stroke-width: 1.4; }
  .nodeB-bdy  { fill: none; stroke: #5a83b3; stroke-width: 1.1; stroke-dasharray: 5 3; opacity: 0.7; }
  .repeater   { fill: #ecfaf2; stroke: #2f8a55; stroke-width: 1.4; }
  .m2o-blk    { fill: #fdeacf; stroke: #b8783c; stroke-width: 1.3; }
  .qfc-blk    { fill: #e2eef9; stroke: #5a83b3; stroke-width: 1.3; }
  .viewport   { fill: #f3f8fd; stroke: #5a83b3; stroke-width: 1.2; }
  .cold-zone  { fill: #d6e8f6; fill-opacity: 0.55; stroke: #2c5d8f; stroke-width: 1.0; stroke-dasharray: 4 2; }
  .cold-tag   { font: 700 7.5px sans-serif; fill: #2c5d8f; text-anchor: middle; }
  .plate      { stroke: #b8783c; stroke-width: 0.7; opacity: 0.55; }

  .data       { fill: #f29453; stroke: #8a3f0e; stroke-width: 1; }
  .comm       { fill: #22c55e; stroke: #15803d; stroke-width: 1; }
  .memory     { fill: #9b87c4; stroke: #6048a3; stroke-width: 1; }
  .photon     { fill: #2f6fd6; stroke: #1a4a99; stroke-width: 0.8; }

  .node-ttl   { font: 700 13px sans-serif; fill: #1a1f2a; text-anchor: middle; }
  .node-sub   { font: 9.5px sans-serif; fill: #4a4f57; text-anchor: middle; }
  .lbl        { font: 600 11px sans-serif; fill: #1a1f2a; text-anchor: middle; }
  .blk-ttl    { font: 700 10px sans-serif; fill: #1a1f2a; text-anchor: middle; }
  .blk-line   { font: 8px sans-serif; fill: #3a4150; text-anchor: middle; }
  .plate-tag  { font: 7.5px sans-serif; fill: #8a5a30; text-anchor: start; opacity: 0.9; }
  .mini       { font: 8.5px sans-serif; fill: #5a6472; text-anchor: middle; }
  .qbit-in    { font: 700 9px sans-serif; fill: #ffffff; text-anchor: middle; dominant-baseline: middle; }
  .qbit-side  { font: 600 9px sans-serif; fill: #1a1f2a; }
  .km         { font: 600 9px sans-serif; fill: #5a6472; text-anchor: middle; }
  .hop        { font: 700 10.5px sans-serif; fill: #1a3458; text-anchor: middle; }
  .midline    { stroke: #aab0ba; stroke-width: 1; fill: none; stroke-dasharray: 3 2; }
  .swap-link  { stroke: #9b87c4; stroke-width: 1.2; fill: none; stroke-dasharray: 3 2; }

  .plane-matter    { fill: #f7f4fb; }
  .plane-photonic  { fill: #eff5fc; }
  .interface-line  { stroke: #6a7280; stroke-width: 0.9; fill: none; stroke-dasharray: 4 3; opacity: 0.55; }
  .plane-tag       { font: 700 9px sans-serif; fill: #6a7280; opacity: 0.75; }

  .fiber           { stroke: #5a6472; stroke-width: 1.4; fill: none; stroke-linecap: round; stroke-linejoin: round; }
  .fiber--quantum  { stroke: #2f6fd6; stroke-width: 1.6; fill: none; stroke-linecap: round; stroke-linejoin: round; opacity: 0.55; }
  .fiber--stub     { stroke: #2f6fd6; stroke-width: 1.8; fill: none; stroke-linecap: butt; }
  .fiber--uv       { stroke: #8c6ad6; stroke-width: 1.3; fill: none; stroke-linecap: round; stroke-dasharray: 4 2; opacity: 0.7; }
"""


# ---------------------------------------------------------------------------
# Figure assembly
# ---------------------------------------------------------------------------


def build() -> Canvas:
    cv = Canvas(
        width=W,
        height=H,
        title=(
            "4-hop heterogeneous quantum network — transmon QPU + M2O at Node A "
            "(in a dilution fridge), 171-Yb+ trap + QFC bench at Node B, three SiV "
            "repeaters with internal QFCs along the photonic chain, midpoint BSM at "
            "M1-M4 using the QuISP BSA glyph."
        ),
        css=CSS,
    )
    Q.register(cv, "quisp-bsa-white")

    _background(cv)  # MUST come first — paints behind everything else
    _node_A(cv)
    _node_B(cv)
    _photonic_chain(cv)
    _midpoints(cv)
    _hop_brackets(cv)
    _legend(cv)
    return cv


# -- Background: two-tone shading + LOCC line ------------------------------


def _background(cv: Canvas) -> None:
    """Two-tone background marking the matter-photon interface.

    Upper band (matter qubits — DQ + MQ at the nodes, C inside each QR) is
    pale lavender. Lower band (photonic / network subsystem — CQ, the
    transducers, the photonic axis, the comm qubits in each QR, BSMs) is
    pale azure. The dashed line at INTERFACE_Y marks where matter qubits
    hand entanglement off to flying photons.

    This is NOT an LOCC boundary — LOCC is a protocol class (not a region),
    and both bands run LOCC at various points (CQ during entanglement
    generation, DQ+MQ during teleportation). See /entanglement#locc.

    Inside each QR the central memory C sits geometrically in the lower
    band but conceptually belongs with the matter plane — that's a quirk
    of collapsing the QR's L-C-R triple onto a horizontal axis; the split
    is fundamentally a *qubit-role* one, not a y-coordinate one.
    """
    # Stop the lower band just above the hop-bracket strip, so the bracket
    # ticks read cleanly against white.
    bottom_y = HOP_BRACKET_Y - 12
    cv.rect(0, 0, W, INTERFACE_Y, cls="plane-matter", name="bg-matter")
    cv.rect(0, INTERFACE_Y, W, bottom_y - INTERFACE_Y, cls="plane-photonic", name="bg-photonic")
    # Dashed boundary, full-width, behind the foreground elements.
    cv.line(0, INTERFACE_Y, W, INTERFACE_Y, cls="interface-line", name="interface-line")
    # Plane labels — centred horizontally, straddling the interface line in
    # the clear band between Node A and Node B so they don't fight either node.
    cv.text(
        W / 2, INTERFACE_Y - 8, "matter qubits (compute + memory)",
        cls="plane-tag", anchor="middle", font_size=9,
        name="plane-tag-matter",
    )
    cv.text(
        W / 2, INTERFACE_Y + 14, "photonic interface + network",
        cls="plane-tag", anchor="middle", font_size=9,
        name="plane-tag-photonic",
    )


# -- Node A -----------------------------------------------------------------


def _node_A(cv: Canvas) -> None:
    # Chandelier silhouette
    C.chandelier(
        cv,
        cx=NODE_A_CX,
        top_y=NODE_A_TOP,
        bottom_y=NODE_A_BOT,
        top_width=CHAND_TOP_W,
        bottom_width=CHAND_BOT_W,
        stages=[(60, "50 K"), (140, "4 K"), (210, "15 mK")],
    )
    # Title
    cv.text(NODE_A_CX, 38, "Node A", cls="node-ttl", font_size=13, name="A-title")
    cv.text(NODE_A_CX, 52, "transmon QPU + M2O", cls="node-sub", font_size=9.5, name="A-sub")

    # Qubit column. Side labels go to the LEFT of Node A's column (anchor=end),
    # leaving the inner-facing side free for a future "entanglement wriggly
    # line" between MQ-A and MQ-B that should not be obscured by labels.
    C.qubit_column(
        cv,
        cx=NODE_A_CX,
        side_anchor="end",
        qubits=[
            (Y_DQ, "data", "ψ", "DQ-A"),
            (Y_MQ, "memory", "M", "MQ-A"),
            (Y_CQ, "comm", "C", "CQ-A"),
        ],
    )

    # SWAP between MQ and CQ
    C.swap_arrow(cv, NODE_A_CX, Y_MQ + 11, Y_CQ - 11)

    # CQ-A microwave link to M2O
    cv.line(
        NODE_A_CX, Y_FIBER_LINK_FROM, NODE_A_CX, Y_TRANSDUCER_TOP,
        cls="fiber", name="A-mw-link",
    )
    cv.circle(NODE_A_CX, Y_PHOTON_NEAR_CQ, 7, cls="photon", name="A-mw-photon")

    # M2O block
    C.transducer_block(
        cv,
        cx=NODE_A_CX,
        top_y=Y_TRANSDUCER_TOP,
        width=TRANSDUCER_W,
        height=TRANSDUCER_H,
        title="M2O",
        line_in="60 mm · 5 GHz",         # wavelength · frequency (matches QFC convention)
        line_out="1550 nm · 193 THz",
        cls="m2o-blk",
    )

    # Elbow fibre to QR-1 left edge
    C.elbow_path(
        cv,
        start_x=NODE_A_CX,
        start_y=Y_TRANSDUCER_BOT,
        end_x=QR_CENTRES[0] - QR_QFC_FACE,  # touches QR-1 left QFC outer face
        end_y=AXIS_Y,
        radius=35,
        name="A-elbow",
    )


# -- Node B -----------------------------------------------------------------


def _node_B(cv: Canvas) -> None:
    # Dashed Node B outline wraps chamber + QFC bench
    C.node_outline(
        cv,
        cx=NODE_B_CX,
        top_y=NODE_B_OUTLINE_TOP,
        bottom_y=NODE_B_OUTLINE_BOT,
        width=124,
    )
    cv.text(NODE_B_CX, 28, "Node B", cls="node-ttl", font_size=13, name="B-title")
    cv.text(NODE_B_CX, 40, "¹⁷¹Yb⁺ trap + QFC bench", cls="node-sub", font_size=9.5, name="B-sub")

    # UHV chamber (capsule) with side viewports above/below the qubit column
    C.vacuum_chamber(
        cv,
        cx=NODE_B_CX,
        top_y=CHAMBER_TOP,
        bottom_y=CHAMBER_BOT,
        width=CHAMBER_W,
        viewport_rows=(78, 186),
    )
    # Cold region — wraps just the qubit cluster *tightly* (3-px buffer
    # each side of the radius-11 circles). The temperature tag lives
    # OUTSIDE the zone on the inner-facing side, rotated vertically, so
    # the zone itself can be narrow.
    cold_x = NODE_B_CX - 14   # 906 — just outside qubit right edge (931 minus circle, wait)
    cold_y = 64               # 3 px above DQ-B top (67)
    cold_w = 28               # right edge at 934 — 3 px outside qubit right edge (931)
    cold_h = 115              # bottom at y=179 — 3 px below CQ-B bottom (176)
    cv.rect(cold_x, cold_y, cold_w, cold_h, cls="cold-zone", rx=8, name="B-cold-zone")
    # Temperature tag — rotated 90° CCW, placed on the LEFT side of the
    # cold zone (outside it). Side labels are on Node B's right, so the
    # left side is free for the vertical tag. Reads bottom-to-top.
    tag_x, tag_y = cold_x - 8, (cold_y + cold_y + cold_h) / 2  # 898, 121.5
    cv.add(
        f'<text x="{tag_x}" y="{tag_y}" class="cold-tag" '
        f'transform="rotate(-90 {tag_x} {tag_y})" '
        f'style="text-anchor:middle">~mK · Yb⁺ ions</text>',
        kind="text",
        name="B-cold-tag",
    )
    # UHV · 300 K — flush against the LEFT wall of the Node B outline, in the
    # band between the chamber and the QFC bench. Kept off the central x-axis
    # so the dashed UV photon link from CQ-B down to the QFC stays unblocked.
    cv.text(
        NODE_B_CX - 62 + 4,  # node-outline width is 124, so left wall = cx-62
        (CHAMBER_BOT + Y_TRANSDUCER_TOP) / 2 + 3,
        "UHV · 300 K",
        cls="plate-tag",
        anchor="start",
        font_size=7.5,
        style="fill:#2a5288",
        name="B-uhv-tag",
    )

    # Qubit column. Side labels go to the RIGHT of Node B's column
    # (anchor=start) — mirror of Node A. Inner-facing sides of both nodes
    # are kept free for a future entanglement wriggly-line between MQs.
    C.qubit_column(
        cv,
        cx=NODE_B_CX,
        side_anchor="start",
        qubits=[
            (Y_DQ, "data", "ψ", "DQ-B"),
            (Y_MQ, "memory", "M", "MQ-B"),
            (Y_CQ, "comm", "C", "CQ-B"),
        ],
    )
    C.swap_arrow(cv, NODE_B_CX, Y_MQ + 11, Y_CQ - 11)

    # UV link from CQ-B (via chamber viewport) to the QFC bench below
    cv.line(
        NODE_B_CX, Y_FIBER_LINK_FROM, NODE_B_CX, Y_TRANSDUCER_TOP,
        cls="fiber--uv", name="B-uv-link",
    )
    # UV photon sits adjacent to CQ-B (matches CQ-A microwave photon spacing).
    cv.circle(NODE_B_CX, 179, 3, cls="photon", name="B-uv-photon")

    # QFC block on the room-temperature bench
    C.transducer_block(
        cv,
        cx=NODE_B_CX,
        top_y=Y_TRANSDUCER_TOP,
        width=TRANSDUCER_W,
        height=TRANSDUCER_H,
        title="QFC",
        line_in="369 nm · 812 THz",
        line_out="1550 nm · 193 THz",
        cls="qfc-blk",
    )
    # ("300 K bench" tag removed — already covered by "UHV · 300 K" on the
    # chamber and the "QFC bench" subtitle below "Node B".)

    # Elbow fibre from QFC bottom to QR-3 right edge
    C.elbow_path(
        cv,
        start_x=NODE_B_CX,
        start_y=Y_TRANSDUCER_BOT,
        end_x=QR_CENTRES[-1] + QR_QFC_FACE,  # touches QR-3 right QFC outer face
        end_y=AXIS_Y,
        radius=35,
        name="B-elbow",
    )


# -- QR chain ---------------------------------------------------------------


def _photonic_chain(cv: Canvas) -> None:
    # Telecom fibre segments — each segment runs from the OUTER FACE of one
    # QR's QFC to the outer face of the next QR's QFC. Drawing the fibre in
    # discrete segments (rather than one line through the QRs) is what lets a
    # future revision animate a photon moving along each segment.
    for i in range(len(QR_CENTRES) - 1):
        x0 = QR_CENTRES[i] + QR_QFC_FACE      # right QFC outer face of QR_i
        x1 = QR_CENTRES[i + 1] - QR_QFC_FACE  # left QFC outer face of QR_{i+1}
        cv.line(x0, AXIS_Y, x1, AXIS_Y, cls="fiber--quantum", name=f"axis-fibre-{i}")

    for cx in QR_CENTRES:
        C.qr_node(
            cv,
            cx=cx,
            axis_y=AXIS_Y,
            label=f"QR-{QR_CENTRES.index(cx) + 1}",
            width=QR_WIDTH,
            qbit_gap=QBIT_GAP,
        )


def _midpoints(cv: Canvas) -> None:
    """M1 / M4 on the elbow verticals; M2 / M3 between the QR chain pairs.

    On the verticals, the BSA icon sits on top of the fibre — so its label
    goes to the side, not above. On the horizontal axis the label goes
    above; the fibre passes through the icon centre without text collision.
    """
    BSM_SIZE = 24
    # M1 — Node A side, label points outward (left, toward Node A)
    C.midpoint_bsm(cv, NODE_A_CX, Y_M1_M4, size=BSM_SIZE, label="M1", label_pos="left")
    # M4 — Node B side, label points outward (right, toward Node B)
    C.midpoint_bsm(cv, NODE_B_CX, Y_M1_M4, size=BSM_SIZE, label="M4", label_pos="right")
    # M2 between QR-1 R₁ and QR-2 L₂
    r1 = QR_CENTRES[0] + QBIT_GAP
    l2 = QR_CENTRES[1] - QBIT_GAP
    m2_x = (r1 + l2) / 2
    C.midpoint_bsm(cv, m2_x, AXIS_Y, size=BSM_SIZE, label="M2", label_pos="above")
    # M3 between QR-2 R₂ and QR-3 L₃
    r2 = QR_CENTRES[1] + QBIT_GAP
    l3 = QR_CENTRES[2] - QBIT_GAP
    m3_x = (r2 + l3) / 2
    C.midpoint_bsm(cv, m3_x, AXIS_Y, size=BSM_SIZE, label="M3", label_pos="above")

    # SNSPD temperature tags — every BSM station is shorthand for "fibre
    # bench at 300 K + SNSPD chip in a He cryostat at ~2 K". Knaut Nature
    # 629.573 uses Photon Spot SNSPDs; ETSI GR QKD 003 §5 lists 0.12–2.3 K
    # sensor temps for NbN/WSi nanowires at 1550 nm.
    for x, y in [(NODE_A_CX, Y_M1_M4 + 22),
                 (NODE_B_CX, Y_M1_M4 + 22),
                 (m2_x, AXIS_Y + 20),
                 (m3_x, AXIS_Y + 20)]:
        cv.text(x, y, "SNSPDs ~2 K", cls="cold-tag", anchor="middle", font_size=6.5,
                name=f"bsm-temp@{x},{y}")


# Kept around in case a future revision wants per-segment distance tags,
# but currently unused — the hop brackets below already encode "100 km" each.
def _kilometre_labels_unused(cv: Canvas) -> None:
    """Eight '50 km' tags around the four hops."""
    # Upper-leg (vertical) labels on each elbow — outside the chandelier/Node B
    cv.text(
        NODE_A_CX - 30, (NODE_A_BOT + Y_M1_M4) / 2, "50 km",
        cls="km", font_size=9, anchor="middle",
        style="writing-mode:vertical-rl;",  # rotates without transform headaches
        name="km-A-upper",
    )
    cv.text(
        NODE_B_CX + 30, (NODE_A_BOT + Y_M1_M4) / 2, "50 km",
        cls="km", font_size=9, anchor="middle",
        style="writing-mode:vertical-rl;",
        name="km-B-upper",
    )
    # Lower-leg label sits below the horizontal section of the elbow
    cv.text(
        (QR_CENTRES[0] - QR_WIDTH / 2 + NODE_A_CX) / 2 + 30, AXIS_Y + 18, "50 km",
        cls="km", font_size=9, anchor="middle", name="km-A-lower",
    )
    cv.text(
        (QR_CENTRES[-1] + QR_WIDTH / 2 + NODE_B_CX) / 2 - 30, AXIS_Y + 18, "50 km",
        cls="km", font_size=9, anchor="middle", name="km-B-lower",
    )

    # Horizontal-segment labels: midpoints of each (R_n -> M_x -> L_{n+1}) half
    r1 = QR_CENTRES[0] + QBIT_GAP
    l2 = QR_CENTRES[1] - QBIT_GAP
    m2 = (r1 + l2) / 2
    r2 = QR_CENTRES[1] + QBIT_GAP
    l3 = QR_CENTRES[2] - QBIT_GAP
    m3 = (r2 + l3) / 2
    for x, name in [((r1 + m2) / 2, "h21"), ((m2 + l2) / 2, "h22"),
                    ((r2 + m3) / 2, "h31"), ((m3 + l3) / 2, "h32")]:
        cv.text(x, AXIS_Y + 48, "50 km", cls="km", font_size=9, anchor="middle", name=f"km-{name}")


def _hop_brackets(cv: Canvas) -> None:
    bounds = [NODE_A_CX, QR_CENTRES[0], QR_CENTRES[1], QR_CENTRES[2], NODE_B_CX]
    labels = [f"Hop {i+1} — 100 km" for i in range(4)]
    C.hop_brackets(cv, HOP_BRACKET_Y, bounds, labels)


def _legend(cv: Canvas) -> None:
    C.legend_row(
        cv,
        base_y=LEGEND_Y,
        items=[
            {"kind": "rect",    "cls": "repeater", "label": "SiV⁻ Repeater (QR)"},
            {"kind": "circle",  "cls": "data",     "label": "Data Qubit (DQ)"},
            {"kind": "circle",  "cls": "comm",     "label": "Comm Qubit (CQ)"},
            {"kind": "circle",  "cls": "memory",   "label": "Memory Qubit (MQ)"},
            {"kind": "photons", "sizes": [7, 4, 2], "label": "Photon (size = λ)"},
        ],
    )
    # BSM glyph isn't a rect/circle/photons - render manually next to first item
    # Actually let the QuISP BSA appear in the figure itself; readers see it
    # at M1/M2/M3/M4 with labels already attached.


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def main(out: Path | None = None, preview_png: Path | None = None) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    out = out or (repo_root / "images" / "4hop-topology.svg")
    cv = build()
    svg = cv.to_svg()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg)
    print(f"wrote {out}")

    # Mirror to web/public/images/ so the Astro app picks it up. Keeping the
    # canonical output at repo-root/images/ (matches the workspace convention)
    # and the web copy in sync avoids manual copy steps.
    web_out = repo_root / "web" / "public" / "images" / out.name
    if web_out.parent.exists():
        web_out.write_text(svg)
        print(f"wrote {web_out}")

    overlaps = cv.check_text_overlaps(pad=0.5)
    if overlaps:
        print(f"WARN: {len(overlaps)} text overlaps:")
        for a, b in overlaps[:10]:
            print(f"  - {a.name!r:30s} ↔ {b.name!r}")

    if preview_png:
        render_png(str(out), str(preview_png), output_width=1600)
        print(f"preview PNG: {preview_png}")


if __name__ == "__main__":
    import sys

    preview = Path("/tmp/4hop.png") if "--preview" in sys.argv else None
    main(preview_png=preview)
