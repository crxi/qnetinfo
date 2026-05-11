# CLAUDE.md — Quantum platforms spectrum chart

Single-file SVG infographic. `data.yaml` is the source of truth; `render.py` emits SVG (default) and optionally PNG/PDF via `cairosvg`.

## Run

```bash
cd qnetinfo/spectrum
python3 render.py                 # SVG → output/spectrum.svg
python3 render.py --format png    # also emits PNG (cairosvg)
python3 render.py --format pdf    # also emits PDF (cairosvg)
make all                          # SVG + PNG + PDF
```

The script uses `Path(__file__).parent` to find `data.yaml`, so always run from this directory (running from a parent cwd will fail to locate the data file).

## ALWAYS check the overlap detector

`render.py` runs `_warn_track_overlaps(layouts)` before emitting SVG. It does a **2D footprint intersection** check on every pair of platform boxes — not just same-track, since taller multi-line boxes on a lower track can intrude into the row above. If you see any line like:

```
warning: 'X' overlaps 'Y' by NxM px (shrink content, raise track, or rework layout)
```

you must fix it before treating the render as done. Visual inspection is not enough — small overlaps look like touching boxes at zoom-out. Check stderr after every render.

## Box widths are auto-fit, not uniform

Each platform box is sized to `widest_content_line + 2 * PAD_X` where `PAD_X = 10`. Pillow + Helvetica Bold gives real font metrics. **Do not** set a global `box_width` thinking it makes things look uniform — that re-introduces overflow problems. The "consistent buffer" is the 10 px padding each side, not the outer width.

If you must force a min width on one platform, use `min_width:` in its `data.yaml` entry (auto-fit kicks in only if content needs more).

## Layout: per-region greedy stacking, no fixed tracks

There's no per-platform `track:` field — every platform's vertical position is computed dynamically by `compute_stacking()` in `render.py`. The algorithm:

1. Each platform is bucketed into a region (= which freq-axis segment its x-center falls in). The microwave segment and the optical segment stack independently.
2. Within a region, sort by left x and greedily place each box on the lowest level whose existing boxes don't horizontally overlap with it.
3. Level-0 boxes sit at `tracks.bottom_y`. Each subsequent level's bottom = previous level's *tallest* box top minus `INTER_TRACK_GAP` (16 px). Inter-box gap is constant; level heights are natural.

This means:

- **Adding/removing a vendor line** on any box just reflows the stack — no manual track-renumbering.
- **3-line and 4-line boxes coexist cleanly**: each level is sized to its tallest box, so a 4-line box on level 0 doesn't force every other level to be 4-line tall.
- **The two regions don't have to align vertically** — the optical stack can have 5 levels while microwave has 3; the chart just adjusts.

`g.track_top` is computed *after* stacking from `min(box_top across all layouts)`, used downstream by the region shading and ITU strip. `g.track_bottom` is the data-supplied `tracks.bottom_y` (anchor point for level 0 box bottoms).

The `_warn_track_overlaps` 2D detector still runs as a safety net even though the greedy packer should make collisions impossible by construction.

## Categories: computers vs memories/sources

| `kind` value | Border style | Right-column in table |
|---|---|---|
| (none) | solid | no — left column |
| `memory` | dashed | yes |
| `source` | dashed | yes |

NV centre is dual-use but **stays as a computer** because Quantum Brilliance ships compute systems (Quoll). Don't conflate categories.

## Hidden platforms

Set `hidden: true` on a platform to make it table-only — no box on the chart. Used for entries like Cold-atom memory (Welinq's QDrive) where the vendor is already inside another box but deserves its own row in the memories table.

## Future/planned machines

In `flagship_machines` strings, wrap planned items in `*asterisks*`:

```yaml
superconducting: "IBM (Heron, *Nighthawk*, *Starling*, *Blue Jay*) · …"
```

`render.py` parses these into `<tspan font-weight="700">` fragments. Use this for unannounced or roadmap-only machine names; current/shipping machines stay plain.

## Vendor classification — verify before listing

Past mistakes that need to be avoided:

- **Welinq is NOT rare-earth** — they use Rb-87 cold atoms (D2 line at 780 nm). Belongs in Neutral atoms / Cold-atom memory, not the rare-earth box.
- **D-Wave is NOT a transmon** — flux/annealing qubits; doesn't belong in superconducting (gate-model) lists.
- **Quandela is photonic** — their QD is the source inside their photonic computer, not a separate QD product. Sparrow Quantum and Aegiq are the QD-component vendors.
- **NV vs SiV** — both diamond color centres but specialised:
  - NV → small-scale compute (Quantum Brilliance), thanks to room-temperature spin coherence.
  - SiV → memory/repeater nodes (Lightsynq, Lukin/Harvard), thanks to clean optical interface at mK.

If you're tempted to add a vendor in a new spot, search for them in `reference/books/ezratty/` or do a WebSearch first.

## Vendor names — alphabetical, no "Academic" wrapper

All vendor lists are sorted A–Z. Institutions (USTC, ANU, Caltech, Geneva) are listed as plain names alongside companies; there's no "Academic (...)" wrapper.

## Annotation arrows are level

The M-O transducer and QFC arrows share a single y level (`ann_y`). Both end at the C-band tip (1550 nm). When changing arrow geometry, remember `last_ann_y = ann_y + 16` (sublabel y), not `ann_y + i * 38` — that's leftover from when arrows were stacked.

## Layout constants live in `render.py`

Don't move them to `data.yaml`:

- `LINE_GAP`, `FIRST_BASELINE_DY`, `DESCENDER_PAD`, `INTER_TRACK_GAP` — text/box geometry
- `PAD_X` — internal box padding
- `BOX_H = box_height_for(n_lines)` — derived; varies per platform

Track heights are computed from these; `data.yaml` only specifies `tracks.count` and `tracks.top_y`.

## YAML float quirk

PyYAML's default loader follows YAML 1.1 and rejects `1.0e9` (no explicit `+`). `load_data()` patches `SafeLoader` with a more permissive resolver. Don't remove the patch.

## Don't auto-commit

Default behaviour is "wait for explicit commit instruction." Don't make a commit per change.

## Cross-references

Vetting sources used during development:
- `reference/books/ezratty/Ezratty2025_UQT_Part2_QuantumHardware_A4.pdf` — the master vendor reference.
- `reference/books/ezratty/Ezratty2025_UQT_Part4_CommunicationsSensing_A4.pdf` — for QKD, transducers, QFC.
- `reference/arXiv/Tittel.2501.06110_*.pdf` — quantum networks using rare-earth ions.
