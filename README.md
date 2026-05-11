# Quantum Network Infographics

A field guide to quantum networking — long-scrolling, visual-first pages covering the field from *what is a qubit* through entanglement distribution and protocol stacks to vendor landscape and TRL. New subjects land as the field evolves; existing ones get updated when the numbers do.

Target reader: a senior professional in government or enterprise — security architect, strategist, procurement officer, CISO — who needs to evaluate, plan, and procure quantum technology without first becoming a physicist. Every technical term is defined on first use.

## Subjects

In reading order — each subject builds vocabulary the next leans on, but readers can stop anywhere and have a coherent fragment.

**Foundations**
[qubits](/qubits) · [entanglement](/entanglement) · [teleportation](/teleportation) · [swapping](/swapping) · [distillation](/distillation) · [metrics](/metrics)

**Components**
[memories](/memories) · [transduction](/transduction) · [spectrum](/spectrum)

**Mechanisms**
[distribution](/distribution) · [repeaters](/repeaters) · [all-photonic](/all-photonic)

**Infrastructure**
[links](/links) · [protocols](/protocols)

**Applications & market**
[applications](/applications) · [maturity](/maturity) · [companies](/companies)

## Running it locally

```bash
cd web
npm install            # once
npm run dev            # http://localhost:4321
npm run build          # → web/dist/
```

For subjects that ship a print-ready static SVG/PDF (currently `spectrum`):

```bash
cd spectrum
make all               # SVG + PNG + PDF in output/
```

## Layout

```
qnetinfo/
├── web/                       # Shared Astro app — one route per subject
│   └── src/
│       ├── pages/             # <subject>.astro per route
│       ├── components/        # shared UI primitives
│       ├── layouts/           # the Infographic layout
│       ├── data/sources.yaml  # citation registry
│       └── lib/               # data loaders, geometry, citation helpers
└── <subject>/                 # per-subject directory (data.yaml, render.py, Makefile)
```

The web page and the Python pipeline both read the subject's `data.yaml` — no sync step.

## Conventions

- **Tone:** precise but plain, confident and direct, no marketing language. Active voice.
- **Citations:** every numeric claim, named mechanism, or non-obvious framing carries a `<SourceNote id="…" />` keyed to `web/src/data/sources.yaml`. Pages list the references they cite via the `references` prop on the `Infographic` layout, and a per-page References section renders only those entries.
- **Visuals:** static build-time SVG for charts; client-side JS reserved for animations and interactions. Topology diagrams use the [QuISP icon library](https://github.com/sfc-aqua/quisp/tree/master/Network%20icons) where applicable.
- See `CLAUDE.md` for the full set of conventions (primary references, prose style, technical accuracy rules).

## Adding a new subject

1. Create `<subject>/` (with `data.yaml` + optionally `render.py` and `Makefile` for static export).
2. Add `web/src/pages/<subject>.astro` composing the page from existing components.
3. Add an entry to `web/src/lib/subjects.ts` so it appears in the rail and on the landing page.

If the subject reuses existing chart geometry (broken-axis log frequency, greedy-stacked boxes), share `web/src/lib/`. If it needs different geometry, add `lib/<subject>/` rather than overloading the existing one.
