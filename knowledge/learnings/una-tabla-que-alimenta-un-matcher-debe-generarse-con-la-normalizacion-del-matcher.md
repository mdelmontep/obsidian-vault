---
title: una tabla que alimenta un matcher debe generarse con la normalización del matcher
date: 2026-09-09
source: simarro
tags: [n8n, supabase, sync, matching, simarro]
---
Cron nuevo que rellena `agents` desde las agendas de Google Calendar: yo generaba la clave con el
**nombre completo** normalizado (`javier villalba ranz`). Pero el consumidor —la RPC
`resolve_property_calendar`, que busca el agente dentro de la descripción de Idealista— matchea
cuando **todas las palabras de `agent_key` aparecen** en el texto. Con la clave larga, "agente:
Javier" no habría casado con nada: cada agente nuevo habría entrado en la tabla y **ninguna vivienda
suya habría resuelto a su calendario**, sin un solo error. Las 8 filas históricas usaban nombre de
pila, hechas a mano; nadie lo había escrito.

Regla: antes de automatizar el poblado de una tabla, **medir empíricamente cómo consume la clave
quien la lee** (aquí: 9 variantes del mismo nombre contra la RPC) y generarla igual. Y cuando la
clave corta colisiona (dos "Carlos"), **reportar la colisión, nunca desempatar por tu cuenta** — un
alias inventado rompe el matcher del mismo modo, solo que más tarde.

Ver [[n8n-un-nodo-sin-items-de-entrada-no-corre-y-corta-la-cadena-hasta-el-aviso]] · [[agrupacion-por-campo-texto-libre-exige-normalizacion-en-write-path]]
