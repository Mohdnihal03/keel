# Nav · Inline-hero

**Use when** the page is a manifesto/marquee statement and a separate chrome bar would dilute it — the nav folds into the top row of the hero composition instead. **Genre fit:** atmospheric, editorial, playful.

## Structure
No standalone `<nav>` bar and no divider. The hero is a grid; its top row holds the wordmark and a short row of links (or one action), sharing the hero's own padding, background, and type scale. Links sit inline with the wordmark — same baseline, lighter weight — then the giant headline drops below. Because the nav rides the hero surface, contrast is checked against the hero background, not a default paper. Mobile: the link row wraps beneath the wordmark (or reduces to one action); the headline still leads.

## Code
```html
<header class="hero">
  <div class="hero__top">
    <a class="hero__mark" href="/">FIELD/WORK</a>
    <nav class="hero__nav" aria-label="Primary">
      <a href="/manifesto">Manifesto</a>
      <a href="/index">Index</a>
      <a href="/join">Join<span aria-hidden="true"> →</span></a>
    </nav>
  </div>
  <h1 class="hero__title">We build in the open, or not at all.</h1>
</header>

<style>
.hero {
  min-height: 88vh; display: flex; flex-direction: column; gap: var(--space-10);
  padding: var(--space-6) var(--space-6) var(--space-9);
  background: var(--color-paper); font-family: var(--font-body);
}
.hero__top { display: flex; align-items: baseline; justify-content: space-between; gap: var(--space-6); flex-wrap: wrap; }
.hero__mark {
  font-family: var(--font-display); font-weight: 700; letter-spacing: -0.01em;
  font-size: var(--text-lg); color: var(--color-ink); text-decoration: none; white-space: nowrap;
}
.hero__nav { display: flex; gap: var(--space-5); flex-wrap: wrap; }
.hero__nav a {
  font-size: var(--text-sm); color: var(--color-ink-2);
  text-decoration: none; white-space: nowrap;
  transition: color var(--dur-fast) var(--ease-out);
}
.hero__nav a:hover { color: var(--color-accent); }
.hero__nav a:focus-visible, .hero__mark:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 3px; border-radius: var(--radius); }
.hero__title {
  margin: auto 0 0; max-width: 18ch;
  font-family: var(--font-display); font-weight: 700; line-height: 0.98;
  font-size: var(--text-5xl); letter-spacing: -0.02em; color: var(--color-ink);
}
@media (prefers-reduced-motion: reduce) { .hero__nav a { transition: none; } }
</style>
```

## SSR / hydration note
Pure static server HTML — no JS, hydrates trivially. The nav is plain markup inside the hero, fully visible on first server paint with no JS dependency — never gate it behind an on-mount reveal (that would blank the top of the page during SSR; see [`../ssr-and-hydration.md`](../ssr-and-hydration.md) § 2 and [`../slop-test.md`](../slop-test.md) gate 35). Any entrance animation on the headline is additive and must not start from `opacity:0`.

## Diversification knobs
- **Alignment:** links right of wordmark (justified) vs both left-clustered.
- **Link count:** 2–3 links vs a single action.
- **Baseline:** links share the wordmark baseline vs sit as a small stacked block.
- **Headline join:** links flush to hero padding vs indented to the headline's measure.
