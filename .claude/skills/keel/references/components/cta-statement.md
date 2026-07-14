# CTA · Statement

**Use when** the page has earned attention and a single sentence can carry the ask — no card, no gradient band, just voice. **Genre fit:** editorial / atmospheric.

## Structure
A centred (or left-set) block on plain `--color-paper`: one bold display line at large `--text` size, then a single action beneath it after `--space-6` of breathing room. The action is one link or one button — never two competing weights. No enclosing card, no background fill, no rule above or below (let whitespace and section rhythm do the framing). Heading is ROMAN, no gradient-text, kept to one line that wraps naturally on narrow screens. Accent shows up only as the button fill or the link's underline colour (≤5%). On mobile: type steps down one `--text` rung, action stays full-width-comfortable but not stretched edge to edge.

## Code
```html
<section class="cta-statement">
  <h2 class="cta-statement__line">Ship the version your users already expect.</h2>
  <a class="cta-statement__action" href="/get-started">Get started</a>
</section>
```
```css
.cta-statement {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--space-6);
  padding: var(--space-12) var(--space-4);
  background: var(--color-paper);
}
.cta-statement__line {
  max-width: 20ch;
  margin: 0;
  font: var(--text-3xl)/1.1 var(--font-display);
  font-weight: 700;
  color: var(--color-ink);
  text-wrap: balance;
}
.cta-statement__action {
  display: inline-flex;
  align-items: center;
  height: var(--space-11);
  padding: 0 var(--space-5);
  font: var(--text-base)/1 var(--font-body);
  color: var(--color-accent-ink);
  background: var(--color-accent);
  border: 1px solid transparent;
  border-radius: var(--radius);
  text-decoration: none;
  transition: filter var(--dur-1) var(--ease-out);
}
.cta-statement__action:hover { filter: brightness(0.94); }
.cta-statement__action:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
@media (max-width: 34rem) {
  .cta-statement__line { font-size: var(--text-2xl); }
  .cta-statement { padding: var(--space-10) var(--space-4); }
}
```

## SSR / hydration note
Static server HTML; hydrates trivially. No client state, so nothing to reconcile — the `<a>`/`<button>` is a plain server-rendered element and the focus ring is a CSS `outline` that appears instantly. If the action becomes a `<button>` wired to a client handler, keep that handler in a small leaf and let this section stay server-rendered around it. Keep the copy honest and specific per `../copywriting.md`; single visible focus target per `../accessibility.md`.

## Diversification knobs
- Alignment: centred column vs. left-set with the action on its own line under the sentence.
- Action form: filled button vs. text link with an accent underline.
- Statement length: a crisp 6-word claim vs. a two-clause sentence set at one rung smaller.
- Optional kicker: a small `--font-mono` label above the line vs. nothing.
