# Accessibility

Universal module. Applies to every page Keel touches. A gorgeous page that a screen reader can't parse, a keyboard can't reach, or a low-vision user can't read is slop. Bake this in from the first commit — it is not a retrofit.

## Contrast

WCAG minimums:

- **Body text** (under 24px regular, or under 18.66px / ~14px bold): **4.5:1** against its background.
- **Large text** (≥24px regular or ≥18.66px bold), **icons, focus rings, UI boundaries**: **3:1**.

Prefer **APCA** as the accurate check — it models perception better than the WCAG ratio: aim for **Lc ≥ 60** for body text and **Lc ≥ 45** for large text. Where APCA and WCAG disagree, both should pass; if forced, trust APCA for perceived legibility but never ship below the WCAG floor.

Keel's theming engine auto-fits accent contrast — the seed-derived accent is nudged until `--color-accent` vs `--color-paper` and `--color-accent-ink` vs `--color-accent` clear threshold. See [theming-engine.md](theming-engine.md). **Hand-authored pairs are not covered.** Any color you type by hand must be checked.

Most-missed cases — check these every time:

- **Text inside a card that switched to `--color-paper-2`.** Muted text tuned for `--color-paper` often fails on the slightly-darker/lighter card surface. Re-check `--color-muted` on `--color-paper-2` specifically.
- **`--color-muted` on `--color-paper-2`** — the single most common failure. It is a double concession (dimmed ink + shifted paper). Verify it or promote to `--color-ink`.
- **Button text vs button fill — the black-on-black bug.** An accent fill with inherited dark body text renders invisible. Every accent-filled control MUST define and apply `--color-accent-ink`:

```css
.btn-primary {
  background: var(--color-accent);
  color: var(--color-accent-ink); /* never inherit --color-ink onto an accent fill */
}
```

Never rely on inherited text color over any colored fill.

## Focus-visible

Every interactive element needs a **visible `:focus-visible` ring at ≥3:1** against its surroundings. Use `outline`, not `border` — a border changes box size and shifts layout on focus. Use `outline-offset` for breathing room.

Reserve a transparent outline at rest so the ring appears without any layout reflow:

```css
:where(a, button, input, select, textarea, summary, [tabindex]) {
  outline: 2px solid transparent; /* reserved at rest */
  outline-offset: 2px;
}
:where(a, button, input, select, textarea, summary, [tabindex]):focus-visible {
  outline-color: var(--color-focus);
  border-radius: inherit;
}
```

The ring appears **instantly**. Never transition or animate `outline`/`outline-color` — a fading focus ring is disorienting and defeats the purpose. See [motion.md](motion.md). Do not remove outlines with `outline: none` unless you replace them with an equivalent visible indicator (a `box-shadow` ring that also clears 3:1 is acceptable).

## The 8 interactive states

Design and verify all eight for every control: **default, hover, focus-visible, active, disabled, loading, error, success.** Hover is not a substitute for focus — keyboard users never hover.

**Disabled needs three channels** — never opacity alone (opacity is invisible to non-sighted users and doesn't block clicks):

```html
<button disabled aria-disabled="true" class="btn-primary">Save</button>
```

```css
.btn-primary:disabled,
.btn-primary[aria-disabled="true"] {
  opacity: 0.5;         /* 1. visual */
  cursor: not-allowed;  /* 2. pointer affordance */
  /* 3. the real disabled / aria-disabled attribute above blocks activation + tells AT */
}
```

Use the real `disabled` attribute when the control should be fully inert. Use `aria-disabled="true"` (plus a JS guard) only when it must stay focusable to explain *why* it's disabled.

**Input-field state checklist:**

- **Border width stays constant across all states.** Change *color*, not *width* — a 1px→2px swap on focus/error reflows layout. Reserve the final width at rest.
- **Height parity** between an input and any adjacent button on the same row — match `height`/`padding`/`line-height` so they align.
- **Reserve helper-text height.** Give the message slot a fixed `min-height` so showing an error doesn't push the form down:

```css
.field-message { min-height: 1.25rem; } /* reserved whether empty, helper, or error */
```

## Semantic landmarks

- Exactly **one `<h1>`** per page. Headings descend logically — no skipping `<h2>` to `<h4>` for visual size (size is CSS's job).
- Use `<header>`, `<nav>`, `<main id="main">`, `<footer>`. Add `role`/`aria-label` only to disambiguate multiples (e.g. two `<nav>`s: `aria-label="Primary"` / `aria-label="Footer"`).
- **Skip link** as the first focusable element, targeting `#main`:

```html
<a class="skip-link" href="#main">Skip to content</a>
```
```css
.skip-link { position: absolute; left: -9999px; }
.skip-link:focus { left: 1rem; top: 1rem; z-index: 100; }
```

- **`<button>` for actions, `<a href>` for navigation.** Never `<div onClick>` — it has no role, no keyboard activation, no focus. If you must, it needs `role`, `tabindex="0"`, and key handlers — so just use the real element.

## Images & decorative art

- Meaningful images get real, descriptive `alt` (convey the *information*, not "image of").
- Purely decorative images get `alt=""` (empty, not missing) so AT skips them.
- Every decorative inline `<svg>`, `<canvas>`, or CSS-art element gets `aria-hidden="true"`. If it conveys meaning, give it `role="img"` + `aria-label` instead:

```html
<svg aria-hidden="true"><!-- ornament --></svg>
<svg role="img" aria-label="Rising revenue"><!-- chart --></svg>
```

## Motion

Honour `prefers-reduced-motion` — reduce or remove non-essential animation. See [motion.md](motion.md) for the full policy. Any content that auto-advances (carousel, marquee, auto-playing video) needs a visible **pause/stop control** (WCAG 2.2.2) and must not be the only way to reach the content.

## Forms

- Every input has an associated `<label>` — `for`/`id` or wrapping. A **placeholder is not a label** (it vanishes on input and often fails contrast).
- Link errors with `aria-describedby`; set `aria-invalid="true"` on the failing field:

```html
<label for="email">Email</label>
<input id="email" type="email" aria-invalid="true" aria-describedby="email-err" />
<p id="email-err" class="field-message" role="alert">Enter a valid email.</p>
```

- **Required is never signalled by colour alone.** Add a text/symbol cue and `required` / `aria-required="true"`.

## Tap targets

Interactive targets are at least **44×44px** for touch (pad small icons/links to reach it), with enough spacing that adjacent targets aren't mis-tapped. This applies to icon buttons, close buttons, and inline links in nav.

## SSR / a11y intersection (Keel differentiator)

Accessibility and the SSR pillar are entangled — get the server output right or a11y breaks before JS loads. See [ssr-and-hydration.md](ssr-and-hydration.md).

- **Skip-links and landmarks live in the server-rendered HTML.** They must work on first paint, before hydration — a keyboard user tabs immediately. Never inject `<main>`, `<nav>`, or the skip link from a client effect.
- **Don't gate above-the-fold focus management on `useEffect`.** Focusing a hero heading or moving focus into an opened dialog via a client-only effect fails for users who act before hydration and misbehaves during SSR. Render focusable structure server-side; only *move* focus in response to real user interaction.
- **Set the theme before paint.** A dark-mode toggle resolved after hydration causes a FOUC that flips background under text tuned for the other theme — contrast is momentarily wrong (light-tuned muted text on a dark flash, or vice versa). Resolve and apply the theme class in a blocking pre-paint inline script so `--color-paper`/`--color-ink` are correct on the *first* paint. See [ssr-and-hydration.md](ssr-and-hydration.md) and [color.md](color.md).
- **Announce streamed / Suspense content with `aria-live`.** Content that arrives after initial render (Suspense boundaries, streamed sections) is silent to screen readers unless it lands in a live region. Wrap the slot in `aria-live="polite"` (or `role="status"`) so its arrival is announced:

```html
<div aria-live="polite" aria-busy="true"><!-- Suspense fallback → resolved content --></div>
```
Flip `aria-busy` to `false` when resolved.

## Checklist

- [ ] Every hand-authored text/background pair clears 4.5:1 (body) / 3:1 (large); muted-on-`paper-2` verified.
- [ ] Every accent fill applies `--color-accent-ink` — no inherited text on colored fills.
- [ ] Every interactive element has a `:focus-visible` ring ≥3:1 via `outline` + reserved transparent outline; never animated.
- [ ] All 8 states designed; disabled uses opacity + `cursor` + real attribute; input border-width and helper-text height reserved.
- [ ] One `<h1>`, logical heading order, `<main>`/`<nav>`/`<footer>`, skip link to `#main` in SSR HTML.
- [ ] `<button>` for actions, `<a>` for nav — no `<div onClick>`.
- [ ] Meaningful images have `alt`; decorative art has `alt=""` / `aria-hidden`.
- [ ] `prefers-reduced-motion` honoured; auto-advancing content has pause/stop.
- [ ] Every input labelled; errors via `aria-describedby` + `aria-invalid`; required not colour-only.
- [ ] Tap targets ≥44×44px with spacing.
- [ ] Theme set before paint; `aria-live` on streamed/Suspense content.
