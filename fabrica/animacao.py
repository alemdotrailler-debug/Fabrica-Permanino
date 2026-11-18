"""Cenas animadas: cada cena é uma função de t (segundos) que devolve um SVG.

Cada cena vira um loop curto (LOOP s) renderizado em 1,5x (2880x1620), e o vídeo
corta a cada ~5 s entre 3 "câmeras": plano geral, close no foco da cena e pan lateral.
"""
import math, os, subprocess
from multiprocessing import Pool

ESCALA = 1.5            # loops renderizados em 2880x1620 para o close ficar nítido
FPS_LOOP = 24


# ---------- utilidades para animar personagens ----------
def onda(t, periodo=3.0, fase=0.0):
    """Seno que fecha o loop se LOOP for múltiplo de 'periodo'."""
    return math.sin(2 * math.pi * (t / periodo + fase))


def piscando(t, loop=3.0, quando=0.6, dur=0.12):
    """True durante uma piscada por loop."""
    x = (t - quando) % loop
    return x < dur


def respirar(conteudo, t, amp=0.012, loop=3.0):
    s = 1 + amp * onda(t, loop)
    return f'<g transform="scale(1,{s:.4f})">{conteudo}</g>'


# ---------- renderização dos loops ----------
def _render_lote(args):
    nomes, caminho_cenas, raiz, pasta, loop = args
    import sys, importlib.util
    sys.path.insert(0, raiz)
    spec = importlib.util.spec_from_file_location("cenas_anim", caminho_cenas)
    C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
    S = C.scenes()
    from playwright.sync_api import sync_playwright
    n = int(round(loop * FPS_LOOP))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=ESCALA)
        for nome, var in nomes:
            chave = f"{nome}__{var}"
            d = os.path.join(pasta, "loops", chave); os.makedirs(d, exist_ok=True)
            mp4 = os.path.join(pasta, "loops", f"{chave}.mp4")
            if os.path.exists(mp4):
                continue
            f = S[nome]
            if hasattr(C, "VAR"):
                C.VAR["v"] = var
            for i in range(n):
                pg.set_content(f'<html><body style="margin:0;background:#000">{f(i / FPS_LOOP)}</body></html>')
                pg.screenshot(path=os.path.join(d, f"{i:03d}.jpg"), type="jpeg", quality=90)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS_LOOP), "-i", os.path.join(d, "%03d.jpg"),
                            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", mp4], check=True)
            for x in os.listdir(d):
                os.remove(os.path.join(d, x))
            os.rmdir(d)
            print("[fábrica] loop pronto:", chave, flush=True)
        b.close()


def render_loops(caminho_cenas, raiz, pasta, nomes, loop):
    """nomes: lista de (cena, variante)."""
    os.makedirs(os.path.join(pasta, "loops"), exist_ok=True)
    nproc = max(1, os.cpu_count() or 2)
    lotes = [nomes[i::nproc] for i in range(nproc)]
    with Pool(nproc) as pool:
        pool.map(_render_lote, [(l, caminho_cenas, raiz, pasta, loop) for l in lotes if l])


# ---------- câmeras ----------
MODOS = ["geral", "close", "pan_d", "close", "geral", "pan_e"]


def filtro_camera(modo, d, foco, W=1920, H=1080):
    fx, fy = foco
    if modo == "geral":
        z = f"max(1.001,min(1.06,1+0.06*t/{d:.3f}))"
        return f"scale=w='trunc({W}*{z}/2)*2':h='trunc({H}*{z}/2)*2':eval=frame,crop={W}:{H}"
    if modo == "close":
        k = 1.4
        sw, sh = int(W * k) // 2 * 2, int(H * k) // 2 * 2
        cx = min(max(fx * k - W / 2, 0), sw - W)
        cy = min(max(fy * k - H / 2, 0), sh - H)
        return (f"scale={sw}:{sh},crop={W}:{H}:x='clip({cx:.0f}+30*sin(t*0.5),0,{sw-W})':"
                f"y='clip({cy:.0f}-12*t/{d:.3f},0,{sh-H})'")
    k = 1.2
    sw, sh = int(W * k) // 2 * 2, int(H * k) // 2 * 2
    folga = sw - W
    x = f"{folga}*t/{d:.3f}" if modo == "pan_d" else f"{folga}-{folga}*t/{d:.3f}"
    cy = min(max(fy * k - H / 2, 0), sh - H)
    return f"scale={sw}:{sh},crop={W}:{H}:x='clip({x},0,{folga})':y={cy:.0f}"


def dividir(a, b, corte):
    d = b - a
    n = max(1, int(round(d / corte)))
    passo = d / n
    return [(a + i * passo, a + (i + 1) * passo) for i in range(n)]


def filtro_camera_vertical(modo, d, foco, W=1080, H=1920):
    """Recorte vertical (Shorts) a partir do loop horizontal 2880x1620, centrado no foco."""
    fx, fy = foco
    k = {"geral": 1.0, "close": 1.3}.get(modo, 1.12)
    sh = int(H * k) // 2 * 2
    sw = int(sh * 16 / 9) // 2 * 2
    f = sw / 1920
    cx = min(max(fx * f - W / 2, 0), sw - W)
    cy = min(max(fy * f - H / 2, 0), sh - H)
    if modo == "geral":
        z = f"max(1.001,min(1.05,1+0.05*t/{d:.3f}))"
        return (f"scale=w='trunc({sw}*{z}/2)*2':h='trunc({sh}*{z}/2)*2':eval=frame,"
                f"crop={W}:{H}:x='clip({cx:.0f}*{z},0,iw-{W})':y='(ih-{H})/2'")
    if modo == "close":
        return f"scale={sw}:{sh},crop={W}:{H}:x='clip({cx:.0f}+20*sin(t*0.6),0,{sw-W})':y='clip({cy:.0f}-10*t/{d:.3f},0,{sh-H})'"
    folga = 260
    x0 = min(max(cx - folga / 2, 0), sw - W - folga)
    x = f"{x0:.0f}+{folga}*t/{d:.3f}" if modo == "pan_d" else f"{x0 + folga:.0f}-{folga}*t/{d:.3f}"
    return f"scale={sw}:{sh},crop={W}:{H}:x='clip({x},0,{sw-W})':y={cy:.0f}"
