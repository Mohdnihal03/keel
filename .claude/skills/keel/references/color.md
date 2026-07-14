# Colour

Most AI-generated UI fails on colour in the same four ways: it picks blue, it uses pure black and pure white, it draws a purple-to-cyan gradient, and it lets the accent cover a third of the page. Keel's [theming engine](theming-engine.md) computes palettes that avoid all four by construction. This file is the *discipline* the engine encodes — and the rules you apply by hand when you adopt an existing project's palette instead of generating one.

## Principles

- **OKLCH only.** Perceptually uniform: equal lightness numbers *look* equally light across hues, and tints hold their hue as lightness changes. `hsl()` and `rgb()` lie about brightness — `hsl(60 100% 50%)` (yellow) and `hsl(240 100% 50%)` (blue) claim the same 50% lightness and are wildly different. Author every colour as `oklch(L% C H)`.
- **One accent.** Two at the absolute most. Everything else is neutral. The accent occupies **≤5%** of any viewport — it is a highlighter, not a wall.
- **No pure extremes.** No `#000`, no `#fff`. Always carry a trace of chroma toward the anchor hue. Pure grey (`oklch(L 0 H)`) reads as flat and lifeless; tinted neutrals read as *considered*, and most people can't say why.
- **Tint the greys toward the accent.** Warm accent → warm neutrals. Cool accent → cool neutrals. A warm accent over cool-grey body text looks subtly wrong; matching the tint is the fix nobody notices, which is the point.

## The four layers

Every Keel palette — generated or hand-built — resolves to four layers. The engine's nine tokens are these four, expanded:

1. **Paper** — the base surface. Light: `oklch(96–98% 0.008–0.014 H)`. Dark: `oklch(12–18% 0.008–0.015 H)`. Plus one or two elevation steps (`--color-paper-2`, `-3`): on light paper, *darker*; on dark paper, *lighter* (higher surfaces catch more light).
2. **Ink** — primary text. Light paper: `oklch(18–22% 0.010–0.015 H)`. Dark paper: `oklch(92–96% 0.006–0.012 H)`. Plus `--color-ink-2` for secondary text, one step toward paper.
3. **Neutrals** — `--color-rule` (dividers), `--color-muted` (de-emphasised text). Stepped in lightness between paper and ink, all tinted (chroma 0.008–0.018). These carry the page's hierarchy; the accent does not.
4. **Accent** — one saturated colour, chroma **0.12–0.20**, plus `--color-accent-ink` (the text colour that rides on an accent fill) and `--color-focus` (accent hue, higher chroma, for the focus ring only).

## Contrast

Author to WCAG minimums; verify with APCA when you can (it models real perceived contrast better than the WCAG ratio).

| Content | WCAG min | APCA target |
| --- | --- | --- |
| Body text (<24px reg / <18.66px bold) | 4.5:1 | Lc ≥ 60 |
| Large text, icons, focus rings | 3:1 | Lc ≥ 45 |
| Placeholder / helper text | 4.5:1 | Lc ≥ 60 |

Keel's engine **fits** accent contrast automatically (§ Contrast fitting in [theming-engine.md](theming-engine.md)) — a generated palette cannot ship a failing CTA. But any colour you place *by hand* must be checked, especially the three failures that ship most often (see [accessibility.md](accessibility.md)):

- text in a card that switched its surface to `--color-paper-2` (the text still inherits ink-on-paper contrast assumptions);
- `--color-muted` on `--color-paper-2` (two low-contrast values stacked);
- **button text ≈ button fill** — the black-on-black bug: `color: var(--color-ink)` left on a `background: var(--color-ink)` button because the model forgot to switch to `--color-accent-ink` / `--color-paper`.

Fast pre-check: if `|L_text − L_bg| < 0.40` in OKLCH, the pair probably fails 4.5:1 — do the full calculation.

## Dark mode

- Paper L 12–18% (not `#000`); ink L 92–96% (not `#fff`).
- Reduce body font-weight ~50 units (400 → 350) — light text on dark looks optically heavier.
- Accent: drop chroma 0.02–0.04 and raise lightness 5–10% versus the light-mode accent.
- Elevation inverts: higher surfaces are *lighter* (+~3% L per level), not darker.
- **Never change the anchor hue between modes.** Only L and C move. Declare the dark tokens under `:root[data-theme="dark"]`, applied before paint per [ssr-and-hydration.md § Dark-mode without the flash](ssr-and-hydration.md).

## Bans (each is a specific tell, not a taste)

- **Pure `#000000`** — no black object in nature; it reads as unfinished. Use `oklch(16% 0.01 H)`.
- **Pure `#ffffff` base** — clinical, and it makes a dark-mode flash more jarring. Use tinted paper.
- **Zero-chroma neutrals** (`oklch(L 0 H)`) — flat grey; the untinted default every generator reaches for.
- **Purple→cyan / purple→blue / orange→pink gradients** — the LLM house style. Every model picks these; that is exactly why they read as generated.
- **`background-clip: text` gradient headlines** — the single most recognisable AI-marketing tell of the era.
- **Accent as a large background fill** (>5% of the view) — the accent stops being a signal the moment it becomes the surface.
- **Grey text on a coloured background** — always reads washed out; use `--color-accent-ink`.
- **Three-stop gradients** — two stops only; the third is vanity.
- **Red/green as the only signal** — colour-blind users lose it; add an icon or label.

## Using the accent

Reach for it to: mark an active nav item, draw a focus ring, underline a link on hover, carry a primary CTA's fill or border, or set one small square beside a heading. Do **not** fill giant buttons wall-to-wall, set whole sections on it, or build decorative gradients from it. If you feel the urge to use more accent, that urge is the slop defaulting. Use less.
