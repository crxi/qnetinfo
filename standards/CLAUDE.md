# standards/ — schema authority

One YAML per standards body. The `/standards` Astro page reads every
`*.yaml` here at build time and renders a filterable / sortable table.

## File layout

```
standards/
  itu-t.yaml      ITU-T (Y.3800-Y.3834 QKDN; Y.Sup75/89/98; Y.TR-QN-UC;
                  X.1702-X.1717; X.1811; Q.4160-Q.4164; FG-QIT4N)
  etsi.yaml       ETSI (ISG QKD GS- and GR- series; TR/TS; TC QT)
  ietf.yaml       IETF / IRTF QIRG (RFC 9340, RFC 9583, active drafts)
  ieee.yaml       IEEE (P7130, P3120 series; relevant approved standards)
  iso-iec.yaml    ISO/IEC JTC1 (SC27 PQC; new Joint TC on Quantum Tech)
  gsma.yaml       GSMA (IG.11, IG.12, IG.14, IG.18, IG.19, Intelligence reports)
  imda.yaml       Singapore IMDA QKDN regulatory specs
  bsi.yaml        German BSI quantum-relevant docs
  usgov.yaml      US national strategies / blueprints (DOE, NQI)
```

A new body gets a new YAML file. The filename slug must match the
`body.id` inside the file.

## Schema

```yaml
body:
  id: itu-t                        # lowercase slug, matches filename
  name: International Telecommunication Union – Telecommunication Standardization Sector
  short_name: ITU-T
  url: https://www.itu.int/itu-t
  scope: |
    UN-treaty-backed standards body for telecommunication. Develops
    Recommendations (binding for member states) plus Technical Reports
    and Supplements (informational). Quantum-network work lives across
    SG13 (architecture), SG17 (security), SG11 (signalling), and the
    FG-QIT4N focus group.
  notes: ""                        # optional structural note

standards:
  - id: Y.3800                     # canonical short identifier
    title: Overview on networks supporting quantum key distribution
    type: recommendation           # see enum below
    date: 2019-10                  # YYYY or YYYY-MM
    group: SG13                    # SG / ISG / TC / WG identifier
    tags: [qkdn]                   # array — see tag enum below
    status: in-force               # see status enum below
    url: https://www.itu.int/rec/T-REC-Y.3800/en
    pdf: reference/standards/ITU/Y.3800.pdf   # relative to qnetinfo root
    summary: >
      Foundational recommendation of the Y.3800-Y.3999 QKDN series.
      Layered model, basic functions for QKD networks.
    note: ""                       # optional editorial note
```

## Enums

`type`: `recommendation | technical-report | supplement | draft | charter | guideline | regulatory`

`tags` (one or more):
- `qkd-protocol` — BB84, E91, MDI-QKD, TF-QKD, DI-QKD, decoy-state, the
  cryptographic-protocol level.
- `qkdn` — QKD networks (key relay, trusted nodes, key management, SDN
  control for QKDN).
- `qnet` — entanglement-based quantum networking beyond QKD (repeaters,
  swapping, distributed compute, sensing-over-quantum). Apply only when
  the document substantively addresses entanglement-based networking.
- `security` — security frameworks, threat models, certifications.
- `sensing` — quantum-sensing standards.
- `qrng` — quantum random-number generation.
- `crypto-meta` — PQC / hybrid PQC-QKD.
- `policy` — government strategy/blueprint documents, regulatory
  frameworks (not technical Recommendations).

`status`: `in-force | superseded | draft | planned | informational`

## Source policy

Strict order, most authoritative first:

1. The standard document itself (PDF in `reference/standards/` or the
   body's web portal).
2. The body's official metadata page (e.g. ITU-T's T-REC handle, IETF
   datatracker, ETSI portal).
3. The body's press release announcing the work item or approval.
4. Third-party industry coverage — last resort.

When in doubt about what a document covers, read its scope / summary
page (typically pp. 1-3 of the PDF). Do not infer tags from titles
alone.

## Updating

- Add a new in-force standard: append to the `standards` array in the
  appropriate body YAML.
- A new revision supersedes an old one: keep the old entry, set its
  `status: superseded`, add the new entry as `in-force`. Keeping the
  historical entry is deliberate — the page is a longitudinal record.
- A new standards body emerges (e.g. ETSI TC QT formalises into ISGs):
  create a new YAML file.

The page on the site rebuilds from these YAMLs at build time; no manual
sync.

## Cross-coupling with other workspaces

- The `_private/LOI-Q*-draft.md` answers cite the same standards. When
  a document changes status (e.g. a draft becomes an RFC), update both
  the YAML here and any LOI draft that cites it.
- The `companies/*.yaml` dossiers may reference standards bodies under
  `key_personnel` (e.g. a person who chairs ETSI TC QT). No automated
  cross-link; manual consistency.
