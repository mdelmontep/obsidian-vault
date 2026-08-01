---
title: un control que deja dentro el test del cambio se mide a sí mismo
date: 2026-08-02
source: claude-code-session
tags: [testing, metodo, medicion, agh]
---
Para comprobar si un fix arreglaba la oscilación del gate, revertí `vitest.config.ts` al de `main`… **dejando en el árbol el test nuevo que existe para detectar esa ausencia**. Resultado: `3/3 en rojo` sin el fix, `3/3 verde` con él. Reproducible, limpio, y **completamente tautológico** — el rojo era mi propio test haciendo su trabajo.

Lo peligroso no fue el error, fue que **daba exactamente el resultado que yo quería** y se reproducía tres veces. Estuve a punto de publicar que el cambio eliminaba un fallo determinista.

- **Síntoma que lo delata:** el control falla *siempre*, no a veces. Una oscilación que se reproduce 3/3 ya no es una oscilación.
- **Regla:** el control se corre en un **árbol limpio del ref de referencia** (`git worktree add --detach origin/main`), nunca revirtiendo ficheros dentro de la rama de trabajo. Lo que no se revierte es justo lo que contamina.
- **Y mirar QUÉ falla, no cuántos.** El grep del comando se quedaba con la línea `Tests …` y me dejó sin el nombre; con el nombre delante, el error saltó a la vista en un segundo.

Control bien hecho: `main` limpio ×3 = idénticas y verdes → el fix se justifica por lo medido (doble ejecución, conteo, tiempo) y **no** por la oscilación, que quedó abierta.

Hermanos: [[comparar-en-bloques-mide-la-hora-no-el-codigo]] · [[una-etiqueta-nacida-de-un-caso-concreto-sobrevive-a-su-contexto]] · [[verificar-que-un-test-tiene-dientes-con-una-mutacion]]
