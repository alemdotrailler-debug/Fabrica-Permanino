import urllib.request, urllib.parse, time, os, sys
OUT = "teste/pollinations"; os.makedirs(OUT, exist_ok=True)
base = "cute chibi anime boy hero, spiky black hair, green hooded cape, brown leather harness, "
prompts = [
 base + "determined face, huge orange explosion behind, vibrant saturated colors, bold outlines, cel shading, 16:9 anime key visual",
 base + "standing in a dark moonlit forest, glowing fireflies, dramatic lighting, anime illustration",
 "gigantic stone wall city on fire, chibi villagers running, red sky, giant armored colossus silhouette, anime illustration, vivid colors",
 "giant hourglass with red sand and chibi anime boy hero in green cape in front, purple red energy clouds, anime thumbnail style",
]
rep = open(OUT + "/report.txt", "w")
for model in ["flux", "turbo"]:
    for i, p in enumerate(prompts):
        url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(p) + f"?width=1280&height=720&model={model}&nologo=true&seed={i+7}"
        t0 = time.time(); status = "?"; size = 0
        for tent in range(4):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=180) as r:
                    data = r.read(); status = r.status; ct = r.headers.get("content-type", "")
                if "image" in ct:
                    open(f"{OUT}/{model}_{i}.jpg", "wb").write(data); size = len(data); break
                status = f"{status} {ct}"
            except Exception as e:
                status = repr(e)[:120]
                time.sleep(15)
        line = f"{model} #{i}: {status} {size}B tentativas={tent+1} {time.time()-t0:.0f}s"
        print(line); rep.write(line + "\n"); rep.flush()
rep.close()
