# `keel hydrate <target>`

The verb Keel adds. `audit` grades how a page *looks*; `hydrate` grades whether it is **correct on the server** — and, unlike `audit`, it may fix what it finds. Point it at a page, a layout, or a component in a framework project (Next.js, Remix/React Router, SvelteKit, Astro-with-islands). It reads the code, runs the SSR & hydration gates, and returns a punch list; with `--fix` it applies the corrections in place.

Load [`ssr-and-hydration.md`](../ssr-and-hydration.md) before running — it is the standard every finding is graded against.

## Scope

`hydrate` is about **runtime correctness**, not visual taste. It will not restyle, re-theme, or re-layout. It touches only what makes the page wrong on first server paint: the theme script, hydration divergences, component boundaries, loading states, and font loading. If the page also looks like slop, say so in one line and point the user at `keel audit` — don't mix the two.

## Pipeline

1. **Detect the stack.** Read `package.json` and the project shape: Next App Router vs Pages Router, Remix/React Router, SvelteKit, Astro. The fixes differ per stack (see the framework quick-map in `ssr-and-hydration.md`). State what you detected.

2. **Run gates 34–43** from [`slop-test.md`](../slop-test.md) against the target. For each finding return:
   - **Gate** — the number + name (e.g. `34 · theme flash`).
   - **Where** — file path and line range.
   - **Severity** — `critical` (the page is visibly broken on load: flash, blank hero, mismatch that resets content), `major` (correctness/perf cost the user will feel: over-clienting, layout-shifting fallback, double font load), `minor` (works but fragile: a suppressor that should be a real fix, a missing `aria-live`).
   - **Why** — one line on what actually goes wrong for the user.
   - **Fix** — the concrete correction, with the code.

3. **Report or fix.**
   - Default: group findings by severity, end with a count (`N critical · M major · K minor`), and stop. Do not edit.
   - `--fix`: apply the corrections in place, smallest-blast-radius first. **Never** disable SSR (`ssr:false`, root `'use client'`) as a fix — that is gate 43, the thing you're removing, not a tool you reach for. After fixing, re-run the gates and report the new count, plus any finding that needs a human decision (e.g. "the hero animation was hiding content — I made it additive; confirm the entrance still reads how you want").

## The checks, in order of how often they bite

1. **Theme flash (gate 34)** — the most common and most visible. Is there a synchronous blocking script in `<head>` setting `data-theme` before paint? If the project has any dark mode / `data-theme` / `next-themes`-style toggle and no such script, this is `critical`. Fix: inject the inline script (per `ssr-and-hydration.md § 1`) and add `suppressHydrationWarning` to `<html>`.
2. **Hidden-until-JS content (gate 35)** — above-the-fold `opacity:0` awaiting mount/scroll. `critical` if it's the hero. Fix: make the initial state visible; the animation becomes additive.
3. **Render non-determinism (gate 36)** — `Date`/`Math.random`/`window` in a shared render body. `critical`. Fix: move to `useEffect` / server-stamped prop / `useId()` / the `mounted` two-pass pattern.
4. **Invalid nesting (gate 37)** — `<p><div>`, nested interactive elements. `major` (silent until it mismatches). Fix the markup.
5. **Over-clienting (gate 39)** — `'use client'` too high; server-only import in a client file. `major` (bundle + lost server data access). Fix: push the directive to leaves; extract the interactive island.
6. **Boundary props (gate 40)** — non-serializable props across server→client. `major`. Fix: serialize (Date→ISO), pass primitives or `children`.
7. **Loading state (gate 41)** — unwrapped slow region, or a layout-shifting spinner fallback. `major` (CLS). Fix: `<Suspense>` + a layout-matched skeleton (see [`motion.md`](../motion.md), [`copywriting.md`](../copywriting.md) for the fallback copy) + `aria-live`.
8. **Font loading (gate 42)** — double load / render-blocking / not wired to `--font-*`. `major`. Fix: single `next/font` loader, `display:swap`, variable wired to the token.
9. **Suppressor abuse (gate 38) / SSR bailout (gate 43)** — `suppressHydrationWarning` as a silencer; `ssr:false` to dodge a bug. `minor`–`critical` depending on what it's hiding. Fix: replace with the real correction.

## Output stamp

When `--fix` runs, update the CSS/route stamp's `ssr:` field to record the pass: `· ssr: pass (34–43) · stack: next-app-router`. If a finding was left for the user, note it: `· ssr: 1 open (gate 35 — hero entrance, confirm)`.

## When there's nothing to fix

If the target is a pure static-HTML artifact (no framework, no hydration), say so plainly: *"No server runtime here — gates 34–43 are N/A. The only SSR-adjacent check that applies is the theme script (gate 34) if you add dark mode."* Don't invent findings to look busy.
