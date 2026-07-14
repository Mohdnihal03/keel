# Anti-patterns — the named tells

Every entry here is a *specific* failure you can point at and explain, not an aesthetic complaint. Each has a **Why** (what actually goes wrong) and a **Fix**. These are what the [slop-test](slop-test.md) gates check for. Two families: **visual/structural** tells (the page looks generated) and **runtime/SSR** tells (the page is broken on the server — Keel's distinct territory).

---

## Visual & structural tells

### Gradient text headline
`background-clip: text` filled with a colour gradient on an `<h1>`.
**Why:** it is the single most recognisable AI-marketing signature of the era — every model reaches for it, so it now reads as "a machine wrote this." It also fails contrast unpredictably (the gradient passes over the background at some points) and disappears entirely if the browser doesn't paint the clip.
**Fix:** solid `--color-ink` or `--color-accent`; carry emphasis with weight or a drawn underline.

### Purple-to-blue / purple-to-cyan / orange-to-pink gradient
Any of these two-hue gradients as a hero background or button fill.
**Why:** these exact ramps are the distribution-default palette of every image and code model. Their ubiquity *is* the tell. They also usually violate the one-accent rule.
**Fix:** one accent from the [theming engine](theming-engine.md); if you need depth, a single-hue tint step, not a rainbow.

### Three equal columns of icon-above-heading cards
The `[icon] / Title / one line` tile, ×3, centred.
**Why:** it is the literal default the model emits for "features section." Identical visual weight across three cards means no hierarchy — the reader can't tell what matters. It is the most-shipped section on the generated web.
**Fix:** vary span/size (bento), or make it a document/list, or lead one feature and demote the rest. See [layout-and-structure.md](layout-and-structure.md).

### Centred-everything hero
Eyebrow + title + lede + CTA all stacked on one centred vertical axis, usually `min-height: 100vh`.
**Why:** perfect central symmetry is the lowest-effort composition; it reads as a template because it *is* the template. Nothing on the page earns its position.
**Fix:** centre at most two elements; push the eyebrow or CTA off-axis (margin-aligned, right-flush, numeral-anchored).

### Nested cards / thick coloured side-stripe cards
A card inside a card; or a card with a fat coloured left border.
**Why:** nested elevation is visual noise with no information gain; the side-stripe is a Bootstrap-era alert pattern the model over-applies. Both signal "decorated to look busy."
**Fix:** one elevation level; separate with a hairline `--color-rule` or a `--color-paper-2` surface shift.

### Italic display headers
`font-style: italic` on any heading — above all a single italicised emphasis word inside an upright headline (`Built to <em>think</em>`).
**Why:** it is a top LLM tell; the model uses italic to fake "editorial" without earning it. An all-italic display face reads as a stock template.
**Fix:** roman headers always. Emphasis via weight, `--color-accent`, or a 1–2px drawn underline. Italic survives only as body-copy emphasis.

### Re-drawn UI chrome
Hand-built fake browser bar (URL pill + traffic-light dots), fake phone frame, fake code-window (title bar + dots around a `<pre>`), fake terminal/IDE chrome.
**Why:** the model invents a UI that already exists in the user's environment — and the fake never matches any real OS, so it reads as uncanny. It is one of the strongest "AI-generated" signals.
**Fix:** a real screenshot in a `<figure>` (hairline border at most), or omit the chrome and let content stand.

### Emoji as feature/step/pricing icons; mixed icon libraries
✨🚀⚡🔥🎯✅ as value-prop icons; or Material + Heroicons + Lucide on one page.
**Why:** emoji icons render differently per OS (your ⚡ is someone else's tofu box) and read as placeholder. Mixed libraries have mismatched stroke weights and grids — instantly incoherent.
**Fix:** one icon library, or a custom SVG, or drop the icon and lead with type.

### Aurora blobs / mesh-gradient-on-everything
Animated multi-colour mesh or floating gradient blobs behind the whole page.
**Why:** heavy, distracting, GPU-hungry, and — again — the default "make it look modern" move every model makes. Usually more than one accent, violating the palette.
**Fix:** at most one low-footprint accent-tinted radial (atmospheric genre only), fixed, unanimated.

### Invented metrics / fabricated proof
"10× faster", "trusted by 50,000+ teams", "+47% conversion", fake testimonials, placeholder logos presented as real.
**Why:** it is dishonest, it is a legal/brand risk for the user, and stat-led sections become decorative lies the moment the numbers are made up. A giant number the model invented is worse than no number.
**Fix:** use the user's real figures, or an em-dash placeholder + "metric to confirm", or rebuild the section without the proof slot. Hard rule; see [copywriting.md](copywriting.md).

### Eyebrow on every section / tag-left, heading-right
A mono-caps `01 · THE TOUR` kicker above every section; or the eyebrow in a left column with the heading in a right column on the same row.
**Why:** eyebrows-everywhere is decorative numbering that means nothing; the two-column tag/heading split is the single most reliable *templated-editorial* tell — it screams "SaaS starter template."
**Fix:** eyebrows default OFF; when genuinely ordinal, stack the heading directly *below* the eyebrow in one column. Never the two-column split.

### Mid-render token improvisation
An inline `#hex` / `oklch()` / `font-family:"…"` that bypasses the `:root` token block.
**Why:** the model picked a theme, then forgot it and freestyled a one-off value — the page drifts out of its own system, and the value can't be re-themed or dark-moded.
**Fix:** every colour and font references a named token; a new value is *added* as a named token first.

---

## Runtime & SSR tells (Keel's territory)

These don't show in a screenshot. They show the moment the page loads on a real server-rendered stack. Full treatment in [ssr-and-hydration.md](ssr-and-hydration.md).

### Theme flash on load (FOUC)
The page paints light, then snaps to the saved dark theme after hydration.
**Why:** the server can't read `localStorage` or the OS preference, so it ships a default the client then overrides — a visible 100–400ms flash on *every* load. Keel pages are `data-theme`-driven, which makes this near-certain if unaddressed.
**Fix:** a synchronous blocking inline script in `<head>` that sets `data-theme` before first paint. ~8 lines.

### Above-the-fold content hidden until JS
`opacity: 0` / `initial={{opacity:0}}` on the hero, revealed by an IntersectionObserver or `whileInView` on mount.
**Why:** during SSR (before hydration) and if JS is slow/blocked/errored, the content is *invisible* — a blank hero. The entrance animation has become a load-bearing dependency for content existing at all.
**Fix:** content visible by default in CSS; entrance animation is additive and only enhances after mount. Animate below-the-fold only, or gate on a `[data-mounted]` that defaults to visible. See [motion.md](motion.md).

### `'use client'` on the whole tree
The directive at the top of the page/layout, dragging every child onto the client.
**Why:** it throws away the framework's central win — server components ship zero JS. The whole static page (hero, copy, footer) now hydrates needlessly, inflating bundle and TBT, and loses server-only data access.
**Fix:** keep the page a Server Component; push `'use client'` to interactive leaves only.

### Non-determinism in the render body
`Date.now()`, `new Date()`, `Math.random()`, `window`/`localStorage` reads during render of a server-shared component.
**Why:** the server value differs from the client value → hydration mismatch → React discards and re-renders the subtree, flickering or blanking it.
**Fix:** compute in `useEffect` (client-only) or pass a server-stamped prop down; `useId()` for ids; the `mounted` two-pass pattern for client-only display.

### `suppressHydrationWarning` as a silencer
Sprinkling it to make the console warning go away.
**Why:** it *hides* the mismatch without fixing the divergence — the content still flickers/resets for the user; you've just muted the alarm. It's correct only on `<html>` (the intentional theme attribute) and `<body>` (benign extension attributes).
**Fix:** fix the actual divergence with the `mounted` pattern; reserve the suppressor for the two legitimate spots.

### Spinner-only Suspense / loading fallback that shifts layout
A bare centred spinner as a `loading.tsx` / `<Suspense fallback>`, collapsing to zero height when content arrives.
**Why:** it causes CLS (a Core Web Vital) as the page jumps, and it tells the user nothing. A skeleton that doesn't match the final dimensions shifts just as badly.
**Fix:** a layout-matched skeleton (same box heights/grid, `--color-paper-2` blocks, reduced-motion-safe shimmer) with honest fallback copy; `aria-live` on the region.

### Duplicate / render-blocking font loading
`next/font` **and** a `<link href="fonts.googleapis.com">` for the same face; or a blocking Google Fonts stylesheet with no `display=swap`.
**Why:** double-loads the font (wasted bytes on the critical path) and re-introduces the external round-trip and FOUT/FOIT that self-hosting removed.
**Fix:** one loader. On Next, `next/font` with `display:'swap'`, wired to `--font-*`; no duplicate `<link>`. See [ssr-and-hydration.md § next/font](ssr-and-hydration.md).

### Disabling SSR to dodge a hydration bug
`ssr: false`, or `'use client'` on root, to make a mismatch disappear.
**Why:** it "fixes" the symptom by throwing away SEO, the fast first paint, and the reason the project uses a server framework at all. The bug is still there; you've just stopped rendering on the server.
**Fix:** find the actual divergence (see above) and fix it; keep SSR on.
