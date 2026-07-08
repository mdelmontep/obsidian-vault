---
title: tabla pending-intent con PK por key necesita claim atómico, no select+delete
date: 2026-07-08
source: claude-code-session
tags: [whatsapp, supabase, race-condition, webhook, postgres]
---

Patrón "guarda intent → manda botones → el callback lee y borra" con una tabla `PK(phone)` (o cualquier key única) tiene ventana de carrera si dos callbacks casi simultáneos (dos taps, o Meta reintentando el webhook) leen ANTES de que ninguno borre.

**Síntoma**: dos confirmaciones distintas (o el mismo botón tocado dos veces) procesan el mismo item dos veces, o el segundo tap "reprocesa" contenido de una confirmación ya cerrada.

**Causa**: `SELECT` + lógica + `DELETE` en pasos separados no es atómico. Ambos requests leen el mismo row antes de que cualquiera lo borre.

**Fix**: condicionar el `DELETE` al contenido leído en un único round-trip y comprobar si devolvió fila:
```
.delete().eq('phone', from).eq('message', rawMsg).select('phone').maybeSingle()
```
Si `data` es null, otro request ya lo reclamó — no reprocesar, silencio.

**Bonus — abrir un lote con "owner" detection en 1 statement**: `insert ... on conflict (key) do update set items = items || excluded.items returning (xmax = 0) as is_owner`. El primer writer (INSERT real) tiene `xmax=0`; los siguientes (conflicto→UPDATE) tienen `xmax≠0`. Permite que "el primero que llega" sea el único que manda el mensaje/pregunta, sin lock explícito.

**Caso real**: `whatsapp_pending_intent`/`whatsapp_media_batch` en TuFacturaIA, PR #797 — doble tap en confirmaciones de subida de documento duplicaba la ingesta OCR.
