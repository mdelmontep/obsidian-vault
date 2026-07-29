---
title: aviso de un módulo sin gatear por su feature es ruido con pinta de error
date: 2026-07-29
source: claude-code-session
tags: [ux, frontend, feature-flags, soporte, saas]
---
Un panel que menciona el comportamiento de OTRO módulo (recordatorios, envíos, automatismos)
debe gatearse por la feature de ese módulo, no solo por el contexto de la pantalla. Si no, la
org que no lo tiene contratado ve un warning con icono de alerta y CTA describiendo algo que
nunca puede pasarle: lo lee como "algo va mal en mi ficha" y abre ticket.

Regla: **gatea con el MISMO criterio que el consumidor real**. Mira quién lee el dato aguas
abajo (aquí el cron: `org_features.feature_id='cobros' AND enabled`) y usa ese predicado
(`hasFeature`), no uno más laxo (`moduleEnabled`, que también da true para módulos en beta
global aunque la org no lo tenga). Un gate más laxo que el consumidor reintroduce el ruido.

Síntoma para detectarlo antes del ticket: el aviso vive en una pantalla de un módulo (agenda,
ficha) y habla de otro. Ahí siempre falta un gate.

Caso real TuFacturaIA 2026-07-29 (ticket #103, PR #1348): el aviso del teléfono del contacto
hablaba de recordatorios WhatsApp a una org sin Cobros. Ver [[verificar-en-ui-promete-envio-de-codigo-si-es-autodeclaracion-di-confirmar]].
