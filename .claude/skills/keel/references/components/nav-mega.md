# Nav · Mega-menu

**Use when** a product has many destinations (a platform with several products, use-cases, and resources) and a flat link row can't hold them. **Genre fit:** technical, editorial. INTERACTIVE — a top-level trigger expands a grouped panel on hover/focus.

## Structure
Wordmark left. Two or three top-level triggers (e.g. Products, Solutions, Resources) each owning a panel; one primary action right. A panel opens on hover AND on focus/click (keyboard parity), holds grouped columns of links, and closes on `Esc`, blur-out, or pointer-leave. Only one panel open at a time. Divider: `--color-rule` base on the bar; the panel is a `--color-paper` sheet with a soft shadow. Mobile: hover is unavailable — triggers become accordions inside a toggled full-height drawer; the panel content stacks vertically.

## Code
```jsx
'use client';
import { useState, useRef, useEffect } from 'react';

const MENUS = {
  Products: [['Ingest','/ingest'], ['Transform','/transform'], ['Warehouse','/warehouse']],
  Resources: [['Docs','/docs'], ['Changelog','/changelog'], ['Status','/status']],
};

export function MegaNav() {
  const [open, setOpen] = useState(null);           // null on server AND first client paint
  const navRef = useRef(null);
  useEffect(() => {
    function onKey(e) { if (e.key === 'Escape') setOpen(null); }
    function onClickOut(e) { if (navRef.current && !navRef.current.contains(e.target)) setOpen(null); }
    window.addEventListener('keydown', onKey);
    window.addEventListener('click', onClickOut);
    return () => { window.removeEventListener('keydown', onKey); window.removeEventListener('click', onClickOut); };
  }, []);
  return (
    <nav className="mega" aria-label="Primary" ref={navRef} onMouseLeave={() => setOpen(null)}>
      <a className="mega__mark" href="/">Strand</a>
      <ul className="mega__row">
        {Object.keys(MENUS).map(label => (
          <li key={label} onMouseEnter={() => setOpen(label)}>
            <button className="mega__trigger" aria-haspopup="true" aria-expanded={open === label}
              onClick={() => setOpen(v => v === label ? null : label)}>{label}</button>
            {open === label && (
              <div className="mega__panel" role="region" aria-label={label}>
                {MENUS[label].map(([t, href]) => <a key={href} href={href}>{t}</a>)}
              </div>
            )}
          </li>
        ))}
      </ul>
      <a className="mega__cta" href="/start">Start</a>
    </nav>
  );
}
```
```css
.mega { display:flex; align-items:center; gap:var(--space-6); padding:var(--space-4) var(--space-6);
  background:var(--color-paper); border-bottom:1px solid var(--color-rule); font-family:var(--font-body); }
.mega__mark { font-family:var(--font-display); font-weight:700; color:var(--color-ink); text-decoration:none; white-space:nowrap; }
.mega__row { list-style:none; display:flex; gap:var(--space-5); margin:0; padding:0; }
.mega__row li { position:relative; }
.mega__trigger { font:inherit; font-size:var(--text-sm); color:var(--color-ink-2); background:none; border:0;
  cursor:pointer; white-space:nowrap; transition:color var(--dur-fast) var(--ease-out); }
.mega__trigger[aria-expanded="true"], .mega__trigger:hover { color:var(--color-ink); }
.mega__panel { position:absolute; top:calc(100% + var(--space-3)); left:0; display:grid; gap:var(--space-2);
  min-width:14rem; padding:var(--space-4); background:var(--color-paper); border:1px solid var(--color-rule);
  border-radius:var(--radius); box-shadow:0 12px 40px color-mix(in oklab, var(--color-ink) 16%, transparent); z-index:40; }
.mega__panel a { font-size:var(--text-sm); color:var(--color-ink-2); text-decoration:none; white-space:nowrap;
  transition:color var(--dur-fast) var(--ease-out); }
.mega__panel a:hover { color:var(--color-accent); }
.mega__cta { margin-left:auto; font-size:var(--text-sm); font-weight:600; white-space:nowrap;
  padding:var(--space-2) var(--space-4); background:var(--color-accent); color:var(--color-accent-ink);
  border-radius:var(--radius); text-decoration:none; }
.mega :where(button,a):focus-visible { outline:2px solid var(--color-focus); outline-offset:3px; border-radius:var(--radius); }
@media (prefers-reduced-motion: reduce) { .mega__trigger, .mega__panel a { transition:none; } }
```

## SSR / hydration note
This is a `'use client'` LEAF — drop it into a Server Component page; do NOT `'use client'` the whole route. `open` starts `null`, so all panels are closed on server HTML and first client paint (no mismatch). The `Esc` and click-outside listeners attach in `useEffect`, never in render. Because it opens on hover only, keyboard and touch users reach panels via the `<button>` triggers (focus/click) — that parity is a hard [`../accessibility.md`](../accessibility.md) requirement, not optional. See [`../ssr-and-hydration.md`](../ssr-and-hydration.md) § 3 on keeping interactive islands at the leaves.

## Diversification knobs
- **Trigger count:** 2 vs 3 top-level menus; single-column vs multi-column panels.
- **Panel reveal:** instant vs short `--dur-fast` fade (reduced-motion guarded, [`../motion.md`](../motion.md)).
- **Panel anchoring:** left-aligned per-trigger vs one full-width sheet spanning the bar.
- **Action style:** filled accent `Start` vs ghost link.
