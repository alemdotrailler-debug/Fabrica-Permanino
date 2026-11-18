from fabrica.desenho import *


def scenes():
    S = {}
    # c0 intro: young shepherd, goliath silhouette, crown -> dramatic triptych
    c0 = bg_heaven() + f'<g opacity="0.35">{g(goliath(), 1500, 980, 0.8)}</g>'
    c0 += P(960, 1000, 0.8, base=AD, crown=True, robe="#4a1a5a", eyes="open", mouth="sad", brows="sad", arms=("down", "down"))
    c0 += P(420, 1000, 0.7, base=YD, arms=("down", "sling"), mouth="smile")
    S["c0"] = frame(c0)
    # c1a: field with sheep
    c1a = bg_field() + "".join(sheep(x, y, 0.7, f) for x, y, f in [(1200, 900, False), (1450, 860, True), (1650, 950, False), (300, 940, True)])
    c1a += P(820, 1000, 0.75, base=YD, arms=("harp", "down"), mouth="smile") + harp(650, 760, 1.1)
    S["c1a"] = frame(c1a)
    # c1b: lion
    c1b = bg_field(dusk=True) + lion(700, 960, 0.9) + sheep(1600, 980, 0.6) + P(1180, 1010, 0.78, base=YD, arms=("forward", "up"), mouth="shout", brows="angry", flip=True)
    S["c1b"] = frame(c1b)
    # c1c: brothers in line + Samuel
    c1c = bg_house()
    for i, x in enumerate([260, 440, 620, 800, 980, 1160, 1340]):
        c1c += P(x, 1000, 0.62, hair="short", beard="yes", beard_col="#4a2a18", tunic=["#7a5a3a", "#5a6a3a", "#6a4a5a", "#7a3a2a", "#4a5a6a", "#8a6a3a", "#5a4a3a"][i], mouth="sad", brows="normal")
    c1c += P(1650, 1000, 0.8, hair="bald", hair_col="#e8e8e8", beard="yes", beard_col="#f0f0f0", tunic="#e8e0d0", robe="#6a5a8a", arms=("point", "down"), mouth="sad", flip=True)
    S["c1c"] = frame(c1c)
    # c1d: anointing
    c1d = bg_house() + P(820, 1000, 0.85, base=YD, eyes="up", mouth="smile", arms=("pray", "pray"))
    c1d += P(1260, 1000, 0.85, hair="bald", hair_col="#e8e8e8", beard="yes", beard_col="#f0f0f0", tunic="#e8e0d0", robe="#6a5a8a", arms=("up", "down"), mouth="smile", flip=True)
    c1d += horn_oil(860, 210, 1.3)
    c1d += '<ellipse cx="820" cy="300" rx="260" ry="60" fill="#fff3b0" opacity="0.35"/>'
    S["c1d"] = frame(c1d)
    # c2: palace harp for Saul
    c2 = bg_palace() + '<path d="M1180 240 q60 -80 140 -20 q80 -60 130 30 q70 20 20 90 q-60 60 -150 20 q-120 20 -150 -50 Z" fill="#3a2a4a" opacity="0.8"/>'
    c2 += f'<rect x="1150" y="560" width="400" height="360" rx="20" fill="#b8862a" stroke="{OL}" stroke-width="{SW}"/>'
    c2 += P(1350, 1000, 0.8, base=SAUL, eyes="closed", mouth="sad", brows="sad", arms=("face", "face"))
    c2 += P(620, 1000, 0.72, base=YD, arms=("harp", "down"), eyes="closed", mouth="smile") + harp(470, 760, 1.0)
    for (x, y) in [(760, 420), (860, 360), (960, 430)]:
        c2 += f'<text x="{x}" y="{y}" font-size="70" fill="#fff3cf" stroke="{OL}" stroke-width="3" font-family="DejaVu Sans">♪</text>'
    S["c2"] = frame(c2)
    # c3a: goliath vs hiding soldiers
    c3a = bg_valley() + g(goliath(), 1350, 1000, 0.85)
    for x in (200, 360, 520):
        c3a += g(soldier(tunic="#3a6a9a", eyes="side", mouth="sad", brows="sad", spear=True, arm_mode=("down", "down")).replace("#2e6fa8", "#3a6a9a"), x, 1010, 0.45)
    S["c3a"] = frame(c3a)
    # c3b: Saul armor too big
    c3b = bg_valley() + P(1300, 1000, 0.82, base=SAUL, arms=("point", "down"), mouth="smile", flip=True)
    c3b += P(650, 1000, 0.75, base=YD, tunic="#9aa0aa", arms=("down", "down"), mouth="sad", brows="sad")
    c3b += f'<path d="M560 210 Q650 120 740 210 L740 270 L560 270 Z" fill="#b08a3a" stroke="{OL}" stroke-width="{SW}" transform="rotate(-12 650 220)"/>'
    S["c3b"] = frame(c3b)
    # c3c: five stones, David facing Goliath
    c3c = bg_valley() + g(goliath(), 1450, 1000, 0.8) + P(560, 1000, 0.7, base=YD, arms=("forward", "sling"), mouth="smile", brows="angry")
    c3c += bag(470, 760, 0.9, stones=5)
    c3c += '<path d="M0 960 Q400 900 800 960" fill="none" stroke="#5aa0d8" stroke-width="30"/>'
    S["c3c"] = frame(c3c)
    # c3d: goliath fallen
    c3d = bg_valley() + f'<g transform="translate(1450,880) rotate(-88)">{g(goliath(fallen=True),0,0,0.75)}</g>'
    c3d += P(560, 1000, 0.75, base=YD, arms=("down", "up"), mouth="shout", brows="angry") + sword(680, 330, 10, 1.1)
    c3d += bag(470, 760, 0.9, stones=4)
    S["c3d"] = frame(c3d)
    # c4a: women with tambourines, jealous Saul
    c4a = bg_city()
    for i, x in enumerate([260, 560, 860]):
        d, _ = dalila(mouth="smile", eyes="closed", brows="normal", arm_mode=("down", "lift"), dress=["#c0392b", "#2e7a4a", "#2e5aa8"][i], dress2=["#e05a4a", "#4a9a6a", "#4a7ac8"][i], tamb=True)
        c4a += g(d, x, 1000, 0.62)
    c4a += P(1550, 1000, 0.8, base=SAUL, eyes="side", mouth="sad", brows="angry", arms=("down", "down"), flip=True)
    S["c4a"] = frame(c4a)
    # c4b: spear thrown
    c4b = bg_palace() + P(1450, 1000, 0.8, base=SAUL, eyes="open", mouth="shout", brows="angry", arms=("forward", "down"), flip=True)
    c4b += P(520, 1000, 0.72, base=YD, arms=("up", "harp"), mouth="shout", brows="sad") + harp(660, 560, 0.9)
    c4b += spear(1150, 470, 760, 420) + f'<path d="M1180 440 h120 M1190 500 h100" stroke="#fff" stroke-width="6" opacity="0.7"/>'
    S["c4b"] = frame(c4b)
    # c4c: window escape, Michal, statue in bed
    c4c = bg_house().replace('fill="#f7e2a8"', 'fill="#1d1640"')
    c4c += f'<rect x="1150" y="700" width="560" height="180" rx="20" fill="#a07a4a" stroke="{OL}" stroke-width="{SW}"/>'
    c4c += f'<path d="M1160 700 Q1430 620 1700 700 L1700 760 L1160 760 Z" fill="#c9b8a0" stroke="{OL}" stroke-width="{SW}"/>'
    c4c += f'<circle cx="1230" cy="660" r="60" fill="#8a8a8a" stroke="{OL}" stroke-width="{SW}"/><path d="M1180 620 q50 -60 110 0" fill="#3a2a20" stroke="{OL}" stroke-width="4"/>'
    d, _ = dalila(mouth="shh", eyes="side", brows="normal", arm_mode=("shh", "down"), dress="#2e5aa8", dress2="#4a7ac8")
    c4c += g(d, 700, 1000, 0.75)
    c4c += f'<g transform="translate(960,420) rotate(-15)">{P(0, 300, 0.4, base=YD, tunic="#2e5aa8", arms=("up", "up"), mouth="shout")}</g>'
    S["c4c"] = frame(c4c)
    # c4d: Jonathan arrows
    c4d = bg_field(dusk=True) + P(560, 1000, 0.78, hair="short", hair_col="#8a5a2a", beard="none", tunic="#7a1f2e", arms=("point", "flex"), mouth="sad", brows="sad")
    c4d += f'<path d="M700 300 Q760 470 700 640" fill="none" stroke="#8a5a30" stroke-width="12"/>'
    for x, y in [(1400, 760), (1500, 790), (1600, 770)]:
        c4d += f'<line x1="{x-80}" y1="{y-60}" x2="{x}" y2="{y}" stroke="{OL}" stroke-width="7"/><path d="M{x-90} {y-70} l-20 -6 l6 20 Z" fill="#c0392b"/>'
    c4d += P(1750, 1000, 0.45, base=AD, mouth="sad", brows="sad", flip=True)
    S["c4d"] = frame(c4d)
    # c5a: feigning madness
    c5a = bg_city() + P(800, 1000, 0.82, base=AD, tunic="#8a7a6a", eyes="side", mouth="shout", brows="sad", arms=("up", "flex"), drool=True)
    c5a += P(1500, 1000, 0.75, hair="short", beard="yes", beard_col="#2a1a10", tunic="#b23a2e", robe="#2e6fa8", crown=True, mouth="sad", brows="angry", arms=("point", "down"), flip=True)
    c5a += '<path d="M300 400 l80 80 M320 380 l90 90 M420 420 l40 120" stroke="#2a1a12" stroke-width="10"/>'
    S["c5a"] = frame(c5a)
    # c5b: cave of Adullam with men
    c5b = bg_cave() + '<ellipse cx="960" cy="900" rx="90" ry="30" fill="#ff8a30"/><path d="M910 900 q50 -150 100 0 Z" fill="#ffcf4a" stroke="#2a1a12" stroke-width="4"/>'
    for i, x in enumerate([450, 640, 1280, 1470]):
        c5b += P(x, 1000, 0.55, hair="short", beard="yes", beard_col="#3a2a20", tunic=["#5a4a3a", "#6a5a4a", "#4a3a2a", "#5a5a3a"][i], mouth="sad", brows="sad", flip=i > 1)
    c5b += P(960, 1000, 0.7, base=AD, tunic="#4a5a7a", mouth="smile", arms=("down", "flex"))
    S["c5b"] = frame(c5b)
    # c5c: cutting robe
    c5c = bg_cave() + P(1300, 1000, 0.8, base=SAUL, eyes="closed", mouth="sad", arms=("down", "down"), flip=True)
    c5c += P(700, 1000, 0.72, base=AD, tunic="#4a5a7a", arms=("down", "forward"), mouth="shh", eyes="side") + sword(1000, 640, 100, 0.6)
    c5c += f'<path d="M1010 760 l60 -20 l20 60 l-60 10 Z" fill="#4a1a5a" stroke="{OL}" stroke-width="4"/>'
    S["c5c"] = frame(c5c)
    # c6a: lament
    c6a = bg_field(top="#5a6a8a", bot="#a0a8c0", sun=False) + P(960, 1000, 0.82, base=AD, tunic="#4a5a7a", eyes="closed", mouth="sad", brows="sad", arms=("face", "face"), tears=True)
    c6a += f'<path d="M1500 620 h160 l-30 60 h-100 Z" fill="#9a958c" stroke="{OL}" stroke-width="5"/>' + sword(1580, 620, 0, 0.6)
    S["c6a"] = frame(c6a)
    # c6b: crowned in Jerusalem
    c6b = bg_city() + P(960, 1000, 0.85, base=AD, crown=True, robe="#7a1f2e", arms=("up", "down"), mouth="smile")
    for x in (300, 520, 1400, 1620):
        c6b += P(x, 1000, 0.5, hair="short", beard="yes", beard_col="#3a2a20", tunic="#6a7a4a", arms=("up", "down"), mouth="smile", flip=x > 960)
    S["c6b"] = frame(c6b)
    # c6c: dancing before ark, Michal at window
    c6c = bg_city() + ark(1300, 920, 1.0) + P(700, 1000, 0.8, base=AD, tunic="#f0ead8", arms=("dance", "up"), mouth="shout", brows="normal")
    c6c += f'<rect x="1640" y="250" width="200" height="200" fill="#1d1640" stroke="{OL}" stroke-width="6"/>'
    d, _ = dalila(mouth="sad", eyes="side", brows="angry", dress="#2e5aa8", dress2="#4a7ac8")
    c6c += f'<clipPath id="win"><rect x="1640" y="250" width="200" height="200"/></clipPath><g clip-path="url(#win)">{g(d, 1740, 1000, 0.6, flip=True)}</g>'
    S["c6c"] = frame(c6c)
    # c7a: rooftop at night
    c7a = bg_city(night=True) + f'<rect x="300" y="600" width="900" height="480" fill="#4a3a5a" stroke="{OL}" stroke-width="6"/>'
    c7a += P(700, 640, 0.6, base=AD, crown=True, robe="#7a1f2e", eyes="side", mouth="sad", arms=("down", "down"))
    c7a += f'<rect x="1500" y="520" width="260" height="240" fill="#3a3050" stroke="{OL}" stroke-width="5"/><rect x="1580" y="580" width="80" height="80" fill="#ffd27a"/>'
    S["c7a"] = frame(c7a)
    # c7b: Uriah with sealed letter
    c7b = bg_palace() + g(soldier(tunic="#3a6a9a", eyes="open", mouth="smile", brows="normal", spear=True, arm_mode=("down", "offer")), 1250, 1000, 0.8, flip=True)
    c7b += f'<g transform="translate(1010,520) rotate(-10)"><rect x="-70" y="-45" width="140" height="90" fill="#f0e2c0" stroke="{OL}" stroke-width="5"/><circle cx="0" cy="0" r="20" fill="#b23a2e" stroke="{OL}" stroke-width="4"/></g>'
    c7b += P(560, 1000, 0.8, base=AD, crown=True, robe="#7a1f2e", eyes="side", mouth="sad", brows="sad")
    S["c7b"] = frame(c7b)
    # c7c: Nathan pointing
    c7c = bg_palace() + f'<rect x="300" y="560" width="420" height="360" rx="20" fill="#b8862a" stroke="{OL}" stroke-width="{SW}"/>'
    c7c += P(510, 1000, 0.82, base=AD, crown=True, robe="#7a1f2e", eyes="open", mouth="shout", brows="sad", arms=("down", "down"))
    c7c += P(1350, 1000, 0.82, hair="short", hair_col="#d0d0d0", beard="yes", beard_col="#e0e0e0", tunic="#6a5a3a", robe="#3a4a3a", arms=("down", "point"), mouth="sad", brows="angry", flip=True)
    c7c += sheep(960, 1000, 0.5)
    S["c7c"] = frame(c7c)
    # c7d: repentance
    c7d = bg_heaven() + P(960, 1000, 0.85, base=AD, eyes="up", mouth="sad", brows="sad", arms=("pray", "pray"), tears=True, tunic="#6a5a4a")
    c7d += f'<g transform="translate(1250,700) rotate(25)"><circle r="45" fill="#f2c84b" stroke="{OL}" stroke-width="5" transform="scale(1.5,0.5)"/></g>'
    S["c7d"] = frame(c7d)
    # c8a: Absalom at gate with long hair
    c8a = bg_city() + P(960, 1000, 0.85, hair="long", hair_col="#2a1a10", beard="none", tunic="#c0392b", robe="#e8c27a", arms=("up", "down"), mouth="smile", brows="sly")
    for x in (400, 600, 1350, 1550):
        c8a += P(x, 1000, 0.5, hair="short", beard="yes", beard_col="#3a2a20", tunic="#6a7a4a", mouth="smile", flip=x > 960)
    S["c8a"] = frame(c8a)
    # c8b: fleeing barefoot up Mount of Olives
    c8b = bg_field(top="#7a6a8a", bot="#c0a8a0", sun=False)
    c8b += '<path d="M0 1080 L1920 400 V1080 Z" fill="#7a8a4a" stroke="#2a1a12" stroke-width="6"/>'
    for x in (1500, 1750):
        c8b += tree(x, 640 - (x - 1500) * 0.2, 0.5)
    c8b += f'<g transform="translate(900,800)">{P(0,0,0.8, base=AD, hood="#4a4a5a", eyes="closed", mouth="sad", brows="sad", bare_feet=True, tears=True, arms=("face","down"))}</g>'
    S["c8b"] = frame(c8b)
    # c8c: Absalom hanging in oak
    c8c = bg_forest() + tree(1000, 1000, 1.25)
    c8c += P(1250, 790, 0.6, hair="long", hair_col="#2a1a10", tunic="#c0392b", eyes="open", mouth="shout", brows="sad", arms=("up", "up"))
    c8c += f'<path d="M1215 250 q15 -40 0 -90 M1250 245 q-10 -40 5 -95 M1285 250 q-15 -40 0 -90" stroke="#2a1a10" stroke-width="22" fill="none" stroke-linecap="round"/>'
    c8c += mule(1550, 1000, 0.8)
    S["c8c"] = frame(c8c)
    # c8d: weeping over gate
    c8d = bg_city(night=True) + f'<rect x="660" y="420" width="600" height="660" fill="#5a4a3a" stroke="{OL}" stroke-width="6"/><path d="M800 1080 V800 Q960 680 1120 800 V1080 Z" fill="#1c1612" stroke="{OL}" stroke-width="6"/>'
    c8d += P(960, 430, 0.42, base=AD, crown=True, robe="#7a1f2e", eyes="closed", mouth="sad", brows="sad", arms=("face", "face"), tears=True)
    S["c8d"] = frame(c8d)
    # c9a: old king
    c9a = bg_heaven() + P(960, 1000, 0.88, base=dict(AD, hair_col="#d8d8d8", beard_col="#e8e8e8"), crown=True, robe="#7a1f2e", eyes="up", mouth="smile", arms=("down", "down"))
    S["c9a"] = frame(c9a)
    # c9b: praying
    c9b = bg_heaven() + P(960, 1000, 0.85, base=dict(AD, hair_col="#d8d8d8", beard_col="#e8e8e8"), robe="#7a1f2e", eyes="closed", mouth="smile", arms=("pray", "pray"))
    S["c9b"] = frame(c9b)
    # c9c: four stones in hand
    c9c = bg_heaven() + bag(960, 760, 3.2, stones=4) + '<ellipse cx="960" cy="520" rx="380" ry="90" fill="#fff6d8" opacity="0.35"/>'
    S["c9c"] = frame(c9c)
    # c10: ebook
    book = (f'<rect x="-250" y="-360" width="500" height="720" rx="14" fill="#5a1f1f" stroke="{OL}" stroke-width="8"/>'
            f'<rect x="-220" y="-330" width="440" height="660" rx="8" fill="none" stroke="#e0b23a" stroke-width="6"/>'
            f'<text x="0" y="-180" font-family="Lora" font-weight="700" font-size="72" fill="#f2d27a" text-anchor="middle">Héroes del</text>'
            f'<text x="0" y="-95" font-family="Lora" font-weight="700" font-size="72" fill="#f2d27a" text-anchor="middle">Pergamino</text>'
            f'<line x1="-140" y1="-50" x2="140" y2="-50" stroke="#e0b23a" stroke-width="4"/>'
            f'<text x="0" y="90" font-family="Lora" font-weight="700" font-size="170" fill="#fff3cf" text-anchor="middle">30</text>'
            f'<text x="0" y="160" font-family="Lora" font-size="50" fill="#f2d27a" text-anchor="middle">días</text>'
            f'<text x="0" y="250" font-family="Lora" font-style="italic" font-size="34" fill="#e8d6b0" text-anchor="middle">con los personajes que</text>'
            f'<text x="0" y="292" font-family="Lora" font-style="italic" font-size="34" fill="#e8d6b0" text-anchor="middle">cambiaron la historia de la fe</text>')
    c10 = bg_heaven() + f'<g transform="translate(620,500) rotate(-5) scale(0.95)">{book}</g>'
    c10 += f'<text x="1350" y="420" font-family="Lora" font-weight="700" font-size="80" fill="#fff3cf" stroke="{OL}" stroke-width="3" text-anchor="middle">30 mañanas</text>'
    c10 += f'<text x="1350" y="510" font-family="Lora" font-weight="700" font-size="80" fill="#fff3cf" stroke="{OL}" stroke-width="3" text-anchor="middle">con los héroes</text>'
    c10 += f'<rect x="1050" y="590" width="600" height="100" rx="50" fill="#e8435a" stroke="{OL}" stroke-width="6"/><text x="1350" y="660" font-family="Inter Display" font-weight="800" font-size="48" fill="#fff" text-anchor="middle">LINK EN LA DESCRIPCIÓN</text>'
    S["c10"] = frame(c10)
    return S



def thumb(variant="A"):
    s = ('<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">'
         '<defs><radialGradient id="L" cx="0.62" cy="0.45" r="0.6"><stop offset="0" stop-color="#ffd27a"/><stop offset="0.5" stop-color="#c0602a"/><stop offset="1" stop-color="#1a0a06"/></radialGradient>'
         '<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff7c9"/><stop offset="0.5" stop-color="#ffd84a"/><stop offset="1" stop-color="#ff9a12"/></linearGradient></defs>'
         '<rect width="1280" height="720" fill="url(#L)"/>')
    if variant == "A":
        s += f'<g opacity="0.45" filter="">{g(goliath(), 1080, 760, 0.62)}</g>'
        c, _ = person(**{**AD, "crown": True, "robe": "#7a1f2e", "eyes": "closed", "mouth": "sad", "brows": "sad", "arms": ("face", "down"), "tears": True})
        s += g(c, 900, 1120, 1.05)
        txt1, txt2, label = "SU PEOR", "ERROR", "NIVEL 7…"
    else:
        c1, _ = person(**{**YD, "arms": ("down", "sling"), "mouth": "smile"})
        c2, _ = person(**{**dict(AD, hair_col="#d8d8d8", beard_col="#e8e8e8"), "crown": True, "robe": "#7a1f2e", "eyes": "closed", "mouth": "sad", "brows": "sad", "tears": True})
        s += g(c1, 700, 760, 0.62) + g(c2, 1060, 1000, 0.85)
        s += '<path d="M880 0 L840 720" stroke="#1a0a06" stroke-width="10"/>'
        txt1, txt2, label = "PASTOR", "→ REY", "Y LUEGO…"
    tg = '<g transform="rotate(-4 300 330)">'
    for y, t in ((300, txt1), (450, txt2)):
        for sw, col in ((30, "#1a0a06"), (14, "#ffffff")):
            tg += f'<text x="60" y="{y}" font-family="Inter Display" font-weight="900" font-size="150" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round">{t}</text>'
        tg += f'<text x="60" y="{y}" font-family="Inter Display" font-weight="900" font-size="150" fill="url(#gold)">{t}</text>'
    tg += '</g>'
    s += tg
    s += f'<g transform="rotate(-4 200 560)"><rect x="70" y="510" width="330" height="86" rx="14" fill="#fff" stroke="#1a0a06" stroke-width="6"/><text x="235" y="571" font-family="Inter Display" font-weight="800" font-size="48" fill="#1a0a06" text-anchor="middle">{label}</text></g>'
    s += '<rect width="1280" height="720" fill="none" stroke="#000" stroke-opacity="0.55" stroke-width="30"/></svg>'
    return s

