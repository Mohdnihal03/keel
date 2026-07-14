# Hero · Stat-led

**Use when** a single number *is* the argument — uptime, throughput, dollars saved, users. **Genre fit:** technical / editorial.

## Structure
Two-track lead: an oversized **figure** and a **worded headline** that finishes its sentence. A bare number alone is banned — the words carry the claim, the figure carries the weight. Compose off-axis: figure left (or spanning two grid columns), headline and one-line qualifier flush to the same left rule, CTA pushed to the opposite edge or dropped a row down — never stacked on one centred spine. The CTA links to the proof (the page/report the number comes from), not a generic "Get started". Keep the whole block left-measured (`max-width` ~70ch), not full-bleed.

## Code
```html
<section class="hero-stat">
  <p class="hero-stat__fig">99.98<span class="hero-stat__unit">%</span></p>
  <h1 class="hero-stat__head">uptime across 14 regions, measured every 30 seconds.</h1>
  <p class="hero-stat__note">Rolling 90-day mean. No maintenance windows excluded.</p>
  <a class="hero-stat__cta" href="/status">See the live status page →</a>
</section>
```
```css
.hero-stat {
  display: grid; gap: var(--space-sm);
  grid-template-columns: minmax(0, max-content) minmax(0, 1fr);
  align-items: end; max-width: 72ch;
  padding: var(--space-2xl) var(--space-lg) var(--space-3xl);
}
.hero-stat__fig {                        /* the figure — outlier face, heavy */
  grid-row: span 2; font-family: var(--font-display); font-weight: 800;
  font-style: normal; font-size: clamp(4rem, 2rem + 12vw, 9rem);
  line-height: .85; letter-spacing: -.04em; color: var(--color-ink);
  font-variant-numeric: tabular-nums;
}
.hero-stat__unit { color: var(--color-accent); font-size: .5em; }  /* accent ≤5% */
.hero-stat__head {                       /* short claim → full display */
  align-self: end; font-family: var(--font-display); font-weight: 700;
  font-style: normal; font-size: var(--text-2xl); line-height: 1.1;
  text-wrap: balance; color: var(--color-ink); margin: 0;
}
.hero-stat__note { grid-column: 2; color: var(--color-muted); font-size: var(--text-sm); }
.hero-stat__cta {                        /* off-axis: opposite edge */
  grid-column: 2; justify-self: end; color: var(--color-accent);
  font-family: var(--font-mono); text-decoration: none;
}
.hero-stat__cta:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 3px; }
@media (max-width: 640px) {
  .hero-stat { grid-template-columns: 1fr; }
  .hero-stat__note, .hero-stat__cta { grid-column: 1; justify-self: start; }
}
```

## SSR / hydration note
Static server HTML, visible without JS. The figure is a **server-stamped string**, not a client `count-up` from 0 — an animated counter that starts at 0 renders `0` during SSR and reflows on mount (CLS + wrong LCP text). If you must animate it, render the final value in the HTML and only tween on mount behind a `mounted` flag with `font-variant-numeric: tabular-nums` reserving width. Any entrance is ADDITIVE — never `opacity:0`-until-mount on this above-the-fold block. See `../ssr-and-hydration.md` and `../motion.md`.

## Diversification knobs
- **Figure placement:** left column vs. baseline-aligned inline with the first headline word.
- **Unit treatment:** accent superscript, mono suffix, or set in the worded headline instead.
- **Proof CTA target:** status page, methodology note, or a downloadable report.
- **Second stat:** none, or a muted supporting figure on the opposite corner (keep one dominant).
