---
title: si valor del enum estado aparece como chip Y como tab tipo doc → duplicación
date: 2026-05-25
source: claude-code-session
tags: [ux, info-arch, tables]
---

Anti-patrón frecuente en tablas con multi-filter: un valor del enum **estado** se "promueve" a TAB de tipo de documento. Resultado: el user ve "Borrador" en DOS sitios (chip filtro estado + tab tipo doc), no sabe cuál seleccionar, las dos pueden contradecirse.

Caso real TuFacturaIA `/emitidas` 2026-05-25:
- Chips estado fiscal: `Sin filtrar / Borrador / Enviada / Pendiente / Cobrada / Vencida`.
- Tabs tipo doc: `Facturas (3) / Borradores (1) / Todos (4)`.

`borrador` es un VALOR del enum `estado` (mig 001), no un tipo documento aparte. Borradores son facturas en estado='borrador'. La tab confundía y duplicaba el chip.

**Resolución**:
1. **El backend dice qué es realmente** — grep el enum, no inventes dimensiones nuevas en UI.
2. Eliminar la duplicación: chip estado se queda, tab tipo desaparece.
3. Redirect legacy URL `?docview=borradores → ?estado=borrador` (backward compat con notifs/cobros/cuadres que linkean).
4. "Sin filtrar" → "Todas" (más natural).

Generalizable: cualquier tabla con tabs "By Type" donde un type colisiona con un valor del enum status → simplificar. Si necesitas distinguir tipos documentales reales (factura vs abono vs proforma) usa selector de ámbito a nivel navegación, no tabs en la pantalla principal.
