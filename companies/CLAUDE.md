# CLAUDE.md — Companies dossier directory

One YAML file per vendor. The `web/src/pages/companies/[slug].astro` page
renders each file as a per-vendor sub-page; `web/src/pages/companies.astro`
reads them all and groups by primary category.

Files are produced by the `quantum-company-research` skill (not yet shipped)
or written by hand. Either way, the schema below is the contract.

## Filename convention

`{slug}.yaml` where `slug` matches `^[a-z0-9-]+$`. Examples:

```
companies/ionq.yaml
companies/id-quantique.yaml
companies/psiquantum.yaml
```

The slug is the URL path component (`/companies/ionq`) and the schema `slug` field must match the filename.

## Schema

```yaml
slug: ionq
name: IonQ
categories: [qc]                  # one or more; index 0 is primary for grouping.
                                   # Allowed: qc, qkd, memory, network,
                                   # source-detect, sensing, software, enabling
hq: College Park, MD, USA
founded: 2015
status: public                     # public | private | acquired | defunct
parent: null                       # parent company slug if acquired

positioning: >
  One-line plain-English description of what the company makes and who it
  sells to. Goes at the top of the per-vendor page.

# Modality blocks. Each block is optional and present only if the company
# operates in that category.

modalities:
  qc:
    qubit_type: trapped-ion        # transmon | trapped-ion | neutral-atom |
                                   # photonic | nv | siv | spin-si | majorana
    physical_qubits_current: 36
    logical_qubits_current: 0      # 0 = NISQ-only
    one_q_fidelity: 0.99962
    two_q_fidelity: 0.9943
    coherence_t1_ms: null
    coherence_t2_ms: null
    ec_code: null                  # surface | color | repetition | gkp | ...
    connectivity: all-to-all
    gate_set: []
  qkd:
    protocol: [BB84, decoy-state]  # one or more
    rate_distance: ""              # one-line summary, e.g. "1 Mbps @ 50 km SMF"
    deployed_demos: []             # list of deployment notes with sources
  memory:
    platform: ""                   # rb-ensemble | trapped-ion | siv | ...
    storage_time_ms: null
    retrieval_efficiency: null     # 0–1
    fidelity: null                 # 0–1
    wavelength_nm: null
    mode_capacity: null            # how many modes stored in parallel
  network:
    role: ""                       # repeater | orchestrator | testbed | ...
    products: []
  source-detect:
    role: ""                       # source | detector | both
    detection_efficiency: null     # 0–1
    dark_count_hz: null
    jitter_ps: null
  sensing:
    target_quantity: ""            # magnetometry | gravimetry | clock | ...
    sensitivity: ""                # one-line summary with units
  software:
    products: []
  enabling:
    products: []

# Unified milestones list: ordered most-recent first. Each entry optionally
# tags a category so multi-category companies can be filtered. Source URL
# is required and source_type follows the priority hierarchy.

milestones:
  - date: 2024-09
    tag: qc                        # optional category filter
    headline: Forte Enterprise commercial launch, 36 algorithmic qubits
    source_url: https://ionq.com/...
    source_type: press             # paper | preprint | press | blog | conf-talk | filing

# Major shareholders / control. Ordered most-significant first. Skip
# this block for fully-private companies without disclosed positions;
# for SPAC / public / acquired entities the controlling holder is
# mandatory. Stake numbers are point-in-time and decay quickly — every
# row carries an `as_of` date and a `source_url` to the primary filing
# (10-K, 13D/G, SEC S-1, equivalent EU/UK/JP/CH filing) or vendor
# press release announcing the position.

shareholders:
  - holder: Honeywell
    stake_percent: 54          # null when only stake_class is known
    stake_class: controlling   # controlling | minority | strategic | founder
    as_of: 2024-12
    source_url: https://www.sec.gov/...
    note: ""                   # optional one-liner (e.g. "post-merger lockup")

# Key personnel. Roles are open-ended; include any of CEO, CTO, CFO,
# COO, Chief Scientist, Chief Quantum Officer, Founder, Principal
# Investigator. Every entry needs `since` (year or YYYY-MM) and a
# `source_url` — vendor's About page is acceptable here because
# leadership rosters are routinely refreshed.

key_personnel:
  - role: CEO
    name: Peter Chapman
    since: 2019
    source_url: https://ionq.com/team/peter-chapman
  - role: Founder & Chief Scientist
    name: Christopher Monroe
    since: 2015
    source_url: https://ionq.com/team/christopher-monroe

# Forward roadmap with target dates (best-effort; vendors are notorious for
# rolling these). Always cite a source.

roadmap:
  - target: 2025
    item: 64 algorithmic qubits (Tempo)
    source_url: ...
    tag: qc

current_flagship:
  name: Forte Enterprise
  generation: trapped-ion gen-3

# References — papers preferred. citation_key matches refs.bib when the paper
# is in the project library.
references:
  - kind: paper                    # paper | preprint | blog | press | conf-talk
    citation_key: chen-prl-2024    # null when not in refs.bib
    url: https://arxiv.org/abs/...
    note: 36 algorithmic qubits demo

# Fields the skill couldn't verify on the last run — rendered with a "—"
# and an "unverified" tag on the per-vendor page. Each entry is either
# a bare dotted path (treated as "unverified as of last_verified") or a
# `{ field, as_of, note }` object when a value IS present in the dossier
# but its provenance is weak. Use the second form when a value is the
# best-available guess and you want reviewers to know it's a guess.
partial:
  - modalities.qc.coherence_t1_ms                                  # bare path = no value
  - modalities.qc.coherence_t2_ms
  - field: modalities.qc.ec_code                                   # value present but unverified
    as_of: 2026-05-13
    note: announced as qLDPC in vendor press; no code-paper citation yet

last_verified: 2026-05-12
verification_method: web           # web | reference-library | mixed
```

## Source priority

When filling in fields, prefer sources in this order:

1. Peer-reviewed paper (cite via `citation_key` if in `refs.bib`).
2. arXiv preprint.
3. Vendor blog / technology page.
4. Press release.
5. Industry tracker (last resort; never sole source for a technical claim).

Wikipedia is acceptable only for company-history facts, never for numbers.

## Staleness

`last_verified` older than 3 months → the skill re-runs and updates.

## When in doubt — `partial`

If a required field cannot be verified to a source-priority-1-or-2 reference,
add it to `partial:` rather than hallucinating a value. The Astro page
renders partial fields with a visible "—" so reviewers see the gap.
