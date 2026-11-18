# Fábrica Pergamino

Fábrica automática de vídeos do canal **Crónicas del Pergamino** (histórias bíblicas em espanhol, cartoon, estilo "nivel por nivel").

## Como funciona

1. O Claude escreve o roteiro e as cenas de um vídeo novo em `videos/<nome>/` e envia pra cá.
2. O GitHub roda sozinho (aba **Actions** → **Gerar vídeo**), de graça:
   narração (voz Kokoro, espanhol) → cenas cartoon → música → legendas → montagem → thumbnails.
3. No fim ele grava em `saida/<nome>/info.json` o **link público do vídeo** (vale 72 h), título, descrição com capítulos, tags e comentário fixado, e as thumbnails `thumb_A.jpg` e `thumb_B.jpg`.
4. Você fala pro Claude **"publica o <nome>"** e ele publica no YouTube pelo vidIQ (sempre público).

O MP4 também fica 14 dias pra baixar em **Actions → execução → Artifacts → videos**.

## Pastas

| Pasta | O que tem |
| --- | --- |
| `fabrica/` | o motor: `pipeline.py` (etapas) e `desenho.py` (personagens e cenários) |
| `videos/<nome>/roteiro.py` | roteiro em espanhol, capítulos, título, descrição, tags |
| `videos/<nome>/cenas.py` | as cenas desenhadas e as thumbnails |
| `saida/<nome>/` | resultado: `info.json` + thumbnails |
| `temas_feitos.txt` | temas já publicados (não repetir) |

## Gerar de novo um vídeo

Aba **Actions** → **Gerar vídeo** → **Run workflow** → digite o nome da pasta (ex.: `david`).

## Rodar no computador (opcional)

```
pip install -r requirements.txt && python -m playwright install chromium
python -m fabrica.pipeline videos/david
```
Precisa de `ffmpeg` e das fontes da pasta `fonts/` instaladas.
