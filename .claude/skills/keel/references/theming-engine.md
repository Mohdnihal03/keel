# The deterministic theming engine

This is Keel's signature. Instead of rotating a fixed catalog of named themes — which becomes recognisable once enough pages ship it — Keel **computes** a theme from a seed. Same seed → byte-identical OKLCH palette + font pairing, every run, forever. Different seeds spread across the whole hue wheel. The output stays distinctive after the ten-thousandth use because there is no catalog to recognise; there is a function.

A runnable reference implementation ships beside this file: [`theming-engine.py`](theming-engine.py). It is ~120 lines of dependency-free Python. **You may run it** (`python theming-engine.py`) to generate and contrast-verify a palette, or port its logic. The prose below is the spec; the file is the ground truth. If they ever disagree, the file wins.

## Why deterministic, not heuristic

A prose heuristic ("derive paper lightness from the vibe, clamp accent chroma to 0.12–0.20") leaves the actual numbers to model judgment, so the same brief yields a different palette each run — irreproducible, and hard to audit. Keel fixes the numbers with a hash. The freedom lives in **two inputs the caller supplies** (seed + optional anchor + genre); everything downstream is computed. That buys three things a catalog can't:

- **Reproducibility** — a design review can re-run the seed and get the exact tokens back. A regression is a diff, not an argument.
- **Distinctiveness at scale** — no "the Keel look." The palette space is the OKLCH gamut, not 20 swatches.
- **Guaranteed floors** — the engine *fits* contrast rather than hoping for it (see § Contrast fitting). It cannot emit a failing accent.

## The three inputs

| Input | Source | Effect |
| --- | --- | --- |
| **seed** (required) | A stable brand string — the product name, or `name · one-line descriptor`. | Drives the hash. Everything not pinned by the other two inputs derives from it. |
| **anchor** (optional) | A vibe word or brand colour: `steel-blue`, `terracotta`, `moss`, `warm`, `technical`, or a hex. | Pins the **hue** so the palette reads *intentional*, not random. Chroma, lightness, ramp, and fonts still derive from the seed. |
| **genre** (optional, default `editorial`) | `editorial` · `technical` · `atmospheric` · `playful`. | Constrains which font-pairing voices are eligible before the deterministic pick. |

Use the anchor whenever you know the intent — it is what keeps the palette from landing on a hue that fights the brief (a pure-magenta logistics tool). Omit it only for a genuine "surprise me" brief, where full-wheel spread is the point.

## Step 1 — hash the seed

FNV-1a, 32-bit. A `stream()` helper rehashes `seed#i` for each independent draw, so draws are uncorrelated but fully reproducible:

```python
def fnv1a(s):
    h = 0x811c9dc5
    for ch in s.encode("utf-8"):
        h ^= ch; h = (h * 0x01000193) & 0xFFFFFFFF
    return h
```

Six draws `d[0..5]` seed every decision below.

## Step 2 — palette parameters

- **Hue** `H` = `anchor` if the anchor names/implies one, else `d[0] % 360` (full wheel).
  Vibe→hue map: warm 40 · technical/steel/cool 233 · botanical/moss/forest 150 · amber 75 · terracotta 30 · neon 300.
- **Accent chroma** `C` = `0.12 + (d[1] % 81)/1000` → `[0.120, 0.200]`. Mid-saturation; the *saturation you perceive* comes from contrast against tinted neutrals, not from cranking chroma.
- **Mode** = `dark` if `d[2] % 8 < 3` else `light` (≈37% dark, biased light — landing pages skew light).

## Step 3 — the ramp

Nine tokens, fixed lightness steps, every neutral tinted toward `H` (never zero-chroma). Light-mode L values shown; dark mode inverts ink/paper and lightens elevation:

| Token | Light L | Chroma | Role |
| --- | --- | --- | --- |
| `--color-paper` | 0.97 | 0.010 | base surface |
| `--color-paper-2` | 0.94 | 0.012 | one elevation step |
| `--color-rule` | 0.86 | 0.014 | dividers / hairlines |
| `--color-muted` | 0.52 | 0.010 | de-emphasised text |
| `--color-ink-2` | 0.34 | 0.012 | secondary text |
| `--color-ink` | 0.20 | 0.014 | primary text |
| `--color-accent` | 0.55* | `C` | the one signal colour |
| `--color-accent-ink` | 0.98 | 0.010 | text on accent fill |
| `--color-focus` | accent L + 0.05 | `C`+0.04 | `:focus-visible` ring |

\* starting value — the contrast-fitting step (below) may lower it. Every token's **chroma** is additionally gamut-fit into sRGB, so the `C` a token ships may be lower than the `C` the seed drew.

The L-steps are the point: they give the palette **typographic depth** (six believable text/surface tiers) without leaning on the accent for hierarchy. The accent stays a highlighter — plan it for ≤5% of any viewport (one CTA fill, one active state, the focus ring). See [`color.md`](color.md).

## Step 4 — contrast fitting (the guarantee)

A raw ramp can fail: a mid-lightness accent at some hues does not clear 4.5:1 against white overlay text. Keel does not ship that and hope. After building, it **nudges the accent lightness deterministically** (down on light paper, up on dark) in fixed 0.01 steps until both hold:

- `accent-ink` vs `accent` ≥ **4.5:1** (CTA label legibility), and
- `accent` vs `paper` ≥ **3:1** (the fill is distinguishable from the page).

```python
step = -0.01 if mode == "light" else +0.01
for _ in range(40):
    accent = fit_gamut(acc_L, C, H)   # gamut-fit BEFORE measuring — see below
    if wcag_ratio(accent_ink, accent) >= 4.5 and wcag_ratio(accent, paper) >= 3.0:
        break
    acc_L = round(acc_L + step, 3)
```

**Gamut fitting comes first, and it is not optional.** OKLCH can express colours sRGB cannot render. At the chroma range Keel draws from (0.12–0.20), a large share of hue/lightness combinations — especially blues and violets around L 0.72 — fall outside sRGB. A browser does not render those as written: it gamut-maps them, silently discarding chroma. So a contrast check run against the *unfitted* value certifies a colour the user will never see. `fit_gamut()` holds L and H and binary-searches chroma down until the colour is renderable (fixed iteration count, so determinism is preserved); every emitted token passes through it. The consequence for pillar 1 is the real reason to care: without this step, a large fraction of seeds get pulled toward the gamut boundary by the browser, which quietly compresses exactly the palette spread the engine exists to produce.

This is a real constraint solver, not "verify in devtools later." Across a sweep of **508 seeds × 3 modes (1,524 palettes)** every palette passes ink/paper, muted/paper, accent-ink/accent, and accent/paper, **and every emitted token is inside sRGB** — checked on the value *as printed into the stylesheet*, not the float in memory, since those can differ at the rounding boundary. Note that `rel_luminance()` clamps out-of-range linear RGB, so a contrast check alone cannot catch a gamut violation; the gamut assertion is a separate, explicit check.

## Step 5 — constraint-filtered font pairing

Two filters run before the deterministic pick, so the seed only ever selects among faces that are *already appropriate*:

1. **Ban-list filter** — no display or body face may be a distribution default: `Inter, Roboto, Open Sans, Poppins, Lato, Work Sans, DM Sans, Montserrat, system-ui`. (Note: **Inter Tight** is a distinct, tighter optical family and is *allowed* as a body face — see [`typography.md`](typography.md).)
2. **Voice filter** — the pairing's voice must be in the active genre's allowed set:
   - `technical` → {technical, modern, warm-tech, condensed}
   - `editorial` → {editorial, classical, literary, grotesk-serif}
   - `atmospheric` → {modern, art, technical}
   - `playful` → {art, warm-tech, modern}

Then: `pair = survivors[d[3] % len(survivors)]`, and `mono = "Geist Mono" if d[4] % 2 else "JetBrains Mono"`. The pool of pairs lives in the reference file and in [`typography.md`](typography.md). A fail-safe re-opens the full ban-filtered pool if a voice filter empties it, so the engine never returns nothing.

## Step 6 — emit tokens

Write every value as a named CSS custom property in `:root`. **Nothing downstream inlines a raw colour or font** — the whole page references `var(--color-*)` / `var(--font-*)`. On a dark-mode-capable page the same tokens are re-declared under `[data-theme="dark"]`; the anchor **hue never changes between modes**, only lightness and chroma move. Because the theme is applied via a `data-theme` attribute, it must be set *before first paint* — this is the seam where the theming engine meets SSR. See [`ssr-and-hydration.md` § Dark-mode without the flash](ssr-and-hydration.md).

## Worked seed (used by [`worked-example.md`](worked-example.md))

`seed = "Wharfline · cold-chain logistics observability"`, `anchor = steel-blue`, `genre = technical`
→ hash `3707062074`, hue `233`, chroma `0.125`, mode `light`.

```css
:root {
  --color-paper:      oklch(97% 0.010 233);
  --color-paper-2:    oklch(94% 0.012 233);
  --color-rule:       oklch(86% 0.014 233);
  --color-muted:      oklch(52% 0.010 233);
  --color-ink-2:      oklch(34% 0.012 233);
  --color-ink:        oklch(20% 0.014 233);
  --color-accent:     oklch(54% 0.111 233);   /* L fitted 55%→54% for contrast; C gamut-fit 0.125→0.111 */
  --color-accent-ink: oklch(98% 0.010 233);
  --color-focus:      oklch(59% 0.121 233);   /* C gamut-fit from 0.165 */
}
```

Fonts: **Space Grotesk** (display) · **Inter Tight** (body) · **Geist Mono** (mono).
Verified contrast: ink/paper **16.6:1** · muted/paper **5.05:1** · accent-ink/accent **4.68:1** · accent/paper **4.54:1** — all pass, all in sRGB.

The seed draws chroma `0.125`, but sRGB cannot hold that chroma at L 54% / hue 233, so the emitted accent is `0.111` — the most saturated steel-blue that actually paints. This is the gamut fit doing its job: the number in the token is the number on the screen.

Chroma is **floored** at 3dp, the precision the CSS prints. Rounding to nearest would round back up across the gamut boundary the search just found and re-emit an unrenderable colour — the value in memory would pass while the value in the stylesheet failed.

## The stamp

Every emitted stylesheet's first line records the seed so the build is reproducible and the next run can diversify against it:

```css
/* Keel · seed:"Wharfline · cold-chain logistics observability" · anchor:steel-blue · genre:technical
 * hue:233 · chroma:0.111 · mode:light · display:Space Grotesk · body:Inter Tight
 * contrast: fitted, all-pass · gamut: sRGB-fit · ssr: next-app-router */
```

## What the engine does NOT do

1. It does not free-pick colours mid-render. Once tokens are emitted, they are locked; a needed value is added as a *new named token*, never inlined. (Slop-test token gate; see [`slop-test.md`](slop-test.md).)
2. It does not use more than one accent. Two consecutive builds still must differ (see the diversification rule in [`SKILL.md`](../SKILL.md)); with computed themes that is usually free, but check the stamp.
3. It does not override an existing project system. If pre-flight finds real tokens/fonts, Keel adopts them and skips generation. The engine is for greenfield or explicit re-theme.
