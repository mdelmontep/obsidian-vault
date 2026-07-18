---
title: mockear createDocument + smoke SQL de RPCs NO caza violaciones de CHECK del núcleo fiscal — solo el dogfood autenticado real
date: 2026-07-18
source: claude-code-session facturaia
tags: [testing, fiscal, supabase, dogfood, facturaia, gotcha]
---

Un flujo nuevo que emite vía `createDocument` puede pasar TODAS las capas de test y aun así romperse en producción por un CHECK del núcleo fiscal:

- Los **unit tests** de los endpoints **mockean `createDocument`** → nunca ejercitan el INSERT real ni sus constraints.
- El **smoke SQL** de los RPCs (reservar/confirmar/revertir contra prod) **salta `createDocument`** (es TS) → tampoco toca el INSERT fiscal.
- El **gate** (lint/typecheck/build) no ve constraints de BD.

Caso real (facturación de obra, 18-jul): el endpoint pasaba `source:'obras'` → `fuente='obras'`, que viola `facturas_fuente_check` (set cerrado sin 'obras') → "No se pudo emitir la factura". 421 tests verdes + smoke SQL verde, y aun así roto. **Lo cazó SOLO el dogfood autenticado end-to-end** (agent-browser, sesión real, factura real). Fix: clamp a una fuente válida (la procedencia ya la da `obra_id`).

Regla: un flujo que emite documento fiscal NO está validado hasta que se ha emitido UNO de verdad con sesión real (org sandbox `is_test=true` + `verifactu_entorno='pre'`). Verbo de enum/columna nuevo pasado a `createDocument` → cruzar contra el CHECK real (`pg_get_constraintdef`). Ver [[consumir-tope-y-emitir-documento-reservar-emitir-confirmar]] y [[agent-browser-click-no-dispara-handler-react]].
</content>
