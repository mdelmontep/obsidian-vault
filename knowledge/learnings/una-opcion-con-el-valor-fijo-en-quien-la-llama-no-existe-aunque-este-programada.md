---
title: una opción con el valor fijo en quien la llama no existe, aunque esté programada y migrada
date: 2026-08-18
source: learn-agentesia
tags: [arquitectura, deuda, gotcha, metodo]
---

Una migración creó cinco formas de generar una lección —concepto, sistema, práctica, chuleta, comparativa— y cada una cambiaba la estructura exigida al generador. Meses después, las **12 lecciones existentes eran todas del mismo tipo**.

**Causa, una línea:** `molde: 'concepto'` escrito a pelo en quien encolaba. La columna existía, el enum existía, los cinco textos existían. El llamador nunca preguntó.

**Por qué no salta.** No hay error, no hay aviso, los tests pasan: el sistema hace algo válido, siempre lo mismo. Solo se ve mirando la **distribución** de lo producido, y nadie mira distribuciones de algo que funciona.

**Cómo detectarlo barato:** `select opcion, count(*) group by opcion` sobre lo generado. Si una opción se lleva el 100 %, o sobra el resto o nadie las está eligiendo.

**Y al arreglarlo, el cabo que casi se lo traga:** el `SELECT` no traía la columna nueva, así que `t.molde ?? 'concepto'` habría seguido dando `'concepto'` para todo **sin que nada avisara** — el mismo fallo, ahora con aspecto de estar resuelto.

**Regla.** Una opción configurable no está viva hasta que hay dos valores distintos en producción. Antes de eso es código muerto con buena documentación.

Ver [[defensa-cableada-vs-codigo-muerto]] · [[el-instrumento-devuelve-cero-sin-decir-que-no-ha-medido]]
