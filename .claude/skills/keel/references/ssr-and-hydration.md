# SSR & hydration correctness

Keel's second reason to exist. Most real landing pages in 2026 ship through Next.js, Remix/React Router, or SvelteKit — they are **server-rendered and then hydrated**, not static `.html` files. A page that looks flawless in a screenshot can still be broken on the server: it flashes the wrong colours on first paint, throws a hydration mismatch that blanks a section, or blocks the whole route on one slow fetch. None of that shows up in a visual review. All of it shows up for the user.

This file is the correctness layer. Load it whenever the target is a framework project (pre-flight found `next`, `@remix-run/*`, `react-router`, `@sveltejs/kit`, or `astro` with islands) — that is most builds. A pure vanilla-HTML artifact skips most of it, but still reads § Dark-mode without the flash.

The failure modes, worst first:

1. Dark-mode / theme flash (FOUC).
2. Hydration mismatch.
3. Server/client boundary mistakes.
4. Loading state (streaming & Suspense).
5. `next/font` misuse.

---

## 1. Dark-mode without the flash

**The bug.** The server has no `localStorage` and no media query — it cannot know the visitor's theme. So the HTML ships with a default (usually light). The browser paints that default, *then* React/JS hydrates, reads the saved preference, and flips to dark. The visitor sees a white flash for 100–400ms on every load. This is the single most common "looks broken" SSR bug, and Keel's theming engine makes it *more* likely because Keel pages are theme-driven by a `data-theme` attribute.

**The fix — a blocking inline script in `<head>`, before any paint.** It is tiny, it is synchronous, it runs before the browser paints the body, and it sets `data-theme` on `<html>` so the very first paint is correct. It is the one place a blocking script is correct.

Next.js App Router — put it in `app/layout.tsx`, and set `suppressHydrationWarning` on `<html>` because the script legitimately mutates the attribute the server didn't set:

```tsx
// app/layout.tsx
const themeScript = `
(function () {
  try {
    var saved = localStorage.getItem('theme');
    var sysDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    var theme = saved || (sysDark ? 'dark' : 'light');
    document.documentElement.dataset.theme = theme;
  } catch (e) {}
})();
`;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

Rules that make this safe and correct:

- It must be **inline and synchronous** — no `src`, no `async`, no `defer`. A deferred script paints the wrong theme first, which is the bug you were fixing.
- It reads `localStorage` first, then the system preference. Wrap in `try/catch` — `localStorage` throws in some privacy modes.
- `suppressHydrationWarning` goes **only on the `<html>` element**, and only because this one attribute is intentionally server/client-divergent. It is not a licence to silence mismatches elsewhere (see § 2).
- The toggle that changes the theme writes `localStorage` *and* updates `document.documentElement.dataset.theme` — it never re-mounts the tree.
- Tokens are declared for both modes with the **same anchor hue** (`:root { … }` and `:root[data-theme="dark"] { … }`), per [`theming-engine.md`](theming-engine.md) and [`color.md`](color.md).

SvelteKit: the same script goes in `src/app.html` inside `<head>` (plain `<script>`, no framework needed — `app.html` is static shell). Remix / React Router: inject it in `root.tsx` before `<Scripts />`, same `dangerouslySetInnerHTML` pattern. Astro: a `<script is:inline>` in the layout `<head>`.

**Do not** "fix" the flash by disabling SSR for the whole page (`ssr: false`, `'use client'` on the root) — that throws away SEO, the LCP win, and the point of the framework. The blocking script is ~8 lines and costs nothing.

---

## 2. Hydration mismatch

**The bug.** Hydration assumes the DOM React builds on the client is identical to the HTML the server sent. When they differ, React (in production) discards the server HTML for that subtree and re-renders on the client — content flickers, disappears, or resets — and logs `Hydration failed because the server rendered HTML didn't match the client`. On a landing page this most often blanks a hero or a dynamic stat.

**The causes, and the fix for each:**

| Cause | Why it diverges | Fix |
| --- | --- | --- |
| `Date.now()`, `new Date()`, `Math.random()` in render | Server value ≠ client value | Compute in a `useEffect` (client-only) or pass a server-stamped value down as a prop. Never in the render body of a shared component. |
| Locale/timezone formatting (`toLocaleString`, `Intl` with no explicit locale) | Server locale ≠ browser locale | Pass an explicit `locale` and `timeZone`; or format client-side after mount. |
| Reading `window`, `document`, `localStorage`, `matchMedia` during render | Undefined on server → different branch | Gate behind a `mounted` flag (below) or `useEffect`. |
| Invalid HTML nesting (`<p><div>`, `<a><a>`, `<button><button>`, block inside `<p>`) | Browser auto-corrects the DOM; React's vDOM doesn't | Fix the markup. This is the sneakiest cause — it looks fine visually. |
| Non-deterministic ids (`Math.random()` keys, `id={uuid()}`) | New id per environment | Use React's `useId()` for stable server/client ids. |
| Browser-extension / Grammarly attributes on `<body>` | Extensions mutate the DOM pre-hydration | `suppressHydrationWarning` on `<body>` only, or ignore — it's benign. |

**The `mounted` two-pass pattern** — the safe way to render something that can *only* be known on the client (e.g. the current theme label, a relative timestamp), without a mismatch:

```tsx
'use client';
import { useState, useEffect } from 'react';

function useMounted() {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  return mounted;
}

// render the SAME thing the server rendered until mounted, THEN enhance:
function ThemeLabel() {
  const mounted = useMounted();
  if (!mounted) return <span>Theme</span>;          // server + first client paint agree
  return <span>{document.documentElement.dataset.theme}</span>;
}
```

The key discipline: **the first client render must match the server render**, so the branch that differs is deferred to *after* mount. This is different from `suppressHydrationWarning`, which merely silences the warning without fixing the divergence — use the flag, not the suppressor, for anything the user can see.

---

## 3. Server/client component boundaries (App Router)

**The model.** In the Next.js App Router, components are **Server Components by default**. They render on the server, ship zero JS, and can read the filesystem / database / secrets directly. A component becomes a **Client Component** — shipped to the browser and hydrated — only when its file (or an ancestor it's imported from) starts with `'use client'`. Everything a Client Component imports becomes client code too.

**The discipline for a landing page:**

- **Keep the page a Server Component.** The hero, copy, feature sections, footer — static content — should be Server Components. They render to HTML with no hydration cost. This is most of the page.
- **Push `'use client'` to the leaves.** Only the genuinely interactive islands need it: the mobile-nav toggle, the theme switcher, a pricing-period toggle, a copy-to-clipboard button, an FAQ accordion. Make each its own small client component; do not slap `'use client'` at the top of the page and drag the whole tree onto the client.
- **Pass serializable props across the boundary.** A Server Component can render a Client Component and pass it strings, numbers, plain objects, and even *JSX children*. It cannot pass functions, class instances, or Dates-as-Dates (serialize to ISO string). Passing `children` down lets a client wrapper (e.g. an animation provider) wrap server-rendered content without making that content client-side:

```tsx
// FadeIn.tsx  — 'use client' island
'use client';
export function FadeIn({ children }: { children: React.ReactNode }) {
  // animates its children on mount; children stay server-rendered HTML
  return <div className="fade-in">{children}</div>;
}

// page.tsx — Server Component
import { FadeIn } from './FadeIn';
export default function Page() {
  return <FadeIn><Hero /></FadeIn>;   // <Hero/> renders on the server
}
```

- **Never import a server-only module into a client component** — a DB client, `fs`, a secret-bearing SDK. It will either leak into the bundle or fail the build. Mark server-only modules with the `server-only` package to fail loudly.
- **`async`/`await` belongs in Server Components** — data fetching happens there. Client Components fetch via `use()` / a data library, not top-level `await`.

---

## 4. Loading states — streaming & Suspense

Server-rendered pages can **stream**: send the shell immediately and fill slow regions as their data resolves. This turns "one slow fetch blocks the whole page" into "the hero is interactive while the testimonials load." A landing page rarely blocks on data, but any above-the-fold dynamic region (a live stat, personalised copy, an embedded feed) should stream rather than delay first paint.

- **`app/loading.tsx`** — an instant route-level fallback shown while the server component tree resolves. Next wraps the route in a Suspense boundary for you.
- **`<Suspense fallback={…}>`** — wrap a specific slow subtree so the rest of the page paints immediately:

```tsx
import { Suspense } from 'react';
export default function Page() {
  return (
    <>
      <Hero />                                {/* instant */}
      <Suspense fallback={<StatsSkeleton />}>
        <LiveStats />                         {/* streams in when ready */}
      </Suspense>
    </>
  );
}
```

**Fallbacks must match the final layout's dimensions** or the content shift causes CLS (Cumulative Layout Shift) — a Core Web Vital. A skeleton is a real design deliverable: same box heights, same grid, muted `--color-paper-2` blocks, a subtle shimmer that respects `prefers-reduced-motion` (see [`motion.md`](motion.md)). A bare centred spinner that collapses to zero height when content arrives is the lazy tell — and it shifts the page.

The fallback's *words* are copy, not decoration — write them per [`copywriting.md`](copywriting.md) (honest, specific: "Loading your usage…" beats a naked spinner past 2s). Wrap streamed regions in an `aria-live="polite"` container so screen readers announce arrival (see [`accessibility.md`](accessibility.md)).

### The Suspense boundary that never streams

A `<Suspense>` boundary is necessary but **not sufficient**. If the region it wraps can be *statically prerendered*, the framework resolves it at build time and bakes the final HTML into the static page. Nothing streams; the skeleton you designed is dead code that no user ever sees. The page still looks correct — which is exactly why this is easy to ship. The build output is the tell:

- `○ (Static)` — the boundary resolved at build. The skeleton never renders.
- `ƒ (Dynamic)` — the region is fetched per request. The skeleton actually streams.

For a genuinely live region (a rate, a live count, anything per-request), opt out of the prerender explicitly:

```tsx
import { unstable_noStore as noStore } from 'next/cache';

async function getRows() {
  noStore();                       // per-request; the Suspense boundary now really streams
  return db.query(/* … */);
}
// or, route-wide:  export const dynamic = 'force-dynamic';
```

**Verify on the wire, not in the source.** Request the page and look at the raw bytes: the skeleton markup must appear *earlier in the response* than the real content, and TTFB should be well under the region's data latency while total transfer time exceeds it. A static prerender gives itself away as a fast TTFB with the *finished* content already inline and the skeleton nowhere in front of it. Note that static prerendering is a perfectly good outcome for content that isn't actually live — the failure is only in believing you are streaming when you are not, and in shipping a skeleton for a region that never defers.

---

## 5. `next/font` usage

`next/font` self-hosts the font at build time: **zero external request, zero layout shift** (it computes a size-adjusted fallback), and no render-blocking round-trip to `fonts.googleapis.com`. On any Next project it is the correct way to load Keel's chosen faces — and you must **not** also add a Google Fonts `<link>`, which re-introduces the external request and a FOUT/FOIT the self-hosting was preventing.

```tsx
// app/layout.tsx
import { Space_Grotesk } from 'next/font/google';

const display = Space_Grotesk({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-display',     // exposes a CSS variable Keel's tokens consume
  weight: ['400', '700'],
});

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={display.variable} suppressHydrationWarning>
      <body>{children}</body>
    </html>
  );
}
```

Then Keel's token references `var(--font-display)` as usual — the font variable and the colour tokens compose. Rules:

- Set `display: 'swap'` so text is visible during load (never invisible/FOIT).
- Use `variable:` and wire it to Keel's `--font-*` token — don't hard-code the family name downstream.
- Only request the `subsets` and `weight`s you use — every extra weight is bytes on the critical path.
- For a local/paid font use `next/font/local` with the file; same `variable` wiring.
- **Vanilla / non-Next projects**: `<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>` + the stylesheet with `&display=swap`, and set a `size-adjust` / matched-fallback `@font-face` to hold layout. See [`typography.md`](typography.md).

---

## Framework quick-map

| Concern | Next.js App Router | Remix / React Router | SvelteKit |
| --- | --- | --- | --- |
| Theme script | inline in `app/layout.tsx <head>` | inline in `root.tsx` before `<Scripts/>` | `src/app.html` `<head>` |
| Client boundary | `'use client'` file directive | components hydrate by default; `clientLoader`/`<ClientOnly>` for client-only | `<script>` in `.svelte` runs client-side; `browser` guard from `$app/environment` |
| Streaming | `loading.tsx` + `<Suspense>` | `defer()` + `<Await>` | `{#await}` with streamed promises from `load` |
| Fonts | `next/font` | `<link>` in `links()` + preload | `@font-face` + preload in `app.html` |

## The correctness checklist (run before shipping any framework build)

- [ ] Blocking inline theme script in `<head>`; first paint is the correct theme; no flash.
- [ ] `suppressHydrationWarning` only on `<html>` (theme) / `<body>` (extensions) — nowhere else.
- [ ] No `Date`/`Math.random`/`window`/`localStorage` in the render body of a server-shared component.
- [ ] No invalid nesting (`<p><div>`, nested `<a>`/`<button>`).
- [ ] `useId()` for any generated id; stable keys.
- [ ] Page is a Server Component; `'use client'` only on interactive leaves; props across the boundary are serializable.
- [ ] Above-the-fold content is visible without JS (entrance animations are additive — see [`motion.md`](motion.md)).
- [ ] Slow regions are `<Suspense>`-wrapped with layout-matched, reduced-motion-safe skeletons and honest fallback copy; `aria-live` on streamed regions.
- [ ] Fonts via `next/font` (or equivalent) with `display:swap`, wired to `--font-*`; no duplicate Google `<link>`.
- [ ] Build runs with **no hydration warnings** in the console.
