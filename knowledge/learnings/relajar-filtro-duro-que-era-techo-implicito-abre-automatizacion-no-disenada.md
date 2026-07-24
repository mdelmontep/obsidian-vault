---
title: relajar un filtro duro que además era techo implícito de un score abre una ruta de auto no diseñada
date: 2026-07-25
source: claude-code-session
tags: [scoring, matching, agentes, arquitectura]
---

En un score aditivo con umbral de auto-aplicación, un filtro duro (`RETURN 0` / `CONTINUE`) hace dos trabajos a la vez: descarta candidatos **y**, sin que nadie lo escriba, garantiza que ninguna combinación de las señales restantes alcance el umbral. Al relajarlo para ganar recall se pierde la segunda garantía en silencio.

Caso real (conciliación bancaria, señales importe 40 · fecha 10 · nº doc 35 · nombre 25 · CIF 30 · regla 30, auto a ≥80): el importe fuera de tolerancia hacía `RETURN 0`, así que ≥80 era **inalcanzable sin señal de importe**. Al convertir esa puerta en penalización graduada, `nº doc 35 + CIF 30 + regla 30 = 95 ≥ 80` **auto-marcaría una factura como cobrada desde un movimiento de importe arbitrario**. El guard anti-regresión que había protegía el número (80), no el invariante.

Patrón:
- Antes de relajar un filtro duro, calcular el **máximo alcanzable sin esa señal** y compararlo con el umbral de auto.
- Separar los dos umbrales con nombres distintos (`umbral_sugerencia` vs `elegible_auto`): la relajación aplica a generación/sugerencia, la ruta de auto conserva la exigencia.
- Codificar el invariante como condición explícita (`breakdown.senal_critica > 0`), no como efecto lateral del filtro.
- El guard de regresión debe verificar el **invariante**, no la constante.
- Penalizar en negativo, no "menos positivo": si solo bajas puntos, dos señales débiles siguen sumando más que una fuerte.

Lo encontraron dos revisores adversariales independientes desde ángulos distintos (Postgres/fiscal y record-linkage) — señal de que es un modo de fallo estructural, no un despiste. Relacionado: [[conciliacion-multi-señal-vs-importe-bruto-falsos-positivos]] · [[3-agentes-paralelos-auditoria-cambios-grandes]] · [[defensa-cableada-vs-codigo-muerto]].
