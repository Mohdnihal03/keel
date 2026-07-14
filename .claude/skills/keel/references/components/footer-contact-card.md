# Footer · Contact Card

**Use when** the site belongs to a studio, agency, or local business and the footer should present real contact facts — address, email, hours — as content, not a link farm. **Genre fit:** editorial / atmospheric.

## Structure
Two or three plain text blocks in a simple row: a studio name + one-line description, a physical address rendered as an `<address>`, and a direct email/phone. These are content first — the address is set as prose, the email is a single `mailto:` link, and there is no column of a dozen page links. A `1px --color-rule` hairline tops the footer; a small copyright line sits at the bottom. Labels (small `--font-mono` eyebrows like "Studio", "Visit", "Reach us") organise the blocks. Wordmark/name in `--color-ink`; body facts in `--color-ink-2`; the email link carries the only accent as its underline colour (≤5%). On mobile the blocks stack with `--space-6` between them, address remains readable prose.

## Code
```html
<footer class="footer-contact">
  <div class="footer-contact__grid">
    <div class="footer-contact__block">
      <span class="footer-contact__eyebrow">Studio</span>
      <p class="footer-contact__name">Keel &amp; Co.</p>
      <p class="footer-contact__body">Design and build for considered products.</p>
    </div>
    <div class="footer-contact__block">
      <span class="footer-contact__eyebrow">Visit</span>
      <address class="footer-contact__body">
        14 Marsh Lane<br>Bristol BS1 4RN<br>United Kingdom
      </address>
    </div>
    <div class="footer-contact__block">
      <span class="footer-contact__eyebrow">Reach us</span>
      <p class="footer-contact__body">
        <a class="footer-contact__mail" href="mailto:studio@keel.co">studio@keel.co</a><br>
        Mon–Fri, 9–17 GMT
      </p>
    </div>
  </div>
  <small class="footer-contact__copy">© 2026 Keel &amp; Co.</small>
</footer>
```
```css
.footer-contact { border-top: 1px solid var(--color-rule); background: var(--color-paper); padding: var(--space-10) var(--space-4) var(--space-6); }
.footer-contact__grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--space-8); max-width: 72rem; margin: 0 auto; }
.footer-contact__eyebrow { display: block; margin-bottom: var(--space-2); font: var(--text-xs)/1 var(--font-mono); letter-spacing: 0.04em; text-transform: uppercase; color: var(--color-muted); }
.footer-contact__name { margin: 0 0 var(--space-2); font: var(--text-lg)/1.2 var(--font-display); font-weight: 700; color: var(--color-ink); }
.footer-contact__body { margin: 0; font: var(--text-sm)/1.6 var(--font-body); font-style: normal; color: var(--color-ink-2); }
.footer-contact__mail { color: var(--color-ink-2); text-decoration: underline; text-decoration-color: var(--color-accent); }
.footer-contact__mail:hover { color: var(--color-ink); }
.footer-contact__mail:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
.footer-contact__copy { display: block; max-width: 72rem; margin: var(--space-8) auto 0; font: var(--text-sm)/1 var(--font-body); color: var(--color-muted); }
@media (max-width: 48rem) { .footer-contact__grid { grid-template-columns: 1fr; gap: var(--space-6); } }
```

## SSR / hydration note
Static server HTML; hydrates trivially. The contact facts are real content in semantic elements — `<address>` for the location, a `mailto:` anchor for email — so there is no client state and nothing to reconcile. Rendering the address as text (not a script-injected widget) keeps it crawlable and available without JS. Keep facts accurate and specific per `../copywriting.md`; the email link is the single accent target and its focus `outline` is instant per `../accessibility.md`.

## Diversification knobs
- Block count: two (studio + contact) vs. three (add a map/hours or social handle line).
- Eyebrows: `--font-mono` uppercase labels vs. no labels, letting order carry meaning.
- Email presentation: plain `mailto:` link vs. email plus a phone number on its own line.
- Location detail: single address block vs. multi-location list for a business with branches.
