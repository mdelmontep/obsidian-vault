---
title: facturaia histórico snapshot 2026-08-01
date: 2026-08-01
source: claude-code-session
tags: [cliente, facturaia, historico]
---

# TuFacturaIA — retirado del NOW el 2026-08-01

Cerrado al completar la auditoría funcional (qa-035 + /admin, onboarding y multiempresa, PR #1443).
Vuelta al hub → [[facturaia]].

- 🟢 **Auditoría funcional total CERRADA: 35 issues, 41 PRs, migs 594·600·601·602·604·606 (30/31-jul)** — 400 controles con `agent-browser` sobre la sandbox `b5f86e8f`, cada cifra contra Postgres. Cerrados los 30 del recorrido más `qa-031`..`qa-034`, manuales al día y **`/fia-cierre` pasado** (0 bloqueantes; sus cabos, en #1440). Cuatro lecciones que costaron: el guard de duplicados colgaba de un flag calculado una vez y cubría **1 de 14**; la primera cifra del daño del emparejado (92 facturas) no agrupaba por organización y en clientes eran 8, con solo 2 errores; dos diagnósticos escritos en los propios issues eran falsos; y **la suite E2E llevaba meses sin ser concluyente** porque apuntaba a un puerto muerto (#1441: ahora 109/8/23, rojos clasificados en `qa-035`, uno de ellos preexistente y demostrado contra el commit anterior). `qa-032` se resolvió mirando Odoo, SAP y Business Central en vez de preguntar al cliente, y está verificado en prod. **IECE reparado** (#1437): sus 2 facturas ya cuelgan del proveedor real. Detalle → [[facturaia-historico-snapshot-2026-07-30]] · [[un-identificador-que-no-casa-tiene-que-vetar-el-respaldo-por-nombre]] · [[el-dato-canonico-vive-en-el-lote-y-el-producto-solo-siembra]] · [[un-checker-que-se-pone-rojo-por-la-razon-equivocada-es-peor-que-no-tenerlo]]
  **Queda**: `qa-035` (clasificar 5 specs E2E rojos) · `/admin` + onboarding + multiempresa **sin auditar** (falta un `is_superadmin`; prompt de continuación listo en `docs/qa/superprompt-cierre-admin-onboarding.md`, con la credencial y los guardarraíles). **#1429 CERRADO**: env puestas y verificadas en prod.

- 🟡 **Sin explicar: entrar en «Ver como esta org» dejó `active_org_id` apuntando a la org impersonada, y «Salir» no lo restauró (29-jul)** — con Borja Galván, dos horas antes, no ocurrió. No tengo la regla. Si se confirma que impersonar reescribe la org activa del superadmin, es un problema por sí solo y explicaría parte del comportamiento errático de esta zona.

> **Nota 2026-08-01 sobre el 🟡 «Sin explicar»**: queda **REFUTADO**. Entrar y salir de «Ver como
> esta org» NO reescribe `active_org_id` — verificado en producción con sesión superadmin real:
> impersonada una org `is_test`, salida por `POST /api/admin/exit-impersonation` (200), y el valor
> seguía en su sitio. Lo que sí produce el síntoma es crear una empresa DESDE la impersonación:
> `POST /api/orgs` no tiene el guard que sí tiene el PATCH, crea la org dentro de la cuenta de
> facturación del cliente y termina llamando a `switch-org`. No se reprodujo: toca Stripe de un
> cliente real.
