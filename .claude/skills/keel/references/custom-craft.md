# Custom craft — how to hand-build the centrepiece

Loaded when [`hero-enrichment.md`](hero-enrichment.md) selects **Tier A** (pure CSS art) or **Tier B** (hand-built inline SVG). It tells you which technique to reach for, what each looks like done well, and the one rule that keeps hand-built artwork from breaking Keel's first-paint guarantee.

**The principle.** Custom-built artwork *is* the design. Library-picked artwork is a shortcut and a good audience reads it as one. Keel's job is to make custom-build the path of least resistance — which it already is, because on a server-rendered page it is also the *correct* path: CSS art and inline SVG ship in the first byte, render with JavaScript disabled, and cost zero bundle. See the tier inversion in [`hero-enrichment.md`](hero-enrichment.md).

---

## The rule that governs every animated illustration

> **The static state is the base. The animation is additive.**

This is the same rule Keel already applies to hero text ([`motion.md`](motion.md) § SSR-critical): content is visible by default in CSS, and motion only enhances it. Applied to artwork it means: **an illustration's resting state — before any animation runs, and after reduced-motion disables it — must be the finished drawing.**

It is easy to get this backwards, and the common recipes for draw-on line art get it backwards by default:

```css
/* WRONG — the base state is an invisible line. */
.line {
  stroke-dasharray: 0 200;                 /* nothing drawn */
  animation: draw 1.6s var(--ease-out) forwards;
}
@keyframes draw { to { stroke-dasharray: 200 200; } }
```

Keel ships a blanket reduced-motion reset (`animation-duration: .001ms !important; animation-iteration-count: 1 !important`). That reset happens to rescue the snippet above — the animation completes instantly and `forwards` holds the drawn state. But it survives by luck: drop `forwards`, or let any tool disable the animation outright, and the illustration is **an empty box**. You have made the drawing depend on the animation, which is exactly the failure gate 35 catches on text.

Write it the other way round. The drawn state is the truth; the animation is a way of arriving at it:

```css
/* RIGHT — the base state is the finished drawing. */
.line {
  stroke-dasharray: 200 200;               /* fully drawn — this is the truth */
  animation: draw 1.6s var(--ease-out);
}
@keyframes draw { from { stroke-dashoffset: 200; } }  /* animate FROM undrawn */

@media (prefers-reduced-motion: reduce) {
  .line { animation: none; }               /* still fully drawn. Nothing to fix. */
}
```

Now reduced-motion, animation failure, and a stylesheet that never loads all land on the same finished drawing. Apply this to every recipe below: opacity starts at 1, dash arrays start drawn, transforms start at rest.

---

## Tier A · Pure CSS art

**When.** Shapes plus colour: bars, dots, rules, sliced forms, geometric marks, gradient compositions, anything a `clip-path` or a stack of gradients can express.
**Cost.** Zero bytes, zero JS, infinitely scalable.

| Feature | Use for |
| --- | --- |
| `clip-path: polygon()` | Chevrons, hexagons, angled cuts |
| `conic-gradient()` | Wheels, pie segments, radial dividers |
| `radial-gradient()` | Spheres, glow points, soft centres |
| `mask-image` | Layered transparency, text-clipped effects |
| `@property` | Typed custom properties the browser can *interpolate* — the key to declarative animation without JS |
| `animation-timeline: view()` | Scroll-linked motion, composited off-thread, no IntersectionObserver |

**Every colour references a token.** No raw `oklch()` or `#hex` in the artwork — gate 15 applies to illustrations exactly as it applies to buttons. Artwork that hardcodes its colours can't be re-themed and will not follow the palette into dark mode. If a shape needs a value the tokens don't have, *add a named token*, gamut-fit it (gate 52), and reference it.

### Why `@property` matters

Without it, an animated custom property jumps from start to end with no in-between. With it, the browser knows the type and interpolates smoothly — GPU-composited, zero JavaScript.

```css
@property --sweep {
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}
```

That is the whole engine behind every loop below.

---

## Tier B · Hand-built inline SVG

**When.** Forms CSS can't express cleanly — curves, diagrams, marks, anything with structure.
**Cost.** 4–15KB inline, typically. Anything over 30KB is suspicious: you have hidden raster embeds or thousands of redundant path commands.

**Inline it.** `<img src="art.svg">` is a second request and renders nothing until it lands. Inline SVG is in the first byte, styleable with your tokens (`fill: var(--color-accent)`), and animatable with CSS. On a Server Component it costs nothing.

**Pipeline.** Design → export → run through [SVGOMG](https://jakearchibald.github.io/svgomg/) → inline. Never ship a raw Figma export; it carries metadata, unused `<defs>`, and doubled transforms, typically 30–60% of the file.

**`viewBox` fits the art.** Not `0 0 1920 1080` for a mark that occupies a corner of it.

**Accessibility.** A meaningful illustration is `role="img"` with an `aria-label` that says what it *shows* — not "illustration". A purely decorative one is `aria-hidden="true"`. Pick one; an unlabelled meaningful graphic is a gap.

---

## Recipes

Four recipes at Tier A/B, in Keel tokens, obeying the base-is-drawn rule. Use them verbatim when they fit; strip them for technique when they don't. The point is that *every illustration on a Keel page is built, not picked.*

### Recipe 1 · Mechanism diagram

Boxes joined by flow lines, one line animated to suggest movement. The default answer for a dev tool with a mechanism worth drawing — the thing that turns "no imagery" into "draw the argument."

```html
<svg class="mech" viewBox="0 0 720 180" role="img"
     aria-label="Seed enters the engine; the engine emits a fitted palette">
  <defs>
    <marker id="mech-tip" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto">
      <path d="M0,0 L7,3 L0,6" fill="currentColor" />
    </marker>
  </defs>

  <g class="mech__node mech__node--a">
    <rect x="16" y="50" width="150" height="80" />
    <text x="91" y="86" text-anchor="middle" class="mech__name">Seed</text>
    <text x="91" y="104" text-anchor="middle" class="mech__sub">a string</text>
  </g>

  <path class="mech__flow mech__flow--live" d="M 166 90 Q 210 72 254 90" marker-end="url(#mech-tip)" />

  <g class="mech__node mech__node--mid">
    <rect x="254" y="50" width="190" height="80" />
    <text x="349" y="86" text-anchor="middle" class="mech__name">Hash → fit</text>
    <text x="349" y="104" text-anchor="middle" class="mech__sub">contrast · gamut</text>
  </g>

  <path class="mech__flow" d="M 444 90 Q 488 108 532 90" marker-end="url(#mech-tip)" />

  <g class="mech__node mech__node--c">
    <rect x="532" y="50" width="172" height="80" />
    <text x="618" y="86" text-anchor="middle" class="mech__name">Palette</text>
    <text x="618" y="104" text-anchor="middle" class="mech__sub">same bytes, forever</text>
  </g>
</svg>
```

```css
.mech { width: 100%; height: auto; display: block; color: var(--color-ink); }

.mech__node rect { fill: var(--color-paper-2); stroke: var(--color-rule); stroke-width: 1; }
.mech__node--mid rect { stroke: var(--color-accent); }
.mech__name { font-family: var(--font-display); font-size: 15px; font-weight: 600; fill: var(--color-ink); }
.mech__sub  { font-family: var(--font-mono);    font-size: 10px; fill: var(--color-muted); }

/* Controlled asymmetry — ±1° reads as drawn; perfect alignment reads as generated. */
.mech__node--a { transform: rotate(-0.6deg); transform-origin: 91px 90px; }
.mech__node--c { transform: rotate(0.4deg);  transform-origin: 618px 90px; }

.mech__flow { fill: none; stroke: var(--color-muted); stroke-width: 1.4; stroke-linecap: round; }
.mech__flow--live {
  stroke: var(--color-accent);
  stroke-dasharray: 5 5;
  animation: mech-flow 2.4s linear infinite;
}
@keyframes mech-flow { to { stroke-dashoffset: -20; } }

/* The line is solid and complete when still — not a gap-toothed dashed remnant. */
@media (prefers-reduced-motion: reduce) {
  .mech__flow--live { animation: none; stroke-dasharray: none; }
}
```

**Use when** the brief is "show how it works" — a dev tool, a pipeline, a data flow. **Avoid when** there are more than five nodes (that's a diagram tool's job) or the topology isn't linear.

### Recipe 2 · Specimen strip — draw the real output

A row of swatches, bars, or type samples rendered **from the product's actual values**. The strongest enrichment available to a technical brief, because it is not an illustration *of* the thing — it *is* the thing.

```css
.spec { display: grid; grid-template-columns: repeat(auto-fit, minmax(3rem, 1fr)); gap: var(--space-3xs); }
.spec__chip {
  aspect-ratio: 1;                          /* reserved — cannot shift (gate 49) */
  border: 1px solid var(--color-rule);
  border-radius: var(--radius);
  background: var(--sw);                    /* the real value, passed in as data */
}
```

The colours arrive as data (a `--sw` custom property per chip), not as stylesheet literals — so the stylesheet still hardcodes no colour of its own and gate 15 holds.

**The honesty rule (gate 30) is load-bearing here.** A specimen strip of *invented* output is worse than no specimen: it is a fabricated proof of the exact claim the page is making. If the values aren't real, don't draw them.

### Recipe 3 · Single small loop

One element, moving, ≤ 4s. Use when the page is otherwise still and needs one sign of life.

```css
@property --orbit {
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}

.pulse {
  width: 3.5rem; aspect-ratio: 1;
  border: 1px solid var(--color-rule);
  border-radius: 50%;
  display: grid; place-items: center;
}
.pulse__dot {
  width: .4rem; aspect-ratio: 1; border-radius: 50%;
  background: var(--color-accent);
  transform: rotate(var(--orbit)) translateX(1.4rem);   /* at rest: a dot, parked, finished */
  animation: orbit 3.2s linear infinite;
}
@keyframes orbit { to { --orbit: 360deg; } }

@media (prefers-reduced-motion: reduce) {
  .pulse__dot { animation: none; }          /* still a composed mark, not a broken one */
}
```

**One loop per page.** Two competing loops read as anxious, and Keel caps the page at ~3 motion primitives total ([`motion.md`](motion.md)).

### Recipe 4 · Rule-and-numeral figure

Hairlines, a measured gap, and a mono numeral — a drawn *measurement* rather than a picture. Suits technical and editorial pages where a literal illustration would be twee, and it is nearly free.

```css
.fig { display: grid; gap: var(--space-2xs); }
.fig__bar { height: 1px; background: var(--color-rule); transform-origin: left; }
.fig__bar--live { height: 2px; background: var(--color-accent); transform: scaleX(var(--pct, 1)); }
.fig__label { font-family: var(--font-mono); font-size: var(--text-xs); color: var(--color-muted); }
```

Scale with `transform: scaleX()`, never `width` — gate 23. The bar's resting state is its true length; if you animate it in, animate `from { transform: scaleX(0) }`, so the base remains correct.

---

## The four habits

What every recipe above shares — the difference between drawn and generated:

1. **`@property` for interpolation.** Typed custom properties give GPU-composited animation with zero JS.
2. **Controlled asymmetry.** ±1° rotations, an 80ms delay between two "identical" elements, leaves at +25° and −30°. Perfect symmetry reads as algorithmic; slight imprecision reads as made by hand.
3. **Opacity layering for secondary detail.** Sub-labels at 60%, veins at 0.6, secondary rules in `--color-muted`. The hierarchy of opacity is the hierarchy of attention.
4. **Mono labels grounding the drawing in fact.** A diagram earns its place by being *accurate*. `--font-mono` at 10px on a real value signals that it is data, not decoration.

---

## Anti-patterns

- **An animation the drawing depends on.** The base state must be the finished drawing. See the rule at the top — it is the whole file in one line.
- **Hardcoded colour in the artwork.** Gate 15. It can't re-theme and it breaks in dark mode.
- **Fake chrome.** A hand-drawn browser bar, phone frame, or code-window title bar with three dots is gate 32 — one of the strongest AI tells there is. If you want to show the product, use a real capture in a `<figure>`.
- **Animating `width`, `height`, `top`, or `left`.** Gate 23. Reflows every frame. Use `transform`.
- **Eight nested wrapper divs.** A pure-CSS illustration should fit in one to three elements. Deep nesting reads as "I gave up structuring this."
- **A raw Figma export.** Run SVGOMG.
- **Linear easing on everything.** `--ease-out` at minimum. It is the difference between *moving* and *alive*.
- **Reaching for a library.** Importing 50KB of animation runtime for a single fade that `transition: opacity var(--dur-slow) var(--ease-out)` does in zero bytes. On a Keel page it also drags a hero onto the client for no reason.

---

*Adapted from the custom-craft discipline in [Hallmark](https://github.com/nutlope/hallmark) (MIT). Re-derived in Keel tokens; the base-is-drawn rule, the token-reference requirement, and the reduced-motion-completeness rule are Keel's own, and they close a real gap — the standard draw-on recipe leaves the illustration invisible when its animation doesn't run.*
