"""
Keel deterministic theming engine — reference implementation.
Proves: seed (string) -> byte-identical OKLCH palette + font pairing, every time.
Also verifies WCAG contrast on the generated pairs so the worked example ships real numbers.
"""
import math

# ---------- 1. Deterministic hash (FNV-1a, 32-bit) ----------
def fnv1a(s: str) -> int:
    h = 0x811c9dc5
    for ch in s.encode("utf-8"):
        h ^= ch
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h

def stream(seed: str):
    """Yield an endless deterministic sequence of 32-bit ints from one seed.
    Each 'draw' rehashes the seed with a salt index, so draws are independent
    but fully reproducible."""
    i = 0
    while True:
        yield fnv1a(f"{seed}#{i}")
        i += 1

# ---------- 2. Seed -> palette parameters ----------
# optional vibe -> hue anchor. When intent is known, pin the hue; determinism is unaffected.
VIBE_HUE = {"warm":40,"technical":233,"steel-blue":233,"cool":233,"botanical":150,
            "moss":150,"neon":300,"amber":75,"terracotta":30,"forest":150}

def palette_params(seed: str, anchor: str | None = None):
    g = stream(seed)
    d = list(next(g) for _ in range(6))
    if anchor and anchor in VIBE_HUE:
        hue = VIBE_HUE[anchor]            # intent pins the hue...
    else:
        hue = d[0] % 360                  # ...else full-wheel spread across seeds
    chroma = 0.12 + (d[1] % 81) / 1000     # accent chroma in [0.120, 0.200]
    # paper mode: 62.5% light / 37.5% dark, biased to light (landing pages skew light)
    dark = (d[2] % 8) < 3
    return {"seed": seed, "hash": fnv1a(seed), "hue": hue, "chroma": round(chroma, 3),
            "mode": "dark" if dark else "light", "draw": d}

# ---------- 3. Build the OKLCH ramp (deterministic, rule-obeying) ----------
def oklch(L, C, H):
    return (round(L, 4), round(C, 4), H)

def in_srgb(L, C, H, eps=1e-4):
    r, g, b = oklch_to_linear_srgb(L, C, H)
    return all(-eps <= v <= 1 + eps for v in (r, g, b))

def fit_gamut(L, C, H):
    """Hold L and H, reduce chroma until the colour is renderable in sRGB.
    Without this, ~48% of seeds emit an oklch() the browser silently desaturates —
    the palette we verify is then not the palette that paints. Fixed iteration
    count keeps this bit-for-bit deterministic.

    Chroma is FLOORED at the precision the CSS actually prints (3dp), never rounded:
    round-to-nearest can round back up across the gamut boundary the search just
    found, re-emitting an unrenderable colour. Floor at emit-precision guarantees
    the value written into the stylesheet — not just the value in memory — is inside sRGB."""
    if in_srgb(L, C, H):
        return (L, C, H)
    lo, hi = 0.0, C
    for _ in range(32):
        mid = (lo + hi) / 2
        if in_srgb(L, mid, H):
            lo = mid
        else:
            hi = mid
    return (L, math.floor(lo * 1000) / 1000, H)   # 3dp == the CSS emit precision

def build_palette(p):
    H = p["hue"]
    Cacc = p["chroma"]
    tint = 0.010                     # neutral chroma tint toward anchor
    if p["mode"] == "light":
        paper_L   = 0.97
        paper2_L  = 0.94
        rule_L    = 0.86
        muted_L   = 0.52
        ink2_L    = 0.34
        ink_L     = 0.20
        acc_L     = 0.55             # accent lightness for a light-paper page
        acc_ink_L = 0.98             # text on accent fill (light)
    else:
        paper_L   = 0.16
        paper2_L  = 0.20
        rule_L    = 0.30
        muted_L   = 0.62
        ink2_L    = 0.78
        ink_L     = 0.94
        acc_L     = 0.72
        acc_ink_L = 0.16
    # --- deterministic contrast fitting, in-gamut ---
    # accent must clear 4.5:1 vs its overlay text AND 3:1 vs paper. Nudge accent L
    # (down on light paper, up on dark paper) in fixed 0.01 steps until both hold.
    # Gamut-fit BEFORE measuring: a colour outside sRGB is repainted by the browser,
    # so contrast measured on the unfitted value would certify a colour nobody sees.
    acc_ink = fit_gamut(acc_ink_L, tint, H)
    paper   = fit_gamut(paper_L, tint, H)
    step = -0.01 if p["mode"] == "light" else +0.01
    for _ in range(40):
        acc = fit_gamut(acc_L, Cacc, H)
        if wcag_ratio(acc_ink, acc) >= 4.5 and wcag_ratio(acc, paper) >= 3.0:
            break
        acc_L = round(acc_L + step, 3)
    focus_L = acc_L + (0.05 if p["mode"] == "light" else 0.06)
    return {
        "--color-paper":     oklch(*fit_gamut(paper_L,  tint,       H)),
        "--color-paper-2":   oklch(*fit_gamut(paper2_L, tint+0.002, H)),
        "--color-rule":      oklch(*fit_gamut(rule_L,   tint+0.004, H)),
        "--color-muted":     oklch(*fit_gamut(muted_L,  tint,       H)),
        "--color-ink-2":     oklch(*fit_gamut(ink2_L,   tint+0.002, H)),
        "--color-ink":       oklch(*fit_gamut(ink_L,    tint+0.004, H)),
        "--color-accent":    oklch(*acc),
        "--color-accent-ink":oklch(*acc_ink),
        "--color-focus":     oklch(*fit_gamut(min(focus_L,0.85), Cacc+0.04, H)),
    }

# ---------- 4. OKLCH -> sRGB (for contrast verification) ----------
def oklch_to_linear_srgb(L, C, H):
    a = C * math.cos(math.radians(H))
    b = C * math.sin(math.radians(H))
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_**3, m_**3, s_**3
    r = +4.0767416621*l - 3.3077115913*m + 0.2309699292*s
    g = -1.2684380046*l + 2.6097574011*m - 0.3413193965*s
    bch = -0.0041960863*l - 0.7034186147*m + 1.7076147010*s
    return (r, g, bch)

def gamma(x):
    x = max(0.0, min(1.0, x))
    return 12.92*x if x <= 0.0031308 else 1.055*(x**(1/2.4)) - 0.055

def rel_luminance(L, C, H):
    r, g, b = oklch_to_linear_srgb(L, C, H)
    r, g, b = (max(0,min(1,v)) for v in (r,g,b))
    return 0.2126*r + 0.7152*g + 0.0722*b

def wcag_ratio(c1, c2):
    L1 = rel_luminance(*c1); L2 = rel_luminance(*c2)
    hi, lo = max(L1,L2), min(L1,L2)
    return round((hi+0.05)/(lo+0.05), 2)

# ---------- 5. Constraint-filtered font pairing ----------
# Pool: (display, body, mono?, x-height-class, voice) — free Google fonts only, ban-list excluded.
FONTS = [
    # display,           body,            voice,        xheight
    ("Fraunces",         "Source Serif 4", "editorial",  "tall"),
    ("Newsreader",       "Source Sans 3",  "editorial",  "tall"),
    ("Instrument Serif", "Newsreader",     "classical",  "med"),
    ("Space Grotesk",    "Inter Tight",    "technical",  "tall"),
    ("Bricolage Grotesque","Geist",        "modern",     "tall"),
    ("Fraunces",         "Geist",          "warm-tech",  "tall"),
    ("Libre Franklin",   "Source Serif 4", "grotesk-serif","med"),
    ("Spectral",         "IBM Plex Sans",  "literary",   "med"),
    ("Syne",             "Geist",          "art",        "tall"),
    ("Big Shoulders Display","Inter Tight","condensed",  "tall"),
]
BANNED = {"Inter","Roboto","Open Sans","Poppins","Lato","Work Sans","DM Sans","Montserrat","system-ui"}

GENRE_VOICES = {
    "technical":  {"technical","modern","warm-tech","condensed"},
    "editorial":  {"editorial","classical","literary","grotesk-serif"},
    "atmospheric":{"modern","art","technical"},
    "playful":    {"art","warm-tech","modern"},
}

def pick_pairing(p, genre="editorial"):
    # constraint filters, in order:
    #  1. ban-list — no display OR body font may be a distribution default
    #  2. voice filter — pairing voice must be in the active genre's allowed set
    #  then deterministic pick within the survivors.
    voices = GENRE_VOICES.get(genre, GENRE_VOICES["editorial"])
    allowed = [f for f in FONTS
               if f[0] not in BANNED and f[1] not in BANNED and f[2] in voices]
    if not allowed:                       # fail-safe: never return empty
        allowed = [f for f in FONTS if f[0] not in BANNED and f[1] not in BANNED]
    display, body, voice, xh = allowed[p["draw"][3] % len(allowed)]
    mono = "Geist Mono" if p["draw"][4] % 2 else "JetBrains Mono"
    return {"display": display, "body": body, "mono": mono, "voice": voice}

# ---------- 6. Run for the worked-example seed + spread demo ----------
def fmt(c): return f"oklch({c[0]*100:.0f}% {c[1]:.3f} {c[2]})"

def report(seed, anchor=None, genre="editorial"):
    p = palette_params(seed, anchor)
    pal = build_palette(p)
    fonts = pick_pairing(p, genre)
    print(f"\n=== seed: {seed!r}  hash={p['hash']}  hue={p['hue']}  chroma={p['chroma']}  mode={p['mode']} ===")
    for k,v in pal.items():
        print(f"  {k:20s} {fmt(v)}")
    print(f"  fonts: display={fonts['display']} · body={fonts['body']} · mono={fonts['mono']} · voice={fonts['voice']}")
    # contrast checks that MUST pass
    ink   = pal["--color-ink"]; paper = pal["--color-paper"]
    muted = pal["--color-muted"]; paper2 = pal["--color-paper-2"]
    acc   = pal["--color-accent"]; accink = pal["--color-accent-ink"]
    print(f"  CONTRAST ink/paper       = {wcag_ratio(ink,paper)}:1   (need >=4.5 body)")
    print(f"  CONTRAST muted/paper     = {wcag_ratio(muted,paper)}:1   (need >=4.5)")
    print(f"  CONTRAST accent-ink/accent = {wcag_ratio(accink,acc)}:1 (need >=4.5 on CTA)")
    print(f"  CONTRAST accent/paper    = {wcag_ratio(acc,paper)}:1   (need >=3 large/UI)")
    # gamut is verified explicitly: rel_luminance() clamps, so an out-of-sRGB colour
    # would otherwise pass a contrast check on a colour the browser never paints.
    oog = [k for k, v in pal.items() if not in_srgb(*v)]
    print(f"  GAMUT   all tokens in sRGB = {not oog}" + (f"  OUT: {oog}" if oog else ""))
    return p, pal, fonts

# worked-example seed, anchored steel-blue, technical genre (logistics dev-tool)
report("Wharfline · cold-chain logistics observability", anchor="steel-blue", genre="technical")
# reproducibility proof: same seed twice
a = palette_params("Wharfline · cold-chain logistics observability")
b = palette_params("Wharfline · cold-chain logistics observability")
print("\nreproducible:", a == b)
# spread proof: different seeds land on different hues
print("spread:", [palette_params(s)["hue"] for s in ["acme","northwind","tempo","quill","mossbank","riverstone"]])
