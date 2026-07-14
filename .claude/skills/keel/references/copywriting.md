# Copywriting

Copy is design. A pixel-perfect layout wrapped around stock copy still reads as generated — the words are the first thing a human parses and the fastest tell of AI slop.

This file is grounded in the Anthropic frontend-design writing principles. Everything below is downstream of them.

## Principles

**Active voice.** The subject does the thing. Passive voice hides who acted and reads like a system covering for itself.
- Good: "We couldn't find your account."
- Bad: "Your account could not be found."

**Specific over clever.** Concrete nouns, verbs, and numbers beat metaphor and wordplay. Cleverness is the reflex of a writer with nothing concrete to say.
- Good: "Deploys to 34 regions in under 90 seconds."
- Bad: "Ship at the speed of thought."

**No invented user names.** Never "Jane Doe," "John Smith," "Sarah from Marketing." Use the real signed-in name, a role, or restructure to avoid a name. Exception: the page is literally a placeholder-name generator or a name-input demo.
- Good: "Signed in as you" / "Signed in as the project owner."
- Bad: "Welcome back, Jane Doe!"

**No fabricated metrics or claims.** Never invent "10× faster," "trusted by 50,000+ teams," "+47% conversion," "99.99% uptime." If the user supplied no number, use an em-dash placeholder and flag it, or drop the proof slot entirely. Hard rule — see [slop-test.md](slop-test.md) and [anti-patterns.md](anti-patterns.md).
- Good: "Trusted by — teams" `<!-- metric to confirm -->` or omit the line.
- Bad: "Trusted by 50,000+ teams worldwide."

## Buttons

Label the button with the verb for the action it performs. The user should predict what happens before clicking.

Good:
- "Save changes"
- "Create project"
- "Send invite"
- "Delete workspace"

Bad:
- "Submit" — verb for the form, not the user's goal
- "OK" — names nothing
- "Continue" — where to?
- "Click here" — describes the mechanic, not the outcome

Ranking: named action ("Save changes") > generic verb ("Submit") > acknowledgement ("OK").

## Error messages

Three parts, in order:
1. **What happened** — plainly, active voice.
2. **Why** — only if you actually know.
3. **What to do** — one imperative fix.

Never apologize for the user's input. Never open with "Oops!" Never blame the user; state the condition and the fix.

Example:
> **Card declined.** Your bank rejected the charge. Try another card or contact your bank.

Not:
> Oops! Something went wrong with your payment. Please try again later.

The bad version fails all three: no what, no why, no actionable fix — and it apologizes with a cutesy interjection on a money-losing path.

## Empty states

Three beats:
1. **Name what's empty** — say what would be here.
2. **Why it matters** — the one-line reason to fill it.
3. **One next-action button** — a single primary verb.

Example:
> **No projects yet.** Projects hold your deploys, domains, and logs in one place.
> [Create project]

One action, not three competing links. The empty state is an onboarding surface, not a dead end.

## Loading copy

Match the wait to the words. A [Suspense](ssr-and-hydration.md) fallback IS loading copy — write it deliberately, not a bare spinner.

- **Short (< 2s):** spinner alone, no text. Words that flash and vanish are noise.
- **Medium (> 2s):** honest verb. "Loading…" or "Saving…". Name the thing if you can: "Loading invoices…".
- **Long (> 10s):** honest label plus progress. "Importing 1,204 rows — 40% done." Never a fake percentage that jumps to 100.

Streaming SSR: every `<Suspense fallback>` is a chance to say what's arriving. `fallback={<InvoiceTableSkeleton />}` with a labeled skeleton beats `fallback={<Spinner />}`. See [ssr-and-hydration.md](ssr-and-hydration.md).

## Microcopy bans

| Banned | Why it fails |
| --- | --- |
| "Click here" | Names the mechanic, not the outcome; useless to screen readers scanning link text. |
| "Oops! / Something went wrong" | Cutesy on a failure path; tells the user nothing and no way forward. |
| Exclamation marks in errors | Manufactured cheer while the user is blocked; reads as tone-deaf. |
| Humour on frustration paths | Payment failed, upload broke, account locked — a joke here reads as mockery. |
| Stock names (Jane Doe, John Smith) | Instant placeholder tell; nobody shipped real copy here. |
| Startup clichés (Acme, Nexus, Unleash, Seamless, Supercharge, Transform, Elevate, Empower, Delight, Magical) | Category-generic; swaps in for any product, so it describes none. |
| Feeling-without-feature ("Experience the power of…") | Asserts an emotion with no concrete thing behind it; pure filler. |

## Banned opening lines

Every one of these fronts a page that could be selling anything. Specificity is the fix — see [slop-test.md](slop-test.md).

| Banned opener | Why it fails |
| --- | --- |
| "Built for the modern team" | "Modern" and "team" name no product, no vertical, no user. |
| "Unleash your [X]" | Metaphor standing in for a feature; unleashing nothing concrete. |
| "Where [X] meets [Y]" | Formula, not a claim; collapses two vague nouns into a third. |
| "Empower your…" | Verb with no mechanism; empowerment via what? |
| "Reimagine…" | Promises novelty, describes nothing. |
| "Supercharge your workflow" | "Workflow" is the everything-noun; "supercharge" the everything-verb. |
| "Innovative solutions" | Two words that survive any find-and-replace across industries. |
| "Seamless integration" | Claims absence of friction without naming what connects to what. |
| "In today's digital landscape" | Throat-clearing; zero information in six words. |
| "Next-generation [X]" | Positions against an unnamed previous generation; asserts newness, not value. |

## Proper typography in copy

Type the real characters. `--` and `...` are the mark of copy pasted from a plain-text editor.

- Curly quotes: “like this” and ‘this’ — never straight `"` `'`.
- Em-dash — for interruption and aside — no surrounding spaces or thin spaces per house style; never `--`.
- En-dash for ranges: 2010–2019, 9 am–5 pm, pages 40–48. Never a hyphen for a range.
- Ellipsis: … one glyph, never `...`.
- Real apostrophe: it’s, don’t, you’re — U+2019, not `'`.
- Non-breaking space before units and between value pairs: `10&nbsp;GB`, `90&nbsp;ms`, `$5&nbsp;/mo` — stops a number orphaning from its unit at a line break.

## Voice by tone

Illustrative patterns, not templates to paste. Notice what each does: names a place, a date, a vertical, a concrete verb — and refuses metaphor. Invent your own plausible specifics; never lift a real company's tagline.

**Editorial** — declarative, has a point of view, reads like a sentence a person wrote.
- "We started migrating in March 2024. It took eleven weeks. Here's what broke."
- "Most invoicing tools assume you bill monthly. Freelancers don't."

**Technical** — precise, quantified, assumes a competent reader.
- "Postgres logical replication with zero downtime cutover. Verified on 2 TB datasets."
- "Sub-100&nbsp;ms p99 reads from three regions. No cache warm-up."

**Austere / luxury** — few words, high confidence, no adjectives doing sales work.
- "Steel. Machined in Solingen. Sharpened by hand."
- "One plan. No tiers."

**Playful** — wit that adds information, never jokes on a frustration path.
- "Your side project deserves a domain it can't afford. This one's on us."
- "Yes, it does dark mode. We're not animals."

Cross-tone rule: playful still obeys the error-message and no-fabrication rules. Wit is allowed in headlines and empty states, banned in failures.

## When the brief gives you nothing

If the user handed you no product noun, no vertical, no place, no number — you cannot invent specificity about their product. Inventing it is fabrication, same rule as metrics.

Say so, then ask exactly one question that forces a concrete answer:

> I can lay this out, but the copy will read generic without one concrete detail. What does the product actually do — in one sentence, name the thing it makes or the task it removes?

Ask for a noun, a verb, or a place — not a vibe. One question, then build with what comes back. Do not fill the gap with clichés from the banned tables above.
