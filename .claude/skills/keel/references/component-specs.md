# Component specs — the index

Structural variety only works if the model has concrete non-default parts to reach for. Naming "use a floating nav" in prose doesn't beat the training prior — the model reverts to the wordmark-left / 3-card / 4-column-footer template unless it has a *specced alternative* in hand. This directory is that set: 16 lean specs, each with real code and its SSR/hydration note.

**Load discipline (index-then-pick).** Read *this index*, pick your nav / hero / CTA / footer, then load **only** the picked spec files from [`components/`](components/). A typical build loads 3–4 spec files. Do not load the whole directory — that's dead tokens.

Each spec follows the same shape: **Use when · Genre fit · Structure · Code · SSR/hydration note · Diversification knobs.** The knobs matter: two builds that pick the same archetype must vary the knobs so they don't look identical (this is the same discipline as the macrostructure rotation in [`layout-and-structure.md`](layout-and-structure.md)).

## Navigation (6)

| Spec | Use when | Interactive? |
| --- | --- | --- |
| [`nav-minimal`](components/nav-minimal.md) | The page has ~1–2 destinations; wordmark + at most one action. | no |
| [`nav-split-justified`](components/nav-split-justified.md) | The de-slopped default marketing nav — logo far-left, one action far-right, no centre link cluster. | no |
| [`nav-command-pill`](components/nav-command-pill.md) | Technical / dev-tool audience; an inline ⌘K search-pill that opens a command palette. | **yes** (client leaf) |
| [`nav-rail`](components/nav-rail.md) | Editorial / portfolio; a vertical side rail with content to its right. | no |
| [`nav-inline-hero`](components/nav-inline-hero.md) | Manifesto / marquee pages; nav folds into the hero, no separate bar. | no |
| [`nav-mega`](components/nav-mega.md) | A product with many destinations; a mega-menu panel on hover/focus. | **yes** (client leaf) |

**Default away from the AI-default nav** (wordmark-left + 4–5 centred links + button-right + hairline + white bg). Reach for `nav-split-justified` as the sober default; `nav-command-pill` for technical; `nav-minimal` only when the page genuinely has ~2 destinations.

## Heroes (5)

| Spec | Use when |
| --- | --- |
| [`hero-stat-led`](components/hero-stat-led.md) | Numbers are the argument — a lead figure paired with a worded headline (never a bare number). |
| [`hero-marquee`](components/hero-marquee.md) | Brand-forward / manifesto; one oversized typographic statement fills the first viewport. |
| [`hero-split`](components/hero-split.md) | A two-sided story (before/after, code/prose, product/photo); a diptych that may invert. |
| [`hero-media`](components/hero-media.md) | Anchored by a real image or video — the LCP element. See [`media-and-performance.md`](media-and-performance.md). |
| [`hero-letter`](components/hero-letter.md) | Founder / editorial voice; a salutation-body-signoff letter. |

**Default away from the centred-everything hero** (eyebrow + title + lede + CTA on one centred axis, `min-height: 100vh`). Every hero is off-axis and — critically — **visible without JS**; entrance animation is additive (see [`motion.md`](motion.md)).

## CTAs (2)

| Spec | Use when | Interactive? |
| --- | --- | --- |
| [`cta-inline-form`](components/cta-inline-form.md) | The action is a capture — email / start-trial input + button on one line. | **yes** (client leaf) |
| [`cta-statement`](components/cta-statement.md) | One bold typographic line + one action; no card, no gradient band. | no |

## Footers (3)

| Spec | Use when |
| --- | --- |
| [`footer-single-line`](components/footer-single-line.md) | The de-slopped default — wordmark + one link cluster + copyright on a row. |
| [`footer-big-type`](components/footer-big-type.md) | An oversized closing statement with minimal links below. |
| [`footer-contact-card`](components/footer-contact-card.md) | Studio / agency / local — real contact info as content, not a link farm. |

**Default away from the AI-default footer** (4 link columns Product/Company/Resources/Legal + social-icon row + tiny copyright + hairline). Reach for `footer-single-line` unless the page is a genuine docs/hub root.

## Genre routing (default → acceptable alternates)

| Genre | Nav default | Nav alternates | Footer default | Hero leanings |
| --- | --- | --- | --- | --- |
| **editorial** | `nav-rail` | `nav-split-justified`, `nav-minimal` | `footer-big-type` | `hero-letter`, `hero-marquee` |
| **technical** | `nav-command-pill` | `nav-split-justified`, `nav-minimal` | `footer-single-line` | `hero-stat-led`, `hero-split` |
| **atmospheric** | `nav-inline-hero` | `nav-minimal`, `nav-split-justified` | `footer-big-type` | `hero-marquee`, `hero-media` |
| **playful** | `nav-split-justified` | `nav-inline-hero`, `nav-mega` | `footer-single-line` | `hero-split`, `hero-media` |

Rotate through the alternates column across builds — reaching for the genre default on *every* build is how eight pages ship two navs. State the pick and why it differs from the last build, per SKILL.md Step 2.

## SSR reminder for interactive specs

`nav-command-pill`, `nav-mega`, and `cta-inline-form` are the only interactive specs. Each is a **`'use client'` leaf** — never lift the directive to the page. Any `window`/`localStorage` read uses the `mounted` two-pass pattern; listeners attach in `useEffect`; the page around them stays a Server Component. See [`ssr-and-hydration.md`](ssr-and-hydration.md).
