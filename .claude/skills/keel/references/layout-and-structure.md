# Layout & Structure

The single loudest AI tell is not colour or font — it is **shape**. Nearly every generated
landing page collapses to the same template:

> centred hero → row of 3 equal feature cards → centred CTA band → 4-column footer.

Ship that and the page reads as machine output before a single word is parsed. **Ban it as a
default.** Not because those parts are wrong, but because the *rhythm* is a fingerprint. Two Keel
pages built from two different briefs must not share a skeleton.

Variety here is **structural**, not decorative. Swapping the accent hue or the heading font on the
same skeleton is not variety — it is the same slop wearing a new coat. Variety means a different
macrostructure, a different heading placement, a different divider language, a different grid
rhythm. See [slop-test.md](slop-test.md) for the fingerprint checklist and
[anti-patterns.md](anti-patterns.md) for the catalogue of banned defaults.

## Macrostructure archetypes

Pick **exactly ONE** archetype per page. It sets the page's spine. **Two consecutive builds must
not use the same archetype** — if the last page was a Bento Grid, this one is not. These are a
small systematic set to *combine and vary*, not a catalogue to memorise.

**Document / Long-read** — editorial default for narrative-heavy briefs (essays, changelogs,
research, founder letters). One measure-width column, left-aligned, headings flush to the text
column. Body is prose with occasional pull-quotes and inline figures. Dividers are whitespace and
the odd `--color-rule` hairline; no cards. Reveal: static, or gentle fade on long scroll.

**Bento Grid** — for products with several parallel capabilities of *unequal* weight. An irregular
grid of tiles spanning different row/column counts (a 2×2 anchor, a wide 1×3, small 1×1s). Headings
live inside tiles, top-left. Divider language is the gap and tile surface (`--color-paper-2`).
Reveal: staggered entrance per tile. Never make all tiles equal — equal tiles are the 3-card slop.

**Marquee / Statement Hero** — atmospheric or brand-forward briefs. One oversized typographic
statement occupies the first viewport; supporting content is deliberately sparse below. Heading is
the hero, often off-centre or baseline-aligned. Body: minimal, one paragraph plus one action.
Dividers: dramatic whitespace, colour-shift between the marquee and what follows. Reveal: static
hero, content below on scroll.

**Stat-led** — for briefs where numbers *are* the argument (performance, scale, savings). Leads
with a band of large figures, each with a terse label. Heading sits above or beside the stat band.
Body composition alternates stat bands with short explanatory sections. Dividers: colour-shift
between bands. Reveal: count-up is optional and must be SSR-safe (see [motion.md](motion.md)).

**Split Studio (diptych)** — for briefs with a strong two-sided story (before/after, code/prose,
product/photo). The viewport splits into two vertical columns that hold different content types;
the split may invert down the page (text-left then text-right). Headings anchor to the text half.
Dividers: the seam itself, sometimes a `--color-rule` centre line. Reveal: halves slide in from
opposite sides, or static.

**Feature Stack (sticky-scroll)** — for a linear product walkthrough with 3–6 steps. A sticky
media/visual column pairs with a scrolling narrative column; content advances as you scroll.
Headings introduce each step in the scrolling column. Divider language is the scroll transition
itself. Reveal: scroll-driven — **must degrade to a plain static stack without JS** (SSR rule in
[motion.md](motion.md)). Use sparingly; it is heavy.

**Manifesto / Poster** — playful or opinionated briefs. Large centred or hard-left declarative
lines, poster typography, minimal chrome, almost no cards. Heading and body blur together as
typographic hierarchy. Dividers: colour blocks and whitespace. Reveal: static, or a single bold
entrance. High personality, low information density.

**Catalogue / Index** — for many peer items (docs, a component library, a directory, pricing
tiers). A dense, list- or table-like index, often with a left rail of categories. Headings are
section labels flush-left. Body: rows or a tight uniform grid where uniformity is *correct* because
the items are genuine peers. Dividers: `--color-rule` between rows. Reveal: static.

## Composition axes

The archetype sets sensible defaults on each axis; **override deliberately** to differentiate two
pages that happen to share an archetype.

- **Heading placement** — flush-left / centred / off-axis / baseline-aligned / inside-tile. Default
  away from centred. A left-flush heading over a centred body already breaks the template.
- **Alignment & asymmetry** — symmetric vs off-axis. Push the eyebrow, CTA, or media off the centre
  line; align content to a margin rather than the page centre.
- **Divider language** — how sections separate: `--color-rule` hairline / colour-shift
  (`--color-paper` ↔ `--color-paper-2`) / pure whitespace / an ornament (dingbat, number, icon).
  Pick a *primary* language per page and stay mostly consistent.
- **Grid rhythm** — even spans vs irregular spans. Even = peers (Catalogue). Irregular = weighted
  content (Bento). Do not default to three equal columns.
- **Density** — airy vs packed. Long-reads and Manifestos are airy; Catalogues and Stat-led run
  dense. Density should track the genre, not habit.
- **Reveal** — static vs scroll-entrance. Every scroll-entrance must render fully without JS and be
  disabled under `prefers-reduced-motion`. Default to static; earn motion. See
  [motion.md](motion.md).

## The 4pt spacing scale

Spacing uses the `--space-*` ladder only. **Never** write arbitrary values like `padding: 17px` —
reach for the nearest semantic step. This keeps vertical rhythm coherent across sections.

| Token         | rem    | px  |
|---------------|--------|-----|
| `--space-3xs` | 0.25   | 4   |
| `--space-2xs` | 0.5    | 8   |
| `--space-xs`  | 0.75   | 12  |
| `--space-sm`  | 1      | 16  |
| `--space-md`  | 1.5    | 24  |
| `--space-lg`  | 2      | 32  |
| `--space-xl`  | 3      | 48  |
| `--space-2xl` | 4      | 64  |
| `--space-3xl` | 6      | 96  |
| `--space-4xl` | 8      | 128 |
| `--space-5xl` | 12     | 192 |

Section vertical padding lives in the `--space-2xl`…`--space-5xl` range; intra-component gaps in
`--space-3xs`…`--space-lg`. Vary section padding — see Section rhythm below.

## Asymmetry & grid-breaks

Centred-everything is the safe, slop default. Break it deliberately:

- **Off-axis eyebrow / CTA** — place the eyebrow or action against a margin, not dead-centre.
- **Asymmetric spans** — let one column dominate. A 7/5 or 8/4 split reads as designed; 6/6 reads
  as default.
- **Margin alignment** — align a heading to the content column's left edge and let the body indent,
  or hang a number/label into the left margin.

One concrete grid: a 12-column track where the heading occupies columns 1–4 and the body occupies
6–12, leaving column 5 as an intentional gutter.

```css
.section-grid {
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  gap: var(--space-lg);
}
.section-grid h2   { grid-column: 1 / 5; }
.section-grid .body { grid-column: 6 / 13; }
```

## Section rhythm

Sections must not all breathe identically — uniform whitespace top to bottom is its own tell. Vary:

- **Surface** — alternate `--color-paper` and `--color-paper-2`, but not in a strict ABAB stripe;
  cluster two paper sections, then shift.
- **Rule usage** — some transitions get a `--color-rule` hairline, others get only whitespace or a
  colour-shift. Do not hairline every seam.
- **Vertical rhythm** — a dense Catalogue block can sit at `--space-2xl` padding while the next
  statement section opens up to `--space-4xl`. Contrast is the point.

## Nav & footer are structure, not chrome

These are top fingerprints. The AI-default **nav** (wordmark-left + 4 centred links + button-right +
a hairline underline) and AI-default **footer** (4 link columns + a social-icon row + tiny centred
copyright) are instantly recognisable. **Default away from the canonical versions.**

Nav alternates: **minimal wordmark-only**, **left-stacked (logo above a thin link row)**, **split
justified (logo far-left, single action far-right, no centre links)**, **sidebar / rail nav**,
**inline-in-hero (nav folded into the hero, no separate bar)**.

Footer alternates: **single-line footer (wordmark + one link cluster + copyright on one row)**,
**big-type sign-off (oversized closing statement, minimal links)**, **two-column
(contact/legal left, nav right)**, **contact-card footer (address / email as the content, not a
link farm)**.

These are the *shapes*; the copy-pasteable specs (with code + SSR notes) live in
[component-specs.md](component-specs.md) — pick nav/hero/CTA/footer there via the genre routing
table, and load only the specs you pick.

## The eyebrow / tag rule

Section eyebrows (small kicker labels above a heading) default **OFF**. They are overused and most
generated pages sprinkle them on every section. Use one only when it earns its place.

When you do use an eyebrow, **stack the heading directly below it in the same column** — a simple
vertical stack, both left-aligned. The **tag-left / heading-right two-column pattern** (tiny label
floated in a narrow left column, heading in a wide right column) is a banned templated-editorial
tell; see [slop-test.md](slop-test.md). Vertical stack only.

## Mobile-structural non-negotiables

Brief, and enforced — details in [accessibility.md](accessibility.md) and [slop-test.md](slop-test.md):

- **No horizontal scroll.** Set `overflow-x: clip` on `html, body`; never let a section push width.
- **Image-bearing grid tracks use `minmax(0, 1fr)`**, not `1fr` — bare `1fr` lets images blow out
  the track and trigger horizontal overflow.
- **Section heads collapse to one column on mobile.** Any asymmetric or two-column head becomes a
  single stacked column below the layout breakpoint.
- **No two-line clickable text.** Links and buttons must not wrap to two lines at mobile width;
  shorten the label or widen the tap target.

## Closer

Reach for the archetype first, set the six axes second, and check the result against
[slop-test.md](slop-test.md) before you call it done. If your page could be described as "hero,
three cards, CTA, footer," you have not started designing yet — you have shipped the template.
