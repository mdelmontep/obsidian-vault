---
title: un grep negativo por el nombre del origen es ciego a un renombrado en la frontera
date: 2026-08-19
source: agh-iberica
tags: [metodo, verificacion, grep, premisas-falsas]
---

AGH 19-ago. El snapshot del proyecto y el triaje de un issue daban por **medida** una premisa que
decidía el alcance de su issue hijo: «el estado ya guarda el texto de la pregunta (`lastQuestion`) y lo
que falla es que **no se proyecta** — `grep lastQuestion llm-turn-interpreter.ts` → **cero**».

El grep es cierto; la conclusión, falsa. El campo cruza la frontera **con otro nombre**:

    hitl-brain.ts:2018            pendingQuestion: state.lastQuestion,     <- aqui se renombra
    llm-turn-interpreter.ts:409   `…: "${ctx.pendingQuestion}"`            <- aqui viaja al modelo

Sin condicional: en todos los turnos. O sea que **la mitad del trabajo que el issue daba por pendiente
ya existía**, y quien lo cogiera habría construido una proyección que ya estaba.

**Fix/patrón:** un grep negativo prueba que **ese identificador** no aparece en **ese fichero**, nada
más — cualquier frontera que renombre (DTO, `TurnContext`, adaptador, `SELECT … AS`, payload) lo vuelve
ciego. Se persigue **desde el productor** (`grep -rn "state.lastQuestion" src/`) y se sigue el valor
hasta donde muere; el sitio donde mirar es el **tipo de la frontera**. Para afirmar una AUSENCIA hace
falta el camino, no una búsqueda por nombre. Y el coste: una premisa falsa dentro de un issue es más
cara que un bug, porque nadie la vuelve a medir — se hereda como dato, así que se corrige **donde vive**
(el issue, el snapshot) y no solo en la PR que la descubrió.

Familia: [[nul-byte-literal-en-markdown-hace-que-git-trate-el-archivo-como-binario]] (grep ciego por el
CONTENIDO; este, por el NOMBRE) · [[grep-classname-plano-subestima-template-literals]] ·
[[auditar-un-lado-de-par-simetrico-revisar-el-espejo]].
