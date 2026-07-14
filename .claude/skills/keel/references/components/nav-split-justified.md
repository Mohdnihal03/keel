# Nav · Split-justified

**Use when** you need a conventional marketing bar but must avoid the banned centred-link default — logo one side, one decisive action the other. **Genre fit:** technical, editorial, playful (the safe de-slopped workhorse for most marketing pages).

## Structure
Wordmark hard-left. Single primary action hard-right (filled button using `--color-accent` / `--color-accent-ink`). NO centre link cluster — that is the AI tell this spec exists to replace. If two or three secondary links are genuinely needed, group them tight against the right action (right-weighted), not spread across the centre. Divider language: prefer a surface shift (`--color-paper` nav over a `--color-paper-2` page, or vice-versa) over a hairline; use a `--color-rule` bottom border only when both surfaces match. Mobile: secondary links (if any) fold into a toggle; the primary action stays visible in the bar.

## Code
```html
<nav class="nav-sj" aria-label="Primary">
  <a class="nav-sj__mark" href="/">Cadence</a>
  <div class="nav-sj__end">
    <a class="nav-sj__link" href="/docs">Docs</a>
    <a class="nav-sj__cta" href="/get">Get started</a>
  </div>
</nav>

<style>
.nav-sj {
  display: flex; align-items: center; justify-content: space-between;
  padding: var(--space-4) var(--space-6);
  background: var(--color-paper);
  border-bottom: 1px solid var(--color-rule);
  font-family: var(--font-body);
}
.nav-sj__mark {
  font-family: var(--font-display); font-weight: 700;
  font-size: var(--text-lg); letter-spacing: -0.01em;
  color: var(--color-ink); text-decoration: none; white-space: nowrap;
}
.nav-sj__end { display: flex; align-items: center; gap: var(--space-5); }
.nav-sj__link {
  font-size: var(--text-sm); color: var(--color-ink-2);
  text-decoration: none; white-space: nowrap;
  transition: color var(--dur-fast) var(--ease-out);
}
.nav-sj__link:hover { color: var(--color-ink); }
.nav-sj__cta {
  font-size: var(--text-sm); font-weight: 600; white-space: nowrap;
  padding: var(--space-2) var(--space-4);
  background: var(--color-accent); color: var(--color-accent-ink);
  border-radius: var(--radius); text-decoration: none;
  transition: opacity var(--dur-fast) var(--ease-out);
}
.nav-sj__cta:hover { opacity: 0.9; }
.nav-sj a:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 3px; border-radius: var(--radius); }
@media (prefers-reduced-motion: reduce) { .nav-sj__link, .nav-sj__cta { transition: none; } }
</style>
```

## SSR / hydration note
Pure static server HTML — no JS, hydrates trivially. If the page needs a mobile toggle for secondary links, that toggle is the only `'use client'` leaf; render its default-closed state identically on server and client (never branch on `window` at render) — see [`../ssr-and-hydration.md`](../ssr-and-hydration.md) § 2.

## Diversification knobs
- **Action style:** filled accent button vs ghost/outline vs bare arrow link.
- **Right cluster:** action-only vs action + 1–2 tight secondary links.
- **Divider:** surface shift vs `--color-rule` hairline vs none.
- **Wordmark treatment:** display bold vs mono uppercase vs mark + short label.
