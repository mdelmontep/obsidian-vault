---
title: nano banana / gemini image gen vive en ~/.claude/skills/design/scripts
date: 2026-04-16
source: claude-code-session
tags: [claude-code, skills, image-gen, gemini, nano-banana]
---

El skill `design` tiene scripts Python en `~/.claude/skills/design/scripts/{cip,logo,icon}/generate.py` que usan la API de Gemini con `response_modalities=['IMAGE']`.

## Modelos disponibles

- `gemini-2.5-flash-image` — Nano Banana Flash, rápido, default
- `gemini-3-pro-image-preview` — Nano Banana Pro, calidad, text rendering 4K

## Prerequisitos

```bash
pip install google-genai pillow
export GEMINI_API_KEY="tu-key"   # persistir en ~/.zshrc
```

Nota: `pip install` y `export` **no funcionan desde dentro de Claude Code** (sandbox bloquea modificaciones a Python global y al shell padre). El usuario tiene que correrlos él en su terminal.

## Patrón de invocación (text-to-image)

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="prompt aquí",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(aspect_ratio="9:16"),
    ),
)
# extraer: response.candidates[0].content.parts[n].inline_data.data (bytes PNG)
```

Soporta también **text-and-image-to-image** (editing) pasando `[prompt, PIL.Image]` como contents.

## Cuándo usar

Cuando un proyecto necesite:
- Screenshots/mockups fotorrealistas de producto
- Fotos de personas para landing pages (evitar stock repetitivo)
- Ilustraciones editoriales on-brand
- Iconos SVG custom (usa `scripts/icon/generate.py`)

Los scripts existentes son específicos para CIP / logo / icon. Para imágenes genéricas hay que escribir un wrapper de <40 líneas replicando el patrón de arriba.
