---
title: un collector que además corre en un GET no puede emitir, solo derivar
date: 2026-08-16
source: claude-code-session
tags: [facturaia, alerts, collectors, rendimiento, escrituras-invisibles]
---

`runSystemCollectors` se invoca desde dos sitios: el cron `system-health-sweep` **y**
`GET /api/admin/alerts`. Un agente escribió un collector que emitía y resolvía incidencias dentro de
`collect()` — razonable si solo lo llamara el cron, y en la práctica **una escritura en la base por
cada apertura del panel de alertas**.

El patrón general: antes de escribir dentro de una función compartida, mirar **todos** sus llamantes,
no el que tienes delante. `grep -rn "<nombreFuncion>" src/ | grep -v "definición"` cuesta 10 segundos.

Por qué no lo caza nada: la escritura va fire-and-forget, no aparece en el TTFB, no rompe ningún test
(los tests llaman al collector, no miden cuántas veces corre) y el gate está verde. Solo lo delata
preguntarse **«¿cada cuánto corre esto?»**. Mismo fallo que en #1752, donde el cierre automático de
una incidencia lanzaba un RPC de escritura por cada render del dashboard.

Separación correcta, y conviene dejarla escrita en el propio fichero para que no vuelva: los
**collectors derivan** (devuelven el estado en vivo) y el **sweep materializa** (emite, deduplica,
emailea y cierra lo recuperado, todo junto y una vez). Fijarlo con un test que afirme que
`collect()` NO llama al emisor — es de las pocas cosas que un test puede afirmar sobre frecuencia.
