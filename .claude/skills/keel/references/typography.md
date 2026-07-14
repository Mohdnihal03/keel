# Typography

Type is where AI slop is most visible. A default font at a mushy weight on a page with no measure control reads as generated before anyone parses a word. This module is loaded on every build. Follow it exactly; the deterministic engine ([theming-engine.md](theming-engine.md)) picks fonts *within* the pools defined here, so these rules constrain every seed.

## The 2+1 rule

A landing page runs on **two** typefaces plus **at most one** outlier.

- `--font-display` — one face for headings, hero, section titles.
- `--font-body` — one face for paragraphs, UI labels, buttons, captions.
- **+1 outlier** — optional, and only for a single reserved job: a wordmark, a hero stat, or a pull-quote. Never for running text.

Hard cap: **3 `font-family` families on a page.** Rules:

- Same family at different weights/optical sizes is **one** family (Fraunces 340 and Fraunces 700 = one).
- `--font-mono` counts as a family *if it appears outside `<code>`/`<pre>`* — e.g. as a nav eyebrow or a stat label. Mono confined to code blocks is free.
- Variable-font axes (weight, optical size, slant) do not add to the count.

Two families is the target. Three is the ceiling, not the goal. If you can't justify the outlier in one sentence, delete it.

## The font ban-list

Never use these as a **display** face. They are the fonts every scaffold, template, and generator reaches for by default — a distribution-default face is a signal the page was assembled, not designed.

| Banned as display | Why it's a tell |
|---|---|
| Inter | The default of defaults; ships in every UI kit. |
| Roboto | Android/Material default; reads as unstyled. |
| Open Sans | 2010s CMS default; invisible from overuse. |
| Lato | Same era, same ubiquity. |
| Montserrat | The "I picked a font" font; geometric cliché. |
| Poppins | Startup-template default; rounded geometric slop. |
| Work Sans | Google Fonts front-page default. |
| DM Sans | The current-gen scaffold default. |
| `system-ui` | Literally the no-decision decision. |

**Inter Tight is NOT banned.** It is a distinct, tighter optical family — narrower spacing, higher x-height discipline — and it is a legitimate, strong **`--font-body`** choice. Do not confuse it with "Inter." If a seed or a user asks for Inter, offer Inter Tight for body instead, and pick a real display face from the pools below.

## Tone → pairing pools

Voice maps to concrete display + body pairs. All faces below are **free on Google Fonts**; do not introduce paid faces unless the user confirms licences. The deterministic engine selects one row from the voice set its genre allows (editorial / technical / atmospheric / playful — see [theming-engine.md](theming-engine.md)); this table is the pool it draws from.

| Voice | `--font-display` | `--font-body` | `--font-mono` | Genre lean |
|---|---|---|---|---|
| Editorial | Fraunces | Newsreader | JetBrains Mono | editorial |
| Technical | Space Grotesk | Inter Tight | Geist Mono | technical |
| Classical | Source Serif 4 | Libre Franklin | IBM Plex Mono | editorial |
| Literary | Newsreader | Spectral | JetBrains Mono | editorial / atmospheric |
| Warm-tech | Bricolage Grotesque | Geist | Geist Mono | technical / playful |
| Art | Syne | Inter Tight | JetBrains Mono | atmospheric / playful |
| Condensed | Big Shoulders Display | Libre Franklin | IBM Plex Mono | playful / editorial |

Extra display serifs in the pool: **Instrument Serif** (high-contrast, hero-only — set it large or not at all). Never pair two serifs of the same contrast class; the eye can't tell them apart and you've spent your outlier for nothing.

## Type scale

Use a **modular scale**. Body-adjacent steps ride a **1.2 (minor third)** ratio; display breaks the ratio with a deliberate jump so headings feel like a different register, not a bigger paragraph.

```css
:root {
  --text-xs:      0.75rem;   /* 12px — captions, legal, eyebrows */
  --text-sm:      0.875rem;  /* 14px — secondary UI, labels      */
  --text-base:    1rem;      /* 16px — body default              */
  --text-lg:      1.25rem;   /* 20px — lead paragraph            */
  --text-xl:      1.5rem;    /* 24px — h4 / card title           */
  --text-2xl:     1.953rem;  /* ~31px — h3                       */
  --text-3xl:     2.441rem;  /* ~39px — h2                       */
  --text-4xl:     3.052rem;  /* ~49px — h1 on interior pages     */
  --text-display: clamp(2.75rem, 1.5rem + 6.25vw, 5.5rem); /* hero */
}
```

`--text-2xl → --text-4xl` follow 1.25 (major third) — the wider ratio gives headings air. `--text-display` is fluid: floor 44px on a 360px phone, ceiling 88px on wide viewports, scaling on viewport width so the hero never overflows small screens or looks stranded on large ones. Set `line-height` tighter as size grows: `1.6` at `--text-base`, `1.05–1.1` at `--text-display`.

## Hero headline sizing by copy length

The display ceiling is for *short* headlines. Long strings at max size wrap into a wall. Bracket by character count (including spaces):

| Headline length | Treatment | Clamp ceiling |
|---|---|---|
| ≤ 50 chars | Full display | `clamp(2.75rem, 1.5rem + 6.25vw, 5.5rem)` |
| 51–90 chars | Step down one rung | `clamp(2.25rem, 1.4rem + 4.25vw, 4rem)` |
| > 90 chars | Rewrite it, or cap hard | `clamp(2rem, 1.4rem + 3vw, 3rem)` |

A hero over 90 characters is almost always a copy problem, not a type problem — cut it before you shrink it. Control wrapping with `text-wrap: balance` on headings and `text-wrap: pretty` on lead paragraphs.

## Measure

Constrain prose line length to **45–75 characters** (`max-width: 60–70ch` for a single body column). Below ~45ch the eye returns too often and rhythm breaks; above ~75ch it loses the start of the next line on the return sweep. Full-width paragraphs are a classic slop tell — real editorial layouts always cap the measure.

```css
.prose { max-width: 68ch; }
```

## Weight contrast

Commit to the extremes. The generated look lives in the **500/600 middle** — every default lands there because it's the safe average.

- Body: `300`–`400`.
- Display: `600`–`800` (or a variable weight axis pushed high).
- Put light body next to heavy display so the contrast is unmistakable: `400` body under a `700`+ hero.
- Never set a hero at `500` or `600`. It reads as "the theme's default weight," which is exactly the tell.
- For serif display with an optical-size axis (Fraunces, Source Serif 4), push `opsz` toward its max at large sizes to earn the high-contrast strokes that flat weight-only scaling can't fake.

## Roman headers only

**No italic display type.** Italic headlines and italic hero words are a top-tier AI tell on landing pages. Headings, hero, section titles, pull-quotes as display — all **roman**.

Carry emphasis without slanting:

- Weight jump (`400 → 700`).
- Accent color on the emphasized word (see [color.md](color.md)).
- An underline or rule.
- Size or a change in `--font-family` to the outlier.

Italic survives in exactly one place: **inline emphasis inside body copy** (`<em>`, a cited title). Never in a heading.

## next/font

On **Next.js**, load fonts with `next/font/google` (or `next/font/local`). It self-hosts the files at build time, injects `size-adjust` fallback metrics automatically, and emits zero external requests — so there is no layout shift and no render-blocking round-trip. **Do not also add a Google Fonts `<link>` in `<head>`** — you'll double-load the family and reintroduce FOUC, defeating the point. Assign the loaded font's CSS variable to `--font-display`/`--font-body`. Full first-paint setup (variable wiring, `className` on `<html>`, avoiding hydration mismatches) is in [ssr-and-hydration.md](ssr-and-hydration.md).

On **vanilla HTML**, use `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>` before the stylesheet link, set `font-display: swap`, and define a **matched fallback metric** so the swap doesn't shift layout:

```css
@font-face {
  font-family: "Fraunces Fallback";
  src: local("Georgia");
  size-adjust: 105%;
  ascent-override: 92%;
}
:root { --font-display: "Fraunces", "Fraunces Fallback", serif; }
```

## Checklist

- [ ] ≤ 3 families; two is the target, the third is a justified outlier.
- [ ] No banned face as display; Inter Tight allowed only as **body**.
- [ ] Display and body pulled from one voice row in the pool.
- [ ] `--text-*` ladder present; `--text-display` is a `clamp()`.
- [ ] Hero clamp matched to headline character count.
- [ ] Prose measure capped at 45–75ch.
- [ ] Weight contrast at the extremes — no 500/600 display.
- [ ] Every heading roman; no italic display anywhere.
- [ ] Fonts via `next/font` **or** `<link>` + fallback metric — never both.
