# Motion

Motion is the easiest place to leak AI slop. The tells are always the same: everything fades up on scroll, buttons bounce, durations run long, and nothing respects reduced-motion. This file is the fix. Read it before adding any transition, keyframe, or JS animation.

## Animate only `transform` and `opacity`

Those two properties are the only ones the browser can composite on the GPU without touching layout or paint. Everything else is expensive:

- **Layout props** (`width`, `height`, `top`, `left`, `right`, `bottom`, `margin`, `padding`) force reflow — the browser recomputes the geometry of the element *and its siblings and ancestors* every frame. Jank.
- **Paint props** (`box-shadow`, `background-position`, `color` on large surfaces) force repaint of the layer every frame.
- `transform` and `opacity` skip both: the element is promoted to its own compositor layer and the GPU interpolates it. 60fps stays cheap.

So never animate `width` — animate `transform: scaleX()`. Never animate `top` — animate `transform: translateY()`. Never animate `height: 0 → auto` — that path can't be composited at all; use a grid-rows or `max-height` trick sparingly, or better, don't animate it.

```css
/* Bad — reflows every frame */
.panel { transition: height var(--dur-base) var(--ease-out); }

/* Good — composited */
.card { transition: transform var(--dur-base) var(--ease-out),
                    opacity var(--dur-base) var(--ease-out); }
.card:hover { transform: translateY(-2px); }
```

## The three named easings

Define these once in your theme layer. Never inline raw cubic-beziers at call sites.

```css
:root {
  --ease-out:    cubic-bezier(0.22, 1, 0.36, 1);   /* decelerate — entrances, most UI */
  --ease-in:     cubic-bezier(0.55, 0, 1, 0.45);   /* accelerate — exits, dismissals */
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);   /* symmetric — moves, reorders */
}
```

Rules:

- **`--ease-out` is your default.** Things entering or responding to input should decelerate into place.
- **`--ease-in` for exits** — elements leaving the screen should accelerate away.
- **Ban the browser default `ease`** (and `ease-in-out`'s builtin). It's the "I didn't choose an easing" signal and it reads as generic.
- **Ban bounce/overshoot on UI state changes.** No `cubic-bezier(.34, 1.56, .64, 1)` on buttons, modals, tooltips, dropdowns, accordions. Overshoot on a state toggle looks like a toy. It is allowed *only* for genuinely physical drag interactions (a card you flick, a sheet you throw) where the spring models real momentum.

## Durations

```css
:root {
  --dur-fast: 120ms;   /* hovers, focus feedback, small toggles */
  --dur-base: 200ms;   /* the default for UI state changes */
  --dur-slow: 320ms;   /* page-level reveals, route transitions */
}
```

- **UI state changes ≤ 200ms.** Hover, press, open/close a menu — use `--dur-fast` or `--dur-base`.
- **Page-level reveals ≤ 320ms.** Hero entrances, section reveals — `--dur-slow` max.
- **Nothing over ~400ms.** If it feels like it needs longer, it's spatial motion that should be cut, not slowed. Long animations make a fast site feel slow.

## `prefers-reduced-motion: reduce` — MANDATORY

Every keyframe and every transition ships with a reduced-motion fallback. This is not optional and not a nice-to-have; for some users motion causes nausea and vestibular distress. Spatial motion (translate, scale, rotate, parallax) collapses to a ≤150ms opacity crossfade or to nothing at all. Opacity-only fades may stay.

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }

  /* Where you still want a gentle acknowledgement, crossfade only: */
  .reveal {
    transition: opacity 150ms var(--ease-out) !important;
    transform: none !important;
  }
}
```

Put the blanket reset near the top of your global styles so it wins by source order plus `!important`. Then opt specific elements back into a bare opacity fade where a hard cut would feel broken.

## Focus rings never animate

Focus rings must appear **instantly** — zero transition. A keyboard user needs to know where they are the instant they tab; a ring that fades in over 200ms is a ring that isn't there yet.

```css
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
  transition: none;   /* never animate the ring itself */
}
```

If the element has a `transition: all` (don't use `transition: all`), the outline gets swept in with it — another reason to name your transitioned properties explicitly. See [accessibility.md](accessibility.md) for focus-ring contrast and `:focus-visible` scoping.

## Cut motion before adding it

Most pages have too much motion, not too little. Default to less.

**Heuristic:** if removing an animation loses the user no information, remove it. Motion should communicate — direction of a transition, cause and effect, spatial continuity. Decorative motion that says nothing is noise.

**Cap ~3 motion primitives per page.** Pick a small vocabulary (e.g. a fade-up for section reveals, a translateY on hover, a crossfade on route change) and reuse it. A page where every element has its own bespoke animation is the AI-slop signature.

## Feedback patterns

- **Silent success over celebratory toasts.** When an action just works, the result appearing *is* the confirmation. Don't fire a toast for every save. Reserve notifications for things the user needs to act on.
- **Optimistic update + Undo over confirmation dialogs.** Apply the change immediately, show a quiet "Undone?" affordance. This is faster and less motion than a modal that animates in to ask "Are you sure?".
- **Tooltip timing:** hover-delay ~800ms (so tooltips don't flash while the pointer crosses the UI), but focus-delay **0ms** (a keyboard user who tabs to the trigger wants the label now).

## SSR-CRITICAL: scroll/entrance animations and hydration

This is where entrance animations silently break server-rendered pages. Read carefully.

**The failure:** you gate initial content visibility on JS. The element renders at `opacity: 0` and only becomes visible when an IntersectionObserver fires or a framer-motion `whileInView`/`initial` resolves. But during SSR and the window *before hydration*, that JS has not run. If JS is slow, blocked, or errored, the content never appears. For above-the-fold content this means a **blank hero on first paint** — the worst possible outcome, and it's invisible to Lighthouse's scripted runs but obvious to real users on slow networks.

```jsx
// ANTI-PATTERN — hero is invisible until JS hydrates and animates
<motion.h1 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
  {headline}
</motion.h1>
// Server sends opacity:0. No JS → permanently blank. Slow JS → flash of nothing.
```

**The principle:** content is visible by default in CSS. The entrance animation is *additive* — it only enhances once the component has mounted. First meaningful paint must never depend on `useEffect`, which does not run during SSR at all.

Three correct patterns:

```jsx
// 1. Only animate BELOW the fold. Above-the-fold ships static and visible.
//    Below-the-fold entrances are fine to gate on IntersectionObserver —
//    the user can't see them until they scroll, by which point JS has hydrated.

// 2. [data-mounted] gate that DEFAULTS TO VISIBLE.
function Hero() {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  return <h1 data-mounted={mounted || undefined}>{headline}</h1>;
}
```
```css
/* Visible by default. The animation only plays once mounted. No JS → visible. */
h1 { opacity: 1; }
h1[data-mounted] { animation: rise var(--dur-slow) var(--ease-out); }
@keyframes rise { from { opacity: 0; transform: translateY(12px); } }
```
```css
/* 3. Pure CSS @starting-style — no JS at all, starts from visible-safe state. */
.hero { opacity: 1; transition: opacity var(--dur-slow) var(--ease-out); }
@starting-style { .hero { opacity: 0; } }
```

Also: **respect reduced-motion inside JS animation libraries.** The CSS `@media` block does not govern framer-motion or GSAP JS values — check the preference explicitly and skip the spatial part.

```js
const reduce = typeof window !== 'undefined'
  && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const variants = reduce
  ? { initial: { opacity: 1 }, animate: { opacity: 1 } }
  : { initial: { opacity: 0, y: 20 }, animate: { opacity: 1, y: 0 } };
```

See [ssr-and-hydration.md](ssr-and-hydration.md) for the general rule: server paint must be correct and complete before any JS runs.

## Do / Don't

- **Do** animate `transform` and `opacity` only; name the properties explicitly.
- **Do** ship a reduced-motion fallback for every animation, always.
- **Do** keep above-the-fold content visible in CSS regardless of JS state.
- **Do** cut motion that carries no information; cap ~3 primitives per page.
- **Don't** use the default `ease`, or bounce/overshoot on UI state changes.
- **Don't** run anything past ~400ms, or animate focus rings.
- **Don't** gate first paint on `useEffect`, IntersectionObserver, or `whileInView` for above-the-fold content.
