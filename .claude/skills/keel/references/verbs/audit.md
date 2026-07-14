# `keel audit <target>`

Read the file(s) the user pointed at, grade them, return a ranked punch list. **Do not edit. Do not redesign.** Auditing is diagnosis; the user decides what to fix.

For each finding return:

- **Tell** — the named anti-pattern from [`anti-patterns.md`](../anti-patterns.md).
- **Where** — file path and line range.
- **Severity** — `critical` (ships as slop / broken on load), `major` (looks AI-generated), `minor` (small taste issue).
- **Fix** — one-line concrete correction.

Group by severity. End with a count: `N critical · M major · K minor`.

## What audit covers

Run the full [`slop-test.md`](../slop-test.md) — visual, structural, colour/token, typography, motion, contrast, honest-copy, chrome, responsive, **and the SSR block (gates 34–43)**. A visual-only audit that ignores hydration is exactly the blind spot Keel exists to close: a page can pass every aesthetic gate and still flash, mismatch, or blank on the server.

- If the SSR gates surface findings, include them in the punch list at their real severity (a theme flash is `critical`), but note that **`keel hydrate --fix` is the verb that fixes them** — `audit` only reports.
- Score the **structural fingerprint** explicitly: if the page is the AI template (centred hero → 3 equal cards → CTA → footer, no asymmetry, no surprise), that is a `critical` structural finding even when the visual treatment is clean.

## Stamp-vs-page check

If the target has a `/* Keel · seed:"…" · … */` stamp, verify the page actually matches it:

- **Seed drift.** Recompute the palette from the stamped seed + anchor + genre (run [`theming-engine.py`](../theming-engine.py) or apply the spec). If the page's live colours/fonts don't match what the seed produces, flag `critical: seed drift` — either the stamp lies or the page was hand-edited off its own system.
- **SSR claim.** If the stamp says `ssr: pass (34–43)` but a gate in that range fails, flag `critical: stamp lies` — the stamp claims a correctness the code doesn't deliver.
- **Missing stamp** on a project that has other Keel output → `major: missing system reference`.

## Genre-aware grading

If the stamp names a genre, apply the genre-scoped gate overrides from [`slop-test.md`](../slop-test.md). A radial-gradient background is a `critical` tell for editorial but allowed for atmospheric; pure-white paper is a tell for editorial but allowed for technical/modern-minimal. Grade against the genre the page declared, not against the default.

## Diversification

On a project with prior Keel output (a stamp or `.keel/log.json`), flag a page that repeats the previous macrostructure or lands on a non-diverse theme as `minor: variety drift`. With computed themes this is rare — but a hand-edit can pull a page back toward the last one.
