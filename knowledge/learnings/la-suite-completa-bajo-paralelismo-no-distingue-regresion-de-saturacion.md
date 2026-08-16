---
title: la suite completa bajo paralelismo no distingue una regresión de una saturación
date: 2026-08-16
source: claude-code-session
tags: [tests, ci, cpu, gate, falso-positivo]
---

Tres corridas de la MISMA suite sobre el mismo árbol dieron **tres conjuntos distintos de rojos**
(1, 18 y 7 ficheros) **sin un solo fichero en común**. Los 41 implicados pasaron aislados en
segundos. La causa fue mía: solapé tres gates y dos barridos de mutación en la misma máquina.

La medida que lo deja claro: en serie, **123 s**; saturada, **11.780 s** y 18 ficheros en rojo. Un
factor 95 en duración es la señal — antes de leer el nombre del test, mira cuánto tardó.

Consecuencias prácticas:
- **Un rojo de la suite completa aquí no es evidencia de regresión.** Reejecutar aislado ANTES de
  diagnosticar; si pasa en segundos, era hambre de CPU.
- **No solapes gates.** En serie tardan menos y no mienten. Encolarlos con un semáforo (aquí
  `fia-gate`) hace esperar minutos, y eso no es un cuelgue.
- Lo que sí sobrevive a la saturación son `lint`, `typecheck` y `build`: fallan por contenido, no por
  contención. Si esos están verdes y solo la suite baila, sospecha de la máquina.

Vecino, sobre el mismo efecto en la UI: [[cpu-contencion-multisesion-falso-positivo-ui-atascada]].
