---
title: verificar un filtro traducido es contar filas, no leer el chip
date: 2026-08-14
source: claude-code-session
tags: [testing, i18n, ui, agent-browser]
---

Al traducir a español los enums de la BD en una barra de filtros hay DOS fallos posibles, y el
barrido de texto sólo ve uno:

- **Visible**: un identificador crudo (`won`, `churned`) llega a la pantalla. Lo caza cualquier
  `grep` sobre `innerText`.
- **Invisible, y peor**: el texto se traduce bien pero el VALOR que viaja a la URL/servidor deja de
  coincidir. El chip pinta «Estado es Ganado», la URL parece razonable, y el listado **no filtra**.
  Un lector de pantalla o un barrido de texto dan verde.

Método que sí lo distingue: elegir dos valores que TIENEN que dar resultados distintos y contar
filas. `Ganado → f=status:in:won → 0 filas` y `Abierto → f=status:in:open → 4` prueban que el
predicado se aplica. El control que remata: la misma URL con un id inexistente → 0 filas (si diera
las mismas filas, el filtro se estaba ignorando).

Vale para cualquier mando cuya etiqueta y cuyo valor viven en sitios distintos, no sólo enums.
