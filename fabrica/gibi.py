"""Template GIBI ANIMADO: o vídeo vira páginas de revista em quadrinhos.

Cada corte de ~5 s é um quadro (com a cena animada por dentro). Os quadros são agrupados em páginas de até 3;
a câmera lê a página quadro a quadro, a narração aparece em caixas amarelas, as falas em balões e os eventos
({CRASH}, {BOOM}…) viram onomatopeias.
"""
import math, os, subprocess
from concurrent.futures import ThreadPoolExecutor

from fabrica.pipeline import (FPS, linha_do_tempo, plano_cortes, mixar_audio, log, analisar)

PS = 1.5                 # página renderizada em 2880x1620 (1,5x)
PW, PH = 1920, 1080      # coordenadas da página
LAYOUTS_V = {
    1: [[(30, 30, 1020, 1860)]],
    2: [[(30, 30, 1020, 915), (30, 975, 1020, 915)]],
    3: [[(30, 30, 1020, 600), (30, 660, 1020, 600), (30, 1290, 1020, 600)],
        [(30, 30, 1020, 860), (30, 920, 495, 970), (555, 920, 495, 970)]],
}
LAYOUTS = {
    1: [[(30, 30, 1860, 1020)]],
    2: [[(30, 30, 1120, 1020), (1180, 30, 710, 1020)], [(30, 30, 910, 1020), (970, 30, 920, 1020)]],
    3: [[(30, 30, 1120, 1020), (1180, 30, 710, 495), (1180, 555, 710, 495)],
        [(30, 30, 710, 495), (770, 30, 1120, 495), (30, 555, 1860, 495)],
        [(30, 30, 600, 1020), (660, 30, 600, 1020), (1290, 30, 600, 1020)]],
}
HALF = ('<defs><pattern id="ht" width="12" height="12" patternUnits="userSpaceOnUse">'
        '<circle cx="6" cy="6" r="2.2" fill="#000"/></pattern></defs>')


def _svg(inner):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{PW}" height="{PH}" viewBox="0 0 {PW} {PH}">'
            f'{HALF}{inner}</svg>')


def base_pagina(rects):
    s = f'<rect width="{PW}" height="{PH}" fill="#f3ead2"/><rect width="{PW}" height="{PH}" fill="url(#ht)" opacity="0.06"/>'
    for (x, y, w, h) in rects:
        s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#e6dac0"/>'
    return _svg(s)


def molduras(rects):
    s = ""
    for (x, y, w, h) in rects:
        s += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#ht)" opacity="0.10"/>'
              f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#111" stroke-width="11"/>')
    return _svg(s)


def quebrar(txt, maxc):
    linhas, atual = [], ""
    for w in txt.split():
        if len(atual) + len(w) + 1 > maxc and atual:
            linhas.append(atual); atual = w
        else:
            atual = (atual + " " + w).strip()
    if atual:
        linhas.append(atual)
    return linhas


def caixa(rect, txt):
    x, y, w, h = rect
    fs = 34 if w > 900 else 30
    if PH > PW:
        fs = 40
    bw = min(w - 60, 760) if PW > PH else int(w * 0.70)
    L = quebrar(txt, int(bw / (fs * 0.56)))
    bh = 30 + len(L) * fs * 1.25
    if PH > PW:
        x = x + (w - bw) / 2 - 22
    t = "".join(f'<text x="{bw/2}" y="{36 + i * fs * 1.25:.0f}" font-family="Inter Display" font-weight="800" font-size="{fs}" '
                f'text-anchor="middle" fill="#111">{l}</text>' for i, l in enumerate(L))
    return _svg(f'<g transform="translate({x + 22},{y + 22}) rotate(-1.2)"><rect width="{bw}" height="{bh:.0f}" fill="#FFE132" '
                f'stroke="#111" stroke-width="6"/>{t}</g>')


def balao(rect, txt):
    x, y, w, h = rect
    fs = 36 if w > 900 else 32
    if PH > PW:
        fs = 42
    bw = min(w - 80, 700) if PW > PH else int(w * 0.68)
    L = quebrar(txt, int(bw / (fs * 0.55)))
    bh = 40 + len(L) * fs * 1.25
    bx = x + w - bw - 30 if PW > PH else x + (w - bw) / 2
    by = y + 30
    t = "".join(f'<text x="{bw/2}" y="{48 + i * fs * 1.25:.0f}" font-family="Inter Display" font-weight="800" font-size="{fs}" '
                f'text-anchor="middle" fill="#111">{l}</text>' for i, l in enumerate(L))
    rabo = f'M{bw*0.30:.0f} {bh-2:.0f} L{bw*0.18:.0f} {bh+70:.0f} L{bw*0.42:.0f} {bh-2:.0f}'
    return _svg(f'<g transform="translate({bx},{by})"><rect width="{bw}" height="{bh:.0f}" rx="40" fill="#fff" stroke="#111" stroke-width="6"/>'
                f'<path d="{rabo} Z" fill="#fff" stroke="#111" stroke-width="6"/><rect x="{bw*0.16:.0f}" y="{bh-12:.0f}" width="{bw*0.30:.0f}" height="14" fill="#fff"/>{t}</g>')


def onomatopeia(rect, txt):
    x, y, w, h = rect
    cx, cy = (x + w * 0.62, y + h * 0.45) if PW > PH else (x + w * 0.5, y + h * 0.55)
    r1, r2 = min(w, h) * 0.30, min(w, h) * 0.19
    pts = " ".join(f"{(r1 if i % 2 == 0 else r2) * 1.5 * math.cos(i * math.pi / 9):.0f},{(r1 if i % 2 == 0 else r2) * math.sin(i * math.pi / 9):.0f}" for i in range(18))
    fs = min(w, h) * 0.20
    return _svg(f'<g transform="translate({cx:.0f},{cy:.0f}) rotate(-9)"><polygon points="{pts}" fill="#FFE132" stroke="#111" stroke-width="8"/>'
                f'<text x="0" y="{fs*0.35:.0f}" font-family="Inter Display" font-weight="900" font-size="{fs:.0f}" text-anchor="middle" '
                f'fill="#ff3b2f" stroke="#111" stroke-width="5" paint-order="stroke">¡{txt}!</text></g>')


def capa_capitulo(a, b):
    return _svg(f'<rect width="{PW}" height="{PH}" fill="#2a6fd8"/><rect width="{PW}" height="{PH}" fill="url(#ht)" opacity="0.18"/>'
                + "".join(f'<path d="M960 540 L{960 + 1400 * math.cos(i * math.pi / 12):.0f} {540 + 1400 * math.sin(i * math.pi / 12):.0f} '
                          f'L{960 + 1400 * math.cos((i + 0.5) * math.pi / 12):.0f} {540 + 1400 * math.sin((i + 0.5) * math.pi / 12):.0f} Z" fill="#1d58b8"/>' for i in range(24))
                + '<g transform="translate(960,470) rotate(-4)">'
                + f'<text x="0" y="0" font-family="Inter Display" font-weight="900" font-size="190" text-anchor="middle" fill="#FFE132" stroke="#111" stroke-width="14" paint-order="stroke">{a}</text>'
                + f'<rect x="-520" y="60" width="1040" height="130" fill="#fff" stroke="#111" stroke-width="8"/>'
                + f'<text x="0" y="150" font-family="Inter Display" font-weight="900" font-size="72" text-anchor="middle" fill="#111">{b.upper()}</text></g>'
                + f'<rect x="20" y="20" width="{PW-40}" height="{PH-40}" fill="none" stroke="#111" stroke-width="14"/>')


def _png(pg, svg, caminho, transparente=False):
    fundo = "transparent" if transparente else "#000"
    pg.set_content(f'<html><body style="margin:0;background:{fundo}">{svg}</body></html>')
    pg.screenshot(path=caminho, omit_background=transparente)


def _cam_rect(rect):
    x, y, w, h = rect
    asp = PW / PH
    cw = max(w, h * asp) * 1.07 if PW > PH else max(w * 0.78, h * asp) * 1.05
    cw = min(cw, PW)
    ch = cw / asp
    cx, cy = x + w / 2, y + h / 2
    return (min(max(cx - cw / 2, 0), PW - cw), min(max(cy - ch / 2, 0), PH - ch), cw)


def _expr(keys, idx):
    """Expressão ffmpeg suave (smoothstep) entre quadros-chave [(t, (x, y, w))]."""
    e = f"{keys[-1][1][idx]:.2f}"
    for (t0, v0), (t1, v1) in reversed(list(zip(keys, keys[1:]))):
        a, b = v0[idx], v1[idx]
        if t1 - t0 < 1e-3:
            seg = f"{b:.2f}"
        else:
            sx = f"clip((t-{t0:.3f})/{t1 - t0:.3f},0,1)"
            seg = f"({a:.2f}+({b - a:.2f})*{sx}*{sx}*(3-2*{sx}))"
        e = f"if(lt(t,{t1:.3f}),{seg},{e})"
    return e


def montar_gibi(R, C, L, pasta, saida_mp4, vertical=False, v0=0):
    global PW, PH
    from playwright.sync_api import sync_playwright
    PW, PH = (1080, 1920) if vertical else (1920, 1080)
    tabela = LAYOUTS_V if vertical else LAYOUTS
    audio, segs, subs, caps, total, falas, eventos = linha_do_tempo(R, L, pasta, not vertical)
    wav_final = mixar_audio(R, audio, segs, caps, total, eventos, pasta)
    pecas = plano_cortes(R, C, segs, pasta, v0, falas)

    # agrupa em páginas (até 3 quadros), quebrando nas capas de capítulo
    blocos, atual = [], []
    for p in pecas:
        if p[4] is None:
            if atual: blocos.append(("pagina", atual)); atual = []
            blocos.append(("capa", p))
        else:
            atual.append(p)
            if len(atual) == 3:
                blocos.append(("pagina", atual)); atual = []
    if atual:
        blocos.append(("pagina", atual))

    gd = os.path.join(pasta, "gibi"); os.makedirs(gd, exist_ok=True)
    falas_txt = []
    for (s0, s1, tx) in subs:
        falas_txt.append((s0, s1, tx))
    quem_fala = {(round(f0, 3)): q for (f0, f1, q, _w) in falas}

    jobs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": PW, "height": PH}, device_scale_factor=PS)
        for k, (tipo, conteudo) in enumerate(blocos):
            out = os.path.join(gd, f"{k:03d}.mp4")
            if tipo == "capa":
                src, a, bb = conteudo[0], conteudo[1], conteudo[2]
                ci = int(os.path.basename(src)[4:-4])
                card = R.CH[ci][0]
                png = os.path.join(gd, f"capa{k:03d}.png"); _png(pg, capa_capitulo(card[0], card[1]), png)
                d = bb - a
                n = round(bb * FPS) - round(a * FPS)
                jobs.append(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", str(FPS), "-i", png, "-frames:v", str(n),
                             "-vf", f"scale={PW}:{PH},fade=t=in:st=0:d=0.3,fade=t=out:st={max(0, d - 0.3):.3f}:d=0.3,format=yuv420p",
                             "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-threads", "1", out])
                continue
            paineis = conteudo
            n = len(paineis)
            opcoes = tabela[n]
            rects = opcoes[k % len(opcoes)]
            t0, t1 = paineis[0][1], paineis[-1][2]
            d = t1 - t0
            base = os.path.join(gd, f"p{k:03d}_base.png"); _png(pg, base_pagina(rects), base)
            mold = os.path.join(gd, f"p{k:03d}_mold.png"); _png(pg, molduras(rects), mold, True)
            overlays = []   # (png, inicio, fim) em tempo local
            for i, (src, a, bb, modo, nome, v) in enumerate(paineis):
                for (s0, s1, tx) in subs:
                    if a <= s0 < bb:
                        quem = quem_fala.get(round(s0, 3))
                        svg = balao(rects[i], tx) if quem else caixa(rects[i], tx)
                        f = os.path.join(gd, f"p{k:03d}_t{len(overlays):02d}.png"); _png(pg, svg, f, True)
                        overlays.append((f, s0 - t0, min(s1 + 0.4, bb) - t0))
                for (te, ev) in eventos:
                    if a <= te < bb:
                        f = os.path.join(gd, f"p{k:03d}_e{len(overlays):02d}.png"); _png(pg, onomatopeia(rects[i], ev), f, True)
                        overlays.append((f, te - t0, min(te + 1.4, bb) - t0))
            # câmera: página inteira -> quadro 1 -> quadro 2 ... -> página inteira
            cheia = (0.0, 0.0, float(PW))
            keys = [(0.0, cheia)]
            for i, (src, a, bb, modo, nome, v) in enumerate(paineis):
                r = _cam_rect(rects[i])
                ini = a - t0
                keys.append((ini + (0.55 if i == 0 else 0.35), r))
                fim = bb - t0 - (0.5 if i == n - 1 else 0.0)
                keys.append((max(fim, ini + 0.6), (r[0] + (8 if i % 2 else -8), r[1], r[2] * 0.97)))
            keys.append((d, cheia))
            ex, ey, ew = (_expr(keys, i).replace("(t-", "(it-").replace("lt(t,", "lt(it,") for i in range(3))
            cam = (f"zoompan=z='{PW}/({ew})':x='({ex})*{PS}':y='({ey})*{PS}':d=1:s={PW}x{PH}:fps={FPS}")
            ins = ["-loop", "1", "-framerate", str(FPS), "-t", f"{d + 0.2:.3f}", "-i", base]
            fc = []
            cur = "0:v"
            idx = 1
            for i, (src, a, bb, modo, nome, v) in enumerate(paineis):
                x, y, w, h = [int(round(z * PS)) for z in rects[i]]
                w -= w % 2; h -= h % 2
                ins += (["-i", src] if "__fala" in src else ["-stream_loop", "-1", "-i", src])
                ini = a - t0
                pad = ",tpad=stop_mode=clone:stop_duration=600" if "__fala" in src else ""
                fc.append(f"[{idx}:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}{pad},setpts=PTS-STARTPTS+{ini:.3f}/TB[q{i}]")
                fc.append(f"[{cur}][q{i}]overlay={x}:{y}:enable='gte(t,{ini:.3f})':eof_action=pass[v{i}]")
                cur = f"v{i}"; idx += 1
            ins += ["-loop", "1", "-i", mold]
            fc.append(f"[{cur}][{idx}:v]overlay=0:0[m]"); cur = "m"; idx += 1
            for j, (f, ia, ib) in enumerate(overlays):
                ins += ["-loop", "1", "-i", f]
                fc.append(f"[{cur}][{idx}:v]overlay=0:0:enable='between(t,{ia:.3f},{ib:.3f})'[o{j}]")
                cur = f"o{j}"; idx += 1
            fc.append(f"[{cur}]{cam},format=yuv420p[out]")
            nf = round(t1 * FPS) - round(t0 * FPS)
            jobs.append(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(fc), "-map", "[out]",
                         "-frames:v", str(nf), "-r", str(FPS), "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
                         "-threads", "2", out])
        b.close()
    log(f"gibi: {sum(1 for b_ in blocos if b_[0] == 'pagina')} páginas")
    with ThreadPoolExecutor(max(1, (os.cpu_count() or 2) // 2)) as ex:
        list(ex.map(lambda c: subprocess.run(c, check=True), jobs))
    lista = os.path.join(gd, "lista.txt")
    open(lista, "w").write("\n".join(f"file '{k:03d}.mp4'" for k in range(len(blocos))))
    mudo = os.path.join(pasta, "mudo.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", mudo], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mudo, "-i", wav_final, "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "160k", "-shortest", "-movflags", "+faststart", saida_mp4], check=True)
    log(f"vídeo pronto (gibi): {total/60:.1f} min")
    return total, caps
