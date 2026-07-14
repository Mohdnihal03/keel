# Nav · Minimal

**Use when** the page has ~1–2 real destinations and the wordmark should carry the whole bar. **Genre fit:** editorial, atmospheric, playful (any genre where the page *is* the message, not a hub).

## Structure
Wordmark hard-left. Either nothing else, or ONE trailing action hard-right (a single link or ghost button) — never a link cluster. The bar breathes: generous side padding, no hairline by default (let the hero's own top edge do the separating), optional thin `--color-rule` bottom border only if the hero background matches the nav. On mobile it is already minimal — the single action stays visible; nothing collapses into a hamburger because there is nothing to collapse.

## Code
```html
<nav class="nav-min" aria-label="Primary">
  <a class="nav-min__mark" href="/">Ledger</a>
  <a class="nav-min__action" href="/start">Start free<span aria-hidden="true"> →</span></a>
</nav>

<style>
.nav-min {
  display: flex; align-items: center; justify-content: space-between;
  gap: var(--space-4);
  padding: var(--space-5) var(--space-6);
  background: var(--color-paper);
  font-family: var(--font-body);
}
.nav-min__mark {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: var(--text-lg);
  letter-spacing: -0.01em;
  color: var(--color-ink);
  text-decoration: none;
  white-space: nowrap;
}
.nav-min__action {
  font-size: var(--text-sm);
  color: var(--color-ink-2);
  text-decoration: none;
  white-space: nowrap;
  transition: color var(--dur-fast) var(--ease-out);
}
.nav-min__action:hover { color: var(--color-accent); }
.nav-min a:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 3px;
  border-radius: var(--radius);
}
@media (prefers-reduced-motion: reduce) { .nav-min__action { transition: none; } }
</style>
```

## SSR / hydration note
Pure static server HTML — no JS, hydrates trivially. Nothing reads `window`/`localStorage`, so it renders identically on server and client and needs no `'use client'`. Safe inside a Server Component. If a theme toggle lives here, it is a separate `'use client'` leaf (see [`../ssr-and-hydration.md`](../ssr-and-hydration.md) § 1) — the bar itself stays server-rendered.

## Diversification knobs
- **Wordmark weight/case:** 600 lowercase vs 700 small-caps vs mono-set from `--font-mono`.
- **Action presence:** none at all, vs one text link, vs one ghost button.
- **Divider:** no rule (float on hero) vs a single `--color-rule` bottom hairline.
- **Arrow glyph:** trailing `→` present or absent on the action.
