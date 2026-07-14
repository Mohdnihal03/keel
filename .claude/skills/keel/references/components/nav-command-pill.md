# Nav · Command-pill

**Use when** the audience is technical (dev tools, APIs, infra) and a `⌘K` search-pill signals "this is built for people who live in keyboards." **Genre fit:** technical (primary); playful if the palette leans terminal. INTERACTIVE — the pill opens a command palette.

## Structure
Wordmark left. A centre-or-right search *pill* — a button styled like an input, with placeholder text and a `⌘K` kbd hint on its trailing edge. Optional single action far-right. Clicking the pill (or pressing `⌘K` / `Ctrl+K`) opens a command palette overlay. Divider: mono wordmark over `--color-paper`, thin `--color-rule` base. Mobile: the pill collapses to a search glyph button; the palette opens full-width.

## Code
```jsx
'use client';
import { useState, useEffect, useRef } from 'react';

export function CommandPillNav() {
  const [open, setOpen] = useState(false);          // default-closed on server AND first client paint
  const inputRef = useRef(null);
  const isMac = useRef(false);
  useEffect(() => { isMac.current = /Mac/i.test(navigator.platform); }, []);
  useEffect(() => {
    function onKey(e) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); setOpen(v => !v); }
      if (e.key === 'Escape') setOpen(false);
    }
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);
  useEffect(() => { if (open) inputRef.current?.focus(); }, [open]);

  return (
    <nav className="nav-cp" aria-label="Primary">
      <a className="nav-cp__mark" href="/">quanta</a>
      <button className="nav-cp__pill" onClick={() => setOpen(true)} aria-haspopup="dialog" aria-expanded={open}>
        <span className="nav-cp__ph">Search docs, commands…</span>
        <kbd className="nav-cp__kbd">⌘K</kbd>
      </button>
      {open && (
        <div className="nav-cp__scrim" role="dialog" aria-modal="true" aria-label="Command palette" onClick={() => setOpen(false)}>
          <div className="nav-cp__panel" onClick={e => e.stopPropagation()}>
            <input ref={inputRef} className="nav-cp__input" placeholder="Type a command…" />
          </div>
        </div>
      )}
    </nav>
  );
}
```
```css
.nav-cp { display:flex; align-items:center; gap:var(--space-6); padding:var(--space-4) var(--space-6);
  background:var(--color-paper); border-bottom:1px solid var(--color-rule); font-family:var(--font-body); }
.nav-cp__mark { font-family:var(--font-mono); font-weight:600; color:var(--color-ink); text-decoration:none; white-space:nowrap; }
.nav-cp__pill { display:flex; align-items:center; gap:var(--space-4); margin-left:auto; min-width:20rem;
  padding:var(--space-2) var(--space-3); background:var(--color-paper-2); border:1px solid var(--color-rule);
  border-radius:var(--radius); color:var(--color-muted); font:inherit; cursor:pointer;
  transition:border-color var(--dur-fast) var(--ease-out); }
.nav-cp__pill:hover { border-color:var(--color-ink-2); }
.nav-cp__ph { font-size:var(--text-sm); white-space:nowrap; }
.nav-cp__kbd { margin-left:auto; font-family:var(--font-mono); font-size:var(--text-xs);
  color:var(--color-ink-2); background:var(--color-paper); border:1px solid var(--color-rule);
  border-radius:var(--radius); padding:0 var(--space-2); }
.nav-cp__scrim { position:fixed; inset:0; background:color-mix(in oklab, var(--color-ink) 40%, transparent);
  display:flex; justify-content:center; padding-top:12vh; z-index:50; }
.nav-cp__panel { width:min(36rem,92vw); background:var(--color-paper); border:1px solid var(--color-rule);
  border-radius:var(--radius); box-shadow:0 12px 40px color-mix(in oklab, var(--color-ink) 20%, transparent); }
.nav-cp__input { width:100%; padding:var(--space-4); border:0; background:transparent; color:var(--color-ink);
  font:inherit; font-size:var(--text-md); }
.nav-cp__pill:focus-visible, .nav-cp__input:focus-visible { outline:2px solid var(--color-focus); outline-offset:2px; }
@media (prefers-reduced-motion: reduce) { .nav-cp__pill { transition:none; } }
```

## SSR / hydration note
This is a `'use client'` LEAF — mount it inside a Server Component page, never `'use client'` the whole route. `open` starts `false` so server HTML and first client paint agree; the `⌘K` listener attaches in `useEffect` (never during render). `navigator.platform` is read only inside `useEffect` behind a ref — reading it in the render body is a mismatch (see [`../ssr-and-hydration.md`](../ssr-and-hydration.md) § 2). The pill button and palette input each carry a `:focus-visible` ring; the palette needs focus-trapping + `Esc`-to-close per [`../accessibility.md`](../accessibility.md).

## Diversification knobs
- **Pill placement:** centre vs right-of-mark (`margin-left:auto`).
- **Hint style:** `⌘K` kbd vs `/` slash-hint vs no hint (glyph only).
- **Palette entrance:** instant vs short `--dur-fast` fade (reduced-motion guarded, per [`../motion.md`](../motion.md)).
- **Wordmark:** mono lowercase vs display bold.
