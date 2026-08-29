---
title: medir la ausencia de consumidor no es medir la ausencia de función
date: 2026-08-29
source: facturaia
tags: [auditoria, metodo, codigo-muerto, huerfanos]
---

Al auditar superficie huérfana, el atajo es grepear `fetch('/api/x')` en `src/` y, si sale cero,
declarar el endpoint muerto. Mide otra cosa: mide que **este repo** no lo llama.

Un endpoint sin llamador en `src/` puede tenerlo en n8n, en el servidor MCP, en el portal de
clientes, en un manual que alguien sigue a mano, o en un `curl` de un cliente que integró contra él.
En el barrido V2 de TuFacturaIA (29-ago) **seis refutaciones** compartieron ese error, y en tres el
propio carril ya tenía la prueba delante.

Lo que sí discrimina, antes de llamar huérfano a nada: grep en `src/`, en `docs/`, en
`services/`, **y una consulta de solo lectura a producción** — ¿ha escrito alguna vez en su tabla?
¿aparece en `audit_log`? ¿en los eventos de integración? Un endpoint con cero filas desde el cutover
es un huérfano medido; uno con cero `fetch()` es una hipótesis.

Corolario: el grep de un literal tampoco ve una plantilla (`/api/${tipo}/algo`). Dos de los tres
falsos positivos de ese mismo barrido salieron de ahí.
