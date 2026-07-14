# The slop test

Run this before handing back any output. Every gate is a yes/no; **every answer must be "no."** If any answer is "yes," fix it and re-run. The gates map to named tells in [anti-patterns.md](anti-patterns.md) — this file is the checklist, that file is the reasoning.

The list is deliberately shorter than a big catalog's: Keel prevents whole gate-families by construction (the [theming engine](theming-engine.md) can't emit a failing-contrast accent, a zero-chroma neutral, or a banned font, so those need one confirming gate, not ten). What Keel *adds* is the **SSR & hydration** block (gates 34–43) — the failures a visual-only review never catches.

Genre note: a few gates loosen by genre (`atmospheric` allows one accent-tinted radial; `technical`/modern-minimal allows pure-white paper and zero-chroma neutrals). Where a gate has no genre note, it is universal.

---

## Pre-emit self-critique (run FIRST, before the gates)

Score the planned output 1–5 on each axis. Anything **< 3 triggers a revision pass** before you touch the gate list — don't bring known weakness into the checklist.

| Axis | Scoring |
| --- | --- |
| **Philosophy** | Is there a clear *why* — a position — or is it just a layout? |
| **Hierarchy** | In 2 seconds, can a reader tell primary from secondary from tertiary? |
| **Execution** | Are rule weights, accent footprint, text-wrap, focus rings, contrast all in spec? |
| **Specificity** | Does it look like *this brief*, or like a page that could be anyone's? |
| **Restraint** | Has everything that isn't earning its place been removed? |
| **Variety** | Structural distance from previous Keel output — not a colour-swap of it? |
| **Soundness** | Will it be correct on first server paint — no flash, no mismatch, visible without JS? |

Stamp the scores at the top of the CSS: `/* Keel · critique: P5 H4 E5 S4 R5 V5 So5 */`.

---

## Visual

1. Is the display font Inter, Roboto, Open Sans, Poppins, Lato, Work Sans, DM Sans, Montserrat, or system-ui? *(Inter Tight as a body face is allowed.)*
2. Is there a purple→blue / purple→cyan / orange→pink gradient anywhere — **including a `background-clip: text` gradient headline?** *(No genre allows gradient text. Atmospheric allows one radial on background only.)*
3. Is there a 3-equal-column grid of icon-above-heading cards?
4. Is any card nested inside another card, or using a thick coloured side-stripe border?
5. **Centred-everything hero** — are eyebrow, title, lede, AND CTA all on one centred axis (or `min-height:100vh` with everything centred)? *(Atmospheric/playful may centre when the canvas is the design.)*
6. Is pure `#000` or pure `#fff` used as a base colour? *(modern-minimal/technical allows pure `#fff` paper.)*
7. Is any heading or display element italic (`font-style: italic` on h1–h6, a title class, wordmark, stat, or an `<em>` inside a heading)?

## Structural

8. Does the page use the AI template (hero → 3 feature cards → CTA → footer), OR the same macrostructure as the previous Keel build in this project (per the CSS stamp / `.keel/log.json`)?
9. Are all sections separated by identical equal whitespace — no rule, no surface shift, no rhythm change?
10. Is the `<nav>` the AI default (wordmark-left + 4–5 centred links + button-right + hairline + white bg)? *(Allowed only when the page truly has ~2 destinations and the genre permits it.)*
11. Is the `<footer>` the AI default (4 link columns + social row + tiny copyright + hairline)? *(Allowed only on a genuine docs/hub root.)*
12. Is there a section eyebrow beside the heading (tag-left/heading-right two-column split), or an eyebrow on *every* section?

## Colour & tokens

13. Does any neutral have zero chroma (`oklch(L 0 H)`)? *(modern-minimal/technical may use zero-chroma neutrals.)*
14. Does the accent cover more than ~5% of any viewport (solid fills, large accent headings, accent backgrounds)? *(Atmospheric allows an accent radial up to ~20%.)*
15. Is any colour or `font-family` inlined outside the `:root` / `[data-theme]` token block (a raw `#hex`, `oklch()`, `rgb()`, or `font-family:"…"`)?
16. Is the Keel stamp (seed · anchor · genre · hue · fonts · contrast · ssr) missing from the top of the CSS?

## Typography

17. More than three `font-family` families on the page? (display + body + at most one outlier; same family at different weights counts once.)
18. Is the hero headline size mismatched to its length (an oversized clamp on a 90-char headline that then overflows the fold)?
19. Is any prose measure outside 45–75ch?

## Motion

20. Is `transition: all` (or `transition-all`) used anywhere?
21. Is a uniform `hover:scale-105` applied across multiple unrelated elements, or does any element stack >1 hover effect (translate+scale+shadow+colour)?
22. Is a bounce/overshoot easing used on a UI state change (button/modal/tooltip), or the browser-default `ease`?
23. Is `width`/`height`/`top`/`left`/`margin`/`padding` being animated?
24. Does any `transform`/`animation`/transition lack a `@media (prefers-reduced-motion: reduce)` fallback?
25. Does the focus ring transition/fade into existence instead of appearing instantly?

## Contrast & states

26. Does any `(color, background)` pair fail its threshold (body 4.5:1 / large-text·icons·rings 3:1)? Check the three usual misses: text in a `--color-paper-2` card, muted-on-paper-2, button-text ≈ button-fill.
27. Is `--color-accent-ink` undefined or unused on any surface that fills with `--color-accent` and carries text? (The black-on-black bug.)
28. Does any interactive element lack `:focus-visible`, `:active`, or `:disabled`? Is disabled signalled by `opacity` alone (needs opacity + `cursor:not-allowed` + the real `disabled`/`aria-disabled`)?
29. Do input fields keep `border-width` constant across states, match the adjacent button's height, and reserve helper-text height so an error doesn't shift layout?

## Honest copy

30. Any quantitative claim ("10× faster", "50,000+ teams", "+47%") the user did not supply and the model invented? Any fabricated testimonial/logo? Any placeholder name (Jane Doe) or startup cliché (Acme, Unleash, Seamless, Supercharge)?
31. Any banned opening line ("Built for the modern team", "Where X meets Y", "Empower your…", "Supercharge your workflow", "In today's digital landscape")?

## Chrome & imagery

32. Did the page hand-draw fake chrome (browser bar, phone frame, code-window dots, terminal, IDE), instead of a real screenshot in a `<figure>`?
33. Emoji used as a feature/step/pricing icon, or two+ icon libraries mixed on one page?

## SSR & hydration (Keel's block — skip only for a pure static-HTML artifact)

34. **Theme flash.** Is there a `data-theme` / dark-mode toggle with **no synchronous blocking script in `<head>`** setting the theme before first paint? (Guaranteed FOUC.) See [ssr-and-hydration.md § 1](ssr-and-hydration.md).
35. **Hidden-until-JS content.** Is any above-the-fold content `opacity:0` / `initial={{opacity:0}}` until an on-mount/scroll handler reveals it? (Invisible during SSR and if JS fails.)
36. **Non-determinism in render.** Is `Date.now()`/`new Date()`/`Math.random()`/`window`/`localStorage` read in the render body of a server-shared component? (Hydration mismatch.)
37. **Invalid nesting.** Any `<p>` wrapping a block element, nested `<a>`/`<button>`, or other auto-corrected markup that will mismatch?
38. **Suppressor abuse.** Is `suppressHydrationWarning` used anywhere except `<html>` (theme) / `<body>` (extensions)?
39. **Over-clienting.** Is `'use client'` at the page/layout root instead of on interactive leaves? Does any client component import a server-only module (db/fs/secret SDK)?
40. **Non-serializable props** passed across the server→client boundary (functions, class instances, raw `Date`)?
41. **Loading state.** Is a slow/dynamic region unwrapped by `<Suspense>`, or given a bare spinner fallback that shifts layout instead of a layout-matched skeleton? Is a streamed region missing `aria-live`? **And does the region actually stream?** A `<Suspense>` boundary around a region the framework can *statically prerender* resolves at build time and never streams — the skeleton is dead code and the route is `○ Static`. If the region is meant to be live, it must opt out of the prerender (`noStore()` / `export const dynamic = 'force-dynamic'` in Next) or it is not a loading state at all. Verify on the wire, not in the source: the route should build as `ƒ (Dynamic)`, and the skeleton must appear *earlier in the response bytes* than the real content.
42. **Font loading.** Is the same face loaded by both `next/font` and a Google `<link>`, or via a render-blocking stylesheet with no `display=swap`? Is the font not wired to `--font-*`?
43. **SSR bailout.** Was `ssr:false` / root `'use client'` used to *dodge* a hydration bug rather than fix it?

## Responsive / mobile

44. Does the page horizontally scroll at any width 320–1920px? (Requires `overflow-x: clip` on **both** `html` and `body` — `clip`, not `hidden`.)
45. Does any button/nav/footer/CTA text wrap to two lines at any width?
46. Does any image-bearing grid track use bare `1fr` instead of `minmax(0, 1fr)`?
47. Does any per-theme/section head keep a multi-column grid on mobile instead of collapsing to one column?

## Media & performance (only when the page carries significant imagery/video)

See [media-and-performance.md](media-and-performance.md). Skip trivially on a typography-only page.

48. Is the LCP hero image lazy-loaded (`loading="lazy"` / no `priority` in `next/image`), or served without `fetchpriority="high"` in vanilla? (Self-inflicted LCP killer.)
49. Does any `<img>`/`<video>`/embed lack reserved dimensions (width+height or `aspect-ratio`), so it shifts layout on load? (CLS.)
50. Is a hero video autoplaying with sound, missing a `poster`, or acting as the lazy LCP? Is there no still/reduced-motion alternative?
51. Are fabricated assets shipped as final — invented stock photos, fake brand logos, or hand-drawn fake browser/phone/IDE chrome instead of a real screenshot in a `<figure>`?

## Colour fidelity

52. **Out-of-gamut colour.** Is any `oklch()` value in the stylesheet outside the sRGB gamut — so the browser silently desaturates it and paints a colour you never chose? This bites **hand-authored** tokens hardest: a hover shade (`--color-accent-2`), a dark-mode accent, or a focus ring written by nudging chroma up. The theming engine gamut-fits everything it emits; anything you add by hand is *not* covered. Check with `fit_gamut()` in [`theming-engine.py`](theming-engine.py), or in DevTools — an out-of-gamut `oklch()` renders visibly flatter than its chroma value implies. Note that a contrast check will **not** catch this: contrast maths clamps RGB, so an unrenderable colour can still "pass" 4.5:1 on a colour that never reaches the screen.

---

Record the SSR result in the stamp: `· ssr: pass (34–43)`; media if applicable: `· media: pass (48–51)`. If any gate is "yes," fix before shipping. **Do not ship slop.**
