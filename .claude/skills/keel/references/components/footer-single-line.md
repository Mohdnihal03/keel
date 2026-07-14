# Footer · Single Line

**Use when** the page is a focused landing or product page that needs a footer, not a sitemap — the de-slopped default. **Genre fit:** technical / editorial.

## Structure
One row, three zones on a single baseline: wordmark left, one flat link cluster centre (or pushed right), copyright at the far right. No four-column grid, no social-icon wall, no centred tiny copyright. A single `1px --color-rule` hairline sits above the row as the only divider; everything below it is `--color-muted` except the wordmark, which stays `--color-ink`. Links are plain body text with an underline on hover — not buttons, never two-line clickable text. Accent is absent here (footers are quiet). On mobile the three zones stack in source order (wordmark, links wrap to a tidy multi-line cluster, copyright last) with `--space-4` between them.

## Code
```html
<footer class="footer-line">
  <div class="footer-line__inner">
    <span class="footer-line__mark">Keel</span>
    <nav class="footer-line__links" aria-label="Footer">
      <a href="/docs">Docs</a>
      <a href="/pricing">Pricing</a>
      <a href="/changelog">Changelog</a>
      <a href="/contact">Contact</a>
    </nav>
    <small class="footer-line__copy">© 2026 Keel Labs</small>
  </div>
</footer>
```
```css
.footer-line {
  border-top: 1px solid var(--color-rule);
  background: var(--color-paper);
}
.footer-line__inner {
  display: flex;
  align-items: center;
  gap: var(--space-6);
  max-width: 72rem;
  margin: 0 auto;
  padding: var(--space-6) var(--space-4);
}
.footer-line__mark {
  font: var(--text-base)/1 var(--font-display);
  font-weight: 700;
  color: var(--color-ink);
}
.footer-line__links {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
  margin-inline: auto; /* pushes copy to the far right */
}
.footer-line__links a {
  font: var(--text-sm)/1 var(--font-body);
  color: var(--color-muted);
  text-decoration: none;
}
.footer-line__links a:hover { color: var(--color-ink-2); text-decoration: underline; }
.footer-line__links a:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
.footer-line__copy {
  font: var(--text-sm)/1 var(--font-body);
  color: var(--color-muted);
}
@media (max-width: 40rem) {
  .footer-line__inner { flex-direction: column; align-items: flex-start; gap: var(--space-4); }
  .footer-line__links { margin-inline: 0; }
}
```

## SSR / hydration note
Static server HTML; hydrates trivially. Pure markup and CSS with no client state — the hairline, layout, and hover/focus styling are all declarative, so there is nothing to reconcile between server and client. Keep the link count small and the labels concrete per `../copywriting.md`; the focus `outline` is instant per `../accessibility.md`.

## Diversification knobs
- Link cluster position: centred vs. right-aligned next to the copyright.
- Copyright content: year + entity vs. a short one-clause tagline.
- Wordmark treatment: text wordmark vs. small inline logo glyph + text.
- Divider: hairline top rule vs. no rule with extra top whitespace.
