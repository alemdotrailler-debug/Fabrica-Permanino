"""Kit de animação compartilhado por todos os vídeos: personagens com variantes, fala (boca), mar, navio,
clima, cidade antiga, animais, efeitos. As cenas de cada vídeo importam daqui: from fabrica.kit import *"""
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


def pessoa(t, x, y, s, flip=False, base=None, piscar=0.6, amp=0.012, balanco=0.0, fixo=False, nome=None, **kw):
    kw = {**(base or {}), **kw}
    if nome and VAR.get("fala") == nome:          # personagem falando: boca acompanha o áudio
        b = VAR.get("boca", 0.0)
        kw["mouth"] = "shout" if b > 0.35 else ("smirk" if b > 0.12 else "sad")
        balanco = max(balanco, 2.5)
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


def cidade_antiga(cor="#c9a46a", noite=False):
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



ninive = cidade_antiga
