---
title: pr grande con migración o bucket privado — checklist antes de mergear
date: 2026-05-02
source: claude-code-session
tags: [github, deploy, seguridad, supabase]
---

Antes de mergear un PR de seguridad/infra que toque cualquiera de estos:

- Migración de schema con data conversion (ej: `documento_url` → `documento_path` para 40 filas en prod).
- Cambio de visibilidad de bucket de Storage (público → privado).
- Eliminación de endpoints público-internos (`/api/generate-pdfs`, etc).
- Modificación de endpoints en uso productivo (`/api/voice/generate`, OCR de email).

Checklist mínima:
1. Contar filas de prod afectadas por la conversión (`SELECT count(*) ...`).
2. Buscar consumidores externos del endpoint a eliminar — workflows n8n, crons Dokploy, scripts, URLs en emails ya enviados al cliente.
3. Plan de rollback explícito: snapshot BD + backup bucket.
4. Lint/typecheck/build local sobre el merge result (test merge en branch temporal).

"Sin CI" no justifica saltarse pasos — exige más cuidado, no menos. Una sesión de cierre no es el momento de mergearlos: dejar abierto y abordar en sesión dedicada con plan completo.
