---
title: las cifras exactas de un informe no avalan las que no comprobaste
date: 2026-08-28
source: claude-code-session tucrmia
tags: [subagentes, verificacion, color, apca]
---

Al remedir un informe de subagente, **verificar dos magnitudes y dar la tercera por buena** es el
hueco. Caso real (TuCRMIA, `issues/225`): sus contrastes APCA (Lc) y sus ΔE2000 reprodujeron
**exactos** con el módulo del repo. Sus ángulos de tono OKLCH, no: había **restado los dos
ángulos** en vez de medir la distancia circular, o sea el **arco largo** de la rueda — 185,3° y
259,8° donde lo cierto es 174,7° y 100,2°. La cifra derivada («3,6 veces más cerca») era 8,4.

Lo peligroso: el argumento salía REFORZADO al corregirlo, así que la conclusión no chirriaba y
nada delataba el error. Dos aciertos comprados el crédito del tercero.

- En una rueda (tono, ángulos, horas) la distancia es `min(|a-b|, 360-|a-b|)`. Una resta cruda
  parece razonable hasta que pasa de 180.
- Al remedir, medir **todas** las magnitudes que sostienen la conclusión, no una muestra.
- Y corregir donde estaba escrita: el comentario del código, la ficha y el manifiesto — no solo
  una de las tres.

Ver [[una-rampa-de-color-validada-contra-el-fondo-no-dice-si-los-pasos-se-distinguen]] y
[[subagente-reporta-hecho-codigo-que-no-existe-o-no-compila]].
