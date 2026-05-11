# Metrics — content stash for the planned subject page

This is content cut from the entanglement page (the "network primitive" section
ended up too long, and the comparison table is more naturally a metrics topic).
Use it as a starting block when the metrics subject is built. Two pieces here:

1. **Quantum-vs-classical headline-metrics table** — a side-by-side framing of
   how the two regimes differ on throughput, quality, loss, latency, etc.
2. **Per-cell sources** — RFC 9340, Cacciapuoti 2020 IEEE T-Comm., Wehner 2018
   *Science*, ITU-T G.652.D.

The section opens with a one-sentence framing and then the table. Astro markup
below is copy-pasteable into the future `web/src/pages/metrics.astro`.

---

## Lede paragraph (HTML, with citations)

```astro
<p>
  A quantum network's headline metrics differ from a classical one's, and the
  differences are forced by physics rather than by engineering choice
  <SourceNote id="cacciapuoti-ieeetc-2020" /><SourceNote id="wehner-science-2018" />:
</p>
```

## Comparison table (HTML, with citation in the loss-recovery row)

```astro
<table class="qvc">
  <thead>
    <tr>
      <th scope="col">Concern</th>
      <th scope="col">Classical network</th>
      <th scope="col">Quantum network</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Unit of service</th>
      <td data-label="Classical">Bit (or packet) delivered from sender to receiver</td>
      <td data-label="Quantum">Bell pair delivered between two named endpoints; the application then
        teleports, distils, or measures</td>
    </tr>
    <tr>
      <th scope="row">Headline throughput</th>
      <td data-label="Classical">Bits per second on the link</td>
      <td data-label="Quantum">Entanglement-generation rate — Bell pairs per second</td>
    </tr>
    <tr>
      <th scope="row">Quality metric</th>
      <td data-label="Classical">Bit-error rate / signal-to-noise ratio</td>
      <td data-label="Quantum">End-to-end fidelity (closeness of the delivered pair to the ideal Bell
        state); below a protocol-specific threshold, downstream uses stop working</td>
    </tr>
    <tr>
      <th scope="row">Information source</th>
      <td data-label="Classical">Can be read without altering it; can be copied and re-transmitted on
        corruption</td>
      <td data-label="Quantum">Cannot be read without altering it (measurement collapse) and cannot be
        copied (no-cloning) — so it cannot be re-transmitted</td>
    </tr>
    <tr>
      <th scope="row">Loss recovery</th>
      <td data-label="Classical">Amplify-and-forward repeaters; retransmit on packet loss</td>
      <td data-label="Quantum">No optical amplification possible (no-cloning forbids it); lost photons
        cannot be recovered, only re-attempted from the source. Quantum repeaters
        use entanglement swapping + distillation, not amplification</td>
    </tr>
    <tr>
      <th scope="row">Reach without intermediaries</th>
      <td data-label="Classical">Thousands of km via amplify-and-forward chains</td>
      <td data-label="Quantum">~100–200 km in standard fibre, set by 0.20 dB/km attenuation
        <SourceNote id="itu-g-652-d" />; longer reach requires repeaters or
        satellite links</td>
    </tr>
    <tr>
      <th scope="row">Latency budget</th>
      <td data-label="Classical">Soft preference; long latency degrades user experience</td>
      <td data-label="Quantum">Hard budget — Bell pairs decohere in memory, so generation-to-use time
        competes with memory coherence and the classical-correction round-trip</td>
    </tr>
    <tr>
      <th scope="row">Auxiliary classical channel</th>
      <td data-label="Classical">None required</td>
      <td data-label="Quantum">Always required — teleportation and entanglement swapping both consume 2
        bits of classical communication per Bell pair to complete the protocol</td>
    </tr>
  </tbody>
</table>
```

## Table CSS (lift into the metrics page's `<style>` block)

```css
/* Quantum-vs-classical comparison table.
   Three columns: concern (row header) | classical | quantum. Row
   headers are bold and aligned top so the eye reads down the
   column of concerns; cell text is aligned top so multi-line
   entries don't drift mid-row. */
.qvc {
  inline-size: 100%;
  border-collapse: collapse;
  font-size: var(--text-sm);
  line-height: var(--leading-snug);
}
.qvc thead th {
  text-align: start;
  padding: var(--space-2) var(--space-3);
  border-block-end: 2px solid var(--color-rule);
  color: var(--color-text);
  font-weight: 600;
}
.qvc tbody th,
.qvc tbody td {
  padding: var(--space-2) var(--space-3);
  vertical-align: top;
  border-block-end: 1px solid var(--color-rule);
}
.qvc tbody th {
  text-align: start;
  font-weight: 600;
  color: var(--color-text);
  inline-size: 14ch;
}
.qvc tbody td { color: var(--color-text-mute); }
.qvc tbody tr:last-child th,
.qvc tbody tr:last-child td { border-block-end: 0; }

/* Stack the table on narrow screens so the three columns don't
   squeeze unreadably. Each row becomes a card-like block with
   the row header on top and two stacked value rows. */
@media (max-width: 50rem) {
  .qvc, .qvc thead, .qvc tbody, .qvc tr, .qvc th, .qvc td {
    display: block;
    inline-size: auto;
  }
  .qvc thead { display: none; }
  .qvc tbody tr {
    padding-block: var(--space-2);
    border-block-end: 1px solid var(--color-rule);
  }
  .qvc tbody tr:last-child { border-block-end: 0; }
  .qvc tbody th,
  .qvc tbody td { border-block-end: 0; padding-inline: 0; }
  .qvc tbody td::before {
    content: attr(data-label);
    display: block;
    font-size: var(--text-xs, 0.7rem);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--color-text-mute);
    margin-block-end: 2px;
  }
}
```

## Closing prose (after the table)

```astro
<p>
  The framing comes from Cacciapuoti et al.'s communication-system view of the
  quantum internet, which models classical and quantum networks against the same
  block diagram and lets the differences fall out where the physics demands them
  (no-cloning forces a classical side-channel; measurement collapse forces a
  fidelity metric instead of an SNR; loss cannot be recovered the classical way and
  forces repeaters of a different kind) <SourceNote id="cacciapuoti-ieeetc-2020" />.
</p>
```

## Citations referenced

These are already in `web/src/data/sources.yaml`:

- `cacciapuoti-ieeetc-2020` — IEEE Trans. Comm. 68 (2020). Communication-system view, Table II in source.
- `kozlowski-rfc9340` — RFC 9340 (2023). Bell-pair-as-link-layer-service.
- `wehner-science-2018` — Wehner et al., *Science* 362 eaam9288 (2018).
- `itu-g-652-d` — ITU-T G.652.D. The 0.20 dB/km @ 1550 nm reference.
