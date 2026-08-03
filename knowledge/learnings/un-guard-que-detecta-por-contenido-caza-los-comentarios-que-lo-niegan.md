---
title: un guard que detecta por contenido caza los comentarios que lo niegan
date: 2026-08-03
source: claude-code-session
tags: [guards, gate, testing, evals, tooling]
---

Un guard exigía una corrida de evals (~19 $) a toda PR que tocara un fichero con `SYSTEM_PROMPT`, buscándolo con `git grep`. Marcaba **diez** ficheros; solo **cuatro** eran prompts. Tres de los otros lo mencionaban **para negarlo**: `«NO es el SYSTEM_PROMPT»`, `«no SYSTEM_PROMPT change»`. O sea, cobraba por comentarios que declaran justo lo contrario de lo que el detector concluye.

Y la cabecera del módulo afirmaba «hoy son nueve: drafter, presenter, deictic…». **La lista era falsa desde el primer día y nada la comprobaba.**

**El error de método a evitar:** sustituir la lista mala por otra lista («que los nueve detectados sigan detectándose») la habría **cementado en un test**, dejando el guard «protegido» cobrando de más para siempre. Una lista solo protege el pasado.

**Fix:** buscar una **invariante cruzada** — dos mecanismos independientes que deban coincidir. Aquí: `lo que el guard marca` == `quién emite role:"system"`. Se pone roja sola el día que alguien añada un prompt con otra variable, cosa que ninguna lista detectaría.

**Al detectar sobre texto fuente**, ignorar comentarios y anclar al contexto (asignación, llamada), no a la palabra suelta. Un guard que salta donde no debe **enseña a saltárselo**, y el día que salte de verdad nadie lo lee.

**Regex vs escáner:** pesar la asimetría. Si el falso negativo es mucho más caro que el falso positivo, el escáner con estados vale su coste — un `//` dentro de una cadena le come código real a un `replace`.

Ver [[recurso-de-test-con-nombre-constante-no-aisla-entre-procesos]] · [[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]]
