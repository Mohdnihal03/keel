# Hero · Marquee

**Use when** the brief is brand-forward or a manifesto — the statement is the product's stance, not a feature list. **Genre fit:** atmospheric / editorial.

## Structure
One **oversized typographic statement** fills the first viewport; support is sparse and pushed to a corner below. The type *is* the composition — no image, no card. Break the line manually so the ragged edge is intentional, not a wrapped accident, and hang it off a left or baseline rule rather than centring the block. Emphasis on one or two words via `--color-accent` or a weight jump — never gradient text, never italic. Below the statement: a single short qualifier and one link, both off-axis (bottom-left or bottom-right), leaving deliberate empty space above the fold.

## Code
```html
<section class="hero-mq">
  <h1 class="hero-mq__stmt">
    Ship the <em>whole</em> idea.<br>Not the demo.
  </h1>
  <div class="hero-mq__foot">
    <p class="hero-mq__sub">A build system for teams who close the last 10%.</p>
    <a class="hero-mq__link" href="/manifesto">Read the manifesto →</a>
  </div>
</section>
```
```css
.hero-mq {
  min-height: 82vh; display: grid; align-content: space-between;
  padding: var(--space-2xl) var(--space-lg) var(--space-xl);
  background: var(--color-paper);
}
.hero-mq__stmt {                          /* short lines → push the display ceiling */
  font-family: var(--font-display); font-weight: 800; font-style: normal;
  font-size: clamp(3rem, 1rem + 11vw, 8.5rem); line-height: .95;
  letter-spacing: -.03em; color: var(--color-ink);
  max-width: 16ch; text-wrap: balance; margin: 0;
}
.hero-mq__stmt em {                        /* roman emphasis via accent, not slant */
  font-style: normal; color: var(--color-accent);
}
.hero-mq__foot {
  display: flex; flex-wrap: wrap; justify-content: space-between;
  align-items: end; gap: var(--space-md); border-top: 1px solid var(--color-rule);
  padding-top: var(--space-sm);
}
.hero-mq__sub { color: var(--color-muted); max-width: 40ch; margin: 0; }
.hero-mq__link { color: var(--color-ink); font-family: var(--font-mono); text-decoration: none; }
.hero-mq__link:hover { color: var(--color-accent); }
.hero-mq__link:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 3px; }
```

## SSR / hydration note
Static server HTML, visible without JS — the statement is the LCP text and must be present in the first byte, not injected client-side. Any reveal (word-by-word rise, ink wipe) is ADDITIVE: the words render fully painted by default and only animate on mount behind a flag; never `opacity:0`-until-mount on the statement or the hero blanks during SSR. Manual `<br>` breaks are content and must match between server and client render. See `../ssr-and-hydration.md` and `../motion.md`.

## Diversification knobs
- **Break rhythm:** 2 short lines vs. one long ragged line vs. a 3-line stanza.
- **Emphasis carrier:** accent word, single heavy word among lights, or one underlined verb.
- **Fold density:** empty upper third (pure statement) vs. a thin top eyebrow rule.
- **Foot alignment:** sub + link split across the baseline vs. both hung bottom-left.
