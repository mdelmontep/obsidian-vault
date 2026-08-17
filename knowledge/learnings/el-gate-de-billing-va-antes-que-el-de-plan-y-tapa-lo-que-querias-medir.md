---
title: el gate de billing corre antes que el de plan y tapa el 403 que querías medir
date: 2026-08-17
source: claude-code-session
tags: [smoke, api, gating, facturaia]
---

Al smokear un gate de PLAN contra prod, elegí una org `is_test` en el plan barato — que es
justo el escenario a probar. Las lecturas salieron como esperaba, pero **todas las
escrituras devolvieron 402 `account_suspended`**: esa org estaba `expired`, y el gate de
billing corre **antes** en el pipeline. No medí nada de lo mío en el camino de escritura.

Al elegir el sujeto de un smoke, no basta con que cumpla la condición que quieres probar:
tiene que **pasar limpiamente todos los gates anteriores**. Mira el orden del pipeline y
comprueba el estado del sujeto en cada uno antes de gastar la corrida.

La salida que funcionó: coger una org sana (activa) y **quitarle la feature con un override
por org** en vez de buscar una org con el plan bajo. De paso confirmó que el override manda
sobre el plan.

Dos trucos que hicieron el smoke concluyente sin escribir datos:
- **Dar scopes de más a la clave a propósito**: si el 403 llega con el scope concedido,
  el corte viene del gate y no de la autorización — sin eso, los dos son indistinguibles.
- **UUID inexistente en el path**: un 404 (o un 422 de validación posterior) prueba que el
  gate DEJÓ PASAR; un 403 prueba que cortó. Se mide el gate sin tocar una fila real.

Ver [[acotar-una-api-por-scopes-no-la-acota-usa-allowlist-de-endpoints]] · [[feedback_smokes_siempre_con_agent_browser]].
