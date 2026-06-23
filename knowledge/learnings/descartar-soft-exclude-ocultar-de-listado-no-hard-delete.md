---
title: accion "descartar" sobre estado soft-exclude debe ocultar del listado, no hard-delete
date: 2026-06-23
source: claude-code-session
tags: [facturaia, frontend, supabase, ux]
---
Bug real (#453): "Descartar" una recibida la marcaba `disputada` (estado de
exclusión fiscal ya respetado en reportes) pero seguía visible, ni al recargar.

Tres reglas cuando una acción de usuario "descarta" hacia un estado soft-exclude:
1. El LISTADO por defecto también debe ocultar ese estado, no solo los reportes
   agregados. El usuario lo da por borrado. Accesible vía filtro explícito.
2. El update optimista debe QUITAR la fila (`filter`), no cambiar estado in-place
   (`map`) — si no, no desaparece hasta recargar (y al recargar tampoco si el
   listado no lo excluye).
3. NO migrar a hard-delete para "que desaparezca de verdad" si hay FKs RESTRICT
   (en facturas: movimiento_factura_asignacion, stock_movimientos,
   fiscal_declaracion_snapshot, cobros_recordatorios) → 500 en pagadas/conciliadas.
Ver [[reportes-financieros-deben-excluir-estados-no-fiscales]] · [[recuperacion-ui-gated-por-estado-pierde-items-en-estado-hermano]]
