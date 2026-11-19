"""Cenas animadas do Gedeón (template gibi). Cada cena é função de t (0..LOOP) que devolve um SVG 1920x1080."""
from fabrica.kit import *
from fabrica.kit_biblia import *

GEDEON = dict(hair="short", hair_col="#3a2414", beard="yes", beard_col="#3a2414", tunic="#7a6a4a", robe="#8a5a3a", belt="#6a4a2a")
JOAS = dict(hair="bald", hair_col="#9a9a9a", beard="yes", beard_col="#b0b0b0", tunic="#a0522d", robe="#5a3a2a")
MADIANITA = dict(hood="#8a1f2e", hair="short", hair_col="#1a1410", beard="yes", beard_col="#1a1410", tunic="#2a2a3a", robe="#4a1a1a", belt="#c9a14a")
MADIANITA2 = dict(hood="#2a4a6a", hair="short", hair_col="#1a1410", beard="yes", beard_col="#1a1410", tunic="#5a3a2a", robe="#2a3a4a", belt="#e8c27a")
PURA = dict(hair="curly", hair_col="#2a1a10", beard="none", tunic="#5a7a5a")
SIERVO = [dict(hair="short", hair_col="#2a1a10", beard="yes", beard_col="#2a1a10", tunic=c) for c in ("#6a8a5a", "#8a6a3a", "#5a6a8a", "#9a5a3a")]
SOLDADO = [dict(hair="short" if i % 2 else "curly", hair_col="#2a1a10", beard="yes" if i % 3 else "none", beard_col="#2a1a10", tunic=POVO[i % len(POVO)]) for i in range(7)]


# ---------------- elementos novos ----------------
def camelo(t, x, y, s=1.0, flip=False, fase=0.0, cor="#c9a060"):
    p = 22 * onda(t, LOOP / 2, fase)
    c = (f'<path d="M-90 -30 l{p:.0f} 130 M-30 -30 l{-p:.0f} 130 M60 -30 l{-p:.0f} 130 M120 -30 l{p:.0f} 130" stroke="{cor}" stroke-width="26" stroke-linecap="round"/>'
         f'<path d="M-90 -30 l{p:.0f} 130 M-30 -30 l{-p:.0f} 130 M60 -30 l{-p:.0f} 130 M120 -30 l{p:.0f} 130" stroke="{OL}" stroke-width="3" stroke-linecap="round" opacity="0.5"/>'
         f'<ellipse cx="0" cy="-90" rx="150" ry="70" fill="{cor}" stroke="{OL}" stroke-width="6"/>'
         f'<path d="M-60 -150 Q-20 -250 30 -150 Z" fill="{cor}" stroke="{OL}" stroke-width="6"/>'
         f'<path d="M100 -120 Q190 -200 190 -280 L240 -300 L246 -250 L220 -240 Q220 -150 140 -50 Z" fill="{cor}" stroke="{OL}" stroke-width="6"/>'
         f'<circle cx="214" cy="-272" r="7" fill="{OL}"/><path d="M-120 -120 q-40 20 -50 70" stroke="{OL}" stroke-width="6" fill="none"/>'
         f'<rect x="-70" y="-160" width="120" height="36" rx="10" fill="#8a1f2e" stroke="{OL}" stroke-width="5"/>')
    return g(c, x, y, s, flip)


def tienda(x, y, s=1.0, cor="#b4332e", cor2="#7a1f1f"):
    c = (f'<path d="M-200 0 L0 -260 L200 0 Z" fill="{cor}" stroke="{OL}" stroke-width="6"/>'
         f'<path d="M0 -260 L60 0 L-60 0 Z" fill="{cor2}" stroke="{OL}" stroke-width="5"/>'
         f'<path d="M0 -260 V-330 L50 -310 L0 -290" fill="#e8c27a" stroke="{OL}" stroke-width="4"/>')
    return g(c, x, y, s)


def campamento(t, noche=True, y=880, n=7, base=0):
    s = ""
    for i in range(n):
        x = 160 + i * (1600 / (n - 1)) + ((i * 37 + base * 53) % 90) - 45
        yy = y - (i % 3) * 40
        s += tienda(x, yy, 0.55 + 0.1 * ((i + base) % 3), *(("#b4332e", "#7a1f1f") if (i + base) % 2 else ("#8a5a2a", "#5a3a1a")))
        if i % 2 == 0:
            s += camelo(t, x + 130, yy + 20, 0.38, flip=bool(i % 4), fase=i * 0.2)
        if noche and i % 2 == 1:
            s += fogo(t, x + 110, yy + 10, 0.28, 3)
    return s


def langostas(t, n=40):
    s = ""
    for i in range(n):
        x = (i * 211 + 400 * t / LOOP) % 2000 - 40
        y = 120 + (i * 97) % 520 + 20 * onda(t, LOOP / 2, i * 0.13)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="16" ry="6" fill="#6a5a1a" stroke="{OL}" stroke-width="2"/>'
    return s


def encina(x, y, s=1.0):
    c = (f'<path d="M-30 0 Q-20 -200 -10 -330 M0 -260 Q-140 -320 -200 -420 M0 -280 Q130 -340 210 -430" stroke="#5a3a1e" stroke-width="44" stroke-linecap="round" fill="none"/>')
    for (cx, cy, r) in [(-200, -470, 130), (0, -520, 170), (200, -470, 130), (-90, -600, 110), (100, -610, 110)]:
        c += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#4a7a2a" stroke="{OL}" stroke-width="6"/>'
    return g(c, x, y, s)


def garba(x, y, s=1.0):
    c = f'<path d="M-30 0 L-18 -150 L18 -150 L30 0 Z" fill="#d9b04a" stroke="{OL}" stroke-width="5"/><rect x="-34" y="-80" width="68" height="16" rx="6" fill="#8a5a30" stroke="{OL}" stroke-width="4"/>'
    for i in range(7):
        c += f'<path d="M{-18 + i * 6} -150 l{(i - 3) * 9} -60" stroke="#e8c85a" stroke-width="7" stroke-linecap="round"/>'
    return g(c, x, y, s)


def lagar(x, y, s=1.0):
    c = (f'<path d="M-340 0 L-300 -170 L300 -170 L340 0 Z" fill="#9a958c" stroke="{OL}" stroke-width="7"/>'
         f'<ellipse cx="0" cy="-170" rx="300" ry="46" fill="#6a5a4a" stroke="{OL}" stroke-width="6"/>'
         f'<ellipse cx="0" cy="-176" rx="270" ry="34" fill="#d9b04a"/>')
    for i in range(-2, 3):
        c += f'<path d="M{i * 90} -176 l{i * 5} -70" stroke="#e8c85a" stroke-width="8" stroke-linecap="round"/>'
    return g(c, x, y, s)


def cabrito(x, y, s=1.0):
    c = (f'<ellipse cx="0" cy="-60" rx="80" ry="46" fill="#f0e8d8" stroke="{OL}" stroke-width="5"/><circle cx="84" cy="-86" r="30" fill="#f0e8d8" stroke="{OL}" stroke-width="5"/>'
         f'<path d="M-50 -20 v50 M-10 -20 v50 M30 -20 v50 M60 -20 v50" stroke="{OL}" stroke-width="12" stroke-linecap="round"/><path d="M80 -112 l-10 -24 M96 -112 l10 -24" stroke="{OL}" stroke-width="5"/>')
    return g(c, x, y, s)


def pena(x, y, s=1.0, t=None):
    c = f'<path d="M-200 0 Q-230 -160 -120 -260 Q0 -320 130 -250 Q230 -150 200 0 Z" fill="#8a8580" stroke="{OL}" stroke-width="7"/>'
    if t is not None:
        c += fogo(t, 0, -240, 0.8, 7)
    return g(c, x, y, s)


def trompeta(x, y, s=1.0, ang=0, flip=False):
    c = (f'<path d="M0 0 L220 -26 Q300 -70 330 -140 L360 -110 Q330 10 220 26 L0 14 Z" fill="#e8b83a" stroke="{OL}" stroke-width="6"/>'
         f'<ellipse cx="0" cy="7" rx="14" ry="10" fill="#c98a1a" stroke="{OL}" stroke-width="5"/>')
    return f'<g transform="translate({x},{y}) rotate({ang}) scale({s * (-1 if flip else 1)},{s})">{c}</g>'


def cantaro(t, x, y, s=1.0, roto=False, luz=True):
    c = ""
    if not roto:
        c += (f'<path d="M-50 0 Q-90 -70 -50 -130 L-36 -160 L36 -160 L50 -130 Q90 -70 50 0 Z" fill="#b0603a" stroke="{OL}" stroke-width="6"/>'
              f'<rect x="-44" y="-178" width="88" height="20" rx="7" fill="#b0603a" stroke="{OL}" stroke-width="6"/>')
        if luz:
            c += f'<circle cx="0" cy="-200" r="{70 + 8 * onda(t, LOOP / 2):.0f}" fill="#ffd27a" opacity="0.35"/>'
    else:
        c += (f'<path d="M-60 0 L-44 -60 L-10 -20 L14 -80 L40 -30 L66 0 Z" fill="#b0603a" stroke="{OL}" stroke-width="6"/>'
              f'<path d="M-90 20 l20 -26 l22 28 Z M80 10 l16 -24 l20 28 Z" fill="#b0603a" stroke="{OL}" stroke-width="5"/>')
    return g(c, x, y, s)


def antorcha(t, x, y, s=1.0):
    c = f'<rect x="-9" y="-10" width="18" height="170" rx="6" fill="#6b4226" stroke="{OL}" stroke-width="4"/>'
    c += fogo(t, 0, -4, 0.22, 3)
    return g(c, x, y, s)


def vellon(x, y, s=1.0, mojado=True):
    cor = "#f4f0e4" if not mojado else "#dfe8f0"
    c = ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{cor}" stroke="{OL}" stroke-width="5"/>' for cx, cy, r in [(-110, -30, 70), (-30, -60, 80), (60, -40, 80), (130, -10, 60), (0, 10, 70)])
    return g(c, x, y, s)


def gotas(t, x, y, n=8, cor="#7ab8e8"):
    s = ""
    for i in range(n):
        f = ((t / LOOP) + i / n) % 1
        s += f'<ellipse cx="{x + (i % 4) * 38 - 60}" cy="{y - 200 + 260 * f:.0f}" rx="6" ry="10" fill="{cor}" opacity="{1 - f:.2f}"/>'
    return s


def idolo(x, y, s=1.0):
    c = (f'<rect x="-30" y="-380" width="60" height="380" rx="12" fill="#7a5a30" stroke="{OL}" stroke-width="6"/>'
         f'<circle cx="0" cy="-420" r="56" fill="#9a7a40" stroke="{OL}" stroke-width="6"/><circle cx="-18" cy="-428" r="7" fill="{OL}"/><circle cx="18" cy="-428" r="7" fill="{OL}"/>'
         f'<path d="M-22 -400 q22 14 44 0" stroke="{OL}" stroke-width="5" fill="none"/><path d="M-50 -470 l-26 -50 M50 -470 l26 -50" stroke="{OL}" stroke-width="12" stroke-linecap="round"/>')
    return g(c, x, y, s)


def altar_baal(x, y, s=1.0):
    return g(altar(0, 0, 1.0, boi=False) + idolo(0, -240, 0.8), x, y, s)


def efod(x, y, s=1.0, t=None):
    c = (f'<path d="M-120 -330 L120 -330 L150 -80 L-150 -80 Z" fill="#e8b83a" stroke="{OL}" stroke-width="7"/>'
         f'<rect x="-100" y="-290" width="200" height="130" rx="12" fill="#c98a1a" stroke="{OL}" stroke-width="6"/>'
         + ''.join(f'<circle cx="{-70 + i * 47}" cy="{-250 if j == 0 else -200}" r="14" fill="{c_}" stroke="{OL}" stroke-width="3"/>' for j in range(2) for i, c_ in enumerate(("#e8435a", "#3a8ae8", "#3ac86a", "#e8e83a")))
         + f'<rect x="-8" y="-80" width="16" height="80" fill="#6b4226" stroke="{OL}" stroke-width="5"/>')
    if t is not None:
        c += f'<circle cx="0" cy="-210" r="{230 + 12 * onda(t, LOOP):.0f}" fill="#ffd27a" opacity="0.18"/>'
    return g(c, x, y, s)


def pequenos(t, y, n, s=0.2, x0=100, x1=1820, olhos="open", pasos=False, nome=None, flip=False):
    out = ""
    for i in range(n):
        x = x0 + i * ((x1 - x0) / max(1, n - 1))
        b = SOLDADO[i % 7]
        yy = y + ((i * 17) % 3) * 14
        sw = 3 * onda(t, LOOP / 3, i * 0.17) if pasos else 0
        out += pessoa(t, x, yy + abs(sw), s, base=b, eyes=olhos, mouth="smile", arms=("down", "down"), piscar=(i * 0.37) % LOOP, flip=flip or i % 2 == 1, fixo=True)
    return out


def noche(estrellas=40, top="#0a0a2a", bot="#2a2a5a"):
    s = ceu(top, bot, "n")
    for i in range(estrellas):
        s += f'<circle cx="{(i * 331) % 1900 + 10}" cy="{(i * 127) % 520 + 20}" r="{2 + i % 3}" fill="#fff" opacity="0.8"/>'
    return s + '<circle cx="1560" cy="170" r="62" fill="#f4f0d0"/>'


def haz(t, x=960, op=0.22):
    return luz_ceu(t, x, op)


# ---------------- cenas ----------------
def g0(t):
    s = noche() + montanha("#2a2a3a", 760) + campamento(t, True, 700, 8) + chao("#1a1a24", 880)
    s += pessoa(t, V(660, 520, 820), 1010, 0.9, base=GEDEON, eyes="side", mouth="sad", brows="sad", arms=("up", "flex"), balanco=1.5)
    s += cantaro(t, V(930, 1000, 860), 1010, 0.8)
    s += trompeta(V(760, 640, 920), 560, 0.45, -25)
    return frame_(s + particulas(t, 15, "#ffd27a"))


def g0b(t):
    s = noche(60) + montanha("#2a2a3a", 700) + campamento(t, True, V(820, 780, 860), 9, base=V(0, 1, 2)) + chao("#1a1a24", 900)
    return frame_(s + calor(t, 960, 560))


def g1a(t):
    s = ceu("#c8b060", "#f0e0a8") + sol_quente(t, 1500, 200, 150) + chao("#9a8a4a", 760)
    s += langostas(t, 46) + campamento(t, False, 900, 7, base=V(0, 1, 2, 3))
    s += garba(V(300, 1500, 900), 960, 0.9)
    return frame_(s)


def g1b(t):
    s = bg_cave()
    for i, x in enumerate((420, 760, 1160, 1500)):
        s += pessoa(t, x + V(0, 40, -40), 1010, 0.62, base=SOLDADO[i % 7], eyes="side", mouth="sad", brows="sad", arms=("face", "down"), flip=i % 2 == 1, piscar=i * 0.4, balanco=1.2)
    s += fogo(t, V(960, 1000), 1000, 0.3, 3)
    return frame_(s)


def g1c(t):
    s = ceu("#d8c890", "#f0e8c0") + montanha("#b09a6a", 700) + chao("#a08a5a", 840) + lagar(V(960, 780, 1160), 960, 1.1)
    s += garba(V(300, 400), 960, 1.0) + garba(V(1560, 1500), 960, 0.9)
    pulso = 10 * onda(t, LOOP / 2)
    s += pessoa(t, V(960, 780, 1160), 960 + pulso * 0.3, 0.68, base=GEDEON, eyes="side", mouth="sad", brows="sad", arms=("hold", "down"), balanco=2)
    s += camelo(t, 1750, 880, 0.3, True, 0)
    return frame_(s)


def g1d(t):
    s = ceu_sol("#8ac8f0", "#e8f6ff") + montanha("#7a8a4a", 640) + chao("#a8a060", 860) + encina(V(1350, 1250, 1500), 920, 1.1)
    s += anjo(t, V(1250, 1200, 1400), 1000, 0.62)
    s += pessoa(t, V(560, 440, 700), 1000, 0.82, base=GEDEON, eyes="open", mouth="sad", brows="sad", arms=("hold", "down"), balanco=1.5)
    return frame_(s + particulas(t, 15))


def g2a(t):
    s = ceu_sol("#8ac8f0", "#e8f6ff") + montanha("#7a8a4a", 640) + chao("#a8a060", 860) + encina(V(1700, 1600), 920, 0.9)
    s += anjo(t, V(1300, 1200, 1400), 1000, 0.6)
    s += pessoa(t, V(520, 640, 420), 1000, 0.85, base=GEDEON, eyes="open", mouth="sad", brows="angry", arms=("flex", "forward"), nome="gedeon", balanco=2)
    return frame_(s)


def g2b(t):
    s = ceu_sol("#ffd890", "#fff0c8") + montanha("#8a8a4a", 660) + chao("#b0a060", 860)
    s += anjo(t, V(1300, 1400, 1200), 1000, 0.6)
    s += pessoa(t, V(560, 460, 700), 1000, 0.85, base=GEDEON, eyes="down" if False else "side", mouth="sad", brows="sad", arms=("face", "down"), nome="gedeon", balanco=2)
    return frame_(s)


def g2c(t):
    s = ceu_sol("#ffd890", "#fff0c8") + montanha("#8a8a4a", 660) + chao("#b0a060", 860)
    s += pena(V(960, 1050, 860), 940, 1.05, t)
    s += cabrito(V(600, 500), 940, 0.9) + pao(V(480, 700), 960, 0.7)
    s += anjo(t, V(1500, 1600), 1000, 0.55)
    return frame_(s + particulas(t, 35, "#ffb040"))


def g2d(t):
    s = ceu("#2a2a5a", "#c08a5a") + montanha("#6a5a3a", 700) + chao("#9a7a50", 880) + haz(t, V(1300, 1200), 0.25)
    s += altar(V(560, 700), 980, 0.75, boi=False)
    s += pessoa(t, V(1000, 900, 1100), 1000, 0.8, base=GEDEON, eyes="closed", mouth="sad", brows="sad", arms=("pray", "pray"), balanco=1)
    s += anjo(t, V(1550, 1500), 1000, 0.55)
    return frame_(s + particulas(t, 20))


def g3a(t):
    s = noche(35) + montanha("#2a3a2a", 760) + chao("#2a3022", 880) + altar_baal(V(1300, 1200, 1450), 960, 1.0)
    for i in range(4):
        x = 280 + i * 190
        s += pessoa(t, x, 1010, 0.62, base=SIERVO[i], eyes="side", mouth="sad", brows="sad", arms=("hold", "down"), balanco=1.2, piscar=i * .5)
        s += antorcha(t, x + 85, 760, 0.9)
    s += pessoa(t, 150, 1010, 0.7, base=GEDEON, eyes="side", mouth="sad", brows="angry", arms=("point", "down"), flip=False, fixo=True)
    return frame_(s)


def g3b(t):
    f = (t / LOOP)
    s = noche(35) + montanha("#2a3a2a", 760) + chao("#2a3022", 880)
    s += g(altar(0, 0, 1.0, boi=False), 1100, 960 + 20 * f, 0.9)
    s += g(idolo(0, 0, 1.0), 1100 + 160 * f, 700 + 280 * f, 0.9).replace('<g transform="', f'<g transform="rotate({40 * f:.0f} 1100 760) ', 1)
    for i in range(6):
        ff = ((t / LOOP) + i / 6) % 1
        s += f'<rect x="{900 + i * 80}" y="{600 + 300 * ff:.0f}" width="60" height="46" rx="10" fill="#9a958c" stroke="{OL}" stroke-width="4" transform="rotate({300 * ff:.0f} {930 + i * 80} {620 + 300 * ff:.0f})"/>'
    s += pessoa(t, V(420, 520), 1010, 0.8, base=GEDEON, eyes="open", mouth="shout", brows="angry", arms=("up", "flex"))
    s += antorcha(t, 200, 760, 1.0)
    return frame_(f'<g transform="translate({6 * onda(t, LOOP / 6):.1f},{4 * onda(t, LOOP / 5):.1f})">{s}</g>')


def g3c(t):
    s = ceu_sol("#ffb070", "#ffe8b8") + montanha("#8a7a4a", 640) + chao("#b89060", 860)
    s += multidao(t, 1040, 0.4, 10, olhos="open", boca="shout", braços=("up", "flex"), cor0=1, nome="pueblo")
    s += pessoa(t, V(1000, 900, 1100), 960, 0.78, base=JOAS, eyes="open", mouth="sad", brows="angry", arms=("up", "point"), nome="joas", fixo=True)
    s += pessoa(t, 1620, 1010, 0.62, base=GEDEON, eyes="side", mouth="sad", brows="sad", arms=("down", "down"), flip=True, fixo=True)
    return frame_(s)


def g3d(t):
    s = ceu_sol("#ffb070", "#ffe8b8") + montanha("#8a7a4a", 700) + chao("#b89060", 880)
    s += altar(V(1250, 1150, 1380), 980, 0.85, boi=True) + fogo(t, V(1250, 1150, 1380), 700, 0.7, 5)
    s += pessoa(t, V(560, 700, 460), 1000, 0.82, base=GEDEON, eyes="open", mouth="smile", brows="normal", arms=("pray", "down"))
    return frame_(s + particulas(t, 18, "#ffd27a"))


def g4a(t):
    s = ceu_sol("#8ac8f0", "#e8f6ff") + montanha("#7a8a4a", 600) + chao("#a8a060", 860)
    s += pequenos(t, 1010, V(8, 10, 12), 0.2, 100, 1820, "side")
    s += pessoa(t, V(960, 820, 1100), 960, 0.85, base=GEDEON, eyes="open", mouth="shout", brows="normal", arms=("up", "flex"), balanco=1.5, fixo=True)
    s += trompeta(V(1060, 920, 1180), 330, 0.55, -50)
    return frame_(s + luz_ceu(t, 960, 0.12))


def g4b(t):
    s = ceu_sol("#ffd890", "#fff0c8") + chao("#c8b070", 780) + haz(t, 960, 0.08)
    s += vellon(V(960, 800, 1100), 820, 1.4, True) + gotas(t, V(960, 800, 1100), 720, 8)
    s += g(f'<path d="M-90 0 Q-80 80 0 80 Q80 80 90 0 Z" fill="#b0603a" stroke="{OL}" stroke-width="6"/>', V(1400, 1500), 960, 1.0)
    s += pessoa(t, V(520, 420, 620), 1000, 0.8, base=GEDEON, eyes="up", mouth="sad", brows="sad", arms=("pray", "down"), nome="gedeon", balanco=1)
    return frame_(s)


def g4c(t):
    s = ceu_sol("#ffd890", "#fff0c8") + chao("#9ac870", 780)
    for i in range(30):
        s += f'<circle cx="{(i * 113) % 1900 + 20}" cy="{800 + (i * 37) % 200}" r="6" fill="#bfe4ff" stroke="#6aa8d8" stroke-width="2"/>'
    s += vellon(V(960, 800, 1100), 880, 1.4, False)
    s += pessoa(t, V(520, 420, 620), 1000, 0.8, base=GEDEON, eyes="open", mouth="sad", brows="sad", arms=("forward", "down"), nome="gedeon", balanco=1)
    return frame_(s + particulas(t, 20, "#e8fff8"))


def g5a(t):
    s = ceu_sol("#8ac8f0", "#e8f6ff") + montanha("#7a8a4a", 600) + chao("#a8a060", 860) + arroyo(t).replace("820", "900").replace("800", "880")
    s += pequenos(t, 960, 12, 0.18, 80, 1840) + pequenos(t, 1010, 12, 0.22, 120, 1800, "side")
    s += pessoa(t, V(960, 860), 930, 0.62, base=GEDEON, eyes="up", mouth="sad", brows="sad", arms=("forward", "down"), fixo=True)
    return frame_(s + haz(t, 960, 0.3))


def g5b(t):
    s = ceu_sol("#8ac8f0", "#e8f6ff") + montanha("#7a8a4a", 600) + chao("#a8a060", 860)
    for i in range(10):
        x = 1840 - ((i * 190 + 260 * t / LOOP) % 1900)
        s += pessoa(t, x, 1000 + (i % 2) * 20, 0.24, base=SOLDADO[i % 7], eyes="side", mouth="sad", arms=("down", "down"), flip=True, fixo=True, piscar=i * .3)
    s += pequenos(t, 940, V(5, 6, 4), 0.2, 160, 700, "open")
    s += pessoa(t, V(960, 1100), 960, 0.7, base=GEDEON, eyes="side", mouth="sad", brows="sad", arms=("flex", "down"), fixo=True)
    return frame_(s)


def g5c(t):
    s = ceu_sol("#8ac8f0", "#e8f6ff") + montanha("#7a8a4a", 600) + chao("#a8a060", 840) + arroyo(t).replace("820", "930").replace("800", "910").replace("900", "1000").replace("890", "990")
    for i in range(4):
        x = 220 + i * 210
        c, _ = person(**{**SOLDADO[i], "eyes": "closed", "arms": ("up", "up"), "mouth": "smile"})
        s += f'<g transform="translate({x},{930 + (i % 2) * 20}) rotate(-80) scale(0.32)">{c}</g>'
    for i in range(3):
        x = 1250 + i * 210
        s += pessoa(t, x, 1000, 0.45, base=SOLDADO[(i + 4) % 7], eyes="open", mouth="smile", arms=("face", "down"), fixo=True, piscar=i * .5)
    return frame_(s)


def g5d(t):
    s = ceu("#6a7aa0", "#e8d8b8") + montanha("#7a7a4a", 640) + chao("#a8a060", 860) + haz(t, 960, 0.35)
    s += pequenos(t, 1000, V(14, 12, 16), 0.3, 100, 1820, "open", False)
    s += pessoa(t, V(960, 800, 1120), 960, 0.78, base=GEDEON, eyes="up", mouth="smile", brows="normal", arms=("up", "flex"), fixo=True)
    return frame_(s + particulas(t, 25, "#fff3c0"))


def g6a(t):
    s = noche(60) + montanha("#1a1a2a", 700) + campamento(t, True, 820, 8, base=V(0, 1, 2)) + haz(t, 1200, 0.1)
    s += pessoa(t, V(420, 560, 320), 1010, 0.7, base=GEDEON, eyes="side", mouth="sad", brows="sad", arms=("down", "hold"), balanco=2)
    s += pessoa(t, V(640, 760, 520), 1010, 0.55, base=PURA, eyes="side", mouth="sad", brows="sad", arms=("down", "down"), balanco=2, piscar=.9)
    return frame_(s)


def g6b(t):
    s = noche(30) + chao("#2a2230", 840) + fogo(t, 960, 920, 0.5, 4) + tienda(1600, 900, 1.1) + tienda(260, 900, 0.8)
    s += pessoa(t, V(660, 560, 760), 1000, 0.78, base=MADIANITA, eyes="open", mouth="sad", brows="sad", arms=("flex", "forward"), nome="soldado", balanco=2)
    s += pessoa(t, V(1260, 1360), 1000, 0.78, base=MADIANITA2, eyes="open", mouth="sad", brows="sad", arms=("down", "point"), flip=True, nome="companero", balanco=2)
    return frame_(s)


def g6c(t):
    s = noche(70) + montanha("#1a1a2a", 760) + chao("#1a1a24", 880) + haz(t, V(960, 800), 0.12)
    s += pessoa(t, V(800, 700, 960), 1000, 0.8, base=GEDEON, eyes="closed", mouth="smile", brows="normal", arms=("pray", "pray"), nome="gedeon", balanco=1)
    s += pessoa(t, V(1100, 1200), 1010, 0.5, base=PURA, eyes="side", mouth="smile", arms=("down", "down"), piscar=.8)
    return frame_(s + particulas(t, 25, "#fff3c0"))


def g7a(t):
    s = noche(50) + montanha("#1a1a2a", 660) + campamento(t, True, 880, 7, base=V(1, 2)) + chao("#1a1a24", 920)
    for k, x0 in enumerate((240, 860, 1480)):
        for i in range(4):
            s += pessoa(t, x0 + i * 90, 1030 - i * 4, 0.2, base=SOLDADO[(i + k) % 7], eyes="open", mouth="sad", arms=("up", "down"), fixo=True)
            s += cantaro(t, x0 + i * 90 + 38, 1030, 0.17)
    return frame_(s)


def g7b(t):
    s = noche(45) + montanha("#1a1a2a", 760) + chao("#1a1a24", 880) + campamento(t, True, 700, 6, base=3)
    s += pessoa(t, V(900, 780, 1050), 1010, 0.85, base=GEDEON, eyes="open", mouth="sad", brows="angry", arms=("hold", "up"), nome="gedeon", balanco=2)
    s += trompeta(V(1060, 940, 1200), 600, 0.5, -30) + cantaro(t, V(1500, 1560), 1010, 0.8)
    for i in range(3):
        s += pessoa(t, 220 + i * 170, 1010, 0.45, base=SOLDADO[i], eyes="open", mouth="sad", arms=("down", "down"), fixo=True, piscar=i * .5)
    return frame_(s)


def g7c(t):
    f = t / LOOP
    s = noche(40) + montanha("#1a1a2a", 760) + chao("#1a1a24", 880) + campamento(t, True, 740, 7, base=2)
    s += f'<rect width="1920" height="1080" fill="#fff6c0" opacity="{0.10 + 0.08 * abs(onda(t, LOOP / 3)):.2f}"/>'
    for i in range(7):
        x = 160 + i * 270
        s += pessoa(t, x, 1020, 0.42, base=SOLDADO[i % 7], eyes="open", mouth="shout", brows="angry", arms=("up", "up"), fixo=True, nome="pueblo" if i == 3 else None)
        s += antorcha(t, x - 70, 640, 1.3) + trompeta(x + 40, 560, 0.28, -60)
        s += cantaro(t, x + 70, 1030 + 10 * f, 0.2, roto=True)
    return frame_(f'<g transform="translate({5 * onda(t, LOOP / 6):.1f},{3 * onda(t, LOOP / 5):.1f})">{s}</g>' + particulas(t, 40, "#ffd27a"))


def g7d(t):
    f = t / LOOP
    s = noche(30) + chao("#2a2230", 860) + haz(t, 960, 0.12)
    for i in range(5):
        x = ((i * 420 + 600 * f * (1 if i % 2 else -1)) % 2000) - 60
        s += camelo(t, x, 960 + (i % 2) * 40, 0.55, bool(i % 2), i * 0.3)
    for i in range(8):
        x = ((i * 250 + 520 * f) % 2100) - 80
        s += pessoa(t, x, 1030, 0.34, base=(MADIANITA if i % 2 else MADIANITA2), eyes="open", mouth="shout", brows="sad", arms=("up", "up"), flip=True, fixo=True, piscar=i * .3)
    s += tienda(V(300, 1500), 900, 0.9) + fogo(t, V(1500, 300), 900, 0.4, 4)
    return frame_(s)


def g7e(t):
    s = ceu("#3a2a6a", "#ff9a5a") + montanha("#5a4a3a", 760) + chao("#9a7a50", 880)
    s += pequenos(t, 1010, 8, 0.28, 120, 900, "open")
    s += pessoa(t, V(1150, 1000), 960, 0.8, base=GEDEON, eyes="open", mouth="smile", brows="normal", arms=("up", "flex"), balanco=1.5, fixo=True)
    for i in range(2):
        s += pessoa(t, 1500 + i * 220, 1010, 0.6, base=MADIANITA2, eyes="side", mouth="sad", brows="sad", arms=("down", "down"), flip=True, fixo=True)
    return frame_(s)


def g8a(t):
    s = ceu_sol("#ffb070", "#ffe8b8") + montanha("#8a7a4a", 640) + chao("#b89060", 860)
    s += multidao(t, 1040, 0.36, 9, olhos="open", boca="shout", braços=("up", "flex"), cor0=3, nome="pueblo")
    s += g(f'<circle cx="0" cy="-30" r="90" fill="none" stroke="#e8b83a" stroke-width="30"/><path d="M-90 -30 l20 -90 l35 50 l35 -80 l35 80 l35 -50 l20 90" fill="#e8b83a" stroke="{OL}" stroke-width="6"/>', V(1400, 1300), 500 + 10 * onda(t, LOOP), 1.0)
    s += pessoa(t, V(780, 700, 900), 960, 0.8, base=GEDEON, eyes="open", mouth="sad", brows="normal", arms=("up", "forward"), nome="gedeon", fixo=True, balanco=1.5)
    return frame_(s)


def g8b(t):
    s = ceu("#6a5a4a", "#e8d0a0") + chao("#a08a5a", 840) + montanha("#8a7a5a", 700)
    s += efod(V(960, 1120, 800), 960, 1.4, t)
    for i in range(6):
        s += moedas(300 + i * 40, 980, 3).replace('<g transform="', '<g transform="') if False else ""
    s += moedas(V(420, 1500), 960, 6)
    s += pessoa(t, V(520, 1500, 420), 1010, 0.7, base=GEDEON, eyes="side", mouth="sad", brows="sad", arms=("face", "down"), balanco=1.2)
    for i, x in enumerate((1550, 1700, 1850)):
        c, _ = person(**{**SOLDADO[i], "eyes": "closed", "arms": ("pray", "pray")})
        s += f'<g transform="translate({x},{1000}) rotate(-25) scale(0.34)">{c}</g>'
    return frame_(s + particulas(t, 25, "#ffd27a"))


def g8c(t):
    s = bg_heaven() + luz_ceu(t, 960, 0.12)
    rolo = (f'<rect x="-420" y="-260" width="840" height="520" rx="10" fill="#f0e2c0" stroke="{OL}" stroke-width="8"/>'
            f'<rect x="-460" y="-290" width="60" height="580" rx="30" fill="#8a5a30" stroke="{OL}" stroke-width="6"/>'
            f'<rect x="400" y="-290" width="60" height="580" rx="30" fill="#8a5a30" stroke="{OL}" stroke-width="6"/>'
            f'<text x="0" y="-40" font-family="Lora" font-weight="700" font-size="76" fill="#5a3a1a" text-anchor="middle">Hebreos 11:32</text>'
            f'<text x="0" y="70" font-family="Lora" font-style="italic" font-size="60" fill="#5a3a1a" text-anchor="middle">Gedeón, el valiente</text>')
    s += g(rolo, V(960, 900, 1020), 520 + 10 * onda(t, LOOP), V(1, 1.12, 0.92))
    return frame_(s + particulas(t, 30))


def g8d(t):
    s = ceu_sol("#ffb070", "#ffe8b8") + montanha("#a0a060", 700) + chao("#c8b070", 860)
    for x in range(120, 1900, 260):
        s += garba(x + V(0, 40, -40), 1000, V(1.0, 1.2, 0.9))
    s += pessoa(t, V(960, 800, 1120), 1000, 0.8, base={**GEDEON, "hair_col": "#9a9a9a", "beard_col": "#b0b0b0"}, eyes="open", mouth="smile", arms=("down", "flex"), fixo=True, balanco=1)
    return frame_(s + particulas(t, 22, "#ffe8a0"))


def g9(t):
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
    return {k: v for k, v in globals().items() if callable(v) and k.startswith("g") and k[1:2].isdigit()}


FOCO = {
    "g0": (700, 380), "g0b": (960, 600), "g1a": (960, 600), "g1b": (960, 600), "g1c": (960, 500), "g1d": (1200, 500),
    "g2a": (560, 380), "g2b": (580, 380), "g2c": (960, 650), "g2d": (900, 450), "g3a": (900, 600), "g3b": (900, 600),
    "g3c": (1000, 450), "g3d": (900, 550), "g4a": (960, 400), "g4b": (960, 700), "g4c": (960, 700), "g5a": (960, 700),
    "g5b": (960, 700), "g5c": (900, 850), "g5d": (960, 600), "g6a": (600, 600), "g6b": (900, 450), "g6c": (900, 500),
    "g7a": (960, 750), "g7b": (950, 550), "g7c": (960, 650), "g7d": (960, 800), "g7e": (1100, 600), "g8a": (900, 450),
    "g8b": (960, 650), "g8c": (960, 520), "g8d": (960, 550), "g9": (900, 520),
}

THUMBS = "AB"


def thumb(variant="A"):
    s = ('<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">'
         '<defs><radialGradient id="L" cx="0.62" cy="0.45" r="0.75"><stop offset="0" stop-color="#ffd27a"/><stop offset="0.45" stop-color="#d0602a"/><stop offset="1" stop-color="#14081a"/></radialGradient>'
         '<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff7c9"/><stop offset="0.5" stop-color="#ffd84a"/><stop offset="1" stop-color="#ff9a12"/></linearGradient>'
         '<pattern id="ht" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="1.8" fill="#000"/></pattern></defs>'
         '<rect width="1280" height="720" fill="url(#L)"/>')
    VAR["v"] = 0
    if variant == "A":
        s += g(campamento(1.0, True, 560, 6), 640, 130, 0.55)
        c, _ = person(**{**GEDEON, "eyes": "open", "mouth": "shout", "brows": "angry", "arms": ("up", "flex")})
        s += g(c, 900, 1100, 0.95)
        s += g(cantaro(1.0, 0, 0, 1.0) + trompeta(60, -430, 0.6, -35), 1130, 700, 1.0)
        t1, t2, etq = "SIN", "ESPADAS", "¿SOLO CÁNTAROS?…"
    else:
        for i in range(14):
            c, _ = person(**{**SOLDADO[i % 7], "eyes": "side", "mouth": "sad", "brows": "sad", "arms": ("down", "down")})
            s += g(c, 640 + (i % 7) * 95, 560 + (i // 7) * 90, 0.2, i % 2 == 1)
        c, _ = person(**{**GEDEON, "eyes": "open", "mouth": "shout", "brows": "sad", "arms": ("face", "face")})
        s += g(c, 1000, 1120, 0.95)
        t1, t2, etq = "LE QUITÓ", "31.700", "ANTES DE PELEAR…"
    s += '<rect width="1280" height="720" fill="url(#ht)" opacity="0.10"/>'
    tg = '<g transform="rotate(-4 300 330)">'
    for y, tx in ((260, t1), (400, t2)):
        for sw, col in ((30, "#1a0a06"), (14, "#ffffff")):
            tg += f'<text x="40" y="{y}" font-family="Inter Display" font-weight="900" font-size="150" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round">{tx}</text>'
        tg += f'<text x="40" y="{y}" font-family="Inter Display" font-weight="900" font-size="150" fill="url(#gold)">{tx}</text>'
    tg += '</g>'
    s += tg
    s += f'<g transform="rotate(-4 200 560)"><rect x="50" y="480" width="520" height="86" rx="14" fill="#fff" stroke="#1a0a06" stroke-width="6"/><text x="310" y="541" font-family="Inter Display" font-weight="800" font-size="44" fill="#1a0a06" text-anchor="middle">{etq}</text></g>'
    s += '<rect width="1280" height="720" fill="none" stroke="#111" stroke-width="22"/></svg>'
    return s
