# Hero · Media

**Use when** a real image or video sells the product better than words — hardware, physical goods, a UI in motion, a place. **Genre fit:** atmospheric / playful. **This is the SSR/performance-critical hero — the media is the LCP.**

## Structure
Hero anchored by one **real image or video** that fills the frame; text sits *over* or beside it, off-axis (bottom-left corner is the safe default), never a centred block floating dead-centre. The media is the LCP element, so its correctness (format, dimensions, priority) matters more than any effect. Keep text legible with a scrim (a token overlay, not baked into the asset). One headline, one lede, one CTA — the media does the persuading. Constrain the frame's aspect-ratio so it never dictates an unbounded height on mobile.

## Code
```tsx
// Next.js — the image IS the LCP: explicit dimensions, priority, no lazy
import Image from 'next/image';
export function HeroMedia() {
  return (
    <section className="hero-media">
      <Image src="/hero.avif" alt="Kiln firing at dusk" fill sizes="100vw"
             priority className="hero-media__img" />
      <div className="hero-media__scrim" />
      <div className="hero-media__copy">
        <h1 className="hero-media__head">Fired in small batches.</h1>
        <p className="hero-media__lede">Every piece leaves the kiln once, glazed by hand.</p>
        <a className="btn btn--primary" href="/shop">Shop the batch</a>
      </div>
    </section>
  );
}
```
```html
<!-- Video variant: poster, muted, playsInline, preload — NOT the lazy LCP, NOT autoplay-with-sound -->
<video class="hero-media__img" poster="/hero-poster.avif" preload="metadata"
       muted playsinline loop autoplay><source src="/hero.webm" type="video/webm"></video>
```
```css
.hero-media { position: relative; aspect-ratio: 16 / 9; max-height: 88vh; overflow: clip;
              border-radius: var(--radius); }
.hero-media__img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.hero-media__scrim { position: absolute; inset: 0;               /* legibility, token not baked-in */
  background: linear-gradient(0deg, color-mix(in oklab, var(--color-ink) 55%, transparent), transparent 60%); }
.hero-media__copy { position: absolute; left: var(--space-lg); bottom: var(--space-lg);  /* off-axis */
  max-width: 34ch; color: var(--color-paper); }
.hero-media__head { font-family: var(--font-display); font-weight: 700; font-style: normal;
  font-size: clamp(2.5rem, 1.5rem + 5vw, 5rem); line-height: 1.02; letter-spacing: -.02em;
  text-wrap: balance; margin: 0; }
.hero-media__lede { color: var(--color-paper-2); max-width: 40ch; }
.btn:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 3px; }
```

## SSR / hydration note
The image is the **LCP element** — get it right or the page is slow regardless of design. Use `next/image` with explicit `width`/`height` (or `fill` + `sizes`) and **`priority`** (which emits a preload and disables lazy) — **never `loading="lazy"`** on the hero. Serve **AVIF/WebP**. A hero **video** needs a `poster` (paints instantly, becomes the effective LCP), `preload="metadata"`, `muted` + `playsInline`; if it autoplays keep it muted (autoplay-with-sound is blocked and hostile) and never let the video file be the lazy-loaded LCP — the poster carries first paint. Reserve space with `aspect-ratio` so decode causes no CLS. Copy and scrim are static server HTML, visible without JS. Cross-ref `../media-and-performance.md` and `../ssr-and-hydration.md`.

## Diversification knobs
- **Copy placement:** overlaid bottom-left, overlaid bottom-right, or beside the frame in a sidebar.
- **Asset:** still image, muted loop video, or a poster'd click-to-play.
- **Scrim:** bottom gradient, a corner vignette, or a solid inset panel behind the copy.
- **Frame:** full-bleed edge-to-edge vs. inset with `--radius` and a `--color-rule` border.
