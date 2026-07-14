# Hero · Letter

**Use when** a founder or editor is speaking in their own voice — a launch note, a change of direction, a point of view. **Genre fit:** editorial.

## Structure
A **letter**: salutation, a short body (two or three tight paragraphs), a sign-off with a name. It reads as prose, not a pitch — so the "headline" is the opening line, set in body-adjacent display, not a slogan. Compose it as a single narrow column hung off a **left rule**, not centred on the page; the eyebrow (date or "A note from…") sits above, the signature drops below-left, off the CTA axis. One quiet CTA at most — a link, not a loud button — because a letter that ends in "Buy now" breaks the voice. Cap the measure tight (~60ch) so it reads like a real column.

## Code
```html
<section class="letter">
  <p class="letter__meta">A note from the founder · 14 July 2026</p>
  <div class="letter__body">
    <h1 class="letter__open">We started this because invoicing shouldn't take an afternoon.</h1>
    <p>For two years we ran the same broken process you do. So we rebuilt it — for us first, then for you.</p>
    <p>It's smaller than our competitors on purpose. It does the one thing, and it does it in seconds.</p>
  </div>
  <p class="letter__sign">— Dana Okafor<br><span>Founder</span></p>
  <a class="letter__cta" href="/story">Read the full story →</a>
</section>
```
```css
.letter {
  max-width: 62ch; margin: 0;                       /* left-hung, not centred */
  padding: var(--space-2xl) var(--space-lg) var(--space-3xl);
  border-left: 2px solid var(--color-rule); padding-left: var(--space-lg);
}
.letter__meta {                                      /* off-axis eyebrow */
  font-family: var(--font-mono); font-size: var(--text-xs);
  letter-spacing: .08em; text-transform: uppercase; color: var(--color-accent); margin: 0 0 var(--space-md);
}
.letter__open {                                      /* opening line as display, restrained size */
  font-family: var(--font-display); font-weight: 700; font-style: normal;
  font-size: var(--text-2xl); line-height: 1.15; letter-spacing: -.01em;
  text-wrap: balance; color: var(--color-ink); margin: 0 0 var(--space-md);
}
.letter__body p { color: var(--color-ink-2); line-height: 1.6; text-wrap: pretty; }
.letter__body p + p { margin-top: var(--space-sm); }
.letter__sign {                                      /* signature drops below-left */
  font-family: var(--font-display); font-weight: 600; font-style: normal;
  color: var(--color-ink); margin: var(--space-lg) 0 var(--space-sm);
}
.letter__sign span { font-family: var(--font-body); font-weight: 400; color: var(--color-muted); }
.letter__cta { color: var(--color-accent); font-family: var(--font-mono); text-decoration: none; }
.letter__cta:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 3px; }
```

## SSR / hydration note
Static server HTML, visible without JS — the letter is text and must be fully present at first byte (it is the LCP text). No typewriter/word-reveal that leaves the paragraph empty until mount, and no `opacity:0`-until-mount on the body — an editorial hero that blanks during SSR reads as broken and tanks LCP. Any entrance is ADDITIVE: the letter is painted, and only a subtle fade or rule-draw plays on mount behind a `mounted` flag. The date in `.letter__meta` should be a **server-stamped string**, not `new Date()` in render, or it will mismatch across timezones (see § Hydration mismatch). Cross-ref `../ssr-and-hydration.md` and `../motion.md`.

## Diversification knobs
- **Salutation:** "A note from…", "Dear reader,", a dateline, or none.
- **Sign-off:** typeset name, name + role, or a real signature image (treat as media — `alt`, dimensions).
- **Rule:** left border, a top hairline over the meta line, or no rule (indent instead).
- **CTA:** quiet text link, a footnote-style reference, or omit entirely for a pure editorial open.
