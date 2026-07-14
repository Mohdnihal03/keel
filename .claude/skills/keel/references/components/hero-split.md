# Hero · Split

**Use when** the message needs a claim *and* a companion — a product shot, a diagram, a code sample, a pull-figure. **Genre fit:** technical / editorial / playful.

## Structure
A **diptych**: one half text, one half media/other. Text half is left-measured (eyebrow, roman headline, one lede line, CTA row) — flush left, not centred inside its column. Media half fills its cell edge-to-edge. Asymmetric split (e.g. `1.1fr / 0.9fr`) reads less like a template than a clean 50/50. Down the page, **invert** the halves (`.split--rev`) so sections alternate sides and no single spine forms. The primary CTA is the action; a secondary text link sits beside it, not stacked. Collapse to stacked (text first) on narrow screens.

## Code
```html
<section class="split">
  <div class="split__text">
    <p class="split__eyebrow">Observability</p>
    <h1 class="split__head">Trace every request to the line that slowed it.</h1>
    <p class="split__lede">Spans, logs, and profiles on one timeline — no sampling.</p>
    <div class="split__cta">
      <a class="btn btn--primary" href="/start">Start tracing</a>
      <a class="split__link" href="/docs">Read the docs →</a>
    </div>
  </div>
  <div class="split__media"><!-- diagram / shot / code sample --></div>
</section>
```
```css
.split {
  display: grid; grid-template-columns: 1.1fr 0.9fr; align-items: center;
  gap: var(--space-xl); padding: var(--space-2xl) var(--space-lg);
}
.split--rev { grid-template-columns: 0.9fr 1.1fr; }
.split--rev .split__text  { order: 2; }         /* invert down the page */
.split--rev .split__media { order: 1; }
.split__text { max-width: 34rem; }
.split__eyebrow {                                 /* off-axis marker */
  font-family: var(--font-mono); font-size: var(--text-xs);
  letter-spacing: .12em; text-transform: uppercase; color: var(--color-accent); margin: 0;
}
.split__head {                                    /* mid-length copy → step down from ceiling */
  font-family: var(--font-display); font-weight: 700; font-style: normal;
  font-size: clamp(2.25rem, 1.4rem + 4.25vw, 4rem); line-height: 1.05;
  letter-spacing: -.02em; text-wrap: balance; color: var(--color-ink); margin: var(--space-xs) 0;
}
.split__lede { color: var(--color-ink-2); max-width: 48ch; }
.split__cta { display: flex; align-items: center; gap: var(--space-md); margin-top: var(--space-md); }
.split__link { color: var(--color-accent); text-decoration: none; white-space: nowrap; }
.split__media {
  background: var(--color-paper-2); border: 1px solid var(--color-rule);
  border-radius: var(--radius); min-height: 22rem; overflow: clip;
}
.btn:focus-visible, .split__link:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
@media (max-width: 720px) {
  .split, .split--rev { grid-template-columns: 1fr; }
  .split--rev .split__text, .split--rev .split__media { order: initial; }
}
```

## SSR / hydration note
Static server HTML, visible without JS — both halves render on the server. If the media half is a real image/video it is the LCP element; treat it per `../media-and-performance.md` (`next/image` with explicit dimensions + `priority`, or a `poster`ed video), never a lazy-loaded above-the-fold asset. Reserve the media cell's height (`min-height` or aspect-ratio box) so the reflow when it loads doesn't cause CLS. Any entrance stagger is ADDITIVE — content visible by default, never `opacity:0`-until-mount. See `../ssr-and-hydration.md`.

## Diversification knobs
- **Split ratio:** 1.1/0.9, 1.2/0.8, or a golden 62/38.
- **Media type:** framed diagram, bleed product shot, syntax-highlighted code, or a single big figure.
- **Invert cadence:** alternate every section vs. invert only once mid-page.
- **Divider:** gap only, a hairline `--color-rule` between halves, or an offset overlap.
