---
title: verificar comportamiento real de api antes de creer al integrador
date: 2026-05-20
source: claude-code-session
tags: [api, integraciones, debugging, zod]
---

Cuando un equipo externo dice "vuestra API hace X" (acepta, ignora, valida), no
tomarlo como hecho.

Caso real PR #49 TuFacturaIA (2026-05-20): el portal (Borja) afirmó "la API ignora
el campo extra `descripcion` sin romper". El Zod `lineaSchema` tenía `.strict()`
→ estaba devolviendo `400 unrecognized_keys` en cada request. Comían 400s
silenciosos o no habían llegado a probar.

Patrón antes de planificar cambios sobre una integración:
1. Grep el schema de validación del endpoint en cuestión (Zod `.strict()`,
   Pydantic `extra='forbid'`, JSON Schema `additionalProperties:false`).
2. Lanzar 1 curl real con el payload exacto que dicen mandar.
3. Mirar logs server-side, no solo la response del cliente — pueden haber 400s
   que el portal traga.

Coste 5 min. Evita planificar contra premisa falsa y descubrirlo en producción.
