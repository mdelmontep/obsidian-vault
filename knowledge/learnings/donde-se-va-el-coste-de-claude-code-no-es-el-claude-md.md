---
title: el coste de claude code está en el tamaño de sesión, no en el CLAUDE.md
date: 2026-08-20
source: claude-harness
tags: [claude-code, coste, contexto, harness]
---

Medido sobre 14 días de transcripts propios (`~/.claude/projects/**/*.jsonl`, 271 sesiones, 105.467 llamadas API):

- **77 % del gasto es cache-read**, 12 % cache-write, 11 % output.
- **91,4 % de ese cache-read ocurre con el contexto por encima de 200k**, y 61,7 % por encima de 400k. Contexto medio: **357k por llamada**.
- El arnés entero (CLAUDE.md global + 99 skills + agentes + plugins + hooks) era ~22-28k tokens sobre un suelo de harness de 22.122 → **~5 % del gasto**.

Regla de conversión útil: **1.000 tokens fijos en el prompt de sistema = 105M tokens de cache-read en 14 días**. Y cada token que entra en contexto se paga **una vez por cada llamada API que quede de sesión**: un `Read` de 5k tokens en la llamada 100 de una sesión de 2.000 cuesta 9,5M de cache-read.

La intuición dice "recorta el CLAUDE.md" y es la palanca equivocada por un factor de ~40. Lo que cuesta es no cerrar sesiones. Orden correcto: `autoCompactWindow` + `/clear` entre tareas + delegar output verboso a subagentes; **después**, el prompt fijo.

Cómo medirlo en cualquier máquina: agregar `message.usage` de los `.jsonl` por sesión, y comparar el primer request con y sin cada componente (`--disable-slash-commands`, `--setting-sources project`, copiar un CLAUDE.md a un proyecto de prueba).

Ver [[statusline-mide-el-contexto-sobre-la-ventana-y-con-1m-no-avisa-nunca]] · [[claude-code-project-rules-no-se-comparten-si-claude-gitignored]]
