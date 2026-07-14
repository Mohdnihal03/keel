# Media & performance

## Thesis

On a landing page, media is not decoration — it is the largest, heaviest, latest-arriving thing on the page, and it decides two of your three Core Web Vitals. The hero image is almost always the **Largest Contentful Paint (LCP)** element. Every unsized image, embed, and iframe is a **Cumulative Layout Shift (CLS)** waiting to fire the moment it loads.

AI-generated pages get this wrong in ways that never show in a hot local preview and only surface on a real server render over a throttled connection: lazy-loaded heroes, missing `width`/`height`, a 2400px JPEG poured into a 480px slot, autoplaying videos as the LCP, fabricated screenshots. Treat media as a performance surface first and an aesthetic one second. Get the bytes and the box right, then make it look good.

See [ssr-and-hydration.md](ssr-and-hydration.md) for the first-paint model this all serves.

## The LCP hero image

The hero image is the LCP element on most marketing pages. Four things must be true or the LCP number blows up:

1. **Reserve its box.** Set explicit `width`/`height`, or `fill` inside a container with a known aspect-ratio. No reserved box means the image drops in after layout and shifts everything below it (CLS) while also delaying a stable paint.
2. **Prioritise it.** In `next/image` set `priority` — this emits `fetchpriority="high"` and drops it out of lazy-loading. The classic self-inflicted LCP killer is `loading="lazy"` on the hero: the browser waits until layout settles to even *start* the fetch, so your biggest paint begins last. Never lazy-load the LCP element.
3. **Serve the right size.** A correct `sizes` attribute stops the browser downloading a 2000px source for a 400px slot. Wrong `sizes` is wasted bytes and a slower LCP on mobile, where it matters most.
4. **Everything below the fold stays lazy.** `priority`/eager loading is for the LCP element only. Eager-loading the whole page just starves the one image that counts.

### Next.js (`next/image`)

```tsx
import Image from "next/image";
import hero from "@/public/hero.jpg"; // static import → width/height + blur inferred

<Image
  src={hero}
  alt="Dashboard showing weekly revenue trending up"
  priority                     // LCP: eager + fetchpriority=high
  sizes="(max-width: 768px) 100vw, 640px"
  placeholder="blur"           // free with a static import
  className="hero-img"
/>
```

For a remote `src`, pass explicit `width`/`height` (or `fill` + a sized parent) — Next cannot infer them.

### Vanilla HTML

```html
<img
  src="/hero-640.jpg"
  srcset="/hero-480.avif 480w, /hero-640.avif 640w, /hero-1280.avif 1280w"
  sizes="(max-width: 768px) 100vw, 640px"
  width="1280" height="720"    /* intrinsic ratio → reserves box, kills CLS */
  fetchpriority="high"         /* the vanilla equivalent of priority */
  decoding="async"
  alt="Dashboard showing weekly revenue trending up"
/>
```

Note there is **no** `loading="lazy"` here — this is the LCP image. Add `loading="lazy"` to every image *below* the fold instead.

## Formats & weight

Serve modern formats with a fallback. Order: **AVIF, then WebP, then JPEG/PNG**. AVIF wins on photographic heroes; WebP is the safe universal step down.

```html
<picture>
  <source type="image/avif" srcset="/hero-640.avif 640w, /hero-1280.avif 1280w" sizes="640px">
  <source type="image/webp" srcset="/hero-640.webp 640w, /hero-1280.webp 1280w" sizes="640px">
  <img src="/hero-640.jpg" width="1280" height="720" fetchpriority="high" alt="…">
</picture>
```

`next/image` negotiates AVIF/WebP automatically from the `Accept` header and resizes per `sizes` — you supply one source, it emits the `<picture>`/`srcset` machinery. Configure `formats: ['image/avif', 'image/webp']` in `next.config` if you want AVIF first.

Weight discipline:

- Cap a hero at roughly **150–200 KB** after compression. If a source won't compress under that at quality, it is the wrong crop or wrong resolution, not a reason to ship 900 KB.
- Compress everything — `sharp`, `squoosh`, or the build pipeline. An uncompressed PNG hero is the single most common slop payload.
- Match pixels to slot: a 640px-wide slot on a 2x screen needs 1280px, not 2400px.

## CLS prevention

Every element that loads asynchronously must reserve its box **before** it loads. Images with `width`/`height` do this for free (the browser computes `aspect-ratio` from them). For `fill` images, embeds, iframes, and ad slots, reserve the box yourself:

```css
.media-box {
  aspect-ratio: 16 / 9;
  width: 100%;
  background: var(--color-paper-2); /* visible while the asset loads */
  border-radius: var(--radius);
  overflow: hidden;
}
.media-box > * { width: 100%; height: 100%; object-fit: cover; }
```

Any `<iframe>` (video embed, map, widget) with no reserved box will shove content down when it loads. Wrap it in a `.media-box` or give it explicit dimensions.

Fonts cause CLS too — a late-swapping webfont reflows every headline. Handle it with `next/font` (self-hosted, `size-adjust`, no layout shift on swap); see [ssr-and-hydration.md](ssr-and-hydration.md).

## Hero video

A hero video is never the lazy LCP and never autoplays with sound. Rules:

- **`poster`** — a compressed still that paints instantly while the video streams. Make the poster the LCP candidate (a `priority` image), then swap in the video after load. The poster is what the user sees at first paint; treat it with the same size/format discipline as a hero image.
- **`preload="metadata"`** — fetch dimensions and duration, not the whole file. `preload="auto"` on a hero drags megabytes into the critical path.
- **`muted` + `playsinline` + `loop`** for autoplay. Browsers block autoplay with sound outright, and audio that starts on load is hostile. `playsinline` stops iOS hijacking to fullscreen.
- **Respect `prefers-reduced-motion`.** Offer a still (the poster) to reduced-motion users instead of playing. See [motion.md](motion.md).

```html
<figure class="media-box">
  <video
    poster="/hero-poster.avif"
    preload="metadata"
    muted playsinline loop
    width="1280" height="720"
    aria-label="Product walkthrough">
    <source src="/hero.webm" type="video/webm">
    <source src="/hero.mp4" type="video/mp4">
  </video>
</figure>
```

```js
// Autoplay only when motion is welcome; otherwise the poster stays.
const v = document.querySelector("video");
if (!matchMedia("(prefers-reduced-motion: reduce)").matches) v.play();
```

## Loading & skeletons

Two honest placeholder strategies while an image loads:

1. **`placeholder="blur"`** in `next/image` — a tiny inlined `blurDataURL`. Free with a static import; for remote images generate the base64 blur at build time.
2. **A `--color-paper-2` box at the correct aspect-ratio** (the `.media-box` above) — the plainest, most robust option and the fallback everywhere `next/image` isn't in play.

The skeleton must match the final rendered dimensions exactly, or dismissing it causes the very CLS you were avoiding. Shimmer is optional and must respect reduced motion:

```css
.skeleton { background: var(--color-paper-2); border-radius: var(--radius); }
@media (prefers-reduced-motion: no-preference) {
  .skeleton { animation: shimmer var(--dur-slow) var(--ease-out) infinite; }
}
@keyframes shimmer { 50% { opacity: .6; } }
```

Tie image/media Suspense boundaries to a skeleton of the same size — never a spinner that collapses to content. See [ssr-and-hydration.md](ssr-and-hydration.md) for Suspense placement and [copywriting.md](copywriting.md) for loading-state copy.

## Icons & logos

- **Icons: inline SVG, one library, no exceptions.** Pick a single set (Lucide, Heroicons, Phosphor — one) and stay in it. Mixing libraries reads as slop because stroke widths and grids don't match. Never use emoji as UI icons. See [anti-patterns.md](anti-patterns.md).
- Inline SVG (not `<img src=icon.svg>`) so icons inherit `currentColor`, add no requests, and don't flash in late.
- **Logo walls: real logos or an honest placeholder.** Never fabricate a brand's logo, never redraw one from memory, never invent "customers." If you don't have permission-cleared assets, use labelled grey boxes at a uniform aspect-ratio and tell the user what to supply.

## No fabricated, no redrawn

- **Do not ship invented stock photos as if final.** A plausible-looking AI photo presented as the real product or a real person is slop and a trust problem.
- **Do not hand-draw fake chrome.** Do not build a CSS "browser window," phone frame, or IDE out of divs to fake a screenshot. Use a **real screenshot** in a `<figure>`, optionally in a genuine device frame with a real captured image inside.
- **When the user hasn't supplied assets, be honest.** Ship a labelled grey box at the correct aspect-ratio (`--color-paper-2`, a `--color-rule` border, a "Hero image — 1280×720" label) or ask for the asset. A truthful placeholder beats a fabricated final. See [anti-patterns.md](anti-patterns.md).

```html
<div class="media-box" style="display:grid;place-items:center;border:1px dashed var(--color-rule)">
  <span style="color:var(--color-ink-2)">Hero image — supply 1280×720 AVIF</span>
</div>
```

## Accessibility

- Meaningful images get descriptive `alt` that states what the image *communicates*, not "image of…".
- Decorative images get `alt=""` (and `aria-hidden="true"` on decorative inline SVG) so screen readers skip them.
- A hero that carries no information beyond mood is decorative — empty `alt`. A product screenshot that shows a feature is meaningful — describe the feature.

See [accessibility.md](accessibility.md).

## Pre-ship checklist

- [ ] LCP element identified; `priority` / `fetchpriority="high"` set on it, `loading="lazy"` on everything below the fold.
- [ ] Every image/video/iframe/embed reserves its box (`width`+`height` or `aspect-ratio`) — no CLS on load.
- [ ] Modern format served (AVIF/WebP) with a fallback; hero under ~150–200 KB compressed.
- [ ] `sizes` matches the real slot at each breakpoint — no oversized downloads.
- [ ] Hero video has a `poster`, `preload="metadata"`, `muted`+`playsinline`+`loop`, and a reduced-motion still.
- [ ] Skeletons/blur placeholders match final dimensions; shimmer respects `prefers-reduced-motion`.
- [ ] One icon library, inline SVG, no emoji icons; logos are real or honest placeholders.
- [ ] No fabricated photos, no redrawn brand logos, no CSS-faked chrome — real screenshots or labelled placeholders.
- [ ] `alt` handled: meaningful images described, decorative images `alt=""`.

Run the result past [slop-test.md](slop-test.md).
