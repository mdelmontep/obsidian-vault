---
title: un presupuesto de reintentos fijo no distingue carga transitoria de sostenida
date: 2026-09-24
source: facturaia
tags: [harness, medicion, hooks, claude-code]
---

El driver de la línea base del gate esperaba hueco con `5 × sleep 60` antes de cada
etapa. Con 7 de 9 etapas descartadas, eso fueron **28 de sus 30 minutos durmiendo
para producir cero filas**: cinco minutos es mucho si la máquina se libera en uno, y
nada si hay tres sesiones compilando (`load1` 20 con `tsc`, `vitest` y `eslint` de
otros worktrees).

**Patrón:** un presupuesto de espera constante trata igual los dos casos que hay que
distinguir. Lo que discrimina es la TENDENCIA, no la lectura: dos descartes seguidos
ya dicen que es carga sostenida y la corrida debe abortar entera, en vez de recorrer
las etapas restantes durmiendo. Y el CSV tiene que registrar **quién** tenía la carga
(`lsof -a -p <pid> -d cwd`), o el diagnóstico se reconstruye a mano después.

Corolario de coste: media hora de reloj por nada se paga igual que media hora midiendo.
Ver [[una-lectura-de-load1-no-acredita-una-ventana-de-medida]] · [[fia-gate]].
