---
title: facturaia-decisiones-14-oct-backlog
date: 2026-10-14
source: AgentesIA-MAdrid/facturaia (tanda 2 del backlog del albarán de venta)
tags: [facturaia, decisiones, backlog, albaran-venta]
---

# Decisiones de Manuel sobre la tanda 2 del albarán de venta (14-oct-2026)

Tomadas sobre la página de decisiones del 14-oct (opciones sacadas de cada issue). Anterior: [[facturaia-decisiones-13-oct-backlog]]. Hub: [[facturaia]].

- **#3336** Reabrir un resto cerrado desde el presupuesto → **A**: hacerlo ahora: botón «Reabrir», vuelve a pendiente de servir y repone la reserva.
- **#3275 (recurrentes)** → **C**: no tocar código; documentar el límite en manual-admin §62.6 y gotchas, cubre #3340.
- **#3275 (borradores sin aviso)** → **B**: avisar al crear el borrador también por duplicar v1, Copiloto y conciliación desde presupuesto.
- **#3247** NIF con «ES» delante en el pedido en PDF → **B**: proponer la ficha como `dudosa` (la persona confirma) y corregir el aviso.
- **#3346** Reservas en la API v1 de movimientos → **A**: la v1 deja fuera `reserva` y `liberacion_reserva`.
- **#3409 sobreservicio** → **A**: una señal por presupuesto, productos en el detalle, enlaces una vez.
- **#3409 «le falta un dato»** → **A**: se deja.
- **#3409 color «Cerrado sin facturar»** → **A**: tono `ok`.
- **#3410 avisos >1024 en WhatsApp** → **C**: avisos en mensaje aparte y resumen entero con los botones.
- **#3410 «Cancelar»** → **A**: se deja.
- **#3411** Soporte apaga una beta y el cliente la reenciende → **B**: procedencia propia de bloqueo de soporte (migración del CHECK); settings responde 403 `no_modificable`.
- **#3414 coste de abono recortado** → **C**: mixto, lo devuelto con sus apuntes y el resto con el unitario del origen.
- **#3414 abono con stock apagado** → **A**: registrar siempre la línea del abono.

## Estado al cierre (15-oct)

- **28 issues cerradas** con su PR mergeado; trenes 4 (#3554) y 5 (#3557) en main.
- **Pendiente de merge (cola de facturaia-39)**: #3559 (#3410, mig 1068), #3556 (#3270 vista de compra, mig 1069), #3562 (#3474 galería, sin mig).
- **#3270 «guarda del enlace por permisos»** → **A** (Manuel, 15-oct): no aplica, porque no hay permiso de lectura por rol. Quedan #3556 y los smokes de #3259/#3271.
- **Bloqueado**: #3416 (visual-app), porque staging va por la 1054. Le faltan de la 1055 a la 1063, y el `db push --db-url` lo denegó el permiso de la sesión: lo lanza Manuel.
- **Decisión de Manuel**: alcance de #3476, borrador de smoke en Tienda Sandbox, #3552, #3560 (PDF regenerado con el nombre de hoy).
- Fuera de alcance: #3561 (movimientos a 375 px).
- Learnings: [[un-test-que-lee-el-fuente-con-readfilesync-escapa-a-vitest-related]] · [[gate-remoto-help-lanza-un-gate-y-un-fichero-sin-trackear-lo-bloquea]] · [[un-helper-de-test-que-devuelve-un-campo-homonimo-contamina-la-peticion-al-esparcirlo]] · [[una-base-de-staging-por-detras-deja-un-candado-sin-medir]].
