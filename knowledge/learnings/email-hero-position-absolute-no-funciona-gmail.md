---
title: email hero overlay position:absolute no funciona en gmail
date: 2026-05-04
source: claude-code-session
tags: [email, html, css, gmail]
---

Gmail strips `position:absolute` y `position:relative`. No hay forma de superponer
elementos con CSS puro en email.

**Fix para overlay en hero**: bakear el overlay directamente en la imagen con PIL.

```python
from PIL import Image, ImageDraw
import io

img = Image.open(io.BytesIO(data)).convert("RGB")
img = img.resize((620, 262), Image.LANCZOS)
overlay = Image.new("RGBA", img.size, (255, 255, 255, 115))  # ~45% opacidad
result = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
result.save("hero_overlay.jpg", quality=90)
```

El logo se coloca encima con `valign="middle"` en tabla — no necesita posicionamiento CSS.
Resultado: imagen con overlay bakeado, compatible con todos los clientes.
