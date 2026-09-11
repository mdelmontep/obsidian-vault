---
title: un id que enseña un saas hay que resolverlo contra la plataforma que lo emite
date: 2026-09-11
source: laserys-las-rozas
tags: [integraciones, kommo, whatsapp, meta, debug]
---
Un panel de terceros rotula un identificador («Cuenta de WhatsApp Business → ID») y das por hecho
qué es por el rótulo. No lo es: hay que **resolverlo contra la plataforma que lo emite** — abrir el
asset por su ID o pedirlo por API — antes de afirmar nada en un ticket.

Caso Laserys (10→11-sep): anoté que el ID que mostraba Kommo era el `phone_number_id`. Falso. El
WABA era `2639880919800077` y el número `1350959428096173`; el de Kommo, `2603510696778315`, **no
corresponde a ningún activo del portfolio**. Con el rótulo por bueno, el diagnóstico iba a soporte
al revés: «vuestra UI confunde dos IDs» cuando el problema real era que guardaban un ID inexistente.

Coste de resolverlo: un minuto de UI. Coste de no hacerlo: mandar a soporte un diagnóstico falso y
gastar un ciclo de ticket (~1 día) en deshacerlo.

Ver [[el-log-de-auditoria-de-la-plataforma-duena-dice-de-que-lado-ocurrio-el-cambio]] ·
[[whatsapp-diagnosticar-numero-waba-por-graph-api]].
