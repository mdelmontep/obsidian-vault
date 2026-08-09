---
title: un gate con ruta relativa no corre desde subdirectorio y sale verde
date: 2026-08-09
source: claude-code-session
tags: [gates, hooks, git, verificacion]
---

Cinco trinquetes del `pre-commit` de TuFacturaIA usaban `if [ -f scripts/x.mjs ]; then node scripts/x.mjs; fi`. Con un cwd que no sea la raíz del repo el `-f` falla, **se salta el bloque entero sin avisar y el hook sale 0**.

Medido, con un fichero que SÍ viola el trinquete:

    desde la raíz   → exit 1, bloquea
    desde src/lib   → exit 0, NINGUNO de los cinco llegó a correr

Git invoca los hooks desde la raíz, así que «no muerde hoy». Pero los comandos de un agente empiezan por `cd ~/wt-X &&`, y ese es el camino real por el que un guard deja de guardar. Un gate que puede degradar a no-op **en silencio** es peor que no tenerlo: el verde se lee como «medido y correcto».

Fix: `RAIZ="$(git rev-parse --show-toplevel)"` una vez, `[ -f "$RAIZ/scripts/x.mjs" ]` y la invocación con `(cd "$RAIZ" && node …)` para que el script resuelva sus baselines.

Prueba que discrimina: invoca el hook **desde un subdirectorio** con una violación real puesta. Si pasa, el gate no existe. Mismo patrón que [[hook-en-verde-que-no-dispara-en-el-camino-real]].
