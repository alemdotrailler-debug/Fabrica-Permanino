"""Cenas animadas do Elías (template gibi). Cada cena é uma função de t (0..LOOP) que devolve um SVG 1920x1080."""
from fabrica.kit import *

ELIAS = dict(hair="long", hair_col="#4a2a14", beard="yes", beard_col="#4a2a14", tunic="#8a6a3a", robe="#6a4a2a", belt="#4a2a10")
ACAB = dict(hair="short", hair_col="#1a1410", beard="yes", beard_col="#1a1410", tunic="#c9a14a", robe="#5a1a6a", crown=True, belt="#e8c27a")
PROFETA_BAAL = dict(hair="bald", hair_col="#2a1a10", beard="yes", beard_col="#2a1a10", tunic="#a02a2a", robe="#5a1010")
CRIADO = dict(hair="short", hair_col="#3a2414", beard="none", tunic="#6a8a5a")
ELISEU = dict(hair="bald", hair_col="#3a2414", beard="yes", beard_col="#3a2414", tunic="#5a6a8a")
POVO = ["#2e5aa8", "#a0522d", "#7a3a5a", "#5a7a3a", "#8a6a3a", "#3a6a8a", "#9a4a2a"]


# ---------------- elementos novos ----------------
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


def cuervo(t, x, y, s=1.0, fase=0.0, pao=False):
    a = 35 * onda(t, LOOP / 6, fase)
    c = (f'<ellipse cx="0" cy="0" rx="70" ry="34" fill="#1a1a22" stroke="{OL}" stroke-width="4"/>'
         f'<circle cx="62" cy="-18" r="26" fill="#1a1a22" stroke="{OL}" stroke-width="4"/><circle cx="70" cy="-24" r="5" fill="#fff"/>'
         f'<path d="M84 -16 L118 -8 L84 -2 Z" fill="#e8a020" stroke="{OL}" stroke-width="3"/>'
         f'<path d="M-60 0 L-110 -18 L-104 16 Z" fill="#1a1a22" stroke="{OL}" stroke-width="4"/>'
         f'<g transform="rotate({-a:.1f} -10 -10)"><path d="M-10 -10 Q-40 -110 -120 -90 Q-60 -40 -10 -10 Z" fill="#2a2a34" stroke="{OL}" stroke-width="4"/></g>')
    if pao:
        c += f'<ellipse cx="128" cy="-6" rx="26" ry="16" fill="#d9a050" stroke="{OL}" stroke-width="4"/>'
    return g(c, x, y, s)


def arroyo(t, seco=False):
    if seco:
        return ('<path d="M0 820 Q480 760 960 820 T1920 800 L1920 900 Q1440 860 960 900 T0 890 Z" fill="#a08060" stroke="#2a1a12" stroke-width="5"/>'
                + "".join(f'<path d="M{x} 850 l30 20 l-20 25 l35 15" fill="none" stroke="#5a3a20" stroke-width="5"/>' for x in range(80, 1900, 220)))
    s = '<path d="M0 820 Q480 760 960 820 T1920 800 L1920 900 Q1440 860 960 900 T0 890 Z" fill="#4f9fd0" stroke="#2a1a12" stroke-width="5"/>'
    for i in range(10):
        x = ((i * 210) + 600 * t / LOOP) % 2000 - 40
        s += f'<path d="M{x:.0f} 850 q30 -10 60 0" fill="none" stroke="#e8f6ff" stroke-width="6" opacity="0.8"/>'
    return s


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


def carro_fogo(t, x, y, s=1.0):
    c = fogo(t, -40, -40, 0.6, 9)
    c += f'<path d="M-260 -60 L180 -60 L220 -220 L-200 -220 Z" fill="#ff9a2a" stroke="{OL}" stroke-width="7"/>'
    c += f'<circle cx="-140" cy="-40" r="70" fill="#ffd84a" stroke="{OL}" stroke-width="7"/><circle cx="110" cy="-40" r="70" fill="#ffd84a" stroke="{OL}" stroke-width="7"/>'
    for k in range(2):
        cx = 420 + k * 230
        perna = 25 * onda(t, LOOP / 4, k * 0.25)
        c += (f'<g transform="translate({cx},-120)"><ellipse cx="0" cy="0" rx="150" ry="70" fill="#ff7a1a" stroke="{OL}" stroke-width="6"/>'
              f'<path d="M100 -30 L190 -150 L240 -120 L160 0 Z" fill="#ff7a1a" stroke="{OL}" stroke-width="6"/>'
              f'<path d="M-100 40 l{perna:.0f} 120 M100 40 l{-perna:.0f} 120" stroke="#ff7a1a" stroke-width="30" stroke-linecap="round"/>'
              f'{fogo(t, 0, -40, 0.35, 5)}</g>')
    return g(c, x, y + 14 * onda(t, LOOP / 2), s)


def torbellino(t, x, y, s=1.0):
    c = ""
    for i in range(8):
        r = 60 + i * 40
        yy = -i * 90
        rot = 360 * t / LOOP * (2 if i % 2 else -2)
        c += f'<ellipse cx="0" cy="{yy}" rx="{r}" ry="{r * 0.25:.0f}" fill="none" stroke="#f0f0ff" stroke-width="10" opacity="0.7" transform="rotate({rot * 0.02:.1f} 0 {yy})"/>'
    return g(c, x, y, s)


def nuvem(x, y, s=1.0, cor="#e8eef8"):
    return g(f'<circle cx="-40" cy="0" r="40" fill="{cor}"/><circle cx="20" cy="-14" r="50" fill="{cor}"/><circle cx="70" cy="4" r="36" fill="{cor}"/>', x, y, s)


def ceu_sol(top="#ffb860", bot="#ffe8b0"):
    return ceu(top, bot) + '<circle cx="1560" cy="200" r="90" fill="#fff4c0"/>'


def chao(cor="#c9a070", y=860):
    return f'<rect x="0" y="{y}" width="1920" height="{1080 - y}" fill="{cor}"/><rect x="0" y="{y}" width="1920" height="10" fill="#2a1a12"/>'


# ---------------- cenas ----------------
def e0(t):
    s = ceu("#2a2a5a", "#c06a4a") + montanha("#6a5a3a", 700) + altar(V(1180, 1000, 1300), 960, V(1.1, 1.25, 1.0), agua=1, molhado=True)
    s += pessoa(t, V(520, 640, 420), 1000, 0.85, base=ELIAS, eyes="up", mouth="sad", brows="normal", arms=("up", "up"), nome="elias")
    return frame_(s + particulas(t, 15))


def e0b(t):
    s = ceu("#3a2a6a", "#ff8a3a") + montanha("#5a4a3a", 760) + luz_ceu(t, V(1300, 900, 1500), 0.2) + fogo(t, V(1300, 1100), 980, V(1.1, 1.4))
    return frame_(s + particulas(t, 30, "#ffd27a"))


def e1a(t):
    s = ceu_sol("#e8a060", "#fbe0a8") + montanha("#c9a46a", 760) + chao("#d8b070", 880)
    s += pessoa(t, V(960, 760, 1160), 1010, 0.9, base=ELIAS, eyes="side", mouth="sad", brows="angry", arms=("down", "down"), balanco=1.5)
    return frame_(s)


def e1b(t):
    s = bg_palace() + f'<rect x="760" y="520" width="400" height="420" rx="20" fill="#c9a14a" stroke="{OL}" stroke-width="6"/>'
    s += pessoa(t, 820, 1000, 0.82, base=ACAB, eyes="side", mouth="smirk", brows="sly", arms=("down", "flex"))
    s += mulher(t, 1220, 1000, 0.82, dress="#5a1a6a", dress2="#7a2a8a", mouth="smirk", brows="sly", arm_mode=("hip", "down"))
    s += g(f'<rect x="-60" y="-300" width="120" height="300" fill="#c9a14a" stroke="{OL}" stroke-width="6"/><circle cx="0" cy="-360" r="70" fill="#c9a14a" stroke="{OL}" stroke-width="6"/>'
           f'<path d="M-60 -400 L-110 -470 M60 -400 L110 -470" stroke="{OL}" stroke-width="16"/>', 360, 1000, 0.9)
    return frame_(s)


def e1c(t):
    s = bg_palace() + pessoa(t, 1350, 1000, 0.82, base=ACAB, eyes="open", mouth="sad", brows="sad", arms=("down", "down"), flip=True)
    s += pessoa(t, 560, 1000, 0.88, base=ELIAS, eyes="open", mouth="sad", brows="angry", arms=("point", "down"), nome="elias")
    return frame_(s)


def e2a(t):
    s = ceu_sol("#7ec8f0", "#d8f0ff") + montanha("#8a7a5a", 640) + chao("#b8a070", 800) + arroyo(t)
    s += pessoa(t, V(600, 900, 1300), 790, 0.62, base=ELIAS, eyes="closed", mouth="smile", arms=("pray", "down"))
    return frame_(s)


def e2b(t):
    s = ceu_sol("#ffb860", "#ffe8b0") + montanha("#8a7a5a", 640) + chao("#b8a070", 800) + arroyo(t)
    s += pessoa(t, 760, 900, 0.75, base=ELIAS, eyes="up", mouth="smile", arms=("up", "down"))
    s += cuervo(t, V(1200, 1000, 1350) + 40 * onda(t, LOOP), 300, 1.1, 0, True) + cuervo(t, V(1500, 1400, 1600), 420 + 30 * onda(t, LOOP, .3), 0.9, .4, True)
    return frame_(s)


def e2c(t):
    s = ceu_sol("#ff9a3a", "#ffe08a") + sol_quente(t, V(1550, 1400), 200) + montanha("#9a7a4a", 640) + chao("#c8a070", 800) + arroyo(t, seco=True)
    s += pessoa(t, V(860, 700, 1100), 900, 0.7, base=ELIAS, eyes="side", mouth="sad", brows="sad", arms=("face", "down"))
    return frame_(s + calor(t, 960, 560))


def e3a(t):
    s = bg_city() + mulher(t, V(1250, 1100, 1350), 1000, 0.8, dress="#5a5a6a", dress2="#7a7a8a", eyes="side", arm_mode=("hold", "down"))
    s += f'<path d="M1300 640 l140 -40 M1300 660 l150 -10" stroke="#6b4226" stroke-width="16" stroke-linecap="round"/>'
    s += pessoa(t, V(560, 460, 680), 1000, 0.82, base=ELIAS, eyes="open", mouth="smile", arms=("forward", "down"), nome="elias")
    return frame_(s)


def e3b(t):
    s = bg_house() + jarro(960, 990, 0.9, "#c08a4a")
    s += mulher(t, 1320, 1000, 0.85, nome="viuda", dress="#5a5a6a", dress2="#7a7a8a", mouth="sad", brows="sad", arm_mode=("hold", "down"))
    s += pessoa(t, 560, 1000, 0.85, base=ELIAS, eyes="open", mouth="smile", arms=("forward", "down"), nome="elias")
    return frame_(s)


def e3c(t):
    s = bg_house() + jarro(V(760, 900), 980, 1.2, "#c08a4a")
    f = (t / LOOP)
    s += f'<path d="M{V(760, 900)} 780 q{20 * onda(t, LOOP):.0f} -60 0 -120" fill="none" stroke="#fff" stroke-width="10" opacity="0.6"/>'
    s += f'<ellipse cx="1260" cy="900" rx="120" ry="34" fill="#d9a050" stroke="{OL}" stroke-width="6"/>'
    s += mulher(t, 1500, 1000, 0.7, dress="#5a5a6a", dress2="#7a7a8a", mouth="smile", arm_mode=("hold", "down"))
    s += pessoa(t, 380, 1000, 0.6, hair="curly", hair_col="#3a2414", beard="none", tunic="#c9a14a", eyes="open", mouth="smile", arms=("up", "down"))
    return frame_(s + particulas(t, 15, "#ffe8a0"))


def e3d(t):
    s = bg_house() + luz_ceu(t, V(960, 700), 0.15)
    s += pessoa(t, V(820, 700), 1000, 0.85, base=ELIAS, eyes="up", mouth="sad", brows="sad", arms=("pray", "pray"))
    s += mulher(t, 1400, 1000, 0.8, nome="viuda", dress="#5a5a6a", dress2="#7a7a8a", mouth="smile", eyes="open", arm_mode=("lift", "down"))
    s += pessoa(t, 1100, 1000, 0.5, hair="curly", hair_col="#3a2414", beard="none", tunic="#c9a14a", eyes="open", mouth="smile", arms=("up", "down"))
    return frame_(s + particulas(t, 20))


def e4a(t):
    s = ceu_sol("#ff9a3a", "#ffe08a") + sol_quente(t, V(1500, 1650), 200) + chao("#c8a070", 760)
    s += "".join(f'<path d="M{x} 900 l40 30 l-30 30" stroke="#6a4a2a" stroke-width="6" fill="none"/>' for x in range(100, 1900, 260))
    s += pessoa(t, V(960, 760, 1160), 1000, 0.82, base=ELIAS, eyes="up", mouth="sad", arms=("down", "down"))
    return frame_(s + calor(t, 960, 520))


def e4b(t):
    s = bg_palace()
    s += pessoa(t, 1340, 1000, 0.85, base=ACAB, eyes="open", mouth="sad", brows="angry", arms=("point", "down"), flip=True, nome="acab")
    s += pessoa(t, 580, 1000, 0.88, base=ELIAS, eyes="open", mouth="sad", brows="angry", arms=("down", "point"), nome="elias")
    return frame_(s)


def e4c(t):
    s = ceu_sol("#7ec8f0", "#d8f0ff") + montanha("#7a8a4a", 560) + chao("#a0a060", 860)
    s += multidao(t, 1040, 0.36, 11, olhos="side")
    return frame_(s)


def e4d(t):
    s = ceu_sol("#7ec8f0", "#d8f0ff") + montanha("#7a8a4a", 560) + chao("#a0a060", 860)
    s += multidao(t, 1060, 0.34, 10, olhos="open", cor0=2)
    s += pessoa(t, 960, 900, 0.7, base=ELIAS, eyes="open", mouth="sad", brows="angry", arms=("up", "point"), nome="elias", fixo=True)
    return frame_(s)


def e5a(t):
    s = ceu_sol("#8ac8f0", "#e8f6ff") + montanha("#7a8a4a", 600) + chao("#a8a060", 860)
    s += altar(V(560, 480), 940, 0.8) + altar(V(1360, 1440), 940, 0.8)
    s += boi(V(960, 900), 1000, 0.5)
    return frame_(s)


def e5b(t):
    s = ceu_sol("#ffb070", "#ffe8b8") + montanha("#8a7a4a", 620) + chao("#c8a870", 860) + altar(960, 960, 0.9)
    pulo = abs(60 * onda(t, LOOP / 3))
    for i, x in enumerate((300, 560, 1360, 1620)):
        s += pessoa(t, x, 1000 - (pulo if i % 2 else 60 - pulo), 0.6, base=PROFETA_BAAL, eyes="closed", mouth="shout", brows="angry",
                    arms=("up", "up"), flip=i > 1, nome="profetas", piscar=i * .4)
    return frame_(s)


def e5c(t):
    s = ceu_sol("#ffb070", "#ffe8b8") + montanha("#8a7a4a", 620) + chao("#c8a870", 860)
    for i, x in enumerate((1240, 1460, 1680)):
        s += pessoa(t, x, 1000, 0.5, base=PROFETA_BAAL, eyes="closed", mouth="shout", arms=("up", "up"), flip=True, piscar=i * .5)
    s += pessoa(t, 560, 1000, 0.85, base=ELIAS, eyes="side", mouth="smirk", brows="sly", arms=("flex", "point"), nome="elias")
    return frame_(s)


def e5d(t):
    s = ceu("#ff8a4a", "#ffd0a0") + montanha("#7a5a3a", 640) + chao("#b89060", 860) + altar(960, 960, 0.9)
    for i, x in enumerate((360, 620, 1300, 1560)):
        s += pessoa(t, x, 1000, 0.55, base=PROFETA_BAAL, eyes="closed", mouth="sad", brows="sad", arms=("face", "face"), flip=i > 1, piscar=i * .4)
    return frame_(s)


def e6a(t):
    s = ceu("#ff8a4a", "#ffd0a0") + montanha("#7a5a3a", 640) + chao("#b89060", 860) + altar(1150, 980, 1.0, boi=False)
    s += pessoa(t, 560, 1000, 0.82, base=ELIAS, eyes="side", mouth="smile", arms=("hold", "forward"))
    s += f'<rect x="{620 + 10 * onda(t, LOOP)}" y="640" width="96" height="66" rx="14" fill="#9a958c" stroke="{OL}" stroke-width="5"/>'
    return frame_(s)


def e6b(t):
    s = ceu("#ff8a4a", "#ffd0a0") + montanha("#7a5a3a", 640) + chao("#b89060", 860) + altar(1000, 960, 1.0, agua=0.6 + 0.4 * (t / LOOP), molhado=True)
    f = t / LOOP
    s += jarro(1180, 520, 0.9, "#7a8a9a").replace('<g transform="', '<g transform="rotate(-120 1180 520) ', 1)
    s += f'<path d="M1100 460 Q{1060 - 20 * onda(t, LOOP / 2):.0f} 560 1040 700" fill="none" stroke="#4f9fd0" stroke-width="26" stroke-linecap="round" opacity="0.85"/>'
    s += pessoa(t, 1400, 1000, 0.8, base=CRIADO, eyes="open", mouth="shout", brows="sad", arms=("up", "down"), flip=True)
    return frame_(s)


def e6c(t):
    s = ceu("#5a3a6a", "#ff9a5a") + luz_ceu(t, 960, 0.1) + montanha("#5a4a3a", 660) + chao("#9a7a50", 860) + altar(1250, 980, 0.9, agua=1, molhado=True)
    s += pessoa(t, 620, 1000, 0.86, base=ELIAS, eyes="up", mouth="sad", brows="normal", arms=("up", "up"), nome="elias")
    return frame_(s + particulas(t, 15))


def e6d(t):
    s = ceu("#3a1a2a", "#ff7a2a") + luz_ceu(t, V(960, 1100), 0.35) + montanha("#5a3a2a", 660) + chao("#7a5a3a", 860)
    s += altar(960, 980, 1.0, agua=0.3, molhado=True) + fogo(t, 960, 760, V(1.6, 1.9, 1.4), 9)
    s += f'<path d="M940 -10 L900 200 L980 210 L920 520" fill="none" stroke="#fff6c0" stroke-width="40" opacity="0.8"/>'
    return frame_(s + particulas(t, 40, "#ffb040"))


def e6e(t):
    s = ceu("#3a1a2a", "#ff9a3a") + montanha("#5a3a2a", 660) + chao("#9a7a50", 860) + fogo(t, 1700, 900, 0.7, 6)
    for i, x in enumerate(range(160, 1500, 190)):
        prostrado, _ = person(hair="short", hair_col="#2a1a10", beard="yes", beard_col="#2a1a10", tunic=POVO[i % len(POVO)],
                              eyes="closed", mouth="shout" if VAR.get("fala") == "pueblo" and VAR.get("boca", 0) > .3 else "sad", arms=("up", "up"))
        s += f'<g transform="translate({x},{960 + (i % 2) * 30}) rotate(-75) scale(0.36)">{prostrado}</g>'
    return frame_(s)


def e6f(t):
    s = ceu("#5a7aa0", "#c8d8e8") + mar_calmo(t, 760) + nuvem(V(1500, 1300, 1600), 700, 0.8 + 0.1 * onda(t, LOOP))
    s += chao("#7a7a4a", 900)
    s += pessoa(t, 560, 1000, 0.8, base=CRIADO, eyes="side", mouth="smile", arms=("point", "down"), nome="criado")
    return frame_(s)


def e6g(t):
    s = ceu("#2a3040", "#4a5060") + nuvens_tempestade(t) + chao("#5a6a3a", 840) + chuva(t, 110) + raio(t, V(1500, 400), 1.0)
    passo = 20 * onda(t, LOOP / 4)
    s += pessoa(t, V(1300, 1100), 1000 + abs(passo) * 0.4, 0.62, base=ELIAS, eyes="closed", mouth="smile", arms=("flex", "forward"), balanco=6)
    s += g(f'<path d="M-260 -60 L180 -60 L220 -200 L-200 -200 Z" fill="#8a5a30" stroke="{OL}" stroke-width="7"/><circle cx="-140" cy="-40" r="60" fill="#5a3a20" stroke="{OL}" stroke-width="7"/><circle cx="110" cy="-40" r="60" fill="#5a3a20" stroke="{OL}" stroke-width="7"/>', 420, 990, 0.8)
    return frame_(s)


def e7a(t):
    s = bg_palace(night=True)
    s += mulher(t, 960, 1000, 0.9, nome="jezabel", dress="#5a1a6a", dress2="#7a2a8a", mouth="smirk", brows="angry", eyes="side", arm_mode=("hip", "lift"))
    return frame_(s)


def e7b(t):
    s = ceu_sol("#ff9a3a", "#ffe08a") + sol_quente(t, 1600, 180) + chao("#d8b070", 800) + enebro(1100, 900, 1.2)
    s += pessoa(t, 980, 990, 0.7, base=ELIAS, eyes="closed", mouth="sad", brows="sad", arms=("face", "face"), nome="elias")
    return frame_(s + calor(t, 600, 600))


def e7c(t):
    s = ceu("#2a2a5a", "#7a6aa0") + '<circle cx="1600" cy="180" r="60" fill="#f4f0d0"/>' + chao("#a08a60", 820) + enebro(560, 900, 1.1)
    dorme, _ = person(**{**ELIAS, "eyes": "closed", "mouth": "smile", "arms": ("down", "down")})
    s += f'<g transform="translate(900,900) rotate(-90) scale(0.6)">{respirar(dorme, t, 0.02)}</g>'
    s += pao(1180, 930, 0.9) + jarro(1300, 960, 0.6, "#7a8a9a")
    s += anjo(t, V(1500, 1600), 1000, 0.75)
    return frame_(s + particulas(t, 25))


def e7d(t):
    s = ceu_sol("#e8a060", "#fbe0a8") + montanha("#8a6a4a", 520) + chao("#c8a070", 880)
    passo = 6 * onda(t, LOOP / 3)
    s += pessoa(t, V(700, 960, 1200), 1000 + passo, 0.55, base=ELIAS, eyes="side", mouth="sad", arms=("down", "down"), balanco=3)
    return frame_(s)


def e7e(t):
    s = bg_cave() + vento(t, 300, 7) + vento(t, 600, 5)
    for i in range(6):
        f = ((t / LOOP) + i / 6) % 1
        s += f'<rect x="{300 + i * 230}" y="{120 + 700 * f:.0f}" width="60" height="50" rx="10" fill="#7a6a5a" stroke="{OL}" stroke-width="4" transform="rotate({360 * f:.0f} {330 + i * 230} {145 + 700 * f:.0f})"/>'
    s += pessoa(t, 960, 1000, 0.75, base=ELIAS, eyes="open", mouth="shout", brows="sad", arms=("face", "face"), balanco=5)
    return frame_(f'<g transform="translate({8 * onda(t, LOOP / 8):.1f},{5 * onda(t, LOOP / 6):.1f})">{s}</g>')


def e7f(t):
    s = bg_cave() + f'<ellipse cx="960" cy="560" rx="{520 + 30 * onda(t, LOOP)}" ry="{420 + 20 * onda(t, LOOP)}" fill="#fff6d8" opacity="0.22"/>'
    s += pessoa(t, 960, 1000, 0.8, base=ELIAS, eyes="closed", mouth="smile", brows="normal", arms=("face", "down"), robe="#4a3a2a")
    for i in range(4):
        f = ((t / LOOP) + i / 4) % 1
        s += f'<path d="M{1180 + 60 * f:.0f} {420 - 40 * i} q40 -20 80 0" fill="none" stroke="#fff" stroke-width="6" opacity="{(1 - f) * 0.8:.2f}"/>'
    return frame_(s + particulas(t, 20, "#fff8d0"))


def e8a(t):
    s = ceu("#3a2a6a", "#ff9a5a") + montanha("#5a4a3a", 760) + chao("#9a7a50", 880)
    s += carro_fogo(t, V(1250, 1150), 620, 0.75) + torbellino(t, V(600, 520), 900, 0.9)
    s += pessoa(t, 600, 900 - 60 * (t / LOOP), 0.5, base=ELIAS, eyes="up", mouth="smile", arms=("up", "up"), fixo=True)
    s += pessoa(t, 300, 1000, 0.55, base=ELISEU, eyes="up", mouth="shout", brows="sad", arms=("up", "down"), fixo=True)
    return frame_(s + particulas(t, 35, "#ffb040"))


def e8b(t):
    s = ceu("#2a1a4a", "#ff8a4a") + luz_ceu(t, 960, 0.2) + carro_fogo(t, V(960, 900) + 80 * onda(t, LOOP), 380 - 30 * (t / LOOP), 0.55)
    s += montanha("#3a2a2a", 860)
    return frame_(s + particulas(t, 40, "#ffd27a"))


def e8c(t):
    s = bg_heaven() + luz_ceu(t, 960, 0.12)
    rolo = (f'<rect x="-420" y="-260" width="840" height="520" rx="10" fill="#f0e2c0" stroke="{OL}" stroke-width="8"/>'
            f'<rect x="-460" y="-290" width="60" height="580" rx="30" fill="#8a5a30" stroke="{OL}" stroke-width="6"/>'
            f'<rect x="400" y="-290" width="60" height="580" rx="30" fill="#8a5a30" stroke="{OL}" stroke-width="6"/>'
            f'<text x="0" y="-40" font-family="Lora" font-weight="700" font-size="80" fill="#5a3a1a" text-anchor="middle">1 Reyes 19:12</text>'
            f'<text x="0" y="70" font-family="Lora" font-style="italic" font-size="60" fill="#5a3a1a" text-anchor="middle">un silbo apacible</text>')
    s += g(rolo, V(960, 900, 1020), 520 + 10 * onda(t, LOOP), V(1, 1.12, 0.92))
    return frame_(s + particulas(t, 30))


def e8d(t):
    s = ceu_sol("#ffb070", "#ffe8b8") + chao("#d8b070", 820) + enebro(V(960, 800, 1100), 900, 1.3)
    s += pao(V(1180, 1000), 930, 1.0) + jarro(V(1320, 1150), 960, 0.7, "#7a8a9a")
    return frame_(s + particulas(t, 25))


def e9(t):
    book = (f'<rect x="-250" y="-360" width="500" height="720" rx="14" fill="#5a1f1f" stroke="{OL}" stroke-width="8"/>'
            f'<rect x="-220" y="-330" width="440" height="660" rx="8" fill="none" stroke="#e0b23a" stroke-width="6"/>'
            f'<text x="0" y="-180" font-family="Lora" font-weight="700" font-size="72" fill="#f2d27a" text-anchor="middle">Héroes del</text>'
            f'<text x="0" y="-95" font-family="Lora" font-weight="700" font-size="72" fill="#f2d27a" text-anchor="middle">Pergamino</text>'
            f'<text x="0" y="90" font-family="Lora" font-weight="700" font-size="170" fill="#fff3cf" text-anchor="middle">30</text>'
            f'<text x="0" y="160" font-family="Lora" font-size="50" fill="#f2d27a" text-anchor="middle">días</text>')
    s = bg_heaven() + f'<g transform="translate({V(620, 560, 680)},{500 + 12 * onda(t, LOOP):.0f}) rotate({V(-5, 4, -9) + 1.5 * onda(t, LOOP):.2f}) scale(0.95)">{book}</g>'
    s += f'<text x="1350" y="420" font-family="Lora" font-weight="700" font-size="80" fill="#fff3cf" stroke="{OL}" stroke-width="3" text-anchor="middle">30 mañanas</text>'
    s += f'<text x="1350" y="510" font-family="Lora" font-weight="700" font-size="80" fill="#fff3cf" stroke="{OL}" stroke-width="3" text-anchor="middle">con los héroes</text>'
    pul = 1 + 0.04 * onda(t, LOOP / 2)
    s += f'<g transform="translate(1350,640) scale({pul:.3f})"><rect x="-300" y="-50" width="600" height="100" rx="50" fill="#e8435a" stroke="{OL}" stroke-width="6"/><text x="0" y="20" font-family="Inter Display" font-weight="800" font-size="48" fill="#fff" text-anchor="middle">LINK EN LA DESCRIPCIÓN</text></g>'
    return frame_(s + particulas(t, 25))


def scenes():
    return {k: v for k, v in globals().items() if callable(v) and k.startswith("e") and k[1:2].isdigit()}


FOCO = {
    "e0": (600, 330), "e0b": (1200, 600), "e1a": (960, 290), "e1b": (1000, 320), "e1c": (900, 330), "e2a": (700, 500),
    "e2b": (900, 330), "e2c": (860, 400), "e3a": (900, 330), "e3b": (900, 320), "e3c": (1000, 650), "e3d": (1000, 350),
    "e4a": (960, 320), "e4b": (960, 320), "e4c": (960, 800), "e4d": (960, 380), "e5a": (960, 700), "e5b": (960, 450),
    "e5c": (600, 330), "e5d": (960, 600), "e6a": (900, 500), "e6b": (1100, 600), "e6c": (800, 330), "e6d": (960, 600),
    "e6e": (800, 900), "e6f": (900, 500), "e6g": (1100, 600), "e7a": (960, 300), "e7b": (980, 500), "e7c": (1200, 600),
    "e7d": (960, 600), "e7e": (960, 400), "e7f": (960, 360), "e8a": (900, 500), "e8b": (960, 400), "e8c": (960, 520),
    "e8d": (1050, 700), "e9": (900, 520),
}

THUMBS = "AB"


def thumb(variant="A"):
    s = ('<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">'
         '<defs><radialGradient id="L" cx="0.6" cy="0.4" r="0.7"><stop offset="0" stop-color="#ffd27a"/><stop offset="0.5" stop-color="#e0502a"/><stop offset="1" stop-color="#2a0806"/></radialGradient>'
         '<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff7c9"/><stop offset="0.5" stop-color="#ffd84a"/><stop offset="1" stop-color="#ff9a12"/></linearGradient>'
         '<pattern id="ht" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="1.8" fill="#000"/></pattern></defs>'
         '<rect width="1280" height="720" fill="url(#L)"/>')
    VAR["v"] = 0
    if variant == "A":
        s += g(altar(0, 0, 1.0, agua=0.5, molhado=True) + fogo(1.0, 0, -220, 1.7, 9), 960, 700, 0.7)
        c, _ = person(**{**ELIAS, "eyes": "up", "mouth": "shout", "brows": "normal", "arms": ("up", "up")})
        s += g(c, 700, 1100, 0.95)
        t1, t2, etq = "TODO", "O NADA", "¿Y SI NO CAE?…"
    else:
        s += g(fogo(1.0, 0, 0, 1.4, 9), 1000, 760, 1.0)
        for i, x in enumerate((760, 900, 1040, 1180)):
            c, _ = person(**{**PROFETA_BAAL, "eyes": "open", "mouth": "shout", "brows": "sad", "arms": ("face", "face")})
            s += g(c, x, 760, 0.38)
        t1, t2, etq = "NADIE", "RESPONDIÓ", "DESDE LA MAÑANA…"
    s += '<rect width="1280" height="720" fill="url(#ht)" opacity="0.10"/>'
    tg = '<g transform="rotate(-4 300 330)">'
    for y, tx in ((260, t1), (400, t2)):
        if not tx:
            continue
        for sw, col in ((30, "#1a0a06"), (14, "#ffffff")):
            tg += f'<text x="40" y="{y}" font-family="Inter Display" font-weight="900" font-size="150" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round">{tx}</text>'
        tg += f'<text x="40" y="{y}" font-family="Inter Display" font-weight="900" font-size="150" fill="url(#gold)">{tx}</text>'
    tg += '</g>'
    s += tg
    s += f'<g transform="rotate(-4 200 560)"><rect x="50" y="480" width="470" height="86" rx="14" fill="#fff" stroke="#1a0a06" stroke-width="6"/><text x="285" y="541" font-family="Inter Display" font-weight="800" font-size="44" fill="#1a0a06" text-anchor="middle">{etq}</text></g>'
    s += '<rect width="1280" height="720" fill="none" stroke="#111" stroke-width="22"/></svg>'
    return s
