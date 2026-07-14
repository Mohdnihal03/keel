# Keel

A design skill for AI coding assistants that build landing pages. It does two things no page-generator reliably does at once: it makes the page **look made, not generated**, and it makes the page **correct on first server paint** — no flash, no hydration mismatch, nothing invisible until JavaScript arrives.

The name is the point. A keel is what keeps a hull upright under load. A Keel page holds its shape the moment the server sends it, before a single line of client JS runs.

## Install

```
/plugin marketplace add Mohdnihal03/keel
/plugin install keel@keel
```

Then just describe a landing page. Keel triggers on briefs about landing pages, marketing sites, heroes, redesigns, audits, and hydration bugs.

## Two pillars

**1. Deterministic theming.** Keel doesn't rotate a fixed catalog of named themes — catalogs become recognisable once enough pages ship them. It *computes* a theme from a seed string: same seed → byte-identical OKLCH palette + font pairing, forever; different seeds spread across the whole hue wheel. Distinctive at the ten-thousandth use.

Every emitted colour is **contrast-fitted** (the accent's lightness is nudged deterministically until it clears WCAG floors against both its overlay text and the page) and **gamut-fitted** (chroma is reduced until the colour is actually renderable in sRGB — otherwise the browser silently desaturates it and you ship a colour you never chose). Verified across 1,524 palettes: zero contrast failures, zero gamut violations, checked on the value *as printed into the stylesheet*.

**2. SSR/hydration correctness.** Most real landing pages ship through Next.js, Remix, or SvelteKit — server-rendered then hydrated. Keel treats the server-render as part of the design: the theme is applied before paint, above-the-fold content is visible without JS, slow regions stream behind layout-matched skeletons.

## Usage

| Invocation | What it does |
| --- | --- |
| *(default)* | Design or build a new landing page. |
| `keel audit <target>` | Grade a page against the full 58-gate slop test — visual, structural, SSR, and craft — and return a ranked punch list. Does not edit. |
| `keel hydrate <target> [--fix]` | Grade a framework page against the SSR/hydration gates and, with `--fix`, correct them in place. |
| `keel redesign <target> [--anchor <name>] [--seed <string>]` | Keep the content and intent; rebuild the visual structure and recompute the theme. |

## Scope

Keel is for **landing / marketing pages and light auth-adjacent pages** (pricing, gated content). It is **not** for authenticated application UI — dashboards, admin panels, data tables, settings, CRUD. Those are a different discipline, and Keel will decline them rather than make them worse.

## The theming engine

`references/theming-engine.py` is a runnable, dependency-free reference implementation. Run it to generate and verify a palette:

```bash
python .claude/skills/keel/references/theming-engine.py
```

It prints the OKLCH ramp, the font pairing, every WCAG contrast ratio, and an explicit sRGB gamut assertion. The prose spec lives in `references/theming-engine.md`; **if the two ever disagree, the file wins.**

## What's inside

```
.claude/skills/keel/
├── SKILL.md                    the entry point — flow, disciplines, verbs
└── references/
    ├── theming-engine.md/.py   deterministic OKLCH + font engine (runnable)
    ├── ssr-and-hydration.md    theme-before-paint, streaming, next/font
    ├── slop-test.md            58 gates, run at handoff
    ├── color.md                tokens, tinted neutrals, the ≤5% accent rule
    ├── typography.md           font pools, scales, the ban-list
    ├── layout-and-structure.md macrostructures, off-axis composition
    ├── hero-enrichment.md      what to BUILD — tiers, archetypes, the gate
    ├── custom-craft.md         hand-built CSS art & inline SVG recipes
    ├── motion.md               transform/opacity only, reduced-motion, the named tells
    ├── copywriting.md          honest copy — never invent a metric
    ├── accessibility.md        8 states, focus, contrast floors
    ├── anti-patterns.md        the banned visual signatures
    ├── media-and-performance.md LCP, CLS, image formats
    ├── worked-example.md       one brief, end to end, real code
    ├── components/             nav / hero / CTA / footer specs
    └── verbs/                  audit · hydrate · redesign
```

## Refusal is only half of it

A design skill made entirely of prohibitions has a failure mode: a page can pass every gate and still be empty, because passing means *avoiding* the bad thing, not making a good one. Strip out everything Keel forbids and what's left is type on tinted paper — a fine look, but only one look, which is exactly what a skill claiming to never settle into one recognisable look cannot have.

So Keel also says yes. [`hero-enrichment.md`](.claude/skills/keel/references/hero-enrichment.md) forces every build to decide what its hero actually *builds* — including when the answer is "nothing," which then has to be a decision rather than a drift. [`custom-craft.md`](.claude/skills/keel/references/custom-craft.md) is how to hand-build it. Gates 53–58 are the only ones on the slop test that an **empty page can fail**; every other gate is satisfiable by building less.

The tier order falls out of the SSR gates rather than out of taste. CSS art and inline SVG ship in the first byte and render with JavaScript off. A Lottie or WebGL hero is an empty box until a payload downloads and a runtime boots — the same failure as an `opacity: 0` headline, wearing a different costume. The tasteful path and the correct-on-first-paint path turn out to be the same path.

## Credits

`hero-enrichment.md`, `custom-craft.md`, and the named-tells section of `motion.md` are adapted from [Hallmark](https://github.com/nutlope/hallmark) (MIT) — a design skill carrying the craft library Keel was missing. The material is re-derived against Keel's SSR gates and anti-pattern set rather than copied: the tier inversion, the base-is-drawn rule, and the constraints on fake chrome, italic numerals, and gradients are Keel's own.

## License

MIT — see [LICENSE](LICENSE). Portions adapted from [Hallmark](https://github.com/nutlope/hallmark), Copyright (c) 2026 Hallmark contributors, MIT.
