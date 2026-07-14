# Hero enrichment — whether to build something, and what

Loaded at **Step 4.5** of the design flow, after the theme is computed and the SSR target is named. It answers one question the rest of this skill never asks: *does this hero build something, or is it type on paper?*

Keel is otherwise a discipline of refusal — no gradients, no italic display, no centred heroes, no three-card rows. Strip out everything Keel forbids and what remains is type on tinted paper. That is a real look, and it is a **fine** look, but it is only one look, and a skill whose whole claim is *"never settles into one recognisable look"* cannot have exactly one composition. This file is the other half of the rule. It says what to build, not just what to avoid.

**The promise.** Enrichment is an option, not a default. A typographic-only hero is *always* an acceptable answer — it is the strongest fail-state on the web. But "acceptable fail-state" is not the same as "the right answer every time," and reaching for it on every build is how eight Keel pages ship one page.

**The bar.** Better nothing than bad something. A quiet, well-set typographic hero beats a stock illustration, a Lottie checkmark, an aurora background, or a generic centred demo-video block — every time, without exception.

---

## The tier inversion — why Keel's hierarchy is not a taste ranking

Most design guidance ranks hero media by taste: hand-built is classy, Lottie is lazy. Keel reaches the same ordering from a different direction, and the difference matters, because **a correctness argument survives disagreement about taste.**

Keel pages must be correct on first server paint (gates 34–43). Above the fold, that means: *in the first byte, visible with JavaScript disabled, dimensions reserved so nothing shifts.* Run every enrichment medium through that filter and the hierarchy sorts itself:

| Tier | Medium | In the first byte? | Visible with JS off? | Verdict |
| --- | --- | --- | --- | --- |
| **0** | Typography only | Yes | Yes | Always correct. The floor. |
| **A** | Pure CSS art | Yes | Yes | **Keel's default when enrichment is earned.** Zero bytes, zero JS. |
| **B** | Hand-built inline SVG | Yes | Yes | **Keel's default for anything CSS can't express.** Inline = shipped in the HTML. |
| **C** | Real media (screenshot, photo, video) | Yes | Yes (poster/`<img>`) | Fine, with the media discipline: reserved dimensions, `priority`/`fetchpriority`, poster. |
| **D** | Generated still | Yes | Yes | Admissible, post-processed and provenance-stamped. Never shipped raw. |
| **X** | **Lottie · WebGL/Three.js · JS-driven canvas** | **No** | **No** | **Refused above the fold.** |

Tier X is not discouraged in Keel. It is a **gate failure**. A Lottie hero centrepiece renders an empty box until a JSON payload downloads and a player boots; a WebGL hero renders an empty `<canvas>` until a shader compiles. On a slow network, a blocked script, or a JS error, that is a blank hero — which is *precisely* the failure gate 35 already catches when a model writes `opacity: 0` on an `<h1>` and reveals it on mount. Same failure, different costume.

So: **the taste argument and the correctness argument are the same argument.** Hand-built CSS and SVG are not merely the classier choice. They are the only tiers that are *in the first byte*. The discipline that makes a Keel page load correctly is the same discipline that makes it look made.

Below the fold, Tier X relaxes — a JS-driven piece is admissible if the region is content-complete without it and the script is additive. Above the fold, it is not.

**Skipping tiers is the tell.** If Tier A can do it, do it in Tier A. Reach for B when CSS can't express the form cleanly. Reach for C when there is a real thing to photograph or capture. Reach for D only when a scene or character genuinely can't be hand-built.

See [`custom-craft.md`](custom-craft.md) for *how* to build at tiers A and B.

---

## Step 1 — does this brief want imagery at all?

Decide this **before** picking a tier. The default is typography-only. Act on the *first* row that fires.

| Brief signal | Strategy |
| --- | --- |
| e-commerce, shop, store, catalogue, fashion, lookbook | Real product photos. Honest placeholder until the user provides them. |
| photography, portfolio, gallery, artist | Imagery *is* the page. Placeholder until provided. |
| food, restaurant, menu, café, wine, recipe | Hero photo + crops. Placeholder until provided. |
| team, "about us", hiring, careers | Portrait crops. Placeholder until provided. |
| travel, hotel, property, listing, real estate | Cover photo + tiles. Placeholder until provided. |
| news, blog, magazine, publication | Feature image per item. Placeholder until provided. |
| SaaS, platform, dev tool, dashboard-adjacent marketing | **Build, don't source.** Tier A/B custom craft — a diagram, a chart, a specimen of the actual output. |
| API, docs, changelog, CLI, library, SDK | **Usually none.** Typography + real code. Build only if there is a *mechanism* worth drawing. |
| editorial, essay, letter, manifesto, type-specimen | **None.** Display typography is the design. |
| (vague / unspecified) | **Default: typography-only.** When in doubt, don't. |

Two rules on top:

- **Never fabricate an asset and ship it as final.** No invented stock photos, no fake brand logos, no hand-drawn fake browser/phone/IDE chrome (gates 32 and 51). A placeholder must *look* like a placeholder, not like a confident decision.
- **When the row is ambiguous, ask one short question.** *"Will you have product photos, or should I leave swappable placeholders?"*

### The row that produces bare pages

Watch the SaaS / dev-tool / CLI rows. They are the ones where "no imagery" is *usually* right and therefore where a model stops thinking. But "no imagery" is not the same as "nothing to build." A dev tool with a mechanism worth drawing — a data flow, a state machine, an architecture, the shape of its own output — should **draw the mechanism**, at Tier A or B, from real values. That isn't decoration. It's the argument, made visually.

The test: *if the reader understood the mechanism, would they buy?* If yes, and the mechanism is hard to say in a sentence, draw it.

---

## Step 2 — pick zero or one archetype

### E1 · Real media, clipped by the viewport edge

Display headline left, real screenshot or footage right, the rightmost 10–20% running past the viewport so it is deliberately cut. The clip implies *there is more product than fits on this screen*.

*Use when:* SaaS / dev tool / platform, **and you have a real capture.**
*Avoid when:* you don't. A clipped-edge stock skyline reads as filler.

**Keel refuses the browser frame.** Hand-drawn chrome — a fake URL pill, three traffic-light dots, a fake title bar — is gate 32, one of the strongest AI tells there is. The frame the model invents never matches any real OS, so it lands in the uncanny valley. Use a real capture in a `<figure>` with a hairline `--color-rule` border, or no frame at all.

```css
.hero-clip { display: grid; grid-template-columns: minmax(20rem, 1fr) 1.4fr; gap: var(--space-2xl); align-items: center; }
.hero-clip__media {
  width: calc(100% + 12vw);          /* the part that runs off the page */
  aspect-ratio: 16 / 10;             /* reserved — cannot shift on load (gate 49) */
  border: 1px solid var(--color-rule);
  border-radius: var(--radius);
  overflow: hidden;
}
@media (max-width: 60rem) {
  .hero-clip { grid-template-columns: 1fr; }
  .hero-clip__media { width: 100%; }  /* the clip reads as broken at 375px — never clip on mobile */
}
```

The media is the LCP element: `priority` in `next/image`, or `fetchpriority="high"` in vanilla. Never `loading="lazy"` (gate 48). Video gets `poster`, `muted`, `playsinline`, and a captions track; the poster is what renders with JS off.

### E2 · Full-bleed muted loop, ghosted

Footage fills the fold, tinted back under a paper-coloured overlay so the type stays readable. The video is wallpaper, not subject.

*Use when:* the product's *feel* is the message.
*Avoid when:* the product needs to be **seen** — use E1.

The headline must clear contrast against the *poster frame*, not the average frame. Verify with JS off: the poster is what a real user sees first.

### E3 · Real screenshot in a figure

A single real capture, hairline border or none, with a margin-aligned caption. The plain, honest answer for a product that looks good already.

*Use when:* the capture is clean and legible.
*Avoid when:* it's busy or blurry — a frame draws attention to the mess; it doesn't hide it.

Tilt (1–3°) is allowed and adds life. Fake chrome is not.

### E4 · Custom illustration centrepiece — **Keel's workhorse**

A hand-built centrepiece at Tier A (CSS) or Tier B (inline SVG): the diagram of the mechanism, the shape of the output, the thing the product makes.

*Use when:* the brand or the product has a *thing* that benefits from being drawn.
*Avoid when:* the brief is "modern professional team" generic — illustrating that is the new template.

This is the archetype Keel reaches for most, because it is the one that is *in the first byte, zero-JS, infinitely scalable, and impossible to buy off a shelf*. Recipes in [`custom-craft.md`](custom-craft.md).

### E5 · Small animated loop (CSS/SVG only)

One small custom loop — an orbiting dot, a drawing line, a breathing form. Small, custom, ≤ 4s, and **only** when reduced-motion is off.

*Use when:* the page is otherwise still and one element gives it life.
*Avoid when:* the page already moves. More motion then reads as anxious.

Pure CSS or SVG. **Not a Lottie** — see the tier table. A spinning logo, a drawing checkmark, a loading ring are all eight lines of CSS; reaching for a 40KB player and a JSON payload to do it is the tell, and in Keel it also fails the first-paint gate.

### E6 · One accent radial, unanimated

A single low-chroma accent-tinted radial behind the hero. Texture you can barely see — paper quality, not decoration.

**Sharply limited in Keel:** `atmospheric` genre only. **One** radial, **one** hue, **unanimated**, fixed, under the accent footprint cap (gate 14). Aurora blobs, mesh gradients, floating orbs, and anything with two hues in it are banned outright (gate 2) — they are the "make it look modern" reflex every model has, and their ubiquity *is* the tell.

If the theme already carries texture, don't double it. Grain on grain is mud.

### E7 · Hero photography

One real, tightly-cropped photograph. Tone-matched to the palette — desaturate a few percent to sit with the paper. Pair with a tone-matched font voice; a luxury photo on a brutalist page jars.

---

## Step 3 — pick zero or one polish pattern

The archetypes decide *what sits beside the headline*. These decide *how the headline itself sits*. Use one when the hero feels shape-flat. **Never two.** A vertical rail *and* an overflow title *and* a decorative numeral on one hero is a panic attack.

### HP1 · Vertical rail title

A wordmark or pull-label running vertically beside the body: `writing-mode: vertical-rl`. Reads as studio, atelier, editorial.

*Avoid when:* the display title is itself large and horizontal — competing axes. Pick one direction; the rail is a supporting voice.

### HP2 · Marquee overflow

The `<h1>` is deliberately wider than the viewport; it bleeds past the right edge. Reads as manifesto, brutal, loud.

*Use when:* the genre is playful/manifesto **and** the title is ≤ 6 words.
*Careful:* scope `overflow-x: clip` to the hero container. Keel already sets `overflow-x: clip` on `html, body` for gate 44; do not switch either to `hidden`, which breaks scroll containment for descendants. Collapse to `white-space: normal` on mobile.

### HP3 · Cursor spotlight

A radial that tracks the pointer, scoped to the hero.

**Keel's constraints are tighter than the pattern's origin.** It is a client-JS effect, so: the hero must be **complete and correct without it**; the spotlight layer is decorative and `aria-hidden`; the gradient's default position is server-rendered so the hero looks finished before hydration; the listener lives on an interactive leaf, never a `'use client'` at the page root (gate 39). Reduced-motion pins the gradient to a static position rather than removing it — otherwise you leave a flat dead surface.

Never page-wide. A cursor-follower that trails across the whole document is slop and a vestibular trigger. `atmospheric` and `playful` only; never on `technical`.

### HP4 · Decorative numeral

A large edition/year/chapter/version glyph in a hero corner, set low-contrast behind the content.

**Roman, never italic.** The pattern's usual form is display-italic; Keel bans italic display type (gate 7), and this is not an exception. Set it in the display face at weight, in `color-mix(in oklch, var(--color-ink) 8%, transparent)`.

**The numeral must mean something** — issue 22, v0.8, chapter 03, 2026. A number in the corner that names nothing is decoration, and decoration that carries no information is exactly what this skill exists to remove. If you can't say what the number *is*, drop it.

---

## Step 4 — hero space discipline

Every hero, enriched or not.

- **Footprint.** 70–90% of the first viewport. `min-height: 100vh` is the fingerprint (gate 5). Aim for `clamp(60vh, 75dvh, 88dvh)` and let the content settle inside.
- **Fit the fold.** On a 13″ laptop (~800px tall) the headline, lede, and primary action must be visible **without scrolling**. When they aren't, it's almost always wasted vertical space: an oversized clamp max, display line-height near 1.2, a three-line lede, padding bloat. Right-size; don't cramp.
- **Asymmetric padding.** `padding-block-end` ≥ 1.3× `padding-block-start`. The hero sits *into* the page; symmetric padding floats.
- **Never centre everything.** At most two centred elements (gate 5).
- **Headline type.** One display weight. Tracking -0.02 to -0.04em. Line-height 0.95–1.05 — never 1.2, which inherits the body value and reads as un-set type. No second weight inside the headline for "emphasis"; use `--color-accent`, which is what the `<em>` override in Keel's tokens is for.
- **One polish pattern. One archetype. Maximum.**

---

## The gate — eight questions, all must be yes

If any answer is *no*, ship the typographic hero instead. It is a good hero.

1. Does the enrichment **communicate** something the typography can't?
2. Does it **survive deletion**? If the hero still works without it, it earned its place. If the hero collapses without it, you propped weak typography on a crutch — and the crutch is the thing to remove, not the thing to keep.
3. Is it **in the first byte** — server-rendered, present in the HTML, visible with JavaScript disabled? *(gate 35, and the tier table above.)*
4. Are its **dimensions reserved** — `aspect-ratio` or width+height — so it cannot shift the layout when it loads? *(gate 49.)*
5. If it is the **LCP element**, is it prioritised rather than lazy-loaded? *(gate 48.)*
6. Does it have a **reduced-motion** state that still looks finished — not just "animation removed," leaving a half-drawn line or an empty box? *(gate 24.)*
7. Is it under **2MB**, all-in?
8. Does its **tone match the page**? A hand-drawn sprig on a technical dev-tool page is as wrong as a brutalist slab on an atelier page.

---

## Stamp the decision

The enrichment choice goes in the CSS stamp, alongside the theme and SSR lines, so the next run and the `audit` verb can both see what was chosen:

```css
/* Keel · enrichment: E4 custom illustration · craft: tier-A CSS art
 * polish: none · motion: 1 loop (6s, reduced-motion static)
 * first-byte: yes · js-off: renders · lcp: h1 (text) */
```

If there is no enrichment, say so — `enrichment: none (typography-only)`. Don't omit the line; an absent line reads as an oversight, and the whole point of Step 4.5 is that **not enriching is a decision, made on purpose, every build.**

---

## Common mistakes

- **Defaulting to typography-only because it always passes.** It does always pass. That's the trap. A gate you can satisfy by building nothing is not a design system; it's a filter. Ask question 1 honestly.
- **Reaching for Lottie or WebGL because it's familiar.** In Keel that's a first-paint failure, not just a taste failure.
- **Enrichment as a crutch.** If deleting the illustration collapses the hero, the typography was too weak. Fix the typography. Then decide about the illustration.
- **Grain everywhere.** Grain is a treatment, not a default.
- **Treating the background as the hero.** It isn't. The headline is. The background is paper.
- **Clipping on mobile.** At 375px, a clipped edge just looks broken. Collapse it.

---

*Adapted from the hero-enrichment discipline in [Hallmark](https://github.com/nutlope/hallmark) (MIT), re-derived against Keel's SSR gates and anti-pattern set. The tier ordering, the first-byte filter, and the fake-chrome, italic-numeral, and gradient constraints are Keel's own — see [`anti-patterns.md`](anti-patterns.md) gates 2, 7, 32, 35, 48, 49, 51.*
