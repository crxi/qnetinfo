# CLAUDE.md — info workspace

Multi-subject infographics workspace. Each subject under `<subject>/` owns its own data + Python pipeline; the shared Astro app at `web/` renders one route per subject.

## Primary references — what to ground claims in

Six papers carry most of the load across the series. Default to these for technical claims, then go further afield only when specifically warranted.

| Reference | What it covers | When to cite |
|---|---|---|
| **Kumar et al. 2025 IJNDC** (`kumar-ijndc-2025`) | Series spine — fundamentals, network components, repeater generations, protocol stack, applications. 2025, the most current of the survey papers. | Default for any concept-level claim. |
| **Meddeb 2025 ComNet** (`meddeb-comnet-2025`) | Building-blocks state of R&D, per-platform memory TRL benchmarks (Table 5). | Hardware-status and TRL numbers. |
| **Purohit et al. 2023 arXiv** (`purohit-arxiv-2023`) | QTRL 1–9 framework for quantum technology readiness. | The maturity subject and any "how mature is this?" claim. |
| **Azuma et al. 2023 RMP** (`azuma-rmp-95`) | The canonical 1G / 2G / 3G repeater taxonomy; linear-optics BSM 50% ceiling. | Repeater and distillation subjects. |
| **Wehner et al. 2018 Science** (`wehner-science-2018`) | The 5-stage quantum-internet roadmap; what each stage requires. | Applications and vision-level framing. |
| **Cacciapuoti et al. 2020 IEEE T-Comm** (`cacciapuoti-ieeetc-2020`) | Communication-system block-diagram view; orthogonal quantum-vs-classical metrics. | Networking-architecture framing. |

**Note on RFC 9340 (Kozlowski et al., 2023, `kozlowski-rfc9340`):** the IRTF "Architectural Principles for a Quantum Internet" is a foundational document but two years old in a fast-moving field, and Kumar 2025 covers most of the same ground with newer numbers. Cite RFC 9340 specifically when referring to the formal link-layer-service definition by RFC number ("RFC 9340 formalises…"); prefer Kumar 2025 for general architecture claims.

**Other papers** (Sangouard 2011, Jones 2016, Forbes 2025, Knaut 2024, Pompili 2021, Yin 2017, Kwiat 1995, Muralidharan 2016, Duan 2001, Bell 1964, Wootters 1982, Bennett 1993/1996, Żukowski 1993, DiVincenzo 2000, etc.) are cited when specifically relevant — search `web/src/data/sources.yaml` for the full index.

## Structure conventions

- **Subject directory** (`<subject>/`): `data.yaml` is the single source of truth. `render.py` reads it and emits `output/<subject>.svg` (plus optional PNG / PDF via `cairosvg`). A `Makefile` wraps the common targets. Any subject-specific notes live in `<subject>/CLAUDE.md`.
- **Shared web app** (`web/`): one Astro project, one `npm install`, one tokens/CSS pipeline. Pages at `web/src/pages/<subject>.astro` import their subject's `data.yaml` via a relative path (`../../../<subject>/data.yaml`).
- **Citations** (`web/src/data/sources.yaml`): one shared file for now. Split per-subject only if the same key would mean different things in different subjects.

The deliberate split: each subject keeps autonomy (its own data, its own Python pipeline if it wants one), but the visual identity, theme, and component library are shared so re-skinning the workspace = editing `web/src/styles/tokens.css`.

## Independence from QNTaxo / QSTaxo / QStd

This workspace is **not** referenced from the taxonomy / standards projects (`QNTaxo/`, `QSTaxo/`, `QStd/`). Don't add cross-references in either direction — the projects ship and evolve on different cadences and the visual deliverables here are not meant to be embedded in the text reports.

## Tone and audience

Same audience as the rest of the workspace — senior professionals in government / enterprise who evaluate, plan, and procure quantum technology. Clear and direct, no marketing language, every technical term defined on first use.

### Prose style — write like Kumar / RFC 9340

Match the tone of the source literature: Kumar 2025 IJNDC, the IETF RFCs (e.g. RFC 9340), Wehner 2018 *Science*, Cacciapuoti 2020 IEEE T-Comm. Technical prose: state the claim and let it carry its own weight. No editorial scaffolding around it.

**Phrases to avoid** — these are AI tells that don't appear in the source literature:

- "That is the headline:" / "The headline is …"
- "Read in plain English:" / "In plain English,"
- "The punchline is …" / "The upshot is …" / "The takeaway is …"
- "The key insight is …" / "The bottom line is …"
- "What this means is …"
- "It's worth noting that …" / "It should be emphasized that …"
- "[X] is consequential." / "That framing is consequential."
- "Boils down to / comes down to"
- "Remarkably," / "Crucially," / "Importantly," / "Notably," / "Essentially," / "Fundamentally," — when used as throat-clearing rather than carrying real meaning
- "the field's canonical …" / "the canonical …" used as honorifics (use "standard" or just drop)

**What to do instead**: open the paragraph directly with the claim. If a paragraph would have started with "The headline is: X", just write "X." The bullet-list and table headlines already do the "what's important" work; prose doesn't need to repeat it.

**Application check**: when drafting any paragraph for an  workspace page, look at the first 4–8 words after writing. If they're framing-the-importance instead of stating-the-claim, cut them.

**Don't introspect on the artifact — focus on the subject.** A reader is on a quantum-networking page to learn about quantum networking, not about how the page was built. Cut anything that talks about the page itself rather than the physics: "Icon from the QuISP library", "This animation does not simulate X", "diagram inspired by Y figure", "as shown above", "we will now discuss". Source citations belong in the references list, not in figcaption bullets. The animation's omissions are interesting only when they materially mislead — in which case fix the animation or rewrite the relevant subject prose, don't add a meta-bullet. Test: if the sentence describes the page rather than the physics it's depicting, delete it.

## Technical accuracy — don't synthesise frameworks the literature already defines

When covering a technical subject (taxonomy, framework, definition, mechanism), use the structure given by the source literature rather than inventing one. If Jones et al. NJP 18 083015 (2016) defines three entanglement-distribution architectures (MeetInTheMiddle, SenderReceiver, MidpointSource), use those — don't reframe as "SPDC sources / light-matter heralded / matter-matter swap" because that's a different axis (device mechanism vs link architecture) and conflating the two produces silently-wrong claims. Same for Forbes RPP 88 086002 (2025) on heralded-vs-postselected, DiVincenzo 2000 on the five criteria, Kumar 2025 IJNDC on the protocol stack, and any other paper that names and counts the categories.

**Why:** synthesised frameworks risk being subtly wrong, conflating orthogonal axes, or missing edge cases the literature already worked out. The audience recognises literature-grounded framings; ad-hoc taxonomies make us look careless. A reader who later opens Jones or Forbes should see the same vocabulary they read here.

**How to apply:**

1. Before writing any "there are N kinds of X" claim, search the indexed library (`reference/`, via the MCP `search()` tool) for that topic. The MCP server exists for exactly this.
2. If a paper defines a structure ("three categories", "five criteria", "seven layers"), use that structure verbatim with citation. Quote the names the paper uses.
3. If multiple papers offer competing structures, pick one and note the choice — don't blend them into a new hybrid.
4. If no paper defines the structure cleanly, present the underlying primitives without imposing a synthetic taxonomy on them. A list of three concrete things is better than a forced "three families" framing.
5. Distinguish *device* (what hardware generates a state) from *architecture* (where it sits and who measures) — these are orthogonal axes that ad-hoc taxonomies tend to conflate.

**When the user asks "where did you get this from?":** answer honestly. If the framing is from a paper, name it. If it's a synthesis, say so and offer to ground it in a real source.

### Light synthesis vs defining a new concept

The "don't synthesise" rule has a calibration. Light synthesis — paraphrasing widely-known physics into one sentence to fit the surrounding prose flow — is fine and unavoidable. What requires a citation is the introduction of a *concept* the reader needs to take away: a name, a categorisation, a numerical claim, a protocol step, a fidelity formula, a TRL number. Those need to track a published source.

**Defaults**:

- For a section that names many platforms or concepts at one paragraph each, cite a survey at the section level (e.g. `ezratty-uqt-2025-p2` for the stationary-qubit grid) and add per-card / per-concept citations only where a specific number or claim is being made.
- For a section that introduces *one* concept (BSM, distillation, MidpointSource, etc.), cite the canonical paper at the point of introduction.
- For numerical claims (a fidelity threshold, a frequency, a wavelength), cite the source of the number.

**Consistent language across the series**. Once a term has been introduced and tied to a citation, use it the same way everywhere. If "ancilla photon" is defined on the entanglement page tied to Forbes RPP 2025, don't drift to "auxiliary photon" or "witness photon" later in the series. Pick one and stick with it.

**If a definition reads as too technical for a procurement-officer audience, choose a different one** — but ground it in a published source that uses that simpler framing. Don't invent your own simpler version. Examples of good simpler-but-cited framings: Aliro's qubits whitepaper for dual-rail vs single-rail (rather than the Fock-state formalism); Kumar 2025 for the network-resource framing of Bell pairs (rather than RFC 9340's link-layer text). Pick the source that matches the audience and cite it.

## Execution — parallelise with subagents on large parallelisable jobs

If the user gives you a job large enough that it can be split into independent units, **don't do it serially yourself**. Spawn parallel subagents (via the Agent tool) to do the units, with you acting as the orchestrator: brief each agent on a clear self-contained scope, run them in parallel where the units are genuinely independent, and watch their outputs as they come in. If an agent gets stuck, send it a `SendMessage` to redirect or stop it; if its output diverges from the rest, course-correct or re-spawn.

Concrete signal: if you find yourself thinking through three or more independent pages / files / tasks before any of them is written, **that's the moment to delegate**. Each unit of work should land in its own subagent context, so your main thread stays as the supervisor — reading agent outputs, integrating them, ensuring consistency, and fixing the seams.

**Examples that match this pattern:**

- Building three sibling pages from the same template (e.g. teleportation + swapping + distillation): one agent per page, in parallel, all briefed against the same conventions and reference page.
- Auditing a bunch of unrelated pages for a single style rule: one agent per page or one per group, parallel.
- Adding the same field to N data files: one agent for the whole set if the change is mechanical, or N agents if the per-file logic differs.

**Counter-examples — don't delegate**:

- A single page where the design has tightly coupled sub-decisions. Keep it in the main thread so the decisions stay coherent.
- Quick edits where spawning an agent costs more overhead than the edit itself.
- Anything where the output needs to land in a single file with shared state across changes — the subagents would conflict.

**Watch-and-stop responsibilities**: when subagents are running, your job is to track them. Each subagent reports back when done; if one stalls or its output is going wrong, intervene. The user's time should never be spent waiting on a stuck agent because the orchestrator was idle.

## Visual conventions

- **Colour as platform identity**: each subject's data file assigns a colour per subject-specific entity. Colours don't yet encode anything semantic (family, TRL, regime); when one of those becomes the right axis, the data file documents the mapping.
- **Capability chips on chart boxes** (spectrum specifically): three small letter chips at top-right of each box — `C` (compute), `M` (memory), `S` (source). Filled with the platform colour when supported, outlined-only when not. Replaces the older dashed-vs-solid border distinction.
- **Build-time SVG**: every chart is static SVG produced at build time. Client JS is reserved for interactions (hover, click-to-scroll, deep-links via `#platform-<id>`), not for measurement or geometry.

### Shared design concepts — reuse, don't reinvent

When the same physical thing or the same animation behaviour appears in more than one page, **draw it the same way every time and reuse the same JS recipe**. A reader who sees a PBS on the entanglement page should recognise the same glyph on the BSM page, the teleportation page, the repeaters page, etc. Inconsistent glyphs or inconsistent animation behaviour make the reader work harder for no reason, and they make it look like you didn't bother to check the existing pages. Look first; copy the existing approach; only invent when nothing fits.

**Container — every animated demo lives in a "demo card"**:

Every animated set-piece on a subject page is wrapped in a card with the same padding, background, border, and gap rhythm as the entanglement page's `.epr` figure. This makes the demos read as the same *kind* of element across the workspace, and stops them from floating loose against the surrounding prose. Recipe:

```css
.demo-card {  /* whatever class you use for your figure */
  margin: var(--space-4) 0;
  padding: var(--space-3) var(--space-4);
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: var(--radius);
  display: grid;
  gap: var(--space-3);
}
.demo-card svg { width: 100%; height: auto; display: block; margin: 0 auto; }
.demo-card figcaption {
  margin: 0;
  font-size: var(--text-sm);
  line-height: var(--leading-snug);
  color: var(--color-text-mute);
}
.demo-card figcaption strong { color: var(--color-text); }
```

First example: `.epr` on the entanglement page (the EPS demo). Every subsequent animated figure on the workspace must use the same wrapper styling — copy the class block above and rename the selector if needed. Do *not* leave an SVG demo floating directly in the prose without the card.

**Glyphs** — visual elements that must look the same everywhere:

- **PBS (polarising beam splitter)**: a small axis-aligned square with a single `\` diagonal line inside (top-left to bottom-right). Stroke = `var(--color-text)`, fill = `var(--color-bg)`, ~16–24 px on a side. First example: entanglement page `data-eps-pbs`.
- **BS (50:50 beam splitter)**: a thin filled plate (rectangle a few px thick × ~28 long), accent-coloured, oriented perpendicular to the bisector of the incoming beams. The plate convention follows the optics literature (Bouwmeester, Azuma RMP, Pan reviews). Distinct from the PBS shape on purpose.
- **Photon detector**: solid black D-shape with the **flat side facing the incoming beam**. Rotate the D so the flat edge is normal to the beam direction. Bouwmeester / Pan / Azuma figures all use this convention.
- **Photon glyph during travel**: fuzzy radial-gradient cloud (`radialGradient` with accent colour) for the *travelling, undefined-state* photon. A sharp horizontal/vertical bar (line element with `rotate(0)` for H, `rotate(90)` for V) replaces the cloud once the polarisation has been resolved (i.e., immediately after the PBS). The bar is **not** rotated to match the beam direction — the bar's own angle encodes the polarisation, full stop.

**Animation behaviours** — recipes to reuse verbatim:

- **Photons disappear at the detector + detector pulses**: when a photon glyph reaches a detector, *hide the photon entirely* and trigger a brief stroke-width pulse on the detector D (or its bounding rect). The first reference implementation lives in entanglement-page `pulse(side, outcome, now)` + `updateBorders(now)`: each fired detector gets `pulseEnd[key] = now + PULSE_DUR` (≈280–320 ms); the per-frame loop interpolates `stroke-width` from `1.5 + 3·t` back to `1.5` as the remaining time `t` decays. Never let the photon glyph "park" on top of the detector glyph after arrival — that reads as lazy and overlaps two design elements instead of handing off cleanly.
- **White-on-black trick for "current state-change"**: when an animation needs to point out the *latest* discrete event (active ket, active history digit, active outcome bit, …), invert it to white text on a black backdrop rect. Implementation pattern: a `<rect fill="var(--color-text)" opacity="0">` behind the text plus a CSS class (`.X-text--active { fill: var(--color-bg); font-weight: 700; }`); toggle the rect opacity and the class together. First example: entanglement-page `eps-ket--active` plus its `data-eps-ket-bg` backdrop rect. Reuse the exact same recipe wherever a similar "what just changed" callout is needed.
- **Reduced-motion fallback**: every animation honours `@media (prefers-reduced-motion: reduce)` (read via `matchMedia("(prefers-reduced-motion: reduce)").matches` in JS) and renders a meaningful end-state still frame plus a pre-populated history if applicable.

**Layout discipline**:

- **All beams at 90° wherever the layout allows**: animation diagrams read better when every intersection is orthogonal (or a clean 45° on a rotated diagram). If beams need to converge or split, do it at a single optical element, not at an arbitrary angle in empty space.
- **Place elements on a grid before drawing beams.** Pick a grid unit (e.g. 70 px) and assign every optical element to an integer grid point. Beam lines are drawn between grid centres; the element glyphs (BS plate, PBS square, detector D) are drawn axis-aligned on top, so the line passes through the element centre without bending or being shifted around the glyph. If your beam appears to dodge an element's bounding box, you placed the element off-grid.

**Process rule (zeroth, applies before any of the above)**: *before* coding a new animated figure, open the most-recently-shipped animated figure in the same workspace, scan its SVG + JS, and explicitly note which patterns you'll reuse. If the new figure needs a new pattern, justify in a comment why the existing recipe didn't fit. The cost of looking is minutes; the cost of shipping an inconsistent recipe is rework after the user notices.

If a future page needs a new shared glyph (mirror, wave plate, modulator, …) or a new animation pattern (sweep, fade-in chain, multi-photon coincidence flash, …), add it to this list with a screenshot or a code reference so the next page can copy it verbatim.

### Standardised network icons — QuISP icon library

For diagrams that depict quantum network *topologies* (nodes + links rather than per-platform anatomy), use the standardised icon set from the QuISP project at <https://github.com/sfc-aqua/quisp/tree/master/Network%20icons>. The library defines 12 node types with a consistent visual grammar — square borders for end nodes, distinct shapes for repeaters and support nodes — and ships SVG, PNG, and diagrams.net library formats. Free to use; derives from Van Meter et al.

The vocabulary:

- **End nodes** (square borders): `COMP` (computation), `MEAS` (measurement), `SNSR` (sensor), `MEM` (memory).
- **Repeater nodes**: `REP1G` (1G memory-based), `REP2G` (2G with QEC), `RTR` (router).
- **Support nodes**: `EPPS` (entangled-photon-pair source), `BSA` (Bell-state analyser), `ABSA` (advanced BSA), `RGSS` (repeater graph-state source), `OSW` (optical switch).

Reach for these whenever a page draws a network topology (the repeaters, distribution, links, applications subjects are obvious candidates). Adopting a shared icon vocabulary across the series — and matching the literature's conventions — beats inventing per-page glyphs. The QuISP source belongs in `sources.yaml` for completeness, but don't surface "Icon: from QuISP" in a figcaption bullet — the reader is here for the subject, not for credit on the glyphs.

## Per-subject CLAUDE.md files take precedence

Anything in `spectrum/CLAUDE.md` overrides anything written here. This file is the workspace-level baseline; each subject can specialise.

## Don't auto-commit

Default behaviour is "wait for explicit commit instruction." Don't make a commit per change.
