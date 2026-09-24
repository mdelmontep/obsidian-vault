---
title: el log de un brazo no es su fichero de resultado
date: 2026-09-24
source: facturaia
tags: [medicion, harness, refutacion]
---

Al refutar un A/B había que comprobar que el brazo A ejecutó de verdad y el B no.
Medí el tamaño de `out/<par>-A` y `out/<par>-B`: **11 y 10 bytes**. Con eso la
conclusión habría sido «los dos hacen lo mismo», que es la inversa de la verdad: ese
fichero es el RESULTADO (`RUN,0,7350`), y el log es `<par>-A.log` — 136 bytes con las
dos etapas nombradas frente a **0 bytes** en B.

**Patrón:** antes de usar el tamaño o el contenido de un artefacto como prueba, hay
que confirmar cuál de los artefactos es. Un directorio de salida con `X` y `X.log`
invita al error, y el fallo es silencioso: los dos ficheros existen, los dos tienen
bytes y la comparación «funciona».

Prueba positiva correcta: el log del brazo caro nombra las etapas reales y el runner
aborta si el bloque extraído no las contiene; el log del brazo que salta pesa 0.
Ver [[un-ensayo-en-seco-que-sustituye-el-gate-no-prueba-la-medida]] · [[un-conteo-con-grep-falla-en-silencio]].
