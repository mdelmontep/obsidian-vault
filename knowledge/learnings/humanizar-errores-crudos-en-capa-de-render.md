---
title: traducir errores técnicos a lenguaje llano en la capa de render, no en el origen
date: 2026-06-27
source: claude-code-session
tags: [observabilidad, alertas, ux, patron]
---

Sistema de alertas/errores que muestra el mensaje crudo del motor (`Could not find the table…`, stack de Postgres) al usuario = aviso inútil: no dice qué pasó ni qué hacer.

Patrón: traductor SSOT `humanize(source, kind, body) → {summary, hint}` aplicado en la **capa de render** (email + panel), NO al emitir la alerta. Ventajas:
- Conservas el `body` crudo en BD para depurar.
- La mejora aplica **retroactivamente** a las alertas ya registradas — no re-emites nada.
- Matchers regex sobre el body (schema cache, columna inexistente, RLS, FK, credencial, red), con fallback genérico accionable; el `summary` incluye el endpoint/método con nombre amable.

Caso TuFacturaIA: `src/lib/system/humanize-alert.ts` (commit `e1f4fd66`) → secciones "Qué ha pasado / Qué puedes hacer" en email y `/admin/alerts`.
