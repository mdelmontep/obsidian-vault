---
title: si el front lee `detail || error || 'frase'`, el transporte derrota al copy revisado
date: 2026-08-23
source: facturaia
tags: [copy, api, errores, frontend]
---
El backend manda el mensaje interno en `detail` y el front lo pinta con
`setError(j.detail || j.error || 'No se pudo …')`. Con `detail` primero, un 500
enseña el error de Postgres y la frase escrita para el cliente solo sale cuando
el backend no manda nada: el orden del `||` decide quién gana, no quién revisó
el texto. No es fuga en algunas pantallas — gana en todas por construcción.

Medido en facturaia (#2131): emisor único del 500 en `src/lib/api-error.ts`,
162 `detail: <err>.message` a mano, **39 call sites en 31 ficheros**.

Fix: no invertir el `||` en cada sitio. Extraer la función que ya existía en
casa (`humanizeError` de `admin/system/email-logs-panel.tsx`: catálogo por
código → familia → `raw` de último recurso) y llamarla. Dos trampas: el
catálogo va **por superficie** (API y copiloto comparten enum con textos
distintos a propósito), y el nombre visible de un estado se toma de su fuente
única — `EstadoPill`, no tecleando el identificador (`sin_aprobar` se filtraba
a un contrato público y al chat del cliente).
