"""Biblioteca de desenho cartoon (SVG): personagens, objetos e cenários."""
import math, os

OL = "#2a1a12"
SW = 5
SKIN = "#e3a571"
SKIN_D = "#c98a55"
HAIR = "#2b1a10"
W, H = 1080, 1920


def g(content, x, y, s=1, flip=False):
    sx = -s if flip else s
    return f'<g transform="translate({x},{y}) scale({sx},{s})">{content}</g>'


def limb(x1, y1, x2, y2, w, color):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{OL}" stroke-width="{w+2*SW}" stroke-linecap="round"/>'
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>')


def arm(sx, sy, ang, length=230, w=58, sleeve=None, chain=False, bent=0):
    # ang in degrees, 0 = straight down, positive = towards outside (handled by caller via sign)
    a = math.radians(ang)
    ex, ey = sx + math.sin(a) * length * 0.5, sy + math.cos(a) * length * 0.5
    b = math.radians(ang + bent)
    hx, hy = ex + math.sin(b) * length * 0.5, ey + math.cos(b) * length * 0.5
    s = limb(sx, sy, ex, ey, w, SKIN) + limb(ex, ey, hx, hy, w - 6, SKIN)
    if sleeve:
        s += limb(sx, sy, sx + math.sin(a) * 60, sy + math.cos(a) * 60, w + 14, sleeve)
    s += f'<circle cx="{hx}" cy="{hy}" r="{w*0.62}" fill="{SKIN}" stroke="{OL}" stroke-width="{SW}"/>'
    if chain:
        s += f'<ellipse cx="{(ex+hx)/2*0.3+hx*0.7}" cy="{(ey+hy)/2*0.3+hy*0.7}" rx="{w*0.62}" ry="18" fill="#8a8f98" stroke="{OL}" stroke-width="{SW}"/>'
    return s, (hx, hy)


def face(eyes="open", mouth="smile", brows="normal", beard=True, cy=0, r=110, female=False, beard_col=None, tears=False, drool=False):
    s = f'<circle cx="0" cy="{cy}" r="{r}" fill="{SKIN}" stroke="{OL}" stroke-width="{SW}"/>'
    # ears
    s = (f'<ellipse cx="{-r+4}" cy="{cy+10}" rx="20" ry="30" fill="{SKIN}" stroke="{OL}" stroke-width="{SW}"/>'
         f'<ellipse cx="{r-4}" cy="{cy+10}" rx="20" ry="30" fill="{SKIN}" stroke="{OL}" stroke-width="{SW}"/>') + s
    ey = cy - 5
    for ex in (-40, 40):
        if eyes == "open":
            s += f'<ellipse cx="{ex}" cy="{ey}" rx="22" ry="28" fill="#fff" stroke="{OL}" stroke-width="4"/>'
            s += f'<circle cx="{ex+4}" cy="{ey+4}" r="13" fill="{OL}"/><circle cx="{ex+9}" cy="{ey-2}" r="5" fill="#fff"/>'
            if female:
                s += f'<path d="M{ex-24} {ey-22} l-12 -10 M{ex-14} {ey-28} l-6 -12" stroke="{OL}" stroke-width="4"/>'
        elif eyes == "closed":
            s += f'<path d="M{ex-22} {ey} Q{ex} {ey+18} {ex+22} {ey}" fill="none" stroke="{OL}" stroke-width="6" stroke-linecap="round"/>'
        elif eyes == "up":
            s += f'<ellipse cx="{ex}" cy="{ey}" rx="22" ry="28" fill="#fff" stroke="{OL}" stroke-width="4"/>'
            s += f'<circle cx="{ex}" cy="{ey-12}" r="13" fill="{OL}"/>'
        elif eyes == "side":
            s += f'<ellipse cx="{ex}" cy="{ey}" rx="22" ry="24" fill="#fff" stroke="{OL}" stroke-width="4"/>'
            s += f'<circle cx="{ex+12}" cy="{ey+2}" r="12" fill="{OL}"/>'
            s += f'<path d="M{ex-24} {ey-8} L{ex+24} {ey-14}" stroke="{OL}" stroke-width="7"/>'
    if eyes == "blind":
        s += f'<path d="M{-r+8} {ey-28} Q0 {ey-38} {r-8} {ey-28} L{r-6} {ey+24} Q0 {ey+14} {-r+6} {ey+24} Z" fill="#d8cbb0" stroke="{OL}" stroke-width="{SW}"/>'
    # brows
    if eyes != "blind":
        if brows == "normal":
            s += f'<path d="M-62 {ey-42} Q-40 {ey-54} -18 {ey-44} M18 {ey-44} Q40 {ey-54} 62 {ey-42}" fill="none" stroke="{OL}" stroke-width="9" stroke-linecap="round"/>'
        elif brows == "sad":
            s += f'<path d="M-62 {ey-36} L-18 {ey-52} M18 {ey-52} L62 {ey-36}" fill="none" stroke="{OL}" stroke-width="9" stroke-linecap="round"/>'
        elif brows == "angry":
            s += f'<path d="M-62 {ey-52} L-18 {ey-36} M18 {ey-36} L62 {ey-52}" fill="none" stroke="{OL}" stroke-width="10" stroke-linecap="round"/>'
        elif brows == "sly":
            s += f'<path d="M-62 {ey-40} L-18 {ey-46} M18 {ey-50} Q40 {ey-62} 62 {ey-48}" fill="none" stroke="{OL}" stroke-width="7" stroke-linecap="round"/>'
    # nose
    s += f'<path d="M0 {cy+8} Q-14 {cy+38} 4 {cy+42}" fill="none" stroke="{SKIN_D}" stroke-width="6" stroke-linecap="round"/>'
    my = cy + 62
    if beard:
        s += (f'<path d="M{-r+10} {cy+10} Q{-r+20} {cy+r+60} 0 {cy+r+70} Q{r-20} {cy+r+60} {r-10} {cy+10} '
              f'Q{r-30} {cy+60} 40 {my-8} Q0 {my-18} -40 {my-8} Q{-r+30} {cy+60} {-r+10} {cy+10} Z" fill="{beard_col or HAIR}" stroke="{OL}" stroke-width="{SW}"/>')
    lip = "#b5523b" if female else "#7a2f22"
    if mouth == "smile":
        s += f'<path d="M-28 {my} Q0 {my+26} 28 {my}" fill="{lip}" stroke="{OL}" stroke-width="5"/>'
    elif mouth == "smirk":
        s += f'<path d="M-24 {my+4} Q8 {my+16} 30 {my-8}" fill="none" stroke="{OL}" stroke-width="6" stroke-linecap="round"/>'
    elif mouth == "sad":
        s += f'<path d="M-24 {my+10} Q0 {my-8} 24 {my+10}" fill="none" stroke="{OL}" stroke-width="6" stroke-linecap="round"/>'
    elif mouth == "shout":
        s += f'<ellipse cx="0" cy="{my+8}" rx="26" ry="22" fill="#5a1a14" stroke="{OL}" stroke-width="5"/>'
    elif mouth == "shh":
        s += f'<ellipse cx="0" cy="{my+4}" rx="12" ry="10" fill="{lip}" stroke="{OL}" stroke-width="4"/>'
    if tears:
        s += f'<path d="M-44 {ey+26} q-10 30 0 44 q10 -14 0 -44 Z M44 {ey+26} q-10 30 0 44 q10 -14 0 -44 Z" fill="#7cc4ff" stroke="{OL}" stroke-width="3"/>'
    if drool:
        s += f'<path d="M10 {my+20} q6 40 -4 70" fill="none" stroke="#bfe6ff" stroke-width="8" stroke-linecap="round"/>'
    if female:
        s += f'<ellipse cx="-62" cy="{cy+34}" rx="18" ry="10" fill="#f08a7a" opacity="0.6"/><ellipse cx="62" cy="{cy+34}" rx="18" ry="10" fill="#f08a7a" opacity="0.6"/>'
    return s


def samson(hair="long", eyes="open", mouth="smile", brows="normal", arms=("down", "down"),
           chains=False, tunic="#8b5a2b"):
    s = ""
    hy = -830
    # long hair behind
    if hair in ("long", "medium"):
        L = 260 if hair == "long" else 120
        s += f'<path d="M-125 {hy-30} Q-150 {hy+L} -110 {hy+L+20} L110 {hy+L+20} Q150 {hy+L} 125 {hy-30} Z" fill="{HAIR}" stroke="{OL}" stroke-width="{SW}"/>'
        if hair == "long":
            for bx in (-150, -120, 120, 150):
                s += limb(bx, hy + 40, bx * 1.05, hy + 330, 26, "#3a2416")
    # legs
    s += limb(-55, -380, -60, -40, 66, SKIN) + limb(55, -380, 60, -40, 66, SKIN)
    s += f'<path d="M-105 -40 h90 v34 h-90 Z M15 -40 h90 v34 h-90 Z" fill="#6b4226" stroke="{OL}" stroke-width="{SW}"/>'
    # arms behind? draw arms after body
    # tunic
    s += f'<path d="M-160 -700 Q0 -740 160 -700 L150 -330 Q0 -300 -150 -330 Z" fill="{tunic}" stroke="{OL}" stroke-width="{SW}"/>'
    s += f'<path d="M-40 -715 L0 -640 L40 -715" fill="{SKIN}" stroke="{OL}" stroke-width="{SW}"/>'
    s += f'<rect x="-155" y="-520" width="310" height="36" rx="8" fill="#d9a52b" stroke="{OL}" stroke-width="{SW}"/>'
    hands = []
    for side, mode in zip((-1, 1), arms):
        ang = {"down": 12, "up": 160, "flex": 100, "push": 130, "forward": 70, "pray": 28}[mode]
        bent = {"down": 0, "up": 0, "flex": 70, "push": 20, "forward": 0, "pray": -55}[mode]
        a, hpos = arm(side * 150, -680, ang * side, bent=bent * side, chain=chains)
        s += a
        hands.append(hpos)
    # neck + head
    s += limb(0, -720, 0, -760, 70, SKIN)
    s += g(face(eyes, mouth, brows, beard=True, cy=0), 0, hy)
    # top hair
    if hair in ("long", "medium"):
        s += f'<path d="M-118 {hy-20} Q-110 {hy-140} 0 {hy-128} Q110 {hy-140} 118 {hy-20} Q90 {hy-80} 30 {hy-92} Q0 {hy-60} -40 {hy-92} Q-90 {hy-80} -118 {hy-20} Z" fill="{HAIR}" stroke="{OL}" stroke-width="{SW}"/>'
    else:
        s += f'<path d="M-108 {hy-30} Q0 {hy-130} 108 {hy-30} Q0 {hy-90} -108 {hy-30} Z" fill="#5a4030" opacity="0.8"/>'
    if chains:
        hx1, hy1 = hands[0]; hx2, hy2 = hands[1]
        n = 9
        for i in range(n + 1):
            t = i / n
            x = hx1 + (hx2 - hx1) * t
            y = hy1 + (hy2 - hy1) * t + math.sin(t * math.pi) * 80
            s += f'<ellipse cx="{x}" cy="{y}" rx="16" ry="10" fill="none" stroke="#8a8f98" stroke-width="7"/>'
    return s


def dalila(mouth="smirk", eyes="open", brows="sly", arm_mode=("down", "down"), hold=None, dress="#7b2d8b", dress2="#9b3fae", tamb=False):
    s = ""
    hy = -800
    s += f'<path d="M-115 {hy-20} Q-170 {hy+300} -120 {hy+380} L120 {hy+380} Q170 {hy+300} 115 {hy-20} Z" fill="#14100c" stroke="{OL}" stroke-width="{SW}"/>'
    # dress
    s += f'<path d="M-120 -690 Q0 -720 120 -690 L190 0 Q0 30 -190 0 Z" fill="{dress}" stroke="{OL}" stroke-width="{SW}"/>'
    s += f'<path d="M-120 -690 Q0 -720 120 -690 L95 -560 Q0 -530 -95 -560 Z" fill="{dress2}" stroke="{OL}" stroke-width="{SW}"/>'
    s += f'<rect x="-110" y="-520" width="220" height="30" rx="8" fill="#e0b23a" stroke="{OL}" stroke-width="{SW}"/>'
    s += f'<path d="M-60 -700 Q0 -640 60 -700" fill="none" stroke="#f2c84b" stroke-width="12"/>'
    for i, cx in enumerate((-40, -20, 0, 20, 40)):
        s += f'<circle cx="{cx}" cy="{-668 + abs(cx)*-0.4 + 10}" r="9" fill="#f2c84b" stroke="{OL}" stroke-width="3"/>'
    hands = []
    for side, mode in zip((-1, 1), arm_mode):
        ang = {"down": 18, "shh": 165, "hold": 60, "hip": 40, "lift": 120}[mode]
        bent = {"down": 0, "shh": 150, "hold": -30, "hip": -120, "lift": 20}[mode]
        a, hp = arm(side * 115, -670, ang * side, length=200, w=44, bent=bent * side)
        s += a
        if tamb and side == 1:
            s += f'<circle cx="{hp[0]}" cy="{hp[1]-40}" r="55" fill="#e8c27a" stroke="{OL}" stroke-width="{SW}"/><circle cx="{hp[0]}" cy="{hp[1]-40}" r="38" fill="#f5deaa"/>'
            for k in range(6):
                aa=k*math.pi/3
                s += f'<circle cx="{hp[0]+math.cos(aa)*55}" cy="{hp[1]-40+math.sin(aa)*55}" r="9" fill="#f2c84b" stroke="{OL}" stroke-width="3"/>'

        hands.append(hp)
    s += limb(0, -700, 0, -740, 56, SKIN)
    s += g(face(eyes, mouth, brows, beard=False, cy=0, r=100, female=True), 0, hy)
    s += f'<path d="M-108 {hy-10} Q-100 {hy-130} 0 {hy-120} Q100 {hy-130} 108 {hy-10} Q70 {hy-90} 0 {hy-80} Q-70 {hy-90} -108 {hy-10} Z" fill="#14100c" stroke="{OL}" stroke-width="{SW}"/>'
    s += f'<path d="M-100 {hy-60} Q0 {hy-100} 100 {hy-60}" fill="none" stroke="#f2c84b" stroke-width="12"/>'
    s += f'<circle cx="0" cy="{hy-84}" r="14" fill="#2fb39a" stroke="{OL}" stroke-width="4"/>'
    s += f'<circle cx="-104" cy="{hy+40}" r="12" fill="#f2c84b" stroke="{OL}" stroke-width="3"/><circle cx="104" cy="{hy+40}" r="12" fill="#f2c84b" stroke="{OL}" stroke-width="3"/>'
    return s, hands


def soldier(tunic="#b23a2e", spear=True, mouth="smirk", brows="angry", eyes="side", arm_mode=("down", "down"), hold=None):
    s = ""
    hy = -760
    if spear:
        s += f'<line x1="200" y1="-1150" x2="200" y2="0" stroke="{OL}" stroke-width="22"/><line x1="200" y1="-1150" x2="200" y2="0" stroke="#8a5a30" stroke-width="12"/>'
        s += f'<path d="M200 -1250 L230 -1150 L170 -1150 Z" fill="#c9ccd2" stroke="{OL}" stroke-width="{SW}"/>'
    s += limb(-45, -340, -50, -30, 56, SKIN) + limb(45, -340, 50, -30, 56, SKIN)
    s += f'<path d="M-140 -650 Q0 -680 140 -650 L130 -300 L80 -270 L40 -300 L0 -270 L-40 -300 L-80 -270 L-130 -300 Z" fill="{tunic}" stroke="{OL}" stroke-width="{SW}"/>'
    s += f'<path d="M-100 -640 h200 v130 h-200 Z" fill="#c9a14a" stroke="{OL}" stroke-width="{SW}"/>'
    for yy in (-610, -575, -540):
        s += f'<line x1="-100" y1="{yy}" x2="100" y2="{yy}" stroke="{OL}" stroke-width="4"/>'
    for side, mode in zip((-1, 1), arm_mode):
        ang = {"down": 15, "spear": 40, "offer": 75, "cut": 95}[mode]
        bent = {"down": 0, "spear": -60, "offer": 0, "cut": 30}[mode]
        a, hp = arm(side * 135, -630, ang * side, length=200, w=48, bent=bent * side)
        s += a
        if hold == "bag" and side == 1:
            s += moneybag(hp[0] + 10, hp[1] + 60, 0.8)
        if hold == "scissors" and side == 1:
            s += scissors(hp[0] + 30, hp[1], 1.0)
    s += limb(0, -660, 0, -700, 60, SKIN)
    s += g(face(eyes, mouth, brows, beard=True, cy=0, r=95), 0, hy)
    # feather headdress
    for i in range(9):
        x = -90 + i * 22.5
        s += f'<path d="M{x-12} {hy-60} Q{x} {hy-230} {x+12} {hy-60} Z" fill="{["#e8e0c8","#d9c79a"][i%2]}" stroke="{OL}" stroke-width="4"/>'
    s += f'<rect x="-105" y="{hy-80}" width="210" height="34" rx="6" fill="#2e6fa8" stroke="{OL}" stroke-width="{SW}"/>'
    for i in range(5):
        s += f'<circle cx="{-80+i*40}" cy="{hy-63}" r="7" fill="#f2c84b"/>'
    return s


def moneybag(x, y, s=1):
    c = (f'<path d="M-70 0 Q-90 110 0 115 Q90 110 70 0 Q50 -40 25 -50 L35 -75 L-35 -75 L-25 -50 Q-50 -40 -70 0 Z" fill="#a9824a" stroke="{OL}" stroke-width="{SW}"/>'
         f'<path d="M-30 -52 Q0 -40 30 -52" stroke="{OL}" stroke-width="6" fill="none"/>'
         f'<text x="0" y="75" font-family="Lora" font-weight="700" font-size="70" text-anchor="middle" fill="#f2c84b" stroke="{OL}" stroke-width="3">$</text>')
    return g(c, x, y, s)


def coin(x, y, r=28):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*0.9}" fill="#d8d8de" stroke="{OL}" stroke-width="4"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{r*0.6}" ry="{r*0.55}" fill="none" stroke="#a5a7ae" stroke-width="4"/>')


def scissors(x, y, s=1):
    c = (f'<path d="M0 0 L120 -30 L118 -14 Z" fill="#cfd3da" stroke="{OL}" stroke-width="4"/>'
         f'<path d="M0 0 L120 30 L118 14 Z" fill="#cfd3da" stroke="{OL}" stroke-width="4"/>'
         f'<circle cx="-22" cy="-22" r="20" fill="none" stroke="#c0392b" stroke-width="10"/>'
         f'<circle cx="-22" cy="22" r="20" fill="none" stroke="#c0392b" stroke-width="10"/>')
    return g(c, x, y, s)


def lion(x, y, s=1, flip=False):
    c = (f'<ellipse cx="0" cy="-170" rx="230" ry="120" fill="#d99a3a" stroke="{OL}" stroke-width="{SW}"/>'
         + limb(-150, -120, -170, -10, 60, "#d99a3a") + limb(150, -120, 170, -10, 60, "#d99a3a")
         + f'<path d="M210 -200 Q330 -260 320 -380" fill="none" stroke="{OL}" stroke-width="22"/><path d="M210 -200 Q330 -260 320 -380" fill="none" stroke="#d99a3a" stroke-width="12"/>'
         + f'<circle cx="320" cy="-390" r="24" fill="#7a4a1a" stroke="{OL}" stroke-width="4"/>')
    mane = ""
    for i in range(14):
        a = i / 14 * 2 * math.pi
        mane += f'<circle cx="{-230 + math.cos(a)*115}" cy="{-300 + math.sin(a)*115}" r="62" fill="#8a4d1a" stroke="{OL}" stroke-width="{SW}"/>'
    head = (f'<circle cx="-230" cy="-300" r="110" fill="#e0a64a" stroke="{OL}" stroke-width="{SW}"/>'
            f'<ellipse cx="-265" cy="-330" rx="14" ry="20" fill="{OL}"/><ellipse cx="-195" cy="-330" rx="14" ry="20" fill="{OL}"/>'
            f'<path d="M-290 -360 L-245 -345 M-170 -360 L-215 -345" stroke="{OL}" stroke-width="9"/>'
            f'<path d="M-250 -290 h40 l-20 22 Z" fill="#4a2a14"/>'
            f'<path d="M-290 -250 Q-230 -170 -170 -250 Z" fill="#6a1a14" stroke="{OL}" stroke-width="{SW}"/>'
            f'<path d="M-275 -246 l10 26 l10 -24 M-205 -246 l10 24 l10 -26" fill="#fff" stroke="{OL}" stroke-width="3"/>')
    return g(c + mane + head, x, y, s, flip)


def column(x, y, w=150, h=1100, crack=False, tilt=0):
    c = f'<rect x="{-w/2}" y="{-h}" width="{w}" height="{h}" fill="#d9c49a" stroke="{OL}" stroke-width="{SW}"/>'
    for i in range(1, 4):
        xx = -w / 2 + i * w / 4
        c += f'<line x1="{xx}" y1="{-h+40}" x2="{xx}" y2="-40" stroke="#b39a6e" stroke-width="6"/>'
    c += f'<rect x="{-w/2-30}" y="{-h-50}" width="{w+60}" height="60" fill="#c9b07e" stroke="{OL}" stroke-width="{SW}"/>'
    c += f'<rect x="{-w/2-30}" y="-50" width="{w+60}" height="50" fill="#c9b07e" stroke="{OL}" stroke-width="{SW}"/>'
    if crack:
        c += f'<path d="M-20 {-h+120} l40 80 l-50 70 l45 90 l-30 60 l40 110" fill="none" stroke="{OL}" stroke-width="8"/>'
        c += f'<path d="M30 {-h/2} l-40 60 l30 70" fill="none" stroke="{OL}" stroke-width="7"/>'
    return f'<g transform="translate({x},{y}) rotate({tilt})">{c}</g>'


def hearts(x, y, n=3):
    s = ""
    for i in range(n):
        hx, hy, sc = x + i * 70 - 60, y - i * 90, 1 - i * 0.15
        s += g(f'<path d="M0 30 C-60 -10 -40 -60 0 -30 C40 -60 60 -10 0 30 Z" fill="#e8435a" stroke="{OL}" stroke-width="5"/>', hx, hy, sc * 1.4)
    return s



# ---- personagens e cenários (vídeo horizontal 1920x1080) ----

W, H = 1920, 1080
HAIRB = "#3a2416"


def person(hair="short", hair_col=HAIR, beard="none", beard_col=None, tunic="#8b5a2b", robe=None,
           crown=False, hood=None, eyes="open", mouth="smile", brows="normal", arms=("down", "down"),
           tears=False, drool=False, height=1.0, bare_feet=False, hold=None, belt="#d9a52b"):
    s = ""
    hy = -830
    if hair == "long":
        s += f'<path d="M-120 {hy-30} Q-140 {hy+180} -105 {hy+200} L105 {hy+200} Q140 {hy+180} 120 {hy-30} Z" fill="{hair_col}" stroke="{OL}" stroke-width="{SW}"/>'
    if hood:
        s += f'<path d="M-150 {hy+40} Q-160 {hy-170} 0 {hy-175} Q160 {hy-170} 150 {hy+40} L170 {hy+230} L-170 {hy+230} Z" fill="{hood}" stroke="{OL}" stroke-width="{SW}"/>'
    s += limb(-55, -380, -60, -40, 66, SKIN) + limb(55, -380, 60, -40, 66, SKIN)
    if not bare_feet:
        s += f'<path d="M-105 -40 h90 v34 h-90 Z M15 -40 h90 v34 h-90 Z" fill="#6b4226" stroke="{OL}" stroke-width="{SW}"/>'
    else:
        s += f'<ellipse cx="-62" cy="-22" rx="46" ry="20" fill="{SKIN}" stroke="{OL}" stroke-width="{SW}"/><ellipse cx="62" cy="-22" rx="46" ry="20" fill="{SKIN}" stroke="{OL}" stroke-width="{SW}"/>'
    if robe:
        s += f'<path d="M-165 -700 Q0 -745 165 -700 L200 -30 Q0 0 -200 -30 Z" fill="{robe}" stroke="{OL}" stroke-width="{SW}"/>'
    s += f'<path d="M-150 -700 Q0 -740 150 -700 L145 -330 Q0 -300 -145 -330 Z" fill="{tunic}" stroke="{OL}" stroke-width="{SW}"/>'
    s += f'<path d="M-40 -715 L0 -640 L40 -715" fill="{SKIN}" stroke="{OL}" stroke-width="{SW}"/>'
    s += f'<rect x="-148" y="-520" width="296" height="34" rx="8" fill="{belt}" stroke="{OL}" stroke-width="{SW}"/>'
    hands = []
    for side, mode in zip((-1, 1), arms):
        ang = {"down": 12, "up": 160, "flex": 100, "push": 130, "forward": 70, "pray": 28, "face": 150, "dance": 145, "point": 95, "harp": 40, "sling": 175, "hold": 60}[mode]
        bent = {"down": 0, "up": 0, "flex": 70, "push": 20, "forward": 0, "pray": -55, "face": 160, "dance": -40, "point": 0, "harp": -70, "sling": 0, "hold": -40}[mode]
        a, hp = arm(side * 145, -680, ang * side, bent=bent * side)
        s += a
        hands.append(hp)
    s += limb(0, -720, 0, -760, 70, SKIN)
    s += g(face(eyes, mouth, brows, beard=(beard != "none"), cy=0, beard_col=beard_col, tears=tears, drool=drool), 0, hy)
    if hair in ("long", "short", "curly"):
        s += f'<path d="M-118 {hy-20} Q-110 {hy-140} 0 {hy-128} Q110 {hy-140} 118 {hy-20} Q90 {hy-80} 30 {hy-92} Q0 {hy-60} -40 {hy-92} Q-90 {hy-80} -118 {hy-20} Z" fill="{hair_col}" stroke="{OL}" stroke-width="{SW}"/>'
        if hair == "curly":
            for cx in (-90, -45, 0, 45, 90):
                s += f'<circle cx="{cx}" cy="{hy-100+abs(cx)*0.35}" r="34" fill="{hair_col}" stroke="{OL}" stroke-width="4"/>'
    if hair == "bald":
        s += f'<path d="M-112 {hy+10} Q-118 {hy-50} -95 {hy-60} M112 {hy+10} Q118 {hy-50} 95 {hy-60}" stroke="{hair_col}" stroke-width="22" fill="none"/>'
    if hood:
        s += f'<path d="M-130 {hy-20} Q-135 {hy-160} 0 {hy-165} Q135 {hy-160} 130 {hy-20} Q100 {hy-110} 0 {hy-112} Q-100 {hy-110} -130 {hy-20} Z" fill="{hood}" stroke="{OL}" stroke-width="{SW}"/>'
    if crown:
        s += f'<path d="M-95 {hy-95} L-95 {hy-175} L-55 {hy-130} L-20 {hy-190} L20 {hy-130} L55 {hy-190} L95 {hy-130} L95 {hy-95} Z" fill="#f2c84b" stroke="{OL}" stroke-width="{SW}"/>'
        s += f'<circle cx="0" cy="{hy-115}" r="12" fill="#c0392b" stroke="{OL}" stroke-width="3"/>'
    return s, hands


def sheep(x, y, s=1, flip=False):
    c = limb(-50, -40, -50, 40, 22, "#3a2a22") + limb(50, -40, 50, 40, 22, "#3a2a22")
    for i in range(9):
        a = i / 9 * 2 * math.pi
        c += f'<circle cx="{math.cos(a)*70}" cy="{-70+math.sin(a)*40}" r="42" fill="#f4f0e6" stroke="{OL}" stroke-width="4"/>'
    c += f'<ellipse cx="0" cy="-70" rx="80" ry="50" fill="#f4f0e6"/>'
    c += f'<ellipse cx="105" cy="-100" rx="34" ry="42" fill="#3a2a22" stroke="{OL}" stroke-width="4"/><circle cx="115" cy="-110" r="6" fill="#fff"/>'
    return g(c, x, y, s, flip)


def harp(x, y, s=1):
    c = (f'<path d="M0 0 L0 -160 Q60 -170 90 -110 Q100 -40 60 0 Z" fill="none" stroke="{OL}" stroke-width="16"/>'
         f'<path d="M0 0 L0 -160 Q60 -170 90 -110 Q100 -40 60 0 Z" fill="none" stroke="#c98a2b" stroke-width="9"/>')
    for i in range(1, 6):
        c += f'<line x1="{i*12}" y1="{-150+i*4}" x2="{i*11}" y2="-4" stroke="#f5e7b5" stroke-width="2"/>'
    return g(c, x, y, s)


def sling_stone(x, y):
    return f'<circle cx="{x}" cy="{y}" r="16" fill="#9a958c" stroke="{OL}" stroke-width="4"/>'


def bag(x, y, s=1, stones=0):
    c = f'<path d="M-50 -60 Q-70 40 0 45 Q70 40 50 -60 Z" fill="#8a5a30" stroke="{OL}" stroke-width="{SW}"/>'
    for i in range(stones):
        c += f'<circle cx="{-36+i*24}" cy="-66" r="14" fill="#9a958c" stroke="{OL}" stroke-width="3"/>'
    return g(c, x, y, s)


def horn_oil(x, y, s=1):
    c = (f'<path d="M0 0 Q60 -20 120 -90 L140 -70 Q80 10 10 30 Z" fill="#e8dcc0" stroke="{OL}" stroke-width="{SW}"/>'
         f'<path d="M5 15 q-10 40 -5 120" fill="none" stroke="#e6c34a" stroke-width="14" stroke-linecap="round" opacity="0.9"/>')
    return g(c, x, y, s)


def sword(x, y, ang=0, s=1):
    c = (f'<rect x="-10" y="-300" width="20" height="300" fill="#cfd3da" stroke="{OL}" stroke-width="4"/>'
         f'<path d="M-10 -300 L0 -340 L10 -300 Z" fill="#cfd3da" stroke="{OL}" stroke-width="4"/>'
         f'<rect x="-45" y="0" width="90" height="18" fill="#8a6a2a" stroke="{OL}" stroke-width="4"/><rect x="-10" y="18" width="20" height="60" fill="#5a3a1a" stroke="{OL}" stroke-width="4"/>')
    return f'<g transform="translate({x},{y}) rotate({ang}) scale({s})">{c}</g>'


def spear(x1, y1, x2, y2):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{OL}" stroke-width="20"/><line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#8a5a30" stroke-width="10"/>'
            f'<circle cx="{x2}" cy="{y2}" r="22" fill="#c9ccd2" stroke="{OL}" stroke-width="5"/>')


def goliath(fallen=False):
    s = ""
    s += limb(-70, -380, -80, -40, 80, SKIN) + limb(70, -380, 80, -40, 80, SKIN)
    s += f'<path d="M-130 -40 h110 v40 h-110 Z M20 -40 h110 v40 h-110 Z" fill="#6b4226" stroke="{OL}" stroke-width="{SW}"/>'
    s += f'<rect x="-120" y="-330" width="80" height="230" fill="#b07a3a" stroke="{OL}" stroke-width="{SW}"/><rect x="40" y="-330" width="80" height="230" fill="#b07a3a" stroke="{OL}" stroke-width="{SW}"/>'
    s += f'<path d="M-190 -720 Q0 -770 190 -720 L170 -320 Q0 -290 -170 -320 Z" fill="#b5803a" stroke="{OL}" stroke-width="{SW}"/>'
    for yy in range(-700, -330, 34):
        for xx in range(-160, 170, 40):
            s += f'<path d="M{xx} {yy} q20 22 40 0" fill="none" stroke="#7a5420" stroke-width="4"/>'
    a, hp = arm(-190, -690, -20, length=300, w=80)
    s += a
    s += spear(190, -1100, 190, 0) if not fallen else ""
    a2, hp2 = arm(190, -690, 30, length=300, w=80, bent=-60)
    s += a2
    s += g(face("open", "shout", "angry", beard=True, r=125), 0, -860)
    s += f'<path d="M-135 -870 Q-135 -1040 0 -1040 Q135 -1040 135 -870 L120 -880 Q0 -900 -120 -880 Z" fill="#c9a14a" stroke="{OL}" stroke-width="{SW}"/>'
    s += f'<path d="M0 -1040 L0 -1110" stroke="{OL}" stroke-width="14"/><path d="M-30 -1100 Q0 -1180 30 -1100" fill="#b23a2e" stroke="{OL}" stroke-width="4"/>'
    return s


def ark(x, y, s=1):
    c = (f'<rect x="-160" y="-120" width="320" height="120" fill="#e8b830" stroke="{OL}" stroke-width="{SW}"/>'
         f'<rect x="-170" y="-140" width="340" height="24" fill="#f2c84b" stroke="{OL}" stroke-width="{SW}"/>'
         f'<path d="M-150 -140 Q-120 -230 -40 -200 L-60 -140 Z M150 -140 Q120 -230 40 -200 L60 -140 Z" fill="#f2c84b" stroke="{OL}" stroke-width="{SW}"/>'
         f'<rect x="-260" y="-70" width="520" height="16" fill="#8a5a30" stroke="{OL}" stroke-width="4"/>')
    return g(c, x, y, s)


def tree(x, y, s=1):
    c = (f'<path d="M-40 0 L-30 -400 Q-200 -420 -260 -520 Q-200 -560 -120 -540 L-20 -460 L20 -460 L200 -560 Q260 -540 260 -500 Q200 -430 30 -400 L40 0 Z" fill="#6b4226" stroke="{OL}" stroke-width="{SW}"/>')
    for (cx, cy, r) in [(-200, -600, 130), (0, -680, 170), (200, -600, 130), (-90, -760, 120), (110, -770, 120)]:
        c += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#3f7a3a" stroke="{OL}" stroke-width="{SW}"/>'
    return g(c, x, y, s)


def mule(x, y, s=1, flip=False):
    c = limb(-90, -120, -100, 0, 34, "#7a6050") + limb(90, -120, 100, 0, 34, "#7a6050")
    c += f'<ellipse cx="0" cy="-170" rx="150" ry="80" fill="#8a7060" stroke="{OL}" stroke-width="{SW}"/>'
    c += f'<path d="M120 -200 L200 -320 L250 -290 L190 -170 Z" fill="#8a7060" stroke="{OL}" stroke-width="{SW}"/>'
    c += f'<path d="M205 -320 l-10 -70 l30 50 M230 -310 l10 -70 l10 60" fill="#8a7060" stroke="{OL}" stroke-width="5"/><circle cx="225" cy="-300" r="7" fill="{OL}"/>'
    return g(c, x, y, s, flip)


# ---------- backgrounds 1920x1080 ----------
def grad(id_, top, bot):
    return f'<defs><linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bot}"/></linearGradient></defs>'


def bg_field(top="#7ec8f0", bot="#d8f0ff", sun=True, dusk=False):
    if dusk:
        top, bot = "#ff8a3d", "#ffd27a"
    s = grad("sky", top, bot) + '<rect width="1920" height="1080" fill="url(#sky)"/>'
    if sun:
        s += f'<circle cx="1550" cy="200" r="90" fill="#fff4c0"/>'
    s += '<path d="M0 640 Q480 540 960 620 T1920 600 V1080 H0 Z" fill="#8fbf5a" stroke="#2a1a12" stroke-width="5"/>'
    s += '<path d="M0 780 Q600 700 1200 780 T1920 760 V1080 H0 Z" fill="#7aae48"/>'
    return s


def bg_house():
    s = grad("sky", "#e8b070", "#f5d9a8") + '<rect width="1920" height="1080" fill="url(#sky)"/>'
    s += '<rect x="0" y="0" width="1920" height="1080" fill="#d9b48a"/>'
    for x in range(0, 1920, 240):
        s += f'<line x1="{x}" y1="0" x2="{x}" y2="760" stroke="#c49a6c" stroke-width="6"/>'
    s += '<rect x="0" y="760" width="1920" height="320" fill="#8a6040"/><rect x="0" y="760" width="1920" height="14" fill="#2a1a12"/>'
    s += '<path d="M820 200 h280 v240 h-280 Z" fill="#f7e2a8" stroke="#2a1a12" stroke-width="8"/>'
    return s


def bg_palace(night=False):
    top, bot = ("#1d1640", "#4a2a6a") if night else ("#6a2c5a", "#c4685a")
    s = grad("sky", top, bot) + '<rect width="1920" height="1080" fill="url(#sky)"/>'
    for x in (300, 960, 1620):
        s += f'<path d="M{x-140} 720 V330 Q{x} 160 {x+140} 330 V720 Z" fill="#0f0c24" stroke="#2a1a12" stroke-width="8"/>'
    if night:
        s += '<circle cx="1000" cy="330" r="50" fill="#f4f0d0"/>'
    s += '<rect x="0" y="760" width="1920" height="320" fill="#5a3322"/><rect x="0" y="760" width="1920" height="16" fill="#2a1a12"/>'
    s += '<path d="M0 0 H200 Q140 400 220 760 H0 Z" fill="#8a1f2e" stroke="#2a1a12" stroke-width="6"/><path d="M1920 0 H1720 Q1780 400 1700 760 H1920 Z" fill="#8a1f2e" stroke="#2a1a12" stroke-width="6"/>'
    return s


def bg_valley():
    s = grad("sky", "#f0a860", "#fbe0a8") + '<rect width="1920" height="1080" fill="url(#sky)"/>'
    s += '<path d="M0 420 L300 300 L600 450 L900 330 L1200 460 L1500 320 L1920 430 V1080 H0 Z" fill="#c9905a" stroke="#2a1a12" stroke-width="5"/>'
    s += '<path d="M0 700 Q960 560 1920 700 V1080 H0 Z" fill="#d8b070" stroke="#2a1a12" stroke-width="5"/>'
    return s


def bg_cave():
    s = '<rect width="1920" height="1080" fill="#1c1612"/>'
    s += '<path d="M0 0 H1920 V1080 H0 Z M300 1080 Q260 300 960 180 Q1660 300 1620 1080 Z" fill="#3a2e24" fill-rule="evenodd" stroke="#2a1a12" stroke-width="8"/>'
    s += '<defs><radialGradient id="lg" cx="0.5" cy="0.6" r="0.5"><stop offset="0" stop-color="#ffb060" stop-opacity="0.35"/><stop offset="1" stop-color="#ffb060" stop-opacity="0"/></radialGradient></defs><rect width="1920" height="1080" fill="url(#lg)"/>'
    s += '<rect x="0" y="880" width="1920" height="200" fill="#2a221b"/>'
    return s


def bg_city(night=False):
    top, bot = ("#1d1a40", "#3a3a7a") if night else ("#79b8e8", "#d8ecf8")
    s = grad("sky", top, bot) + '<rect width="1920" height="1080" fill="url(#sky)"/>'
    if night:
        s += '<circle cx="1600" cy="160" r="70" fill="#f4f0d0"/>'
        for (x, y) in [(200, 120), (500, 200), (800, 90), (1200, 150), (1400, 260), (1800, 300)]:
            s += f'<circle cx="{x}" cy="{y}" r="5" fill="#fff"/>'
    col = "#3a3050" if night else "#d9c49a"
    for i, (x, w, h) in enumerate([(0, 300, 380), (280, 260, 300), (520, 340, 450), (840, 280, 330), (1100, 380, 420), (1460, 260, 300), (1700, 260, 360)]):
        s += f'<rect x="{x}" y="{760-h}" width="{w}" height="{h}" fill="{col}" stroke="#2a1a12" stroke-width="5"/>'
        for wx in range(x + 40, x + w - 40, 90):
            s += f'<rect x="{wx}" y="{760-h+60}" width="40" height="60" fill="{"#ffd27a" if night else "#6a4a2a"}" stroke="#2a1a12" stroke-width="4"/>'
    s += f'<rect x="0" y="760" width="1920" height="320" fill="{"#2a2440" if night else "#c9a070"}"/><rect x="0" y="760" width="1920" height="14" fill="#2a1a12"/>'
    return s


def bg_heaven():
    s = ('<defs><radialGradient id="h" cx="0.5" cy="0.1" r="0.9"><stop offset="0" stop-color="#fff6d8"/><stop offset="0.45" stop-color="#ffcf6b"/><stop offset="1" stop-color="#5a2a5a"/></radialGradient></defs>'
         '<rect width="1920" height="1080" fill="url(#h)"/>')
    for i in range(13):
        a = -72 + i * 12
        s += f'<path d="M960 60 L{960+math.tan(math.radians(a-3))*1100} 1100 L{960+math.tan(math.radians(a+3))*1100} 1100 Z" fill="#fffbe6" opacity="0.16"/>'
    s += '<path d="M0 820 Q960 740 1920 820 V1080 H0 Z" fill="#6a3a2a"/>'
    return s


def bg_forest():
    s = grad("sky", "#3a5a3a", "#8ab07a") + '<rect width="1920" height="1080" fill="url(#sky)"/>'
    for x in (100, 400, 1650, 1850):
        s += tree(x, 900, 0.9)
    s += '<rect x="0" y="880" width="1920" height="200" fill="#4a6a2a"/>'
    return s


def frame(inner):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">{inner}'
            f'<rect width="1920" height="1080" fill="none" stroke="#000" stroke-opacity="0.35" stroke-width="44"/></svg>')


YD = dict(hair="curly", hair_col="#6a3a1a", tunic="#c8a060")           # young David
AD = dict(hair="curly", hair_col="#5a3018", beard="yes", beard_col="#5a3018", tunic="#2e5aa8")  # adult David
SAUL = dict(hair="short", beard="yes", beard_col="#3a2a20", tunic="#7a1f2e", robe="#4a1a5a", crown=True)


def P(x, y, s, flip=False, base=None, **kw):
    c, h = person(**{**(base or {}), **kw})
    return g(c, x, y, s, flip)


