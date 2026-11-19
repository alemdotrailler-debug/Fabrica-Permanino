import json, urllib.request, time, os
OUT = "teste/horde"; os.makedirs(OUT, exist_ok=True)
H = {"apikey": "0000000000", "Content-Type": "application/json", "Client-Agent": "fabrica-teste:1:anon"}
def call(url, data=None):
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None, headers=H)
    with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read())
rep = open(OUT + "/report.txt", "w")
payload = {"prompt": "cute chibi anime boy hero, spiky black hair, green hooded cape, huge orange explosion behind, vibrant colors, bold outlines, anime key visual", "params": {"width": 832, "height": 448, "steps": 25, "n": 1, "sampler_name": "k_euler"}, "nsfw": False, "censor_nsfw": True, "models": ["Anything Diffusion"]}
t0 = time.time()
try:
    r = call("https://stablehorde.net/api/v2/generate/async", payload); rid = r["id"]; rep.write(f"id {rid}\n")
    while time.time() - t0 < 600:
        s = call(f"https://stablehorde.net/api/v2/generate/check/{rid}"); rep.write(f"{time.time()-t0:.0f}s {s}\n"); rep.flush()
        if s.get("done"): break
        time.sleep(10)
    f = call(f"https://stablehorde.net/api/v2/generate/status/{rid}")
    img = f["generations"][0]["img"]; rep.write(f"img {img[:80]}\n")
    urllib.request.urlretrieve(img, OUT + "/horde_0.webp")
    rep.write(f"OK em {time.time()-t0:.0f}s\n")
except Exception as e:
    rep.write("ERRO " + repr(e)[:300] + "\n")
rep.close()
