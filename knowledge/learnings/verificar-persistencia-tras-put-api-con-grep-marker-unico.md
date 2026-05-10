---
title: verificar persistencia tras PUT a API con grep marker único
date: 2026-05-10
source: claude-code-session
tags: [api, n8n, ops, idempotency]
---

HTTP 200 al PUT NO garantiza que el cambio aplicó. Dos formas de fallar silenciosamente:

1. **Idempotency check defectuoso del script de patch**: si el marker para detectar "ya aplicado" coincide entre versiones (ej. cabecera del bloque), el script ve match falso → no aplica el diff → JSON enviado al PUT es idéntico al actual → server responde 200.

2. **Patch parcial**: el script aplica una parte y otra falla en silencio (try/catch tragador).

**Validación obligatoria** post-PUT:
```bash
curl GET .../resource/X | jq <campo> | grep "<marker EXCLUSIVO de la versión nueva>"
```

El marker debe ser literal único — no cabecera de bloque ni texto que aparezca en versiones previas.

**Patrón patch script**: usar `MARCADOR_EXCLUSIVO_VERSION` que solo aparece en el contenido nuevo, no en el viejo. Ejemplo:
```python
def patch(msg):
    if "MATCHING PERMISIVO (criterio):" in msg:  # marker único nuevo
        return msg
    if OLD_BLOCK not in msg:
        raise RuntimeError(...)
    return msg.replace(OLD_BLOCK, NEW_BLOCK)
```

Caso real FacturaIA: idempotency con `OLD_BLOCK[:80] == NEW_BLOCK[:80]` (ambos arrancaban "CONVERTIR_PRESUPUESTO - REGLAS CRITICAS") → patch reportó OK sin aplicar → bot seguía con prompt viejo. Detectado solo al hacer grep del marker en el GET post-PUT.
