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

**15-ago: el escáner con estados TAMPOCO basta, y el mismo guard lo demostró.** Conocía cadenas y plantillas, no **literales de regex**: `const R = /[/*]/;` le abre un comentario que se come el resto del fichero, y `containsPromptMarker` devuelve `false` — o sea el guard **callado**, que es el error caro que su propio docblock declaraba evitar. Solo es exacto el **parser** (AST): entre dos tokens solo hay trivia, así que ahí un `/*` no puede estar dentro de nada. Y el barrido llegó a **nueve** despojadores a mano en un repo: cablearlos no basta —volver al naive dejaba las suites en verde—, hay que cerrar la clase con un candado sobre lo versionado, y **el detector tiene que despojar comentarios antes de escanear**, porque la prosa que explica lo prohibido casa con el patrón.

**28-ago, el caso extremo: el comentario lo escribió el MISMO cambio que añadió el guard.** Un guard de accesibilidad exigía que `mobile-header.tsx` pintara su `<h1>`. Con el `<h1>` sustituido a mano por un `<span>`, seguía dando OK — el comentario que hay justo encima, el que explica POR QUÉ tiene que ser un `h1`, contiene la cadena `<h1>` y el detector la contaba. O sea: **bastaba con documentar la regla para dejar de cumplirla**, y el guard nació ciego el día que se escribió. No lo vio ninguna revisión; lo destapó `mutate`. Todo detector sobre texto fuente **se prueba al revés** (romper lo vigilado y exigir el rojo) antes de fiarse de su verde.

Ver [[recurso-de-test-con-nombre-constante-no-aisla-entre-procesos]] · [[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]] · [[un-candado-que-vive-en-tsc-es-invisible-para-la-suite-y-para-la-mutacion]]
