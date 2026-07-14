# `keel redesign <target> [--anchor <name>] [--seed <string>]`

Take the target's **content and intent**, then rebuild its visual structure — new section rhythm, new heading placement, new component voice, a freshly computed theme. Preserve what the page *says* and *does*; replace how it looks.

**Redesign inside the existing implementation boundaries unless the user explicitly confirms a full rebuild.** Preserve existing routes, component ownership, copy intent, brand, and information architecture. Replace only the visual/interaction layer needed for the requested scope.

## Safety rail

Keel is a design skill, not a licence to bulldoze a codebase. In any existing project:

- Never delete production files, route trees, component directories, or an existing site unless the user explicitly asks for deletion or approves a file-level plan that lists them.
- Default to in-place edits of the named files, or additive new components/tokens wired through the existing route. If the redesign needs multiple components removed, stop and ask first.
- Treat PDFs, READMEs, `.md` briefs, transcripts, and decks as *reference*, not copy — don't paste them verbatim unless the user says to.
- Before editing, state the exact files you expect to modify / create / delete. Deletions require explicit confirmation.

## Pipeline

1. **Read the target.** Extract its content (headings, copy, sections, real data/metrics) and its intent (audience, use case, tone). Keep the real numbers — never swap a user's real metric for an invented one.
2. **Pre-flight the stack.** Same scan as a build (framework, existing tokens/fonts, motion library). A redesign of a Next page must stay SSR-correct — carry [`ssr-and-hydration.md`](../ssr-and-hydration.md) forward; a redesign is a common place to *introduce* a theme flash by adding dark mode without the blocking script.
3. **Diversify the structure.** Read the current macrostructure (stamp or eyeball) and pick a *different* one from [`layout-and-structure.md`](../layout-and-structure.md). The whole point is that the redesign doesn't share the old page's fingerprint.
4. **Re-theme.** Compute a fresh palette + pairing via the [theming engine](../theming-engine.md). Default the seed to the brand/product name; honour `--anchor` / `--seed` if the user supplies them. If the project already has a locked token system the user wants kept, adopt it instead of generating.
5. **Preview, build, slop-test.** Same as a default build (SKILL.md Design flow steps 5–7). Emit the preview block, build, run the full slop test including the SSR gates, stamp, and log.

## `--mood` / silent-context note

When invoked with an explicit mood/anchor, the redesign reads its context from the target and the flag — it does **not** re-ask the audience/use/tone gate. Otherwise, if intent is ambiguous, ask the one bundled context question before rebuilding.

## What redesign preserves vs replaces

| Preserve | Replace |
| --- | --- |
| Routes, URLs, IA | Section rhythm / macrostructure |
| Component ownership & boundaries | Heading placement, alignment, asymmetry |
| Real copy intent & real metrics | Theme (palette + fonts, recomputed) |
| Brand name, legal, real assets | Nav/footer archetype, component voice |
| SSR correctness (keep it correct) | Motion treatment, enrichment |
