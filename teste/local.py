import time, os, torch
from diffusers import AutoPipelineForText2Image
OUT = "teste/local"; os.makedirs(OUT, exist_ok=True)
rep = open(OUT + "/report.txt", "w")
t0 = time.time()
pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sd-turbo", torch_dtype=torch.float32)
rep.write(f"carregou em {time.time()-t0:.0f}s\n"); rep.flush()
p = "cute chibi anime boy hero, spiky black hair, green hooded cape, huge orange explosion behind, vibrant colors, bold outlines, anime illustration"
for i in range(3):
    t1 = time.time()
    img = pipe(p, num_inference_steps=2, guidance_scale=0.0, width=512, height=512, generator=torch.Generator().manual_seed(i)).images[0]
    img.save(f"{OUT}/sd_{i}.jpg"); rep.write(f"img {i}: {time.time()-t1:.0f}s\n"); rep.flush()
rep.close()
