# CTA · Inline Form

**Use when** the primary action is capture itself — email for a trial, waitlist, or newsletter — and one field is enough. **Genre fit:** technical / editorial.

## Structure
One row: a short lead line above, then `[ input ][ button ]` sharing a baseline. Input and button are equal height (`--space-11`-ish), the button sits flush against the input with a single `--space-2` gap — no card, no band. A reserved helper-text slot lives under the row at a fixed min-height so validation never reflows the layout. On mobile the pair stacks (input full width, button full width beneath) and the helper slot stays reserved. Divider language: none needed; the input's own `1px` border does the separating. Accent appears only on the button fill (≤5%).

## Code
```tsx
'use client';
import { useState } from 'react';

export function InlineFormCTA() {
  const [state, setState] = useState<'idle'|'loading'|'error'|'success'>('idle');
  const [msg, setMsg] = useState('');

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setState('loading'); setMsg('');
    const fd = new FormData(e.currentTarget);
    const res = await fetch('/api/subscribe', { method: 'POST', body: fd });
    if (res.ok) { setState('success'); setMsg('Check your inbox to confirm.'); }
    else { setState('error'); setMsg('That address looks off. Use name@domain.com and try again.'); }
  }

  return (
    <form onSubmit={onSubmit} action="/api/subscribe" method="post" noValidate className="cta-form">
      <label htmlFor="cta-email" className="cta-form__lead">Start the free trial — no card.</label>
      <div className="cta-form__row">
        <input id="cta-email" name="email" type="email" required autoComplete="email"
          placeholder="name@domain.com" disabled={state === 'loading' || state === 'success'}
          aria-invalid={state === 'error'} aria-describedby="cta-help" className="cta-form__input" />
        <button type="submit" disabled={state === 'loading' || state === 'success'} className="cta-form__btn">
          {state === 'loading' ? 'Setting up…' : 'Start trial'}
        </button>
      </div>
      <p id="cta-help" role={state === 'error' ? 'alert' : undefined}
        className="cta-form__help" data-state={state}>{msg}</p>
    </form>
  );
}
```
```css
.cta-form__row { display: flex; gap: var(--space-2); align-items: stretch; }
.cta-form__input {
  flex: 1; height: var(--space-11); padding: 0 var(--space-3);
  font: var(--text-base)/1 var(--font-body); color: var(--color-ink);
  background: var(--color-paper); border: 1px solid var(--color-rule); border-radius: var(--radius);
  transition: background var(--dur-1) var(--ease-out), border-color var(--dur-1) var(--ease-out);
}
.cta-form__input:hover { border-color: var(--color-ink-2); }
.cta-form__input:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; } /* instant */
.cta-form__input[aria-invalid="true"] { border-color: var(--color-accent); background: var(--color-paper-2); }
.cta-form__input:disabled { opacity: 0.55; cursor: not-allowed; }
.cta-form__btn {
  height: var(--space-11); padding: 0 var(--space-4); border: 1px solid transparent; border-radius: var(--radius);
  font: var(--text-base)/1 var(--font-body); color: var(--color-accent-ink); background: var(--color-accent); cursor: pointer;
}
.cta-form__btn:disabled { opacity: 0.55; cursor: not-allowed; }
.cta-form__help { min-height: var(--space-5); margin-top: var(--space-2); font: var(--text-sm)/1.4 var(--font-body); color: var(--color-muted); }
.cta-form__help[data-state="error"] { color: var(--color-ink); }
@media (max-width: 34rem) { .cta-form__row { flex-direction: column; } .cta-form__btn { width: 100%; } }
```

## SSR / hydration note
This is a `'use client'` LEAF — keep it small and let the server render everything around it statically. The input must express all states (default / hover / focus-visible / active / disabled / loading / error / success); `border-width` stays `1px` throughout, so state changes ride on `border-color`, `background`, and the `outline` ring. Focus ring uses `outline` and appears instantly — never transition it. On submit show optimistic/loading copy ("Setting up…"), not a celebratory toast. The email error is a 3-part message: what's wrong, the expected shape, and the retry ("That address looks off. Use name@domain.com and try again."). Because `action`/`method` are set, it works as a real POST target / server action even before hydration, and labels/errors are wired with `htmlFor`, `aria-describedby`, `aria-invalid`, and `role="alert"`. See `../accessibility.md` and `../copywriting.md`; `../motion.md` for the focus-ring rule.

## Diversification knobs
- Lead line placement: above the row vs. inline label to the left.
- Button label register: imperative ("Start trial") vs. object ("Get access").
- Success behaviour: swap the row for a quiet confirmation line vs. keep row disabled with a check glyph.
- Field affordance: bare border vs. subtle `--color-paper-2` inset fill at rest.
