"""Fábrica de vídeos do Crónicas del Pergamino.

Uso:  python -m fabrica.pipeline videos/<slug>

Etapas: narração (Kokoro) -> cenas (SVG -> PNG) -> música + legendas -> montagem (FFmpeg)
-> thumbnail -> link público temporário -> saida/<slug>/info.json
"""
import hashlib, importlib.util, json, os, re, subprocess, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import soundfile as sf

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELOS = os.path.join(RAIZ, "modelos")
SR = 24000
FPS = 24
URL_MODELOS = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"


def log(*a):
    print("[fábrica]", *a, flush=True)


def carregar(caminho, nome):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nome] = m
    spec.loader.exec_module(m)
    return m


def frases(p):
    partes = re.split(r'(?<=[\.\?!»])\s+(?=[A-ZÁÉÍÓÚÑ¿¡\[\{])', p)
    return [x.strip() for x in partes if x.strip()]


RE_FALA = re.compile(r'^\s*\[([a-zA-Z0-9_áéíóúñ]+)\]\s*')
RE_EVENTO = re.compile(r'\{([A-ZÁÉÍÓÚÑ¡!¿?\.\- ]+)\}\s*')


def analisar(txt):
    """'[capitan] {CRASH} ¿Qué tienes?' -> ('capitan', ['CRASH'], '¿Qué tienes?')"""
    m = RE_FALA.match(txt)
    quem = m.group(1) if m else None
    if m:
        txt = txt[m.end():]
    eventos = RE_EVENTO.findall(txt)
    return quem, eventos, RE_EVENTO.sub("", txt).strip()


def linhas(CH):
    L = []
    for ci, (card, paras) in enumerate(CH):
        for sc, p in paras:
            for s in frases(p):
                L.append((ci, card, sc, s))
    return L


# ---------------- 1. narração ----------------
def narrar(R, L, pasta):
    os.makedirs(MODELOS, exist_ok=True)
    for f in ("kokoro-v1.0.onnx", "voices-v1.0.bin"):
        if not os.path.exists(os.path.join(MODELOS, f)):
            log("baixando modelo", f)
            urllib.request.urlretrieve(URL_MODELOS + f, os.path.join(MODELOS, f))
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(MODELOS, "kokoro-v1.0.onnx"), os.path.join(MODELOS, "voices-v1.0.bin"))
    os.makedirs(os.path.join(pasta, "wav"), exist_ok=True)
    for i, l in enumerate(L):
        f = wav_de(pasta, l[3])
        if os.path.exists(f):
            continue
        quem, _, limpo = analisar(l[3])
        texto = limpo.replace("…", ",").replace(":", ",").replace("«", "").replace("»", "")
        voz = getattr(R, "VOZES", {}).get(quem, getattr(R, "VOZ", "em_alex")) if quem else getattr(R, "VOZ", "em_alex")
        a, sr = k.create(texto, voice=voz, speed=getattr(R, "VELOCIDADE", 0.9), lang="es")
        sf.write(f, a, sr)
        if i % 20 == 0:
            log(f"narração {i+1}/{len(L)}")


def wav_de(pasta, t):
    return os.path.join(pasta, "wav", hashlib.md5(t.encode()).hexdigest()[:12] + ".wav")


# ---------------- 2. cenas ----------------
def cartao(a, b, W, H):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">'
            f'<defs><radialGradient id="r" cx="0.5" cy="0.5" r="0.7"><stop offset="0" stop-color="#3a2416"/><stop offset="1" stop-color="#0e0806"/></radialGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#r)"/>'
            f'<rect x="80" y="80" width="{W-160}" height="{H-160}" fill="none" stroke="#b8862a" stroke-width="4" opacity="0.6"/>'
            f'<text x="{W/2}" y="{H/2-70}" font-family="Inter Display" font-weight="800" font-size="64" letter-spacing="18" fill="#e8c27a" text-anchor="middle">{a}</text>'
            f'<line x1="{W/2-200}" y1="{H/2-20}" x2="{W/2+200}" y2="{H/2-20}" stroke="#b8862a" stroke-width="4"/>'
            f'<text x="{W/2}" y="{H/2+100}" font-family="Lora" font-weight="700" font-size="96" fill="#f2d27a" text-anchor="middle">{b}</text></svg>')


def renderizar(R, C, pasta, W, H, caminho_cenas=None):
    from playwright.sync_api import sync_playwright
    os.makedirs(os.path.join(pasta, "png"), exist_ok=True)
    animado = getattr(C, "ANIMADO", False)
    tudo = {} if animado else dict(C.scenes())
    for ci, (card, _) in enumerate(R.CH):
        if card:
            tudo[f"card{ci}"] = cartao(card[0], card[1], W, H)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        for k, v in tudo.items():
            pg.set_content(f'<html><body style="margin:0">{v}</body></html>')
            pg.wait_for_timeout(80)
            pg.screenshot(path=os.path.join(pasta, "png", f"{k}.png"))
        if hasattr(C, "thumb"):
            pg.set_viewport_size({"width": 1280, "height": 720})
            for v in getattr(C, "THUMBS", "AB"):
                pg.set_content(f'<html><body style="margin:0">{C.thumb(v)}</body></html>')
                pg.wait_for_timeout(120)
                pg.screenshot(path=os.path.join(pasta, f"thumb_{v}.jpg"), type="jpeg", quality=92)
        b.close()
    log("cenas/cartões renderizados:", len(tudo))
    if animado:
        from fabrica import animacao
        _, segs, _, _, _, falas, _ = linha_do_tempo(R, linhas(R.CH), pasta, W > H)
        pl = plano_cortes(R, C, segs, pasta, 0, falas)
        pedidos = [(p[4], p[5]) for p in pl if p[4] is not None and "__fala" not in p[0]]
        animacao.render_loops(caminho_cenas, RAIZ, pasta, pedidos, getattr(C, "LOOP", 3.0))
        diretos = [(p[4], p[5], p[1], p[2], p[0]) for p in pl if p[4] is not None and "__fala" in p[0]]
        if diretos:
            animacao.render_falas(caminho_cenas, RAIZ, pasta, diretos, envelopes(falas), getattr(C, "LOOP", 3.0))
        log("loops animados (todos diferentes):", len(pedidos), "| cortes com fala sincronizada:", len(diretos))


# ---------------- 3. montagem ----------------
def acorde(freqs, dur):
    n = int(dur * SR); tt = np.arange(n) / SR
    s = sum(np.sin(2*np.pi*f*tt) + 0.3*np.sin(2*np.pi*f*2.003*tt) + 0.15*np.sin(2*np.pi*f*0.5*tt) for f in freqs)
    env = np.minimum(1, np.minimum(tt / 1.2, (dur - tt) / 1.2))
    return s * env * (0.65 + 0.35 * np.sin(2*np.pi*0.2*tt))


MENOR = [[110, 130.8, 164.8], [87.3, 110, 130.8], [98, 116.5, 146.8], [82.4, 98, 123.5]]
MAIOR = [[130.8, 164.8, 196], [98, 123.5, 146.8], [110, 130.8, 164.8], [87.3, 110, 130.8]]


from fabrica.animacao import dividir as animacao_dividir, MODOS as ANIM_MODOS


def envelopes(falas):
    """Para cada fala: (início, fim, personagem, nível da voz por quadro de 24 fps)."""
    out = []
    for (f0, f1, quem, wav) in falas:
        a, _ = sf.read(wav)
        n = max(1, int(len(a) / SR * FPS))
        e = np.array([np.sqrt(np.mean(a[int(i * SR / FPS):int((i + 1) * SR / FPS)] ** 2) + 1e-12) for i in range(n)])
        out.append((f0, f1, quem, (e / max(1e-6, e.max())).tolist()))
    return out


def ass_karaoke(s0, s1, tx, a, d):
    """Legenda palavra por palavra: falada em branco e maior, já ditas em amarelo, próximas invisíveis."""
    ws = tx.split()
    if not ws:
        return ""
    tot = sum(len(w) for w in ws); acc = 0; out = ""
    for i, w in enumerate(ws):
        w0 = s0 + (s1 - s0) * acc / tot; acc += len(w); w1 = s0 + (s1 - s0) * acc / tot
        if i == len(ws) - 1:
            w1 = s1 + 0.25
        x0, x1 = max(0, w0 - a), min(d, w1 - a)
        if x1 <= 0 or x0 >= d:
            continue
        partes = []
        for j, ww in enumerate(ws):
            if j < i:
                partes.append(ww)
            elif j == i:
                partes.append("{\\c&HFFFFFF&\\fscx112\\fscy112}" + ww + "{\\r}")
            else:
                partes.append("{\\alpha&HFF&}" + ww + "{\\r}")
        out += f"Dialogue: 0,{ts(x0)},{ts(x1)},Sub,,0,0,0,,{' '.join(partes)}\n"
    return out


def ts(x):
    return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"


def linha_do_tempo(R, L, pasta, longo):
    CARD, GAP, EXTRA, FIM_CAP = 2.6, 0.38, 0.35, 0.9
    audio, segs, subs, caps, falas, eventos = [], [], [], [], [], []
    st = {"t": 0.0, "cena": None, "ini": 0.0}

    def pausa(n):
        audio.append(np.zeros(int(round(n * SR)))); st["t"] += n

    def fecha(fim):
        if st["cena"] is not None and fim > st["ini"] + 0.05:
            segs.append((os.path.join(pasta, "png", f"{st['cena']}.png"), st["ini"], fim))
        st["cena"] = None

    prev = None
    pausa(0.3)
    for ci, card, sc, txt in L:
        if ci != prev:
            if prev is not None:
                pausa(FIM_CAP)
            if card and longo:
                fecha(st["t"])
                nome = f"{card[0].title()}: {card[1]}" if card[0] != "FINAL" else f"Final: {card[1]}"
                caps.append((nome, st["t"]))
                segs.append((os.path.join(pasta, "png", f"card{ci}.png"), st["t"], st["t"] + CARD))
                pausa(CARD)
            elif not caps:
                caps.append(("Introducción", 0.0))
            prev = ci
        if sc != st["cena"]:
            fecha(st["t"]); st["cena"], st["ini"] = sc, st["t"]
        a, sr = sf.read(wav_de(pasta, txt))
        d = len(a) / SR
        quem, evs, limpo = analisar(txt)
        subs.append((st["t"], st["t"] + d, limpo))
        if quem:
            falas.append((st["t"], st["t"] + d, quem, wav_de(pasta, txt)))
        for e in evs:
            eventos.append((st["t"], e))
        audio.append(a); st["t"] += d
        pausa(GAP + (EXTRA if len(txt.split()) <= 6 else 0))
    pausa(1.5)
    fecha(st["t"])
    return audio, segs, subs, caps, st["t"], falas, eventos


def plano_cortes(R, C, segs, pasta, v0=0, falas=()):
    """Divide cada cena em cortes de ~CORTE_SEG s. Cada corte ganha uma variante única (desenho diferente)."""
    animado = bool(C is not None and getattr(C, "ANIMADO", False))
    pecas, k_cam, cont = [], 0, {}
    for (png, a, b) in segs:
        if "card" in os.path.basename(png) or not animado:
            pecas.append((png, a, b, None, None, None))
            continue
        nome = os.path.splitext(os.path.basename(png))[0]
        for i, (x0, x1) in enumerate(animacao_dividir(a, b, getattr(R, "CORTE_SEG", 5.0))):
            v = cont.get(nome, v0); cont[nome] = v + 1
            modo = "geral" if i == 0 else ANIM_MODOS[k_cam % len(ANIM_MODOS)]
            k_cam += 1
            fala = any(f0 < x1 and f1 > x0 for (f0, f1, _q, _w) in falas)
            arq = f"{nome}__{v}__fala{int(x0 * 100)}_{int(x1 * 100)}.mp4" if fala else f"{nome}__{v}.mp4"
            pecas.append((os.path.join(pasta, "loops", arq), x0, x1, modo, nome, v))
    return pecas


def mixar_audio(R, audio, segs, caps, total, eventos, pasta):
    voz = np.concatenate(audio)

    humor = getattr(R, "MUSICA", ["menor"] * len(R.CH))
    inicios = [c[1] for c in caps] + [total]
    mus = []
    for k in range(len(caps)):
        a, b = inicios[k], inicios[k + 1]; mt, j = a, 0
        prog = MAIOR if (humor[k] if k < len(humor) else "menor") == "maior" else MENOR
        while mt < b - 0.01:
            dd = min(5.0, b - mt); mus.append(acorde(prog[j % 4], dd)); mt += dd; j += 1
    musica = np.concatenate(mus) if mus else np.zeros(len(voz))
    musica = np.pad(musica, (0, max(0, len(voz) - len(musica))))[:len(voz)]
    musica = musica / max(1e-6, np.abs(musica).max()) * 0.075
    mix = voz / max(1e-6, np.abs(voz).max()) * 0.9 + musica
    rng = np.random.RandomState(7)
    tt = np.arange(int(0.5 * SR)) / SR
    whoosh = rng.randn(len(tt)) * np.exp(-((tt - 0.12) / 0.06) ** 2) * 0.18
    boom = np.convolve(rng.randn(len(tt)), np.ones(60) / 60, "same") * np.exp(-tt * 5) * 2.2
    for (png, a0, b0) in segs[1:]:
        if "card" not in os.path.basename(png) and getattr(R, "EFEITOS", True):
            i0 = max(0, int((a0 - 0.12) * SR)); seg = whoosh[:max(0, min(len(whoosh), len(mix) - i0))]
            mix[i0:i0 + len(seg)] += seg
    for (te, _e) in eventos:
        i0 = int(te * SR); seg = boom[:max(0, min(len(boom), len(mix) - i0))]
        mix[i0:i0 + len(seg)] += seg
    mix = mix / max(1.0, np.abs(mix).max() / 0.98)
    f = int(2 * SR); mix[-f:] *= np.linspace(1, 0, f)
    wav_final = os.path.join(pasta, "audio.wav")
    sf.write(wav_final, mix, SR)
    return wav_final


def montar(R, L, pasta, W, H, saida_mp4, C=None, v0=0):
    longo = W > H
    audio, segs, subs, caps, total, falas, eventos = linha_do_tempo(R, L, pasta, longo)
    wav_final = mixar_audio(R, audio, segs, caps, total, eventos, pasta)

    fs, mv, ml = (50, 56, 160) if longo else (74, 520, 90)
    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Inter Display,{fs},{getattr(R, "COR_LEGENDA", "&H0032E1FF")},&H00FFFFFF,&H00120A06,&H64000000,-1,0,0,0,100,100,0,0,1,{4.5 if longo else 6},1.5,2,{ml},{ml if longo else 150},{mv},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    sd = os.path.join(pasta, "seg"); os.makedirs(sd, exist_ok=True)
    pecas = plano_cortes(R, C, segs, pasta, v0, falas)
    karaoke = getattr(R, "LEGENDA", "karaoke") == "karaoke"
    jobs = []
    vistos = set()
    for k, (src, a, b, modo, nome_cena, var) in enumerate(pecas):
        d = b - a
        ass = cab
        for (s0, s1, tx) in subs:
            if s1 > a and s0 < b:
                if karaoke:
                    ass += ass_karaoke(s0, s1, tx, a, d)
                else:
                    ass += f"Dialogue: 0,{ts(max(0, s0-a))},{ts(min(d, s1-a+0.2))},Sub,,0,0,0,,{tx}\n"
        af = os.path.join(sd, f"{k:03d}.ass"); open(af, "w").write(ass)
        n = round(b * FPS) - round(a * FPS)
        saida = os.path.join(sd, f"{k:03d}.mp4")
        if "card" in os.path.basename(src):
            vf = f"scale={W}:{H},fade=t=in:st=0:d=0.4,fade=t=out:st={max(0,d-0.4):.3f}:d=0.4,format=yuv420p"
            entrada = ["-loop", "1", "-framerate", str(FPS), "-i", src]
        elif modo is None:
            z = f"max(1.001,min(1.07,1+0.07*t/{d:.3f}))" if k % 2 == 0 else f"max(1.001,min(1.07,1.07-0.07*t/{d:.3f}))"
            vf = (f"scale=w='trunc({W}*{z}/2)*2':h='trunc({H}*{z}/2)*2':eval=frame,crop={W}:{H},"
                  f"subtitles={af},fade=t=in:st=0:d=0.35,fade=t=out:st={max(0,d-0.35):.3f}:d=0.35,format=yuv420p")
            entrada = ["-loop", "1", "-framerate", str(FPS), "-i", src]
        else:
            from fabrica import animacao
            foco = getattr(C, "FOCO", {}).get(nome_cena, (W / 2, H / 2))
            nova_cena = nome_cena not in vistos and k > 0
            vistos.add(nome_cena)
            if nova_cena and modo == "geral" and getattr(R, "EFEITOS", True):
                z = f"max(1.001,1+0.14*max(0,1-t/0.28)+0.05*t/{d:.3f})"
                cam = (f"scale=w='trunc({W}*{z}/2)*2':h='trunc({H}*{z}/2)*2':eval=frame,crop={W}:{H},"
                       f"gblur=sigma=22:enable='lt(t,0.10)'")
            else:
                cam = animacao.filtro_camera(modo, d, foco, W, H) if W > H else animacao.filtro_camera_vertical(modo, d, foco, W, H)
            extra = ""
            for (te, _e) in eventos:
                if a <= te < b:
                    L0 = te - a
                    extra += (f",scale={int(W*1.04)//2*2}:{int(H*1.04)//2*2},crop={W}:{H}:x='{int(W*0.02)}+30*sin(t*95)*between(t,{L0:.2f},{L0+0.6:.2f})'"
                              f":y='{int(H*0.02)}+18*cos(t*80)*between(t,{L0:.2f},{L0+0.6:.2f})',"
                              f"drawbox=x=0:y=0:w=iw:h=ih:color=white@0.55:t=fill:enable='between(t,{L0:.2f},{L0+0.12:.2f})'")
                    break
            vf = f"{cam}{extra},subtitles={af},format=yuv420p"
            entrada = ["-i", src] if "__fala" in src else ["-stream_loop", "-1", "-i", src]
        jobs.append(["ffmpeg", "-y", "-loglevel", "error", *entrada, "-frames:v", str(n), "-vf", vf, "-r", str(FPS),
                     "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-threads", "1", saida])
    segs = pecas
    with ThreadPoolExecutor(os.cpu_count() or 2) as ex:
        list(ex.map(lambda c: subprocess.run(c, check=True), jobs))
    lista = os.path.join(sd, "lista.txt")
    open(lista, "w").write("\n".join(f"file '{k:03d}.mp4'" for k in range(len(segs))))
    mudo = os.path.join(pasta, "mudo.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", mudo], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mudo, "-i", wav_final, "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "160k", "-shortest", "-movflags", "+faststart", saida_mp4], check=True)
    log(f"vídeo pronto: {total/60:.1f} min")
    return total, caps


# ---------------- 4. link público e info ----------------
def link_publico(arq):
    """Sites temporários (reserva). O caminho principal é a Release do GitHub (no workflow)."""
    erros = []
    tentativas = [
        ("uguu", ["curl", "-sS", "--fail", "-m", "600", "-F", f"files[]=@{arq}", "https://uguu.se/upload"], "json_uguu"),
        ("litterbox", ["curl", "-sS", "--fail", "-m", "600", "-F", "reqtype=fileupload", "-F", "time=72h",
                       "-F", f"fileToUpload=@{arq}", "https://litterbox.catbox.moe/resources/internals/api.php"], None),
        ("catbox", ["curl", "-sS", "--fail", "-m", "600", "-F", "reqtype=fileupload", "-F", f"fileToUpload=@{arq}",
                    "https://catbox.moe/user/api.php"], None),
    ]
    for nome, cmd, modo in tentativas:
        r = subprocess.run(cmd, capture_output=True, text=True)
        out = r.stdout.strip()
        if r.returncode == 0:
            if modo == "json_uguu":
                try:
                    out = json.loads(out)["files"][0]["url"]
                except Exception:
                    pass
            if out.startswith("https://"):
                return out, erros
        erros.append(f"{nome}: código {r.returncode} {r.stderr.strip()[:150]} {out[:150]}")
    return None, erros


def mmss(x):
    x = int(x); return f"{x//3600}:{x%3600//60:02d}:{x%60:02d}" if x >= 3600 else f"{x//60}:{x%60:02d}"


def main(pasta_video, enviar=True):
    pasta_video = os.path.abspath(pasta_video)
    R = carregar(os.path.join(pasta_video, "roteiro.py"), "roteiro")
    sys.path.insert(0, RAIZ)
    C = carregar(os.path.join(pasta_video, "cenas.py"), "cenas")
    W, H = (1920, 1080) if getattr(R, "FORMATO", "longo") == "longo" else (1080, 1920)
    trabalho = os.path.join(RAIZ, "trabalho", R.SLUG); os.makedirs(trabalho, exist_ok=True)
    saida = os.path.join(RAIZ, "saida", R.SLUG); os.makedirs(saida, exist_ok=True)
    L = linhas(R.CH)
    log(f"{R.SLUG}: {len(L)} frases")
    narrar(R, L, trabalho)
    renderizar(R, C, trabalho, W, H, os.path.join(pasta_video, "cenas.py"))
    mp4 = os.path.join(trabalho, f"{R.SLUG}.mp4")
    if getattr(R, "TEMPLATE", "niveles") == "gibi":
        from fabrica.gibi import montar_gibi
        total, caps = montar_gibi(R, C, L, trabalho, mp4)
    else:
        total, caps = montar(R, L, trabalho, W, H, mp4, C)
    for v in getattr(C, "THUMBS", "AB"):
        t = os.path.join(trabalho, f"thumb_{v}.jpg")
        if os.path.exists(t):
            subprocess.run(["cp", t, saida])
    capitulos = "\n".join(f"{mmss(t)} {n}" for n, t in caps)
    info = {
        "slug": R.SLUG, "formato": getattr(R, "FORMATO", "longo"), "duracao_seg": round(total, 1),
        "tamanho_bytes": os.path.getsize(mp4), "titulo": R.TITULO,
        "descricao": R.DESCRICAO.replace("{CAPITULOS}", capitulos), "tags": R.TAGS,
        "comentario_fixado": getattr(R, "COMENTARIO", ""), "capitulos": capitulos,
        "gerado_em": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
    }
    if enviar:
        url, erros = link_publico(mp4)
        info["video_url_temporario"] = url
        info["erros_envio"] = erros
        log("link temporário:", url, erros)
    json.dump(info, open(os.path.join(saida, "info.json"), "w"), indent=1, ensure_ascii=False)
    log("ok")


if __name__ == "__main__":
    main(sys.argv[1], enviar="--sem-envio" not in sys.argv)
