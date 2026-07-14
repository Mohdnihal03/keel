---
name: keel
description: >-
  Anti-AI-slop design skill for landing and marketing pages — plus light
  auth-adjacent pages like pricing and gated content — that must look made, not
  generated, AND be correct on first server paint. Use when building, auditing,
  redesigning, or fixing the SSR/hydration correctness of a landing page,
  marketing site, product homepage, or launch page, especially on Next.js,
  Remix/React Router, SvelteKit, or Astro. Generates a distinctive theme
  deterministically from a seed (a reproducible OKLCH palette + constraint-filtered
  font pairing) so it never settles into one recognisable look, and prevents the
  failures a visual review misses — dark-mode flash, hydration mismatches,
  hidden-until-JS heroes, and layout-shifting loading states. Triggers on: keel,
  landing page, marketing site, hero, redesign, audit, hydrate, dark-mode flash,
  hydration, next/font, Suspense skeleton. NOT for authenticated app UI,
  dashboards, admin panels, data tables, or CRUD/settings screens — that is a
  different problem this skill will decline.
---

# Keel

A design skill for AI coding assistants that build landing pages. It does two things no page-generator reliably does at once: it makes the page **look made, not generated**, and it makes the page **correct on first server paint** — no flash, no hydration mismatch, nothing invisible until JavaScript arrives.

The name is the point. A keel is what keeps a hull upright under load. A Keel page holds its shape the moment the server sends it, before a single line of client JS runs.

## Two pillars

1. **Deterministic theming.** Keel doesn't rotate a fixed catalog of named themes — catalogs become recognisable once enough pages ship them. It **computes** a theme from a seed string: same seed → byte-identical OKLCH palette + font pairing, forever; different seeds spread across the whole hue wheel. Distinctive at the ten-thousandth use. See [`references/theming-engine.md`](references/theming-engine.md) (with a runnable [`theming-engine.py`](references/theming-engine.py)).
2. **SSR/hydration correctness.** Most real landing pages ship through Next.js, Remix, or SvelteKit — server-rendered then hydrated. Keel treats the server-render as part of the design: the theme is applied before paint, above-the-fold content is visible without JS, slow regions stream behind layout-matched skeletons. See [`references/ssr-and-hydration.md`](references/ssr-and-hydration.md).

## Scope — read this before anything

Keel is for **landing / marketing pages and light auth-adjacent pages** (pricing, gated content, a marketing homepage with a login link). It is **not** for authenticated application UI — dashboards, admin panels, data tables, settings, CRUD. Those are a different discipline (dense information, statefulness, data-grid ergonomics) and Keel will make them worse, not better. If the brief is app UI, say so and decline: *"That's app/dashboard UI, which Keel isn't built for — it's a landing-page skill. I can still help, but not through Keel."*

## How to use this skill

One default behaviour and three explicit verbs.

| Invocation | What it does |
| --- | --- |
| *(default)* | Design or build a new landing page. Follow the **Design flow** below. |
| `keel audit <target>` | Read the target, grade it against the full [slop test](references/slop-test.md) — visual, structural, **and SSR** — return a ranked punch list. **Do not edit.** Load [`references/verbs/audit.md`](references/verbs/audit.md). |
| `keel hydrate <target> [--fix]` | Grade a framework page against the SSR/hydration gates and, with `--fix`, correct them in place (theme flash, mismatches, boundaries, loading states, fonts). The verb Keel adds. Load [`references/verbs/hydrate.md`](references/verbs/hydrate.md). |
| `keel redesign <target> [--anchor <name>] [--seed <string>]` | Keep the content and intent; rebuild the visual structure and recompute the theme, inside existing implementation boundaries unless a full rebuild is confirmed. Load [`references/verbs/redesign.md`](references/verbs/redesign.md). |

Anything that doesn't map to a verb is default. Attach nothing special — Keel infers structure and theme from the brief.

## Disciplines that hold across every verb

1. **Correct on first paint.** Any framework build must pass the SSR gates ([`slop-test.md`](references/slop-test.md) gates 34–43): a blocking theme script before paint, no hydration mismatch, above-the-fold content visible without JS, streamed regions behind layout-matched skeletons. A page that looks perfect and flashes on load has failed.
2. **Locked, computed tokens.** The theme is computed once at the top of the run and written as named CSS custom properties. Every colour and font downstream references a token (`var(--color-accent)`, `var(--font-display)`); no inline `#hex` / `oklch()` / `font-family:"…"`. See [`theming-engine.md`](references/theming-engine.md), [`color.md`](references/color.md).
3. **Honest copy — no fabricated content.** Never invent a metric, testimonial, logo count, or user name. Use the user's real figures, an em-dash placeholder + "metric to confirm", or a different section. See [`copywriting.md`](references/copywriting.md).
4. **Structural variety.** Two Keel pages for two briefs must not share the hero→3-features→CTA→footer rhythm. Pick a different macrostructure each build; the diversification rule ([`.keel/log.json`](#25-project-memory)) enforces it. See [`layout-and-structure.md`](references/layout-and-structure.md).
5. **Roman headers, one accent, tinted neutrals, ≤3 fonts.** The non-negotiable visual floor. Italic display type, gradient text, purple→blue gradients, zero-chroma greys, and >5% accent footprint are banned. See [`anti-patterns.md`](references/anti-patterns.md).
6. **Motion is cut before it's added, and never load-bearing.** `transform`/`opacity` only, three named easings, reduced-motion fallback on every keyframe, focus rings instant. Entrance animations are additive — content is visible without them. See [`motion.md`](references/motion.md).
7. **Refusal is half the skill; the other half is what you build.** A page can pass every gate in this skill and still be empty, because passing means avoiding the bad thing, not making a good one. Every build decides its hero enrichment explicitly (Step 4.5) — and when the answer is "build something," it is **hand-built**: CSS art or inline SVG, in the first byte, correct with JS off. Custom-build is both the tasteful path and the only one that survives first paint. See [`hero-enrichment.md`](references/hero-enrichment.md), [`custom-craft.md`](references/custom-craft.md).
8. **Accessible by construction.** Visible `:focus-visible`, 8 interactive states, contrast floors met, semantic landmarks, alt text. See [`accessibility.md`](references/accessibility.md).

## Design flow (default)

### 0. Pre-flight scan
If the project has code, **read it before asking anything**: framework (Next / Remix / SvelteKit / Astro / vanilla), existing tokens (`:root` OKLCH/HSL, Tailwind theme, `tokens.json`), font stack (`next/font`, `@fontsource`, Google `<link>`), motion library, spacing scale. Emit a short findings block with file:line citations and state what Keel will **preserve** (an existing token system, an existing font stack) vs **introduce**. If a token system already exists, **adopt it — do not run the theming engine over it.** The engine is for greenfield or an explicit re-theme. Cache findings to `.keel/preflight.json`.

### 1. Context gate
Ask once, in one message — audience, use case, tone — even on a short brief. Bold the three labels. Offer *"or say 'go ahead' and I'll infer and tell you what I picked."* If the user waves you through, infer and **state the inferences in one sentence** at the top of your reply. Then settle the **genre**: `editorial` (default), `technical`/modern-minimal, `atmospheric`, `playful` — it scopes font voices and a few slop gates.

**Scope check happens here too:** if the answers describe app/dashboard UI, decline per § Scope.

### 2. Pick the structure FIRST
Pick the page's spine *before* any visual ruleset. First read [`layout-and-structure.md`](references/layout-and-structure.md) and pick one **macrostructure**. Then read the index at [`component-specs.md`](references/component-specs.md) and pick a **nav**, **hero**, **CTA**, and **footer** spec — using the genre routing table — and **load only those picked spec files** from [`components/`](references/components/) (index-then-pick; a typical build loads 3–4). Default **away** from the AI template and the canonical wordmark-nav / centred-hero / 4-column-footer. State the picks in plain text: *"Macrostructure: Stat-led. Nav: command-pill. Hero: stat-led. Footer: single-line. Differs from the last build on macrostructure + theme."*

### 2.5 Project memory
If `.keel/log.json` exists (from prior runs), read the last 3–5 entries. Your macrostructure must differ from the last three; your theme must not clone the last one. State the rotation in one line before picking. Create/append the file in Build (step 6).

### 3. Compute the theme
Run the [theming engine](references/theming-engine.md): seed = the brand/product name (or `name · descriptor`); anchor = a vibe word or brand colour when intent is known (recommended) else omit for full-wheel spread; genre from step 1. The engine returns the OKLCH ramp (contrast-fitted) + the constraint-filtered font pairing. You may run [`theming-engine.py`](references/theming-engine.py) to generate and verify, or apply its spec. This replaces a theme catalog entirely.

### 4. Detect the SSR target
Name the stack and its consequences out loud: *"Next App Router + dark mode → I'll add the blocking theme script, load fonts via next/font, and stream the live panel behind a Suspense skeleton."* This is where the two pillars meet — a computed dark theme is exactly what must survive first paint. Load [`ssr-and-hydration.md`](references/ssr-and-hydration.md) for any framework build.

### 4.5 Decide the hero enrichment — **every build, on purpose**
Load [`hero-enrichment.md`](references/hero-enrichment.md) and decide what the hero *builds*. Every other step in this flow tells you what to avoid; this is the one that asks what to make. Pick **zero or one** enrichment archetype and **zero or one** polish pattern, then state the pick in one line — *including when the pick is "none"*.

The default is typography-only, and it is a good default: it is the strongest fail-state on the web. But it is also the answer that passes every gate by building nothing, which makes it the answer a model drifts into on every brief — and eight Keel pages that all drift there are eight pages with one composition. **Not enriching is a decision. Make it, don't default into it.** The gate is [`hero-enrichment.md`](references/hero-enrichment.md) § The gate: if the enrichment doesn't communicate something the typography can't, or the hero collapses without it, ship the typographic hero — deliberately.

Keel's tier order is not a taste ranking; it falls out of the SSR gates. Hand-built CSS art and inline SVG are in the first byte and render with JS off; Lottie, WebGL, and JS-driven canvas are an empty box until a payload lands, which is gate 35 wearing a different costume. So above the fold they are **refused**, not merely discouraged. When enrichment is earned, build it — [`custom-craft.md`](references/custom-craft.md).

### 5. Load the visual ruleset (index-then-pick; don't over-load)
- **Every build:** [`color.md`](references/color.md), [`typography.md`](references/typography.md), [`layout-and-structure.md`](references/layout-and-structure.md), [`motion.md`](references/motion.md), [`copywriting.md`](references/copywriting.md), [`anti-patterns.md`](references/anti-patterns.md), [`hero-enrichment.md`](references/hero-enrichment.md) (Step 4.5).
- **Structure picks (Step 2):** the [`component-specs.md`](references/component-specs.md) index, then **only** the nav/hero/CTA/footer spec files you picked from [`components/`](references/components/).
- **Enrichment at Tier A/B (Step 4.5):** add [`custom-craft.md`](references/custom-craft.md) — CSS-art and inline-SVG recipes. Skip it when the pick is typography-only.
- **Framework build:** add [`ssr-and-hydration.md`](references/ssr-and-hydration.md).
- **Image/video-bearing brief:** add [`media-and-performance.md`](references/media-and-performance.md) — LCP, CLS, `next/image`, formats, placeholder honesty.
- **Any interactive/stateful UI:** add [`accessibility.md`](references/accessibility.md) (states + focus + forms).
- **At handoff only:** [`slop-test.md`](references/slop-test.md) — it's a post-build check, not a pre-build reference.

### 5.5 Preview
Before emitting code, output the tight preview block (macrostructure · theme summary · nav/footer · sections · motion · **SSR plan** · slop-test row). The user should be able to redirect in five seconds. Format and a full example in [`worked-example.md`](references/worked-example.md) § 5.

### 6. Build
Emit code that satisfies the tone and the structural fingerprint. Always:
- Reference tokens by name; emit `tokens.css` (both modes if dark is in scope, same hue).
- Match hero headline size to copy length; roman headers; off-axis composition (not centred-everything).
- Design every interactive element for its 8 states; `transform`/`opacity` motion only; reduced-motion fallback; instant focus ring.
- On a framework: server components by default, `'use client'` on leaves only; blocking theme script; `next/font` wired to `--font-*`; `<Suspense>` + layout-matched skeleton for slow regions.
- **Never clobber an existing global stylesheet** — append Keel's `:root` + rules below the framework's directives; keep `@tailwind`/`@import "tailwindcss"` in place.
- **Stamp the output** — first CSS line: `/* Keel · seed:"…" · anchor:… · genre:… · hue:… · fonts:… · contrast:fitted,all-pass · gamut:sRGB-fit · ssr:<stack> */`, then the enrichment line: `/* enrichment:<archetype|none> · craft:<tier|—> · polish:<pattern|none> · first-byte:yes · js-off:renders */`. Write the line even when the answer is `none` — an absent line reads as an oversight, and Step 4.5 exists so that "no enrichment" is a decision on the record rather than a default no one made.
- **Any colour you hand-author** (a hover shade, a dark-mode accent) must be gamut-fit into sRGB like the engine's own tokens — slop-test gate 52. An out-of-gamut `oklch()` is silently repainted by the browser, and a contrast check won't catch it.
- **Append to `.keel/log.json`** — `{date, macrostructure, seed, anchor, hue, ssr}` at the front; trim to 20.

### 7. Slop test
Run the full [slop test](references/slop-test.md) — including SSR gates 34–43 — and the 7-axis pre-emit critique. Every answer "no." Fix and re-run. Update the preview's slop-test row to the real result. Do not ship slop.

## When the brief is a single component
If the brief names one element (a button, a card, a pricing toggle), skip macrostructure / nav / footer / hero and emit the component + an 8-state demo, adopting the project's existing tokens. If the component is interactive **and** the project is a framework, the SSR discipline still applies (a theme-aware component must not assume `window` at render; a client island stays a leaf). Component runs don't rotate the log.

## Verbs
- `keel audit` → [`references/verbs/audit.md`](references/verbs/audit.md)
- `keel hydrate` → [`references/verbs/hydrate.md`](references/verbs/hydrate.md)
- `keel redesign` → [`references/verbs/redesign.md`](references/verbs/redesign.md)

A full brief carried from intent to SSR-correct code is in [`references/worked-example.md`](references/worked-example.md).
