---
title: un UPDATE post-insert que LANZA sobre un documento fiscal ya numerado puede re-emitir en el reintento — hazlo best-effort
date: 2026-07-18
source: claude-code-session facturaia
tags: [fiscal, idempotencia, facturaia, gotcha, arquitectura]
---

Patrón peligroso: `createDocument` numera+inserta la factura atómicamente (RPC), y luego persiste campos extra (obra_id, es_intracom…) con un **UPDATE post-insert**. Si ese UPDATE **lanza** en fallo:

- El caller que orquesta (p.ej. `facturarObra`: reservar→emitir→confirmar) cae al catch → **revierte** el acumulador y devuelve **500** sobre una factura que **YA está numerada y emitida** (acto fiscal consumado, huérfana).
- Si el 500 **no se cachea** en la capa de idempotencia (la mayoría NO cachea 5xx, a propósito, para permitir reintentar fallos transitorios), un **reintento con la misma Idempotency-Key re-emite una SEGUNDA factura** → duplicado fiscal.

Regla: un UPDATE de metadatos posterior a numerar un documento fiscal debe ser **best-effort** (log, NO throw). El documento ya existe; el dato extra es reconciliable o vive redundante en otra tabla (caso obra: el vínculo también está en `obras_facturacion.factura_id`, así que la contabilidad y la anulación no se pierden; solo un listado por `facturas.obra_id` lo omitiría). Lanzar cambia una degradación rara por un duplicado fiscal.

Corolario: en el patrón reservar→emitir→confirmar, distinguir bien "la EMISIÓN falló" (revertir OK) de "un paso POSTERIOR a emitir falló" (NO revertir, la factura es real). Caso: facturación de obra, aviso /fia-cierre 2026-07-18. Ver [[consumir-tope-y-emitir-documento-reservar-emitir-confirmar]].
</content>
