# Distribution — content stash for the planned subject page

Cut from the entanglement page (the architectures conflated *device-level
generation* with *link-architecture distribution* — different axes). Use this
as a starter section when the distribution subject is built. Already grounded
in the canonical taxonomy: **Jones et al. NJP 18 083015 (2016)** —
MeetInTheMiddle, SenderReceiver, MidpointSource.

The reading sequence is generation → distribution, with distribution
relying on the entanglement-swapping primitive introduced on the
entanglement page. The distribution subject answers: given a generated
matter-photon Bell pair (or photon-photon pair from a midpoint source),
how do you place one half of the pair at each of two distant nodes?

---

## Lede paragraph

```astro
<p>
  Generating an entangled pair is a local physics question. Distributing one —
  placing one half at each of two distant nodes — is a network-design question
  with several distinct architectural answers. Three architectures span
  essentially every quantum-network experiment to date, distinguished by where
  the entangled-photon source sits and who runs the Bell-state analyser
  <SourceNote id="jones-njp-2016" />.
</p>
```

## The three architectures (HTML, copy-pasteable)

```astro
<Grid min="18rem" gap="var(--space-3)">
  <article class="use-card">
    <h3>MeetInTheMiddle (MM)</h3>
    <p>
      Each of the two repeater nodes generates a matter-photon entangled pair
      locally and sends its photon toward the link midpoint. The two photons
      interfere on a beam splitter at a midpoint Bell-state analyser; a successful
      coincidence detection erases which-node-emitted-which information and
      heralds an entangled pair between the two matter qubits. The arrangement
      behind most current solid-state and ion-trap remote-entanglement
      experiments <SourceNote id="pompili-science-2021" />.
    </p>
  </article>

  <article class="use-card">
    <h3>SenderReceiver (SR)</h3>
    <p>
      The sender (Alice) generates a matter-photon pair and sends its photon all
      the way to the receiver (Bob), who interferes it with a photon entangled
      with his own memory and runs the Bell-state analyser at his end. Memory
      qubits are needed only at the receiver; the sender re-tries if a photon is
      lost. Simpler hardware than MM, but more sensitive to round-trip
      loss <SourceNote id="jones-njp-2016" />.
    </p>
  </article>

  <article class="use-card">
    <h3>MidpointSource (MS)</h3>
    <p>
      An entangled-pair source sits at the midpoint and emits one photon outward
      toward each of the two endpoints, where each is captured by a memory.
      Heralding here is on the source-side detection of the partner photon, which
      is more robust to photon loss than two-photon interference at distance —
      MS achieves higher rates than MM or SR when loss is high. SPDC is the
      natural device choice for the midpoint source
      <SourceNote id="jones-njp-2016" />.
    </p>
  </article>
</Grid>
```

## Closing paragraph

```astro
<p>
  The choice between architectures is a network-design decision rather than a
  physics one. MM dominates the current solid-state demos because hardware for
  near-coincident two-photon interference at telecom wavelengths is mature; MS
  becomes attractive at long links where one-way photon loss is the dominant
  impairment. The repeater subjects later in the series go into the rate-vs-loss
  trade-offs in detail.
</p>
```

## Citations referenced (already in `web/src/data/sources.yaml`)

- `jones-njp-2016` — Jones et al., *New J. Phys.* 18 083015 (2016). The canonical 3-architecture taxonomy.
- `pompili-science-2021` — Pompili et al., *Science* 372 259 (2021). Three-node SiV network demo, MM-style.

## Related content the distribution page should cover

Beyond the three architectures themselves:

- **Rate-vs-loss curves** comparing MM, SR, MS as a function of fibre length.
  Numbers from Jones 2016 §4 simulations.
- **MidpointSource scaling** when memory qubits are added — fast-clock vs
  link-latency regime trade-off.
- **The classical side-channel** required for each: heralding signal must
  travel from the BSA back to the memory-holding node before the memory's
  coherence runs out; for MM and MS this is one t_link, for SR it can be
  shorter since the receiver controls the BSA.
- **Multiplexing** — running multiple time-bins, frequency-bins, or memory
  qubits in parallel to amortise the round-trip waiting time. Multiplexing
  is independently composable with all three architectures.
- **End-to-end via swapping**: how single-link distribution chains into
  multi-hop reach via the swapping primitive (the bridge into the repeaters
  subject).
