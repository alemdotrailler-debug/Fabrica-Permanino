"""Shorts verticais (1080x1920) a partir das cenas animadas de um vídeo.

Uso:  python -m fabrica.shorts videos/<slug>
Lê videos/<slug>/shorts.py (lista SHORTS) e gera saida/<slug>/short_<id>.json com o link temporário.
"""
import json, os, sys, time
from types import SimpleNamespace

from fabrica.pipeline import (RAIZ, carregar, linhas, narrar, linha_do_tempo, plano_cortes, montar, link_publico, log, envelopes)
from fabrica import animacao


def gerar(pasta_video, enviar=True):
    pasta_video = os.path.abspath(pasta_video)
    sys.path.insert(0, RAIZ)
    R = carregar(os.path.join(pasta_video, "roteiro.py"), "roteiro")
    caminho_cenas = os.path.join(pasta_video, "cenas.py")
    C = carregar(caminho_cenas, "cenas")
    S = carregar(os.path.join(pasta_video, "shorts.py"), "shorts")
    saida = os.path.join(RAIZ, "saida", R.SLUG); os.makedirs(saida, exist_ok=True)
    for n, sh in enumerate(S.SHORTS):
        sid = sh["id"]
        pasta = os.path.join(RAIZ, "trabalho", R.SLUG, f"short_{sid}"); os.makedirs(pasta, exist_ok=True)
        cfg = SimpleNamespace(CH=sh["CH"], VOZ=getattr(R, "VOZ", "em_alex"), VOZES=getattr(R, "VOZES", {}), VELOCIDADE=sh.get("velocidade", 0.95),
                              MUSICA=[sh.get("musica", "menor")], CORTE_SEG=sh.get("corte", 3.5),
                              COR_LEGENDA=getattr(R, "COR_LEGENDA", "&H0032E1FF"), TEMPLATE=getattr(R, "TEMPLATE", "niveles"))
        L = linhas(cfg.CH)
        log(f"short {sid}: {len(L)} frases")
        narrar(cfg, L, pasta)
        v0 = 50 + n * 25          # variantes diferentes das do vídeo longo e dos outros shorts
        _, segs, _, _, _, falas, _ = linha_do_tempo(cfg, L, pasta, False)
        pl = plano_cortes(cfg, C, segs, pasta, v0, falas)
        pedidos = [(p[4], p[5]) for p in pl if p[4] is not None and "__fala" not in p[0]]
        animacao.render_loops(caminho_cenas, RAIZ, pasta, pedidos, getattr(C, "LOOP", 3.0))
        diretos = [(p[4], p[5], p[1], p[2], p[0]) for p in pl if p[4] is not None and "__fala" in p[0]]
        if diretos:
            animacao.render_falas(caminho_cenas, RAIZ, pasta, diretos, envelopes(falas), getattr(C, "LOOP", 3.0))
        mp4 = os.path.join(pasta, f"{R.SLUG}_short_{sid}.mp4")
        if getattr(R, "TEMPLATE", "niveles") == "gibi":
            from fabrica.gibi import montar_gibi
            total, _ = montar_gibi(cfg, C, L, pasta, mp4, vertical=True, v0=v0)
        else:
            total, _ = montar(cfg, L, pasta, 1080, 1920, mp4, C, v0)
        info = {"slug": R.SLUG, "short": sid, "formato": "short", "duracao_seg": round(total, 1),
                "tamanho_bytes": os.path.getsize(mp4), "titulo": sh["titulo"], "descricao": sh["descricao"],
                "tags": sh.get("tags", []), "gerado_em": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}
        if enviar:
            url, erros = link_publico(mp4)
            info["video_url_temporario"] = url
            info["erros_envio"] = erros
        json.dump(info, open(os.path.join(saida, f"short_{sid}.json"), "w"), indent=1, ensure_ascii=False)
        log(f"short {sid} pronto: {total:.0f} s")


if __name__ == "__main__":
    gerar(sys.argv[1], enviar="--sem-envio" not in sys.argv)
