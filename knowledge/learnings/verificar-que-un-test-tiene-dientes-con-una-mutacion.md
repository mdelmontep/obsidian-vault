---
title: un test nuevo no vale hasta que le rompes el código a propósito y falla
date: 2026-07-28
updated: 2026-08-07
source: claude-code-session
tags: [testing, qa, metodo, verificacion]
---
Que un test pase no demuestra nada: puede saltarse, medir otra cosa o afirmar algo siempre cierto.
Rompe **a propósito** lo que dice vigilar y confirma el rojo. Dos minutos. Disciplina: mutar
**producción** (no el test), una por vez, revertir desde copia (nunca `git checkout --`), y dejar en
la PR qué mutación se usó y qué falló.

**La firma dominante — aserción negativa sin contraparte positiva** (AGH: 15 casos medidos, **9** así).
«No ejecuta», «cero acciones», «no contiene X» están verdes tanto si el código acierta **como si no
hace nada**. Un test llamado «re-propone» lo cumplía un brain que contestara «no te he entendido».
Arreglo: **añadir la mitad positiva** (que el outbound NOMBRE la propuesta, que el pending SIGA ahí).
Hermanas: fixture de tamaño 1 · fake **ya ordenado** (ordenar por `createdAt` == por `occurredAt` si
insertas en orden cronológico) · test **sin un solo `expect`** que cierra con un comentario · guard
cuyo escenario **no se puede construir** (mismo proveedor para escribir y leer = ciego por estructura).

**El arnés miente en las dos direcciones:**
- *Falso verde:* mutación **parcial**. Quité 1 de **4** menciones y el caso siguió 3/3. `grep -c` antes
  de romper y comprueba que llega a cero — si no, mediste tu `sed`.
- *Falso «sin víctima»*, y tiene **cuatro** causas; saltamos a la peor («no protege nada»): (1) la
  mutación no se aplicó (heredoc/comillas: el fichero nunca cambió); (2) el símbolo mutado **no está en
  el camino de ese test** (mutar `serialized-brain.ts` no tumba un test que construye `HitlBrain` a
  pelo); (3) es equivalente **solo con los datos de hoy** — tras arreglar un token, reintroducir un
  redondeo ya no tumba nada porque no queda dato en el filo, y eso se cierra con un **fixture en el
  filo**, no declarando equivalencia (ver [[un-candado-que-redondea-el-valor-que-compara-mueve-su-umbral]]);
  (4) el hueco real. Hay mutaciones **genuinamente equivalentes** (early-return por comparación consigo
  misma): ésas se **declaran por escrito**, no se cuentan como cubiertas.

Caza además el test que **se salta** sin que nadie lo note ([[e2e-smoke-skip-honesto]]) y el que mide
un artefacto vecino (el visor y el PDF son dos cosas: una perfecta y la otra rota dos meses).

**Y antes de creerte una mutación SIN víctima, sospecha del arnés: medido 3 de cada 4** (AGH, 7-ago).
Los tres modos: mutar **la aparición equivocada** del literal (el fichero cambia, pero no la línea que
importa) · apuntar a **un artefacto que esa ruta ni ejecuta** (mutar la migración cuando el bootstrap
aplica el schema) · lanzar el arnés **sin el entorno de la medición** (sin `DATABASE_URL`, contra otra
BD). La cuarta sí era del test, y era real: **no era re-ejecutable** — sembraba en la 1ª corrida lo
que la 2ª daba por hecho. Un test que solo mide la primera vez es un candado que se abre solo.
