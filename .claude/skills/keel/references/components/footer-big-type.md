# Footer · Big Type

**Use when** the footer should double as a closing note — a confident sign-off line set huge, with only the few links that matter beneath. **Genre fit:** atmospheric / editorial.

## Structure
An oversized display line spanning most of the container width, set left, in ROMAN weight (no gradient-text, no two-line clickable text). Below it, after generous space, a single quiet row: a small link cluster on the left and copyright on the right, both in `--color-muted`. The big line is `--color-ink`; it is a statement, not a link. No hairline is required — the scale shift between the huge line and the small row is the divider. Accent stays out of it. On mobile the display line steps down two `--text` rungs and the bottom row stacks (links, then copyright).

## Code
```html
<footer class="footer-big">
  <p class="footer-big__line">Build the version users already expect.</p>
  <div class="footer-big__row">
    <nav class="footer-big__links" aria-label="Footer">
      <a href="/docs">Docs</a>
      <a href="/pricing">Pricing</a>
      <a href="/contact">Contact</a>
    </nav>
    <small class="footer-big__copy">© 2026 Keel Labs</small>
  </div>
</footer>
```
```css
.footer-big {
  max-width: 72rem;
  margin: 0 auto;
  padding: var(--space-14) var(--space-4) var(--space-8);
  background: var(--color-paper);
}
.footer-big__line {
  max-width: 18ch;
  margin: 0 0 var(--space-10);
  font: var(--text-5xl)/1.05 var(--font-display);
  font-weight: 700;
  color: var(--color-ink);
  text-wrap: balance;
}
.footer-big__row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: var(--space-6);
  padding-top: var(--space-6);
  border-top: 1px solid var(--color-rule);
}
.footer-big__links { display: flex; flex-wrap: wrap; gap: var(--space-4); }
.footer-big__links a {
  font: var(--text-sm)/1 var(--font-body);
  color: var(--color-muted);
  text-decoration: none;
}
.footer-big__links a:hover { color: var(--color-ink-2); text-decoration: underline; }
.footer-big__links a:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
.footer-big__copy { font: var(--text-sm)/1 var(--font-body); color: var(--color-muted); }
@media (max-width: 40rem) {
  .footer-big__line { font-size: var(--text-3xl); }
  .footer-big__row { flex-direction: column; align-items: flex-start; gap: var(--space-4); }
}
```

## SSR / hydration note
Static server HTML; hydrates trivially. The oversized line is a plain `<p>`, not an interactive element, so there is no client state and nothing to reconcile. Guard against layout shift by keeping the display type in a system/`--font-display` stack that is preloaded, so the big line does not reflow on font swap — see `../ssr-and-hydration.md`. Keep the closing line specific and unhyped per `../copywriting.md`; focus `outline` is instant per `../accessibility.md`.

## Diversification knobs
- Line scale: `--text-5xl` hero-close vs. a more restrained `--text-4xl`.
- Bottom row divider: hairline top rule vs. no rule, spacing only.
- Line role: pure statement vs. statement ending in one inline text link for the primary action.
- Alignment: left-set line vs. line right-aligned to mirror the copyright edge.
