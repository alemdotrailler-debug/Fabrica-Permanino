"""Cenas animadas do Jonás. Cada cena é uma função de t (0..LOOP) que devolve um SVG 1920x1080."""
from fabrica.kit import *

JONAS = dict(hair="short", hair_col="#3a2414", beard="yes", beard_col="#3a2414", tunic="#7a6a4a", robe="#35566e")

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
    s += pessoa(t, 1300, 1000, 0.85, base=dict(MARINHEIRO[0], beard_col="#7a7a7a", hair_col="#7a7a7a"), eyes="open", mouth="sad", brows="angry", arms=("point", "flex"), flip=True, balanco=2, nome="capitan")
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
    s += pessoa(t, 960, 1000, 0.85, base=JONAS, eyes="open", mouth="sad", brows="sad", arms=("pray", "down"), nome="jonas")
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
