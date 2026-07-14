# Worked example — "Wharfline"

One brief carried the whole way: intent → seed → computed tokens → real code that is correct on first server paint. Every colour value below was produced by [`theming-engine.py`](theming-engine.py) and contrast-verified; you can reproduce it by running the file with this seed.

---

## 1. The brief

> *"Build the landing page for **Wharfline** — cold-chain logistics observability. It watches temperature and location across refrigerated freight and tells operations teams when a shipment is about to breach. Audience: logistics ops leads and the platform engineers who integrate us. Use case: start a trial or book a demo. Tone: technical, precise, cool. It's a Next.js app; we want dark mode."*

## 2. Context gate

- **Audience** — logistics ops leads + integrating platform engineers.
- **Use case** — one primary action: **start a trial** (secondary: book a demo).
- **Tone** — technical, precise, cool.
- **Genre** — the brief signals a developer/infra/B2B tool → **technical** (modern-minimal school).
- **Stack** — Next.js App Router, dark mode wanted → SSR correctness is in scope from the start.

## 3. Structure picks (stated before any code)

> Macrostructure: **Stat-led**. Nav: **nav-command-pill** (technical audience, not a marketing bar). Hero: **hero-stat-led** (a live figure leads, paired with a worded headline so it's never a bare number). Footer: **footer-single-line** (not the 4-column default). Differs from any prior build on macrostructure and theme.

## 4. Seed → theme

Seed = the brand + descriptor; anchor = the "cool/technical" tone → `steel-blue`; genre = `technical`.

```
seed   = "Wharfline · cold-chain logistics observability"
anchor = steel-blue        genre = technical
→ hash 3707062074 · hue 233 · chroma 0.125 → 0.111 (gamut-fit) · mode light
→ display Space Grotesk · body Inter Tight · mono Geist Mono
```

Verified contrast: ink/paper **16.6:1** · muted/paper **5.05:1** · accent-ink/accent **4.68:1** · accent/paper **4.54:1** — all pass, all inside sRGB (the accent was auto-fitted from L55% → L54% to clear the CTA floor, and its chroma gamut-fit from 0.125 → 0.111 because sRGB cannot hold 0.125 at that lightness and hue).

## 5. Preview block (emitted before code, so the user can redirect)

```markdown
**Keel**

- **Macrostructure** · Stat-led
- **Theme** · seed "Wharfline…" · anchor steel-blue · light paper · steel-blue accent · Space Grotesk + Inter Tight
- **Nav / Hero / Footer** · nav-command-pill / hero-stat-led / footer-single-line
- **Sections** · Hero (stat-led) · Live breach panel · How it integrates · Pricing · CTA · Footer
- **Motion** · counter (below-fold) · focus-ring · nav-pill active — all reduced-motion-safe
- **SSR** · Next App Router · blocking theme script · next/font · breach panel streamed via Suspense
- **Slop test** · 47 / 47 applicable ✓ (media gates 48–51 N/A — no imagery) (run after build)
```

## 6. Generated code

### `tokens.css` — computed, locked, both modes (same hue, only L/C move)

```css
/* Keel · seed:"Wharfline · cold-chain logistics observability" · anchor:steel-blue · genre:technical
 * hue:233 · chroma:0.111 · mode:light · display:Space Grotesk · body:Inter Tight
 * contrast: fitted, all-pass · gamut: sRGB-fit · ssr: next-app-router */
:root {
  --color-paper:      oklch(97% 0.010 233);
  --color-paper-2:    oklch(94% 0.012 233);
  --color-rule:       oklch(86% 0.014 233);
  --color-muted:      oklch(52% 0.010 233);
  --color-ink-2:      oklch(34% 0.012 233);
  --color-ink:        oklch(20% 0.014 233);
  --color-accent:     oklch(54% 0.111 233);   /* C gamut-fit from 0.125 — sRGB max at this L/H */
  --color-accent-2:   oklch(50% 0.103 233);   /* accent hover — one L step down, still ≥4.5 on ink */
  --color-accent-ink: oklch(98% 0.010 233);
  --color-focus:      oklch(59% 0.121 233);   /* C gamut-fit from 0.165 */

  --font-display: var(--font-space-grotesk), ui-sans-serif, sans-serif;
  --font-body:    var(--font-inter-tight), ui-sans-serif, sans-serif;
  --font-mono:    var(--font-geist-mono), ui-monospace, monospace;

  --space-3xs: .25rem; --space-2xs: .5rem; --space-xs: .75rem; --space-sm: 1rem;
  --space-md: 1.5rem; --space-lg: 2.5rem; --space-xl: 4rem; --space-2xl: 6rem; --space-3xl: 9rem;

  --text-sm: .875rem; --text-base: 1rem; --text-lg: 1.25rem; --text-xl: 1.5rem;
  --text-2xl: 2rem; --text-3xl: 2.75rem;
  --text-display: clamp(2.75rem, 1.6rem + 4.6vw, 5rem);

  --ease-out: cubic-bezier(.16,1,.3,1); --ease-in: cubic-bezier(.7,0,.84,0);
  --ease-in-out: cubic-bezier(.65,0,.35,1);
  --dur-fast: 120ms; --dur-base: 200ms; --dur-slow: 320ms;
  --radius: 6px;
}
:root[data-theme="dark"] {
  --color-paper:      oklch(16% 0.012 233);
  --color-paper-2:    oklch(20% 0.014 233);
  --color-rule:       oklch(30% 0.014 233);
  --color-muted:      oklch(62% 0.010 233);
  --color-ink-2:      oklch(78% 0.010 233);
  --color-ink:        oklch(94% 0.008 233);
  --color-accent:     oklch(72% 0.105 233);   /* dark: +L, −C, same hue */
  --color-accent-ink: oklch(16% 0.012 233);
  --color-focus:      oklch(78% 0.134 233);   /* C gamut-fit from 0.155 */
}
html, body { overflow-x: clip; }              /* gate 44 */
body { background: var(--color-paper); color: var(--color-ink);
       font-family: var(--font-body); line-height: 1.55; }
@media (prefers-reduced-motion: reduce) {     /* gate 24 */
  *, *::before, *::after { animation-duration: .001ms !important; transition-duration: .001ms !important; }
}
```

### `app/layout.tsx` — the SSR seam: theme-before-paint + `next/font` wired to tokens

```tsx
import './tokens.css';
import { Space_Grotesk, Inter_Tight } from 'next/font/google';
import { GeistMono } from 'geist/font/mono';

const display = Space_Grotesk({ subsets: ['latin'], weight: ['400','700'],
  display: 'swap', variable: '--font-space-grotesk' });
const body = Inter_Tight({ subsets: ['latin'], weight: ['400','600'],
  display: 'swap', variable: '--font-inter-tight' });

// Runs synchronously, before first paint. Prevents the dark-mode flash (gate 34).
const themeScript = `!function(){try{var s=localStorage.getItem('theme'),
d=window.matchMedia('(prefers-color-scheme: dark)').matches;
document.documentElement.dataset.theme=s||(d?'dark':'light')}catch(e){}}();`;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning
      className={`${display.variable} ${body.variable} ${GeistMono.variable}`}>
      <head><script dangerouslySetInnerHTML={{ __html: themeScript }} /></head>
      <body>
        <a href="#main" className="skip-link">Skip to content</a>
        {children}
      </body>
    </html>
  );
}
```

### `app/page.tsx` — a Server Component; interactivity is pushed to leaves

```tsx
import { Suspense } from 'react';
import { ThemeToggle } from './ThemeToggle';        // 'use client' leaf
import { BreachPanel } from './BreachPanel';         // async server component (data)
import { BreachSkeleton } from './BreachSkeleton';

export default function Page() {
  return (
    <main id="main">
      {/* Hero: stat-led, static, server-rendered → zero JS, visible without hydration */}
      <section className="hero">
        <nav className="pill">
          <span className="pill__mark">Wharfline</span>
          <a href="#integrate">Integrate</a><a href="#pricing">Pricing</a>
          <ThemeToggle />
          <a href="/trial" className="btn">Start trial</a>
        </nav>
        <p className="hero__stat"><span className="mono">−0.4&thinsp;°C</span> drift, 11 min to breach.</p>
        <h1 className="hero__title">Know the shipment&rsquo;s temperature before the shipment does.</h1>
        <p className="hero__lede">Live temperature and location across refrigerated freight,
          with a breach clock your ops team can act on. Drop-in OTLP; no agent.</p>
        <div className="hero__cta">
          <a href="/trial" className="btn btn--primary">Start trial</a>
          <a href="/demo" className="btn btn--ghost">Book a demo</a>
        </div>
      </section>

      {/* Live data streams in; hero was interactive the whole time (gate 41) */}
      <section aria-live="polite">
        <Suspense fallback={<BreachSkeleton />}>
          <BreachPanel />
        </Suspense>
      </section>
      {/* …integrate / pricing / cta / footer… */}
    </main>
  );
}
```

### `app/ThemeToggle.tsx` — the only hydrated island, and the `mounted` pattern

```tsx
'use client';
import { useEffect, useState } from 'react';

export function ThemeToggle() {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  function toggle() {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;     // no re-mount
    localStorage.setItem('theme', next);
  }
  // First client render matches the server (label is static) → no mismatch (gate 36).
  return (
    <button className="toggle" onClick={toggle} aria-label="Toggle colour theme">
      {mounted ? (document.documentElement.dataset.theme === 'dark' ? 'Light' : 'Dark') : 'Theme'}
    </button>
  );
}
```

### `app/BreachSkeleton.tsx` — a layout-matched fallback, not a spinner (gate 41)

```tsx
export function BreachSkeleton() {
  // same grid + box heights as BreachPanel → zero layout shift when data arrives
  return (
    <div className="breach breach--skeleton" aria-hidden="true">
      {Array.from({ length: 4 }).map((_, i) => (
        <div key={i} className="breach__row"><span className="sk sk--wide" /><span className="sk" /></div>
      ))}
    </div>
  );
}
```

### Key page CSS (token-only, off-axis hero, instant focus ring)

```css
.hero { display: grid; gap: var(--space-md); padding: var(--space-2xl) var(--space-lg) var(--space-3xl);
        max-width: 68ch; }                                   /* not centred-everything (gate 5) */
.hero__stat { font-family: var(--font-mono); color: var(--color-accent); font-size: var(--text-lg); }
.hero__title { font-family: var(--font-display); font-weight: 700; font-style: normal; /* roman (gate 7) */
               font-size: var(--text-display); line-height: 1.04; letter-spacing: -.02em;
               overflow-wrap: anywhere; min-width: 0; }       /* long-word wrap */
.hero__lede { color: var(--color-ink-2); max-width: 60ch; }
.hero__cta { display: flex; gap: var(--space-sm); align-items: center; }
.btn { font: inherit; border-radius: var(--radius); padding: var(--space-2xs) var(--space-md);
       white-space: nowrap; transition: background var(--dur-base) var(--ease-out); }
.btn--primary { background: var(--color-accent); color: var(--color-accent-ink); }  /* accent-ink (gate 27) */
.btn--primary:hover { background: var(--color-accent-2); }        /* token, not inline (gate 15) */
.btn:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; } /* instant (gate 25) */
.skip-link { position: absolute; left: -9999px; }
.skip-link:focus { left: var(--space-sm); top: var(--space-sm); }
```

## 7. Slop test

47 / 47 applicable gates pass (media gates 48–51 are N/A — this build is data/typography-led with no imagery). The load-bearing ones for this build: **5** (hero is off-axis, max-width, left-aligned — not centred-everything), **7** (title is roman), **14** (accent is the stat + one CTA + focus ring, well under 5%), **27** (`--color-accent-ink` on the primary button), **34** (blocking theme script), **35** (hero is static server HTML, visible with no JS), **36** (the only client state is deferred behind `mounted`), **41** (breach panel streams behind a layout-matched skeleton with `aria-live`), **42** (`next/font`, no duplicate `<link>`), **44** (`overflow-x: clip`).

## 8. What the seed guarantees

Re-run `theming-engine.py` with this seed a year from now and the palette is byte-identical — the design review is reproducible. Change the brand to "Northwind" and the hue moves to a different band; there is no shared "Keel look" to recognise. That is the difference between a computed theme and a catalog.
