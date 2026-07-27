---
title: una FK ON DELETE CASCADE desde la tabla de auditoría convierte cualquier poda en borrado de la prueba
date: 2026-07-25
source: claude-code-session
tags: [postgres, auditoria, retencion, facturaia]
---

**Patrón**: `copiloto_tool_calls` y `copiloto_feedback` (auditoría de acciones que mueven dinero: emitir factura, marcar cobrada) tenían `message_id` con `ON DELETE CASCADE` contra `copiloto_mensajes`. Mientras nada borraba mensajes era invisible. Al añadir retención, la poda del historial se llevaba por delante la prueba de qué se ejecutó — pérdida silenciosa y con lectura legal, no solo técnica.

**Regla**: si una tabla es la prueba de algo, su FK hacia la tabla podable va `ON DELETE SET NULL`, nunca CASCADE. La auditoría sobrevive al dato que la originó. Corolario: **al escribir retención sobre una tabla, revisar sus FK entrantes antes que la query de borrado** — el alcance real del `DELETE` es el grafo, no la tabla.

**Migración** (562 en TuFacturaIA): resolver el nombre del constraint por catálogo (`pg_constraint`), no hardcodearlo; idempotente; y bloque de verificación al final que hace `raise` si queda algún CASCADE. Sin ese bloque, un `NOTICE` optimista pasa por verificación.

Ver [[retencion-en-tabla-compartida-por-dos-superficies-una-ventana-borra-la-otra]] · [[bandeja-staging-tabla-real-fk-restrict-borrar-sincroniza-ambos-lados]].
