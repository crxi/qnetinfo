/**
 * Workspace-level subject registry. Single source of truth for the
 * SiteNav rail and the landing page card grid; both read this same
 * array so they never disagree.
 *
 * Reading order is foundations → components → mechanisms →
 * infrastructure → applications → market. Each subject builds
 * vocabulary used by the next; readers can stop anywhere and have a
 * coherent fragment.
 *
 * Adding a new subject:
 *   1. Create <subject>/{data.yaml, render.py, Makefile} for the
 *      print-ready static export pipeline.
 *   2. Add web/src/pages/<subject>.astro for the web page.
 *   3. Flip the row's status from "planned" to "shipped" here.
 */

export type SubjectStatus = "shipped" | "planned";

/**
 * Tier groups subjects by their role in the reading sequence.
 *   A — Foundations (qubits, entanglement, …)
 *   B — Components (memories, transduction, the spectrum cheat-sheet)
 *   C — Mechanisms (distillation, distribution, repeaters)
 *   D — Infrastructure (links, protocols)
 *   E — Applications & market
 */
export type SubjectTier = "A" | "B" | "C" | "D" | "E";

export const TIER_LABEL: Record<SubjectTier, string> = {
  A: "Foundations",
  B: "Components",
  C: "Mechanisms",
  D: "Infrastructure",
  E: "Applications & market",
};

export interface Subject {
  slug: string;
  title: string;
  /** Short label used in the SiteNav rail; falls back to title when absent. */
  navLabel?: string;
  /** Card blurb on the landing page; can be longer than navLabel. */
  blurb: string;
  status: SubjectStatus;
  tier: SubjectTier;
}

export const SUBJECTS: Subject[] = [
  {
    slug: "qubits",
    title: "What is a qubit",
    navLabel: "Qubits",
    blurb: "Modalities, encodings, what 0 and 1 actually mean in each platform — the vocabulary every other subject builds on.",
    status: "shipped",
    tier: "A",
  },
  {
    slug: "entanglement",
    title: "Entanglement and Bell pairs",
    navLabel: "Entanglement",
    blurb: "What makes the network-relevant correlations stronger than classical correlation, and why Bell pairs are the unit of currency.",
    status: "shipped",
    tier: "A",
  },
  {
    slug: "teleportation",
    title: "Quantum teleportation — sending an unknown qubit through a Bell pair",
    navLabel: "Teleportation",
    blurb: "How a shared Bell pair plus two classical bits transfers an unknown qubit. The fundamental quantum-internet primitive — the network's replacement for sending a copy.",
    status: "shipped",
    tier: "A",
  },
  {
    slug: "swapping",
    title: "Entanglement swapping — extending a Bell pair across an extra hop",
    navLabel: "Swapping",
    blurb: "Bell-state measurement at a relay station joins two Bell pairs into one across a longer distance, without the endpoints ever interacting. The primitive every memory-based repeater is built on.",
    status: "shipped",
    tier: "A",
  },
  {
    slug: "distillation",
    title: "Entanglement distillation — trading throughput for fidelity",
    navLabel: "Distillation",
    blurb: "Why fidelity matters for distributed protocols, and the BBPSSW pattern of trading two low-fidelity pairs for one higher-fidelity pair.",
    status: "shipped",
    tier: "A",
  },
  {
    slug: "metrics",
    title: "Loss, decoherence, fidelity — the metrics that bound a quantum link",
    navLabel: "Metrics",
    blurb: "The engineering vocabulary the rest of the series leans on, grounded in concrete channel and process numbers — fibre 0.20 dB/km, hollow-core 0.091 dB/km, free-space, satellite, transduction.",
    status: "shipped",
    tier: "A",
  },
  {
    slug: "memories",
    title: "Quantum memories — what stores a qubit, and for how long",
    navLabel: "Memories",
    blurb: "Storage time, fidelity, and TRL across atomic ensembles, trapped ions, solid-state defects, quantum dots, photonic, and superconducting memories.",
    status: "shipped",
    tier: "B",
  },
  {
    slug: "transduction",
    title: "Transduction and quantum frequency conversion",
    navLabel: "Transduction",
    blurb: "Bridging microwave qubits to telecom and visible-band photons to telecom — the two open problems on the frequency axis.",
    status: "shipped",
    tier: "B",
  },
  {
    slug: "spectrum",
    title: "Quantum platforms on the electromagnetic spectrum",
    navLabel: "Spectrum",
    blurb: "Eleven qubit, memory, and photon-source platforms placed by transition frequency, with vendor flagship machines and the C-band fibre window.",
    status: "shipped",
    tier: "B",
  },
  {
    slug: "distribution",
    title: "Entanglement distribution — the network's core service",
    navLabel: "Distribution",
    blurb: "Multi-hop swap chains, why MidpointSource wins on long links, and the layered service contract of an entanglement-delivery network.",
    status: "shipped",
    tier: "C",
  },
  {
    slug: "repeaters",
    title: "Quantum repeaters — 1G / 2G / 3G families",
    navLabel: "Repeaters",
    blurb: "Three architectural families compared side by side, including the 50 % linear-optics BSM ceiling and the boosted-BSM workarounds.",
    status: "shipped",
    tier: "C",
  },
  {
    slug: "all-photonic",
    title: "All-photonic quantum repeaters",
    navLabel: "All-photonic QR",
    blurb: "Tree- and graph-state distribution as an alternative to memory-based repeaters — Azuma 2015 and the architectures it inspired.",
    status: "shipped",
    tier: "C",
  },
  {
    slug: "links",
    title: "Links — fibre, hollow-core fibre, free-space, satellite",
    navLabel: "Links",
    blurb: "Where each link medium wins on loss, latency, and reach. ITU fibre bands, hollow-core attenuation, FSO atmospheric turbulence, and Micius-style satellite links.",
    status: "shipped",
    tier: "D",
  },
  {
    slug: "protocols",
    title: "Protocol stack and RFC 9340 architectural principles",
    navLabel: "Protocols",
    blurb: "Wehner / Van Meter / RFC 9340 stacks side by side, the link-layer service primitive, and how naming and addressing are deliberately deferred.",
    status: "shipped",
    tier: "D",
  },
  {
    slug: "applications",
    title: "What the quantum internet is for",
    navLabel: "Applications",
    blurb: "QKD, distributed quantum computing, blind quantum computing, networked sensing, and clock synchronisation — what each needs from the network.",
    status: "shipped",
    tier: "E",
  },
  {
    slug: "maturity",
    title: "TRL landscape — per-platform, per-capability",
    navLabel: "Maturity",
    blurb: "Purohit's QTRL framework over Meddeb's per-platform memory-TRL benchmark, with capability-aware ratings rather than one-size-fits-all numbers.",
    status: "shipped",
    tier: "E",
  },
  {
    slug: "companies",
    title: "Vendors — landscape and long-term tracking",
    navLabel: "Companies",
    blurb: "A growing per-vendor index with milestone timelines, public roadmaps, and links to canonical announcements. Maintained as the field evolves.",
    status: "shipped",
    tier: "E",
  },
];

export const SHIPPED_SUBJECTS = SUBJECTS.filter((s) => s.status === "shipped");
export const PLANNED_SUBJECTS = SUBJECTS.filter((s) => s.status === "planned");
