"""Cenas animadas do Jonás. Cada cena é uma função de t (0..LOOP) que devolve um SVG 1920x1080."""
import math
from fabrica.desenho import *
from fabrica.animacao import onda, piscando, respirar

ANIMADO = True
LOOP = 3.0
TAU = 2 * math.pi

JONAS = dict(hair="short", hair_col="#3a2414", beard="yes", beard_col="#3a2414", tunic="#7a6a4a", robe="#35566e")
MARINHEIRO = [dict(hair="short", hair_col="#2a1a10", beard="yes", beard_col="#2a1a10", tunic=c) for c in ("#a0522d", "#5a7a3a", "#7a3a5a", "#3a6a8a")]
REI = dict(hair="curly", hair_col="#1a1410", beard="yes", beard_col="#1a1410", tunic="#c9a14a", robe="#5a1a6a", crown=True, belt="#e8c27a")
SACO = "#8a7a5a"

# ---- variantes: cada corte do vídeo usa um desenho diferente (VAR["v"] muda a cada corte) ----
VAR = {"v": 0}
POSES = {"down": ["down", "flex", "hold", "point"], "pray": ["pray", "face", "up"], "face": ["face", "pray", "down"],
         "up": ["up", "flex", "pray"], "forward": ["forward", "point", "up"], "point": ["point", "forward", "flex"],
         "flex": ["flex", "down", "point"], "hold": ["hold", "down", "flex"]}
DESLOC = [0, -160, 150, -90, 100, -220, 210, -40]
ESCALAS = [1.0, 1.07, 0.94, 1.12, 0.97, 1.04]


def V(*opcoes):
    """Escolhe uma opção conforme a variante do corte."""
    return opcoes[VAR["v"] % len(opcoes)]


def luz_variante():
    v = VAR["v"] % 5
    return ["", '<rect width="1920" height="1080" fill="#ff9a40" opacity="0.10"/>',
            '<rect width="1920" height="1080" fill="#4060c0" opacity="0.10"/>',
            '<defs><radialGradient id="vg"><stop offset="0.55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.55"/></radialGradient></defs><rect width="1920" height="1080" fill="url(#vg)"/>',
            '<rect width="1920" height="1080" fill="#ffe8a0" opacity="0.08"/>'][v]


def pessoa(t, x, y, s, flip=False, base=None, piscar=0.6, amp=0.012, balanco=0.0, fixo=False, **kw):
    kw = {**(base or {}), **kw}
    v = VAR["v"]
    if v and not fixo:
        semente = int(x) % 5
        braços = kw.get("arms", ("down", "down"))
        kw["arms"] = tuple(POSES.get(a, [a])[(v + semente + i) % len(POSES.get(a, [a]))] for i, a in enumerate(braços))
        x = x + DESLOC[(v + semente) % len(DESLOC)] * s
        s = s * ESCALAS[v % len(ESCALAS)]
        y = y + (s - s / ESCALAS[v % len(ESCALAS)]) * 40
    if kw.get("eyes", "open") in ("open", "side", "up") and piscando(t, LOOP, piscar):
        kw["eyes"] = "closed"
    c, _ = person(**kw)
    c = respirar(c, t, amp, LOOP)
    if balanco:
        c = f'<g transform="rotate({balanco * onda(t, LOOP):.2f})">{c}</g>'
    return g(c, x, y, s, flip)


# ---------------- elementos ----------------
def mar(t, y0, cor, amp=18, comp=420, ciclos=1, contorno=True):
    pts = []
    for x in range(-40, 1981, 30):
        y = y0 + amp * math.sin(TAU * (x / comp - ciclos * t / LOOP))
        pts.append(f"{x},{y:.1f}")
    st = f'stroke="{OL}" stroke-width="5"' if contorno else ''
    return f'<path d="M-40 1100 L{" L".join(pts)} L1980 1100 Z" fill="{cor}" {st}/>'


def mar_calmo(t, y0=700):
    return (mar(t, y0, "#3f8fc0", 8, 600) + mar(t, y0 + 90, "#2f78aa", 10, 500, 1, False) +
            mar(t, y0 + 220, "#26679a", 12, 700, 1, False))


def mar_bravo(t, y0=640):
    return (mar(t, y0, "#2a4a6a", 60, 380, 1) + mar(t, y0 + 120, "#20405e", 70, 330, 2, False) +
            mar(t, y0 + 260, "#183450", 80, 450, 1, False))


def navio(t, x, y, s=1, tilt=3, vela="#efe2c0"):
    c = (f'<path d="M-380 -40 L380 -40 L300 110 L-300 110 Z" fill="#7a4a24" stroke="{OL}" stroke-width="6"/>'
         f'<path d="M-380 -40 L380 -40" stroke="#5a3418" stroke-width="16"/>'
         + "".join(f'<circle cx="{i}" cy="30" r="14" fill="#3a2414" stroke="{OL}" stroke-width="4"/>' for i in range(-240, 260, 120))
         + f'<rect x="-10" y="-520" width="20" height="480" fill="#5a3418" stroke="{OL}" stroke-width="5"/>'
         f'<path d="M-10 -500 Q-300 -330 -10 -120 Z" fill="{vela}" stroke="{OL}" stroke-width="6"/>'
         f'<path d="M10 -480 Q260 -330 10 -160 Z" fill="{vela}" stroke="{OL}" stroke-width="6"/>')
    ang = tilt * onda(t, LOOP)
    dy = 10 * onda(t, LOOP / 2)
    return f'<g transform="translate({x},{y + dy:.1f}) rotate({ang:.2f}) scale({s})">{c}</g>'


def chuva(t, n=70, cor="#cfe3ff", op=0.55):
    s = ""
    for i in range(n):
        x = (i * 137) % 1980
        y0 = (i * 91) % 1080
        y = (y0 + 1080 * 2 * t / LOOP) % 1180 - 100
        s += f'<line x1="{x}" y1="{y:.0f}" x2="{x - 18}" y2="{y + 60:.0f}" stroke="{cor}" stroke-width="4" opacity="{op}"/>'
    return s


def raio(t, x=1400, quando=1.2):
    v = (t - quando) % LOOP
    if v > 0.25:
        return ""
    op = 0.7 if v < 0.08 else 0.25
    return (f'<rect width="1920" height="1080" fill="#fff" opacity="{op * 0.5}"/>'
            f'<path d="M{x} 0 L{x - 60} 160 L{x + 10} 170 L{x - 80} 380 L{x - 20} 390 L{x - 120} 600" fill="none" stroke="#fff6c0" stroke-width="12" opacity="{op + 0.3}"/>')


def ceu(top, bot, id_="c"):
    return grad(id_, top, bot) + f'<rect width="1920" height="1080" fill="url(#{id_})"/>'


def nuvens_tempestade(t):
    s = ""
    for i, (x, y, r) in enumerate([(200, 120, 160), (520, 90, 190), (880, 140, 170), (1240, 100, 200), (1620, 130, 180), (1880, 90, 150)]):
        dx = 25 * onda(t, LOOP, i * 0.17)
        s += f'<ellipse cx="{x + dx:.0f}" cy="{y}" rx="{r * 1.4}" ry="{r * 0.7}" fill="#2a3040" opacity="0.92"/>'
    return s


def peixe(t, x, y, s=1, boca=0.3, flip=False):
    rabo = 18 * onda(t, LOOP / 2)
    c = (f'<g transform="rotate({rabo:.1f} 520 0)"><path d="M480 0 L720 -170 Q680 0 720 170 Z" fill="#3a6a8a" stroke="{OL}" stroke-width="7"/></g>'
         f'<path d="M-560 0 Q-420 -260 0 -270 Q420 -250 520 0 Q420 250 0 270 Q-420 260 -560 0 Z" fill="#4a7ea6" stroke="{OL}" stroke-width="8"/>'
         f'<path d="M-500 40 Q-300 220 0 230 Q350 220 470 40 Z" fill="#a9cfe0" opacity="0.9"/>'
         + "".join(f'<path d="M{xx} 30 q-14 70 0 140" fill="none" stroke="#7aa8c4" stroke-width="7"/>' for xx in range(-380, 360, 70))
         + f'<path d="M-40 -265 Q60 -400 200 -255" fill="#3a6a8a" stroke="{OL}" stroke-width="7"/>'
         f'<circle cx="-360" cy="-80" r="38" fill="#fff" stroke="{OL}" stroke-width="6"/><circle cx="-368" cy="-76" r="18" fill="{OL}"/>'
         f'<path d="M-560 0 L-330 {20 + 160 * boca:.0f} L-330 {20 - 30 * boca:.0f} Z" fill="#5a1a24" stroke="{OL}" stroke-width="6"/>')
    dy = 14 * onda(t, LOOP)
    return g(c, x, y + dy, s, flip)


def bolhas(t, x, y, n=8):
    s = ""
    for i in range(n):
        yy = y - ((i * 70 + 300 * t / LOOP * 3) % 420)
        xx = x + 20 * math.sin(i + TAU * t / LOOP)
        s += f'<circle cx="{xx:.0f}" cy="{yy:.0f}" r="{8 + (i % 3) * 5}" fill="none" stroke="#cfefff" stroke-width="4" opacity="0.8"/>'
    return s


def algas(t, x, y, n=5, alt=260, cor="#2f7a4a"):
    s = ""
    for i in range(n):
        xx = x + i * 26
        b = 30 * onda(t, LOOP, i * 0.2)
        s += f'<path d="M{xx} {y} Q{xx + b:.0f} {y - alt / 2} {xx - b / 2:.0f} {y - alt}" fill="none" stroke="{cor}" stroke-width="14" stroke-linecap="round"/>'
    return s


def moedas(x, y, n=5):
    return "".join(coin(x + i * 30, y - i * 12, 24) for i in range(n))


def lanterna(t, x, y):
    a = 14 * onda(t, LOOP)
    return (f'<g transform="translate({x},{y}) rotate({a:.1f})"><line x1="0" y1="0" x2="0" y2="120" stroke="{OL}" stroke-width="5"/>'
            f'<rect x="-34" y="120" width="68" height="90" rx="10" fill="#ffcf6b" stroke="{OL}" stroke-width="6"/>'
            f'<circle cx="0" cy="165" r="90" fill="#ffcf6b" opacity="0.18"/></g>')


def barril(x, y, ang=0, s=1):
    c = (f'<rect x="-60" y="-80" width="120" height="160" rx="30" fill="#8a5a30" stroke="{OL}" stroke-width="6"/>'
         f'<line x1="-60" y1="-40" x2="60" y2="-40" stroke="{OL}" stroke-width="6"/><line x1="-60" y1="40" x2="60" y2="40" stroke="{OL}" stroke-width="6"/>')
    return f'<g transform="translate({x},{y}) rotate({ang:.1f}) scale({s})">{c}</g>'


def ninive(cor="#c9a46a", noite=False):
    s = ""
    s += f'<path d="M700 640 L760 560 L1160 560 L1220 640 Z M780 560 L830 470 L1090 470 L1140 560 Z M860 470 L900 390 L1020 390 L1060 470 Z" fill="{cor}" stroke="{OL}" stroke-width="6"/>'
    s += f'<rect x="0" y="600" width="1920" height="220" fill="{cor}" stroke="{OL}" stroke-width="6"/>'
    for x in range(0, 1920, 80):
        s += f'<rect x="{x + 10}" y="570" width="50" height="34" fill="{cor}" stroke="{OL}" stroke-width="5"/>'
    s += f'<path d="M860 820 V700 Q960 620 1060 700 V820 Z" fill="#2a1a12" stroke="{OL}" stroke-width="6"/>'
    for x in (300, 1600):
        s += f'<rect x="{x - 70}" y="520" width="140" height="300" fill="{cor}" stroke="{OL}" stroke-width="6"/>'
    if noite:
        for i in range(60):
            x = (i * 311) % 1880 + 20; y = 640 + (i * 53) % 160
            s += f'<rect x="{x}" y="{y}" width="12" height="16" fill="#ffd27a"/>'
    return s


def boi(x, y, s=1, saco=True, flip=False):
    c = (limb(-120, -40, -120, 70, 34, "#6a4a30") + limb(120, -40, 120, 70, 34, "#6a4a30") +
         f'<ellipse cx="0" cy="-90" rx="190" ry="110" fill="#8a6a4a" stroke="{OL}" stroke-width="6"/>'
         f'<ellipse cx="220" cy="-130" rx="80" ry="64" fill="#8a6a4a" stroke="{OL}" stroke-width="6"/>'
         f'<path d="M190 -185 q-30 -60 -70 -50 M250 -185 q30 -60 70 -50" fill="none" stroke="#e8e0c8" stroke-width="14" stroke-linecap="round"/>'
         f'<circle cx="245" cy="-140" r="9" fill="{OL}"/><ellipse cx="285" cy="-105" rx="22" ry="16" fill="#c98a6a"/>')
    if saco:
        c += f'<path d="M-170 -170 Q0 -230 170 -170 L180 -20 Q0 10 -180 -20 Z" fill="{SACO}" stroke="{OL}" stroke-width="6"/>'
        c += f'<path d="M-120 -150 l20 120 M-40 -170 l10 140 M60 -170 l-6 140 M130 -150 l-16 120" stroke="#6a5a3a" stroke-width="5"/>'
    return g(c, x, y, s, flip)


def ovelha_saco(x, y, s=1, flip=False):
    c = sheep(0, 0, 1) + f'<path d="M-100 -120 Q0 -150 100 -120 L105 -40 Q0 -20 -105 -40 Z" fill="{SACO}" stroke="{OL}" stroke-width="5"/>'
    return g(c, x, y, s, flip)


def sol_quente(t, x=1550, y=200, r=110):
    s = f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff0a0" stroke="#ffb030" stroke-width="10"/>'
    rot = 360 * t / LOOP / 3
    raios = "".join(f'<line x1="0" y1="{-r - 30}" x2="0" y2="{-r - 90}" stroke="#ffb030" stroke-width="12" stroke-linecap="round" transform="rotate({a})"/>' for a in range(0, 360, 30))
    return s + f'<g transform="translate({x},{y}) rotate({rot:.1f})">{raios}</g>'


def vento(t, y0=300, n=6):
    s = ""
    for i in range(n):
        x = ((i * 380) + 1920 * 2 * t / LOOP) % 2300 - 300
        y = y0 + i * 70
        s += f'<path d="M{x:.0f} {y} q120 -30 240 0 t240 0" fill="none" stroke="#fff3d0" stroke-width="8" stroke-linecap="round" opacity="0.7"/>'
    return s


def calor(t, x=960, y=500):
    s = ""
    for i in range(5):
        xx = x - 300 + i * 150
        b = 14 * onda(t, LOOP / 2, i * 0.2)
        s += f'<path d="M{xx} {y} q{b:.0f} -40 0 -80 q{-b:.0f} -40 0 -80" fill="none" stroke="#ffb070" stroke-width="6" opacity="0.5"/>'
    return s


def choca(x, y, s=1):
    c = (f'<path d="M-260 0 L-240 -360 M240 0 L220 -360 M-40 0 L-40 -380" stroke="#6b4226" stroke-width="22"/>'
         f'<path d="M-300 -330 Q0 -460 300 -330 L300 -300 Q0 -420 -300 -300 Z" fill="#8a6a3a" stroke="{OL}" stroke-width="6"/>')
    return g(c, x, y, s)


def calabacera(t, x, y, cresce=1.0, seca=False, s=1):
    verde, folha = ("#8a7a3a", "#a08a4a") if seca else ("#3f8a3a", "#58a84a")
    c = f'<path d="M0 0 Q-60 -200 40 -380 Q140 -520 -40 -620" fill="none" stroke="{verde}" stroke-width="18" stroke-linecap="round"/>'
    for i, (fx, fy, r) in enumerate([(-80, -260, 70), (90, -360, 80), (-120, -480, 90), (60, -560, 100), (-20, -650, 110), (200, -520, 80), (-240, -560, 80)]):
        if i / 7 > cresce:
            continue
        b = 0 if seca else 4 * onda(t, LOOP, i * 0.1)
        rr = r * (0.7 if seca else 1)
        c += f'<g transform="rotate({b:.1f} {fx} {fy})"><ellipse cx="{fx}" cy="{fy}" rx="{rr}" ry="{rr * 0.7}" fill="{folha}" stroke="{OL}" stroke-width="5"/></g>'
    if not seca and cresce >= 1:
        c += f'<ellipse cx="150" cy="-300" rx="40" ry="30" fill="#e8c24a" stroke="{OL}" stroke-width="5"/>'
    return g(c, x, y, s)


def verme(t, x, y, s=1):
    c = ""
    for i in range(7):
        yy = 14 * math.sin(TAU * (i / 6 - 2 * t / LOOP))
        c += f'<circle cx="{i * 26}" cy="{yy:.1f}" r="20" fill="#e88a9a" stroke="{OL}" stroke-width="4"/>'
    c += f'<circle cx="168" cy="{14 * math.sin(TAU * (1 - 2 * t / LOOP)) - 6:.1f}" r="5" fill="{OL}"/>'
    return g(c, x, y, s)


def luz_ceu(t, x=960, op=0.18):
    s = ""
    for i in range(13):
        a = -72 + i * 12 + 2 * onda(t, LOOP, i * 0.1)
        s += f'<path d="M{x} -40 L{x + math.tan(math.radians(a - 3)) * 1150:.0f} 1100 L{x + math.tan(math.radians(a + 3)) * 1150:.0f} 1100 Z" fill="#fffbe6" opacity="{op}"/>'
    return s


def particulas(t, n=30, cor="#fff3c0"):
    s = ""
    for i in range(n):
        x = (i * 173) % 1920
        y = 1080 - ((i * 97 + 1080 * t / LOOP) % 1180)
        s += f'<circle cx="{x + 15 * math.sin(TAU * (t / LOOP + i * 0.1)):.0f}" cy="{y:.0f}" r="{3 + i % 4}" fill="{cor}" opacity="0.7"/>'
    return s


def zzz(t, x, y):
    s = ""
    for i in range(3):
        f = ((t / LOOP) + i / 3) % 1
        s += f'<text x="{x + 60 * f + i * 10:.0f}" y="{y - 140 * f:.0f}" font-family="Lora" font-weight="700" font-size="{50 + 30 * f:.0f}" fill="#cfd8ff" opacity="{1 - f:.2f}">Z</text>'
    return s


def interior_peixe(t):
    s = '<rect width="1920" height="1080" fill="#2a0e10"/>'
    s += '<defs><radialGradient id="pi" cx="0.5" cy="0.55" r="0.6"><stop offset="0" stop-color="#7a2a2a"/><stop offset="1" stop-color="#1a0606"/></radialGradient></defs><rect width="1920" height="1080" fill="url(#pi)"/>'
    pulso = 1 + 0.015 * onda(t, LOOP)
    costelas = ""
    for i in range(7):
        x = 160 + i * 270
        costelas += f'<path d="M{x} -20 Q{x - 120} 540 {x} 1100" fill="none" stroke="#e8c8b0" stroke-width="34" opacity="0.55"/>'
    s += f'<g transform="translate(960,540) scale({pulso:.4f}) translate(-960,-540)">{costelas}</g>'
    s += '<path d="M0 900 Q480 840 960 900 T1920 880 V1080 H0 Z" fill="#4a1a1a"/>'
    return s


def frame_(inner):
    return frame(inner + luz_variante())


# ---------------- cenas ----------------
def j0(t):
    return frame_(interior_peixe(t) + algas(t, 560, 1000, 4, 220, "#2f6a3a") + algas(t, 1300, 1000, 5, 260, "#2f6a3a") +
                  pessoa(t, 960, 1000, 0.82, base=JONAS, eyes="up", mouth="sad", brows="sad", arms=("pray", "pray")) +
                  f'<path d="M880 260 q30 -40 10 -90 M950 245 q-20 -50 10 -100 M1020 260 q20 -40 -10 -90" stroke="#2f7a4a" stroke-width="14" fill="none" stroke-linecap="round"/>' +
                  particulas(t, 18, "#ffb0a0"))


def j0b(t):
    return frame_(ceu("#1a2030", "#3a4a60") + nuvens_tempestade(t) + mar_bravo(t, V(700, 640, 760)) + navio(t, V(960, 620, 1300, 800), V(700, 650, 760), V(0.9, 1.15, 0.7), V(7, 10, 5)) + chuva(t) + raio(t))


def j1a(t):
    return frame_(ceu("#1a1640", "#5a3a6a") + luz_ceu(t, 960, 0.2) + '<rect x="0" y="820" width="1920" height="260" fill="#5a4030"/>' +
                  pessoa(t, 960, 1000, 0.85, base=JONAS, eyes="up", mouth="sad", brows="normal", arms=("up", "up")) + particulas(t, 25))


def j1b(t):
    return frame_(ceu("#e08a4a", "#f5c890") + ninive() + "".join(
        g(soldier(tunic="#7a2a2a", eyes="side", mouth="smirk", brows="angry", spear=True), x, 1020, 0.42) for x in V((420, 640, 1280, 1500), (200, 1700), (520, 760, 1160, 1400), (900,))))


def j1c(t):
    return frame_(bg_house() + pessoa(t, 960, 1000, 0.88, base=JONAS, eyes="side", mouth="sad", brows="angry", arms=("face", "down"), balanco=1.5))


def j2a(t):
    s = bg_field(top="#f0b070", bot="#fbe0a8") + '<path d="M600 1080 Q900 800 1500 640" fill="none" stroke="#c9a070" stroke-width="140"/>'
    passo = 30 * onda(t, LOOP / 3)
    s += f'<g transform="translate(0,{abs(passo) * 0.3:.1f})">{pessoa(t, 1000, 960, 0.7, base=JONAS, eyes="side", mouth="sad", brows="angry", arms=("down", "down"), flip=True, balanco=3)}</g>'
    s += bag(870, 730, 0.7)
    return frame_(s)


def j2b(t):
    s = ceu("#7ec8f0", "#d8f0ff") + mar_calmo(t, 720) + navio(t, 1350, 720, 0.75, 2)
    s += '<rect x="0" y="760" width="900" height="320" fill="#8a6a4a" stroke="#2a1a12" stroke-width="6"/>'
    s += pessoa(t, 380, 1000, 0.7, base=JONAS, eyes="side", mouth="smile", brows="normal", arms=("down", "forward"))
    s += pessoa(t, 720, 1000, 0.7, base=MARINHEIRO[0], eyes="open", mouth="smile", arms=("forward", "down"), flip=True)
    s += moedas(510, 600 - 10 * onda(t, LOOP / 2), 3)
    return frame_(s)


def j2c(t):
    return frame_(ceu("#ff8a3d", "#ffd27a") + '<circle cx="1500" cy="560" r="130" fill="#fff1b8"/>' + mar_calmo(t, 680) + navio(t, V(760, 1100, 460, 940), 690, V(0.65, 0.8, 0.5, 1.0), 2) + particulas(t, 12, "#fff"))


def j3a(t):
    return frame_(ceu("#141a26", "#2a3444") + nuvens_tempestade(t) + mar_bravo(t, 660) + navio(t, V(960, 700, 1250, 1000), V(680, 640, 720), V(1.0, 1.25, 0.8, 1.4), V(9, 12, 7)) + chuva(t, V(90, 120, 60)) + raio(t, V(1500, 400, 1100), V(0.9, 0.3, 2.0)))


def j3b(t):
    s = ceu("#141a26", "#2a3444") + nuvens_tempestade(t) + mar_bravo(t, 860)
    s += '<path d="M0 820 L1920 820 L1820 1080 L100 1080 Z" fill="#7a4a24" stroke="#2a1a12" stroke-width="6"/>'
    s += pessoa(t, 380, 980, 0.62, base=MARINHEIRO[1], eyes="up", mouth="shout", brows="sad", arms=("up", "up"), balanco=3)
    s += pessoa(t, 1450, 980, 0.62, base=MARINHEIRO[2], eyes="up", mouth="shout", brows="sad", arms=("pray", "pray"), flip=True, balanco=3)
    fx = (t / LOOP)
    s += barril(820 + 500 * fx, 640 - 300 * math.sin(math.pi * fx), 360 * fx, 0.8)
    s += pessoa(t, 900, 980, 0.62, base=MARINHEIRO[3], eyes="open", mouth="shout", brows="angry", arms=("up", "flex"), balanco=3)
    s += chuva(t, 80) + raio(t, 300, 2.2)
    return frame_(s)


def j3c(t):
    s = '<rect width="1920" height="1080" fill="#3a2414"/>'
    for x in range(0, 1920, 160):
        s += f'<rect x="{x}" y="0" width="150" height="1080" fill="#4a2e1a" stroke="#2a1a10" stroke-width="5"/>'
    s += lanterna(t, 1300, 0)
    s += '<rect x="300" y="760" width="1100" height="120" rx="20" fill="#8a6a4a" stroke="#2a1a12" stroke-width="6"/>'
    dorme, _ = person(**{**JONAS, "eyes": "closed", "mouth": "smile", "arms": ("down", "down")})
    bx = V(0, -250, 200, -120)
    s += f'<g transform="translate({1180 + bx},770) rotate(-90) scale({V(0.7, 0.8, 0.62, 0.75)})">{respirar(dorme, t, 0.02)}</g>'
    s += zzz(t, 560 + bx, 600)
    s += f'<g transform="rotate({2 * onda(t, LOOP):.2f} 960 540)"><rect x="-100" y="-100" width="2120" height="1280" fill="none"/></g>'
    return frame_(f'<g transform="rotate({1.5 * onda(t, LOOP):.2f} 960 540)">{s}</g>')


def j3d(t):
    s = '<rect width="1920" height="1080" fill="#3a2414"/>' + lanterna(t, 960, 0)
    for x in range(0, 1920, 160):
        s += f'<rect x="{x}" y="0" width="150" height="1080" fill="#4a2e1a" stroke="#2a1a10" stroke-width="5" opacity="0.6"/>'
    s += pessoa(t, 620, 1000, 0.82, base=JONAS, eyes="open", mouth="shout", brows="sad", arms=("down", "down"))
    s += pessoa(t, 1300, 1000, 0.85, base=dict(MARINHEIRO[0], beard_col="#7a7a7a", hair_col="#7a7a7a"), eyes="open", mouth="shout", brows="angry", arms=("point", "flex"), flip=True, balanco=2)
    return frame_(f'<g transform="rotate({1.2 * onda(t, LOOP):.2f} 960 540)">{s}</g>')


def j3e(t):
    s = ceu("#141a26", "#2a3444") + nuvens_tempestade(t)
    s += '<path d="M0 760 L1920 760 L1920 1080 L0 1080 Z" fill="#7a4a24" stroke="#2a1a12" stroke-width="6"/>'
    for i, (x, b) in enumerate([(260, MARINHEIRO[1]), (520, MARINHEIRO[2]), (1400, MARINHEIRO[3]), (1660, MARINHEIRO[0])]):
        s += pessoa(t, x, 1000, 0.55, base=b, eyes="side", mouth="sad", brows="angry", arms=("down", "point" if i < 2 else "down"), flip=i > 1, piscar=0.3 * i)
    s += pessoa(t, 960, 1000, 0.62, base=JONAS, eyes="open", mouth="sad", brows="sad", arms=("down", "down"))
    f = (t / LOOP)
    for k in range(3):
        y = 760 + min(1, f * 1.5) * 120
        s += f'<g transform="translate({880 + k * 70},{y:.0f}) rotate({360 * f + k * 40:.0f})"><rect x="-24" y="-18" width="48" height="36" rx="8" fill="#d8cbb0" stroke="{OL}" stroke-width="4"/><text x="0" y="10" font-size="26" text-anchor="middle" fill="{OL}">{"×" if k == 1 else "•"}</text></g>'
    return frame_(s + chuva(t, 50))


def j3f(t):
    s = ceu("#141a26", "#2a3444") + nuvens_tempestade(t) + raio(t, 1700, 2.0)
    s += '<path d="M0 760 L1920 760 L1920 1080 L0 1080 Z" fill="#7a4a24" stroke="#2a1a12" stroke-width="6"/>'
    s += pessoa(t, 960, 1000, 0.85, base=JONAS, eyes="open", mouth="sad", brows="sad", arms=("pray", "down"))
    for i, (x, b) in enumerate([(330, MARINHEIRO[1]), (1590, MARINHEIRO[2])]):
        s += pessoa(t, x, 1000, 0.7, base=b, eyes="open", mouth="shout", brows="sad", arms=("face", "face"), flip=i == 1, piscar=1.5)
    return frame_(s + chuva(t, 50))


def j4a(t):
    s = ceu("#141a26", "#2a3444") + nuvens_tempestade(t) + mar_bravo(t, 760)
    s += '<path d="M0 700 L1920 700 L1820 900 L100 900 Z" fill="#7a4a24" stroke="#2a1a12" stroke-width="6"/>'
    for i, x in enumerate((300, 560, 1360, 1620)):
        rema = 25 * onda(t, LOOP / 2, i * 0.1)
        s += f'<line x1="{x}" y1="700" x2="{x + 140 + rema:.0f}" y2="1000" stroke="#5a3418" stroke-width="18"/>'
        s += pessoa(t, x, 860, 0.5, base=MARINHEIRO[i], eyes="closed", mouth="shout", brows="angry", arms=("forward", "forward"), flip=i > 1, balanco=4)
    s += pessoa(t, 960, 860, 0.62, base=JONAS, eyes="open", mouth="sad", brows="sad", arms=("up", "down"))
    return frame_(s + chuva(t, 60))


def j4b(t):
    s = ceu("#141a26", "#2a3444") + nuvens_tempestade(t)
    f = t / LOOP
    y = 200 + 700 * f
    caindo, _ = person(**{**JONAS, "eyes": "closed", "mouth": "shout", "brows": "sad", "arms": ("up", "up")})
    s += f'<g transform="translate({V(980, 900, 1060)},{y:.0f}) rotate({V(180, -160, 220) * f:.0f}) scale({V(0.45, 0.55, 0.4)})">{caindo}</g>'
    s += mar_bravo(t, 760)
    if f > 0.75:
        k = (f - 0.75) / 0.25
        for a in range(-60, 61, 20):
            s += f'<line x1="980" y1="780" x2="{980 + math.sin(math.radians(a)) * 260 * k:.0f}" y2="{780 - math.cos(math.radians(a)) * 220 * k:.0f}" stroke="#e8f6ff" stroke-width="16" stroke-linecap="round"/>'
    return frame_(s + chuva(t, 60))


def j4c(t):
    s = ceu("#8ac8f0", "#e8f6ff") + luz_ceu(t, 960, 0.12) + mar_calmo(t, 720) + navio(t, V(960, 1250, 700), 720, V(0.85, 1.1, 0.7), 1.5)
    s += f'<path d="M940 420 q{20 * onda(t, LOOP):.0f} -80 0 -160 q{-20 * onda(t, LOOP):.0f} -80 0 -160" fill="none" stroke="#e8e8e8" stroke-width="20" opacity="0.6"/>'
    return frame_(s + particulas(t, 15, "#fff"))


def j5a(t):
    s = ceu("#0a2a4a", "#04101e") + luz_ceu(t, 700, 0.06)
    s += pessoa(t, 620, 520 + 20 * onda(t, LOOP), 0.42, base=JONAS, eyes="closed", mouth="sad", brows="sad", arms=("up", "up"), balanco=8)
    s += bolhas(t, 640, 260) + algas(t, 120, 1080, 6, 400, "#1f5a3a") + algas(t, 1600, 1080, 6, 360, "#1f5a3a")
    s += peixe(t, V(1450, 1300, 1550) - 60 * onda(t, LOOP), V(640, 560, 720), V(0.9, 1.1, 0.8), boca=0.6 + 0.3 * onda(t, LOOP))
    return frame_(s)


def j5b(t):
    s = interior_peixe(t) + algas(t, 400, 1000, 5, 260, "#2f6a3a") + algas(t, 1400, 1000, 4, 200, "#2f6a3a")
    s += pessoa(t, 960, 1000, 0.82, base=JONAS, eyes="closed", mouth="sad", brows="sad", arms=("face", "face"))
    s += f'<path d="M880 260 q30 -40 10 -90 M950 245 q-20 -50 10 -100 M1020 260 q20 -40 -10 -90" stroke="#2f7a4a" stroke-width="14" fill="none" stroke-linecap="round"/>'
    return frame_(s)


def j5c(t):
    s = interior_peixe(t)
    for i in range(3):
        s += f'<g transform="translate({1350 + i * 90},300)"><circle r="34" fill="#f4f0d0" opacity="0.8"/><circle cx="14" cy="-8" r="30" fill="#2a0e10"/></g>'
    s += luz_ceu(t, 960, 0.08)
    s += pessoa(t, 900, 1000, 0.82, base=JONAS, eyes="up", mouth="sad", brows="sad", arms=("pray", "pray"))
    return frame_(s + particulas(t, 20, "#ffe0a0"))


def j5d(t):
    s = ceu("#7ec8f0", "#e8f6ff") + '<circle cx="1600" cy="180" r="90" fill="#fff4c0"/>' + mar_calmo(t, 640)
    s += '<path d="M0 760 Q600 700 1200 760 T1920 740 V1080 H0 Z" fill="#f0d8a0" stroke="#2a1a12" stroke-width="5"/>'
    s += peixe(t, V(1450, 1550, 1350), 640, V(0.6, 0.7, 0.55), boca=1.0)
    f = t / LOOP
    voa, _ = person(**{**JONAS, "eyes": "closed", "mouth": "shout", "brows": "sad", "arms": ("up", "up")})
    x = V(1180, 1280, 1100) - 520 * f; y = 600 - V(260, 340, 200) * math.sin(math.pi * f) + 200 * f
    s += f'<g transform="translate({x:.0f},{y:.0f}) rotate({-200 * f:.0f}) scale(0.4)">{voa}</g>'
    return frame_(s)


def j6a(t):
    s = ceu("#ffd8a0", "#fff4dc") + luz_ceu(t, 960, 0.22) + mar_calmo(t, 700)
    s += '<path d="M0 780 Q600 720 1200 780 T1920 760 V1080 H0 Z" fill="#f0d8a0" stroke="#2a1a12" stroke-width="5"/>'
    s += pessoa(t, 960, 1000, 0.82, base=JONAS, eyes="up", mouth="smile", brows="normal", arms=("pray", "pray"))
    return frame_(s + particulas(t, 25))


def j6b(t):
    s = ceu("#e8a060", "#fbe0a8") + ninive()
    passo = 6 * onda(t, LOOP / 3)
    s += pessoa(t, V(960, 600, 1300), 1020 + passo, 0.32, fixo=True, base=JONAS, eyes="side", arms=("down", "down"), balanco=3)
    s += '<rect x="0" y="1020" width="1920" height="60" fill="#c9a070"/>'
    return frame_(s)


def j6c(t):
    s = bg_city()
    for i, x in enumerate((180, 380, 1540, 1740)):
        s += pessoa(t, x, 1040, 0.5, hair="short", beard="yes", beard_col="#1a1410", tunic=["#2e5aa8", "#a0522d", "#7a3a5a", "#5a7a3a"][i], eyes="open", mouth="sad", brows="sad", flip=i > 1, piscar=i * 0.4)
    s += pessoa(t, 960, 1000, 0.85, base=JONAS, eyes="open", mouth="shout", brows="angry", arms=("up", "point"), balanco=2)
    return frame_(s)


def j6d(t):
    s = bg_city()
    for i, x in enumerate(range(140, 1900, 240)):
        s += pessoa(t, x, 1020 + (i % 2) * 30, 0.5, hair="short", beard="yes" if i % 2 else "none", beard_col="#1a1410", tunic=SACO, robe=None,
                    eyes="closed", mouth="sad", brows="sad", arms=("pray", "pray") if i % 2 else ("face", "face"), piscar=i * 0.3)
    return frame_(s + particulas(t, 12, "#bbb"))


def j6e(t):
    s = bg_palace() + f'<rect x="760" y="520" width="400" height="420" rx="20" fill="#c9a14a" stroke="{OL}" stroke-width="6"/>'
    f = t / LOOP
    s += pessoa(t, 960, 1000, 0.88, base=REI, eyes="open", mouth="sad", brows="sad", arms=("up", "down"))
    s += f'<path d="M{1180 + 200 * f:.0f} {560 + 240 * f:.0f} l140 -40 l40 200 l-150 30 Z" fill="#5a1a6a" stroke="{OL}" stroke-width="6" transform="rotate({40 * f:.0f} 1250 650)"/>'
    return frame_(s)


def j6f(t):
    s = bg_palace() + '<ellipse cx="960" cy="1000" rx="420" ry="70" fill="#8a8a8a" stroke="#2a1a12" stroke-width="5"/>'
    s += pessoa(t, 960, 1000, 0.82, base=dict(REI, robe=None, tunic=SACO), eyes="closed", mouth="sad", brows="sad", arms=("face", "face"))
    s += particulas(t, 25, "#9a9a9a")
    return frame_(s)


def j6g(t):
    s = bg_field(top="#d8c0a0", bot="#f0e0c8", sun=False)
    s += boi(V(560, 400, 760), 960 + 5 * onda(t, LOOP), V(0.9, 1.1, 0.8)) + boi(V(1460, 1600, 1300), 990, 0.75, flip=V(True, False))
    s += ovelha_saco(980, 1000 + 6 * onda(t, LOOP / 2), 0.9) + ovelha_saco(240, 1010, 0.7, True) + ovelha_saco(1760, 1010, 0.7)
    return frame_(s)


def j6h(t):
    s = ceu(V("#ffd8a0", "#ffc890", "#ffe0b0"), "#fff4dc") + luz_ceu(t, V(960, 600, 1300), 0.25) + g(ninive("#e0c080"), V(0, -200, 150), V(0, 60, -40), V(1, 1.15, 0.9))
    return frame_(s + particulas(t, 40))


def j7a(t):
    s = ceu("#c0502a", "#f08a4a") + '<rect x="0" y="820" width="1920" height="260" fill="#8a5a3a"/>'
    s += pessoa(t, 960, 1000, 0.9, base=JONAS, eyes="open", mouth="shout", brows="angry", arms=("up", "up"), balanco=2)
    for i in range(4):
        f = ((t / LOOP) + i / 4) % 1
        s += f'<path d="M{1100 + i * 30} {300 - 120 * f:.0f} q20 -30 0 -60" fill="none" stroke="#fff" stroke-width="8" opacity="{1 - f:.2f}"/>'
    return frame_(s)


def j7b(t):
    s = ceu("#e8a060", "#fbe0a8") + g(ninive(), 1300, 160, 0.5)
    s += '<rect x="0" y="820" width="1920" height="260" fill="#c9a070"/>'
    s += choca(560, 1000, 1.0) + pessoa(t, 560, 1000, 0.62, base=JONAS, eyes="side", mouth="sad", brows="angry", arms=("down", "down"))
    return frame_(s)


def j7c(t):
    s = ceu("#1a1640", "#3a3a7a") + '<circle cx="1600" cy="160" r="60" fill="#f4f0d0"/>'
    s += '<rect x="0" y="820" width="1920" height="260" fill="#8a7050"/>'
    s += choca(760, 1000, 1.0) + calabacera(t, 980, 1000, 1.0, s=1.0)
    s += pessoa(t, 760, 1000, 0.62, base=JONAS, eyes="up", mouth="smile", brows="normal", arms=("up", "down"))
    return frame_(s + particulas(t, 10, "#e8ffd0"))


def j7d(t):
    s = ceu("#ffb070", "#ffe0b0") + '<rect x="0" y="820" width="1920" height="260" fill="#c9a070"/>'
    s += choca(760, 1000, 1.0) + calabacera(t, 980, 1000, 1.0, seca=True)
    s += verme(t, V(900, 820, 960), V(880, 860, 900), V(1.6, 2.0, 1.4))
    return frame_(s)


def j7e(t):
    s = ceu("#ff9a3a", "#ffe08a") + sol_quente(t) + '<rect x="0" y="820" width="1920" height="260" fill="#d8a870"/>'
    s += choca(760, 1000, 1.0) + calabacera(t, 980, 1000, 1.0, seca=True)
    s += pessoa(t, 760, 1000, 0.62, base=JONAS, eyes="closed", mouth="sad", brows="sad", arms=("face", "down"), balanco=4)
    return frame_(s + vento(t) + calor(t, 760, 560))


def j8a(t):
    s = ceu("#141238", "#2a2a6a") + '<circle cx="300" cy="180" r="60" fill="#f4f0d0"/>' + ninive("#4a4070", noite=True)
    s += '<rect x="0" y="820" width="1920" height="260" fill="#2a2440"/>'
    s += pessoa(t, 360, 1040, 0.5, base=JONAS, eyes="side", mouth="sad", brows="sad", arms=("down", "down"))
    s += luz_ceu(t, 960, 0.06)
    return frame_(s)


def j8b(t):
    s = bg_city()
    for i, x in enumerate((300, 560, 820, 1100, 1360, 1620)):
        s += pessoa(t, x, 1040, 0.42, hair="curly", hair_col="#1a1410", tunic=["#c0392b", "#2e7a4a", "#2e5aa8", "#c9a14a", "#7a3a5a", "#a0522d"][i],
                    eyes="open", mouth="smile", arms=("up", "down") if i % 2 else ("down", "up"), piscar=i * 0.45, balanco=3)
    s += sheep(200, 1060, 0.4) + sheep(1780, 1060, 0.4, True)
    return frame_(s)


def j8c(t):
    s = bg_heaven() + luz_ceu(t, 960, 0.12)
    rolo = (f'<rect x="-420" y="-260" width="840" height="520" rx="10" fill="#f0e2c0" stroke="{OL}" stroke-width="8"/>'
            f'<rect x="-460" y="-290" width="60" height="580" rx="30" fill="#8a5a30" stroke="{OL}" stroke-width="6"/>'
            f'<rect x="400" y="-290" width="60" height="580" rx="30" fill="#8a5a30" stroke="{OL}" stroke-width="6"/>'
            f'<text x="0" y="-40" font-family="Lora" font-weight="700" font-size="80" fill="#5a3a1a" text-anchor="middle">Jonás 4:11</text>'
            f'<text x="0" y="80" font-family="Lora" font-style="italic" font-size="120" fill="#5a3a1a" text-anchor="middle">¿…?</text>')
    s += g(rolo, V(960, 900, 1020), 520 + 10 * onda(t, LOOP), V(1, 1.15, 0.9))
    return frame_(s + particulas(t, 30))


def j8d(t):
    s = ceu("#ffd8a0", "#fff4dc") + luz_ceu(t, 960, 0.2)
    s += f'<text x="{V(960, 640, 1280)}" y="{V(560, 520, 600)}" font-family="Lora" font-weight="700" font-size="{V(220, 300, 180) + 10 * onda(t, LOOP):.0f}" fill="#5a3a1a" text-anchor="middle" opacity="0.9">?</text>'
    return frame_(s + particulas(t, 35))


def j9(t):
    book = (f'<rect x="-250" y="-360" width="500" height="720" rx="14" fill="#5a1f1f" stroke="{OL}" stroke-width="8"/>'
            f'<rect x="-220" y="-330" width="440" height="660" rx="8" fill="none" stroke="#e0b23a" stroke-width="6"/>'
            f'<text x="0" y="-180" font-family="Lora" font-weight="700" font-size="72" fill="#f2d27a" text-anchor="middle">Héroes del</text>'
            f'<text x="0" y="-95" font-family="Lora" font-weight="700" font-size="72" fill="#f2d27a" text-anchor="middle">Pergamino</text>'
            f'<line x1="-140" y1="-50" x2="140" y2="-50" stroke="#e0b23a" stroke-width="4"/>'
            f'<text x="0" y="90" font-family="Lora" font-weight="700" font-size="170" fill="#fff3cf" text-anchor="middle">30</text>'
            f'<text x="0" y="160" font-family="Lora" font-size="50" fill="#f2d27a" text-anchor="middle">días</text>'
            f'<text x="0" y="250" font-family="Lora" font-style="italic" font-size="34" fill="#e8d6b0" text-anchor="middle">con los personajes que</text>'
            f'<text x="0" y="292" font-family="Lora" font-style="italic" font-size="34" fill="#e8d6b0" text-anchor="middle">cambiaron la historia de la fe</text>')
    s = bg_heaven() + f'<g transform="translate({V(620, 560, 680)},{500 + 12 * onda(t, LOOP):.0f}) rotate({V(-5, 4, -9) + 1.5 * onda(t, LOOP):.2f}) scale({V(0.95, 1.02, 0.9)})">{book}</g>'
    s += f'<text x="1350" y="420" font-family="Lora" font-weight="700" font-size="80" fill="#fff3cf" stroke="{OL}" stroke-width="3" text-anchor="middle">30 mañanas</text>'
    s += f'<text x="1350" y="510" font-family="Lora" font-weight="700" font-size="80" fill="#fff3cf" stroke="{OL}" stroke-width="3" text-anchor="middle">con los héroes</text>'
    pul = 1 + 0.04 * onda(t, LOOP / 2)
    s += f'<g transform="translate(1350,640) scale({pul:.3f})"><rect x="-300" y="-50" width="600" height="100" rx="50" fill="#e8435a" stroke="{OL}" stroke-width="6"/><text x="0" y="20" font-family="Inter Display" font-weight="800" font-size="48" fill="#fff" text-anchor="middle">LINK EN LA DESCRIPCIÓN</text></g>'
    return frame_(s + particulas(t, 25))


def scenes():
    return {k: v for k, v in globals().items() if callable(v) and (k.startswith("j") and k[1:2].isdigit())}


# foco do close (x, y) em coordenadas 1920x1080 — normalmente o rosto do personagem principal
FOCO = {
    "j0": (960, 330), "j0b": (960, 420), "j1a": (960, 300), "j1b": (960, 450), "j1c": (960, 270), "j2a": (1000, 380),
    "j2b": (500, 450), "j2c": (760, 450), "j3a": (960, 420), "j3b": (900, 450), "j3c": (700, 700), "j3d": (960, 360),
    "j3e": (960, 500), "j3f": (960, 300), "j4a": (960, 370), "j4b": (980, 500), "j4c": (960, 450), "j5a": (620, 300),
    "j5b": (960, 330), "j5c": (900, 330), "j5d": (1100, 500), "j6a": (960, 330), "j6b": (960, 600), "j6c": (960, 300),
    "j6d": (960, 650), "j6e": (960, 280), "j6f": (960, 320), "j6g": (700, 800), "j6h": (960, 450), "j7a": (960, 250),
    "j7b": (560, 500), "j7c": (800, 500), "j7d": (980, 700), "j7e": (760, 500), "j8a": (600, 600), "j8b": (960, 700),
    "j8c": (960, 520), "j8d": (960, 450), "j9": (900, 520),
}

THUMBS = "AB"


def thumb(variant="A"):
    s = ('<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">'
         '<defs><radialGradient id="L" cx="0.62" cy="0.5" r="0.65"><stop offset="0" stop-color="#c0503a"/><stop offset="0.6" stop-color="#4a1418"/><stop offset="1" stop-color="#0a0204"/></radialGradient>'
         '<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff7c9"/><stop offset="0.5" stop-color="#ffd84a"/><stop offset="1" stop-color="#ff9a12"/></linearGradient></defs>'
         '<rect width="1280" height="720" fill="url(#L)"/>')
    if variant == "A":
        for i in range(5):
            x = 620 + i * 170
            s += f'<path d="M{x} -20 Q{x - 80} 360 {x} 740" fill="none" stroke="#e8c8b0" stroke-width="30" opacity="0.45"/>'
        c, _ = person(**{**JONAS, "eyes": "open", "mouth": "shout", "brows": "sad", "arms": ("face", "face"), "tears": True})
        s += g(c, 920, 1120, 1.0)
        s += '<path d="M850 190 q30 -40 10 -90 M920 175 q-20 -50 10 -100 M990 190 q20 -40 -10 -90" stroke="#2f7a4a" stroke-width="14" fill="none" stroke-linecap="round"/>'
        t1, t2, etiqueta = "NO DEBÍ", "HUIR", "NADIE ME OYE…"
    else:
        s = s.replace('url(#L)"/>', 'url(#L)"/>' + mar_bravo(0.0, 470).replace("1100", "760"), 1)
        s += peixe(0.6, 1080, 430, 0.75, boca=1.0)
        c, _ = person(**{**JONAS, "eyes": "open", "mouth": "shout", "brows": "sad", "arms": ("up", "up")})
        s += g(c, 700, 660, 0.25)
        t1, t2, etiqueta = "¿SOBRE-", "VIVIÓ?", "EN LO OSCURO…"
    tg = '<g transform="rotate(-4 300 330)">'
    for y, tx in ((290, t1), (440, t2)):
        for sw, col in ((30, "#1a0a06"), (14, "#ffffff")):
            tg += f'<text x="50" y="{y}" font-family="Inter Display" font-weight="900" font-size="150" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round">{tx}</text>'
        tg += f'<text x="50" y="{y}" font-family="Inter Display" font-weight="900" font-size="150" fill="url(#gold)">{tx}</text>'
    tg += '</g>'
    s += tg
    s += f'<g transform="rotate(-4 200 560)"><rect x="60" y="505" width="450" height="86" rx="14" fill="#fff" stroke="#1a0a06" stroke-width="6"/><text x="285" y="566" font-family="Inter Display" font-weight="800" font-size="46" fill="#1a0a06" text-anchor="middle">{etiqueta}</text></g>'
    s += '<rect width="1280" height="720" fill="none" stroke="#000" stroke-opacity="0.55" stroke-width="30"/></svg>'
    return s
