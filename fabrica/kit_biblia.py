"""Elementos bíblicos reutilizáveis (copiados do Elías): mulher, fogo, montanha, altar, multidão, anjo, enebro, jarro, pão, nuvem, céu, chão."""
from fabrica.kit import *

POVO = ["#2e5aa8", "#a0522d", "#7a3a5a", "#5a7a3a", "#8a6a3a", "#3a6a8a", "#9a4a2a"]


def mulher(t, x, y, s, nome=None, flip=False, dress="#6a6a7a", dress2="#8a8a9a", mouth="sad", eyes="open", brows="normal", arm_mode=("down", "down")):
    if nome and VAR.get("fala") == nome:
        b = VAR.get("boca", 0.0)
        mouth = "shout" if b > 0.35 else ("smile" if b > 0.12 else "sad")
    if eyes == "open" and piscando(t, LOOP, 1.1):
        eyes = "closed"
    v = VAR["v"]
    x = x + [0, -120, 110, -60, 80][v % 5] * s
    c, _ = dalila(mouth=mouth, eyes=eyes, brows=brows, arm_mode=arm_mode, dress=dress, dress2=dress2)
    return g(respirar(c, t, 0.012, LOOP), x, y, s, flip)


def fogo(t, x, y, s=1.0, n=7):
    out = ""
    for i in range(n):
        fx = (i - n / 2) * 46
        h = 260 + 90 * onda(t, LOOP / 3, i * 0.13) + (n / 2 - abs(i - n / 2)) * 60
        w = 70 + 10 * onda(t, LOOP / 2, i * 0.2)
        out += (f'<path d="M{fx - w / 2:.0f} 0 Q{fx - w:.0f} {-h * 0.5:.0f} {fx + 12 * onda(t, LOOP / 3, i * .3):.0f} {-h:.0f} '
                f'Q{fx + w:.0f} {-h * 0.5:.0f} {fx + w / 2:.0f} 0 Z" fill="#ff7a1a" stroke="{OL}" stroke-width="4"/>'
                f'<path d="M{fx - w / 4:.0f} 0 Q{fx - w / 2:.0f} {-h * 0.35:.0f} {fx:.0f} {-h * 0.62:.0f} Q{fx + w / 2:.0f} {-h * 0.35:.0f} {fx + w / 4:.0f} 0 Z" fill="#ffd84a"/>')
    return g(out, x, y, s)


def montanha(cor="#7a6a4a", y=620):
    return (f'<path d="M-50 1080 L-50 {y + 120} L400 {y - 160} L760 {y + 40} L1100 {y - 260} L1500 {y + 20} L1980 {y - 120} L1980 1080 Z" fill="{cor}" stroke="#2a1a12" stroke-width="6"/>')


def altar(x, y, s=1.0, agua=0.0, molhado=False, boi=True):
    c = ""
    for row in range(3):
        for i in range(4 - row):
            px = -150 + i * 100 + row * 50
            py = -row * 70
            cor = "#7a7a80" if molhado else "#9a958c"
            c += f'<rect x="{px - 48}" y="{py - 66}" width="96" height="66" rx="14" fill="{cor}" stroke="{OL}" stroke-width="5"/>'
    c += f'<path d="M-200 -210 L200 -210 L180 -240 L-180 -240 Z" fill="#8a5a30" stroke="{OL}" stroke-width="5"/>'
    if boi:
        c += f'<ellipse cx="0" cy="-270" rx="150" ry="44" fill="#b07a4a" stroke="{OL}" stroke-width="5"/>'
    if agua > 0:
        c += f'<path d="M-280 10 Q0 {40 + 20 * agua:.0f} 280 10 L300 40 Q0 {80 + 20 * agua:.0f} -300 40 Z" fill="#4f9fd0" stroke="{OL}" stroke-width="4" opacity="{0.4 + 0.6 * agua:.2f}"/>'
    return g(c, x, y, s)


def multidao(t, y=1000, s=0.42, n=9, braços=("down", "down"), olhos="open", boca="sad", cor0=0, base_extra=None, nome=None):
    out = ""
    for i in range(n):
        x = 80 + i * (1760 / max(1, n - 1))
        b = dict(hair="short" if i % 3 else "curly", hair_col="#2a1a10", beard="yes" if i % 2 else "none", beard_col="#2a1a10",
                 tunic=POVO[(i + cor0) % len(POVO)])
        if base_extra:
            b.update(base_extra)
        out += pessoa(t, x, y + (i % 2) * 24, s, base=b, eyes=olhos, mouth=boca, arms=braços, piscar=i * 0.37 % LOOP,
                      flip=i % 2 == 1, nome=nome, fixo=True)
    return out


def anjo(t, x, y, s=0.85):
    asa = 8 * onda(t, LOOP / 2)
    w = (f'<g transform="rotate({-asa:.1f} -60 -620)"><path d="M-60 -620 Q-420 -820 -360 -360 Q-200 -480 -60 -560 Z" fill="#f4f0ff" stroke="{OL}" stroke-width="6"/></g>'
         f'<g transform="rotate({asa:.1f} 60 -620)"><path d="M60 -620 Q420 -820 360 -360 Q200 -480 60 -560 Z" fill="#f4f0ff" stroke="{OL}" stroke-width="6"/></g>')
    c, _ = person(hair="curly", hair_col="#e8c27a", beard="none", tunic="#f8f4e8", robe="#e8e0ff", eyes="open", mouth="smile",
                  arms=("forward", "down"), belt="#e8c27a")
    if VAR.get("fala") == "angel":
        c, _ = person(hair="curly", hair_col="#e8c27a", beard="none", tunic="#f8f4e8", robe="#e8e0ff", eyes="open",
                      mouth="shout" if VAR.get("boca", 0) > 0.3 else "smile", arms=("forward", "down"), belt="#e8c27a")
    glow = f'<circle cx="0" cy="-560" r="420" fill="#fff8d0" opacity="{0.22 + 0.06 * onda(t, LOOP):.2f}"/>'
    return g(glow + w + respirar(c, t, 0.01), x, y + 10 * onda(t, LOOP), s)


def enebro(x, y, s=1.0):
    c = f'<path d="M-20 0 L-10 -240 M-10 -150 L-120 -260 M-10 -190 L110 -300" stroke="#6b4226" stroke-width="22" stroke-linecap="round"/>'
    for (cx, cy, r) in [(-120, -280, 80), (0, -300, 100), (120, -320, 80), (-50, -380, 70), (60, -400, 70)]:
        c += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#6a8a3a" stroke="{OL}" stroke-width="5"/>'
    return g(c, x, y, s)


def jarro(x, y, s=1.0, cor="#b0603a"):
    return g(f'<path d="M-40 0 Q-70 -60 -40 -110 L-30 -140 L30 -140 L40 -110 Q70 -60 40 0 Z" fill="{cor}" stroke="{OL}" stroke-width="5"/>'
             f'<rect x="-36" y="-156" width="72" height="18" rx="6" fill="{cor}" stroke="{OL}" stroke-width="5"/>', x, y, s)


def pao(x, y, s=1.0):
    return g(f'<ellipse cx="0" cy="0" rx="60" ry="28" fill="#d9a050" stroke="{OL}" stroke-width="5"/>'
             f'<path d="M-30 -8 q10 -10 20 0 M0 -10 q10 -10 20 0" stroke="#a0702a" stroke-width="4" fill="none"/>', x, y, s)


def nuvem(x, y, s=1.0, cor="#e8eef8"):
    return g(f'<circle cx="-40" cy="0" r="40" fill="{cor}"/><circle cx="20" cy="-14" r="50" fill="{cor}"/><circle cx="70" cy="4" r="36" fill="{cor}"/>', x, y, s)


def ceu_sol(top="#ffb860", bot="#ffe8b0"):
    return ceu(top, bot) + '<circle cx="1560" cy="200" r="90" fill="#fff4c0"/>'


def chao(cor="#c9a070", y=860):
    return f'<rect x="0" y="{y}" width="1920" height="{1080 - y}" fill="{cor}"/><rect x="0" y="{y}" width="1920" height="10" fill="#2a1a12"/>'




def arroyo(t, seco=False):
    if seco:
        return ('<path d="M0 820 Q480 760 960 820 T1920 800 L1920 900 Q1440 860 960 900 T0 890 Z" fill="#a08060" stroke="#2a1a12" stroke-width="5"/>'
                + "".join(f'<path d="M{x} 850 l30 20 l-20 25 l35 15" fill="none" stroke="#5a3a20" stroke-width="5"/>' for x in range(80, 1900, 220)))
    s = '<path d="M0 820 Q480 760 960 820 T1920 800 L1920 900 Q1440 860 960 900 T0 890 Z" fill="#4f9fd0" stroke="#2a1a12" stroke-width="5"/>'
    for i in range(10):
        x = ((i * 210) + 600 * t / LOOP) % 2000 - 40
        s += f'<path d="M{x:.0f} 850 q30 -10 60 0" fill="none" stroke="#e8f6ff" stroke-width="6" opacity="0.8"/>'
    return s
