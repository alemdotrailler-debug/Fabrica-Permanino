import time, os, torch
from diffusers import StableDiffusionPipeline, LCMScheduler, AutoPipelineForText2Image, AutoencoderTiny
OUT = "teste/local2"; os.makedirs(OUT, exist_ok=True)
rep = open(OUT + "/report.txt", "w")
def R(s): print(s, flush=True); rep.write(s + "\n"); rep.flush()
STY = ", masterpiece, best quality, vibrant saturated colors, thick clean outlines, cel shading, anime key visual"
P = [
 "chibi, 1boy, spiky black hair, green hooded cape, brown leather harness, determined expression, huge orange explosion background" + STY,
 "chibi, 1boy, green cape, standing in dark moonlit forest, glowing fireflies, dramatic lighting" + STY,
 "giant stone wall city on fire, tiny chibi villagers running, red sky, colossal armored giant silhouette, wide shot" + STY,
]
NEG = "lowres, bad anatomy, bad hands, text, error, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, blurry, realistic, photo"
torch.set_num_threads(os.cpu_count())
R(f"cpus {os.cpu_count()}")
def rodar(nome, carregar, passos, gs, usa_neg, taesd=False):
    try:
        t0 = time.time(); pipe = carregar()
        if taesd:
            pipe.vae = AutoencoderTiny.from_pretrained("madebyollin/taesd", torch_dtype=torch.float32)
        R(f"[{nome}] carregou em {time.time()-t0:.0f}s")
        for i, p in enumerate(P):
            t1 = time.time()
            kw = dict(num_inference_steps=passos, guidance_scale=gs, width=768, height=432, generator=torch.Generator().manual_seed(i + 3))
            if usa_neg: kw["negative_prompt"] = NEG
            img = pipe(p, **kw).images[0]; img.save(f"{OUT}/{nome}_{i}.jpg", quality=92)
            R(f"[{nome}] img {i}: {time.time()-t1:.0f}s")
        del pipe
    except Exception as e:
        R(f"[{nome}] ERRO {repr(e)[:300]}")
def lcm(repo):
    def f():
        pipe = StableDiffusionPipeline.from_pretrained(repo, torch_dtype=torch.float32, safety_checker=None)
        pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
        pipe.load_lora_weights("latent-consistency/lcm-lora-sdv1-5"); pipe.fuse_lora()
        return pipe
    return f
rodar("anything5", lcm("stablediffusionapi/anything-v5"), 4, 1.5, True)
rodar("anything5taesd", lcm("stablediffusionapi/anything-v5"), 4, 1.5, True, taesd=True)
rodar("anything3", lcm("Linaqruf/anything-v3.0"), 4, 1.5, True)
rodar("sdturbo", lambda: AutoPipelineForText2Image.from_pretrained("stabilityai/sd-turbo", torch_dtype=torch.float32), 2, 0.0, False)
rep.close()
