# Nav · Rail

**Use when** the layout is editorial or portfolio and a persistent vertical spine reads better than a horizontal bar — content sits to its right. **Genre fit:** editorial, atmospheric, playful.

## Structure
A fixed (or sticky) vertical rail pinned to the left edge: wordmark at the top, a short stack of links below it, an optional action or meta line pinned to the bottom. Content is offset right by the rail's width. Divider language: a single `--color-rule` vertical hairline on the rail's right edge, or a `--color-paper-2` surface shift — not both. Mobile: the rail is too wide for narrow screens, so below ~48rem it reflows to a horizontal top bar (or collapses behind a toggle); do NOT keep a full-height rail on a phone.

## Code
```html
<div class="rail-layout">
  <nav class="rail" aria-label="Primary">
    <a class="rail__mark" href="/">Margin<br>Notes</a>
    <ul class="rail__links">
      <li><a href="/work">Work</a></li>
      <li><a href="/essays">Essays</a></li>
      <li><a href="/about">About</a></li>
    </ul>
    <a class="rail__foot" href="/contact">Contact<span aria-hidden="true"> →</span></a>
  </nav>
  <main class="rail-main"><!-- page content --></main>
</div>

<style>
.rail-layout { display: grid; grid-template-columns: 14rem 1fr; }
.rail {
  position: sticky; top: 0; align-self: start;
  height: 100vh; display: flex; flex-direction: column;
  gap: var(--space-8); padding: var(--space-6);
  background: var(--color-paper); border-right: 1px solid var(--color-rule);
  font-family: var(--font-body);
}
.rail__mark {
  font-family: var(--font-display); font-weight: 700; line-height: 1.05;
  font-size: var(--text-xl); color: var(--color-ink); text-decoration: none;
}
.rail__links { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: var(--space-3); }
.rail__links a, .rail__foot {
  font-size: var(--text-sm); color: var(--color-ink-2);
  text-decoration: none; white-space: nowrap;
  transition: color var(--dur-fast) var(--ease-out);
}
.rail__links a:hover, .rail__foot:hover { color: var(--color-accent); }
.rail__foot { margin-top: auto; }
.rail a:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 3px; border-radius: var(--radius); }
@media (max-width: 48rem) {
  .rail-layout { grid-template-columns: 1fr; }
  .rail { position: static; height: auto; flex-direction: row; align-items: center;
    gap: var(--space-5); border-right: 0; border-bottom: 1px solid var(--color-rule); }
  .rail__mark { font-size: var(--text-lg); }
  .rail__links { flex-direction: row; }
  .rail__foot { margin: 0 0 0 auto; }
}
@media (prefers-reduced-motion: reduce) { .rail__links a, .rail__foot { transition: none; } }
</style>
```

## SSR / hydration note
Pure static server HTML — no JS, hydrates trivially. `position: sticky` and the responsive reflow are CSS-only, so there is no server/client divergence and no `'use client'` needed. If a mobile collapse-toggle is added, it is a separate `'use client'` leaf whose closed state must match on server and first client paint (see [`../ssr-and-hydration.md`](../ssr-and-hydration.md) § 2).

## Diversification knobs
- **Rail width & alignment:** 12–16rem; links top-aligned vs vertically centred.
- **Divider:** right hairline vs `--color-paper-2` surface shift.
- **Wordmark:** stacked two-line display vs single-line vs vertical (writing-mode) set.
- **Active state:** accent text vs a short leading accent tick before the current link.
