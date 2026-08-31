---
title: un comentario no puede afirmar el estado de un panel de deploy — y si justifica, caduca peor
date: 2026-08-18
source: claude-code-session agh-iberica
tags: [documentacion, metodo, revision-codigo, feature-flags]
---
Un comentario que **describe** código envejece; uno que **justifica** con estado que vive FUERA del repo miente, y arrastra a quien decida sobre él.

Medido (AGH #1348). `gateway-llm-client.ts` decía: *«muerde SÓLO con `READ_PRESENTER_ENABLED=true`, **hoy apagado en prod**: esto es desactivar una mina antes de que alguien encienda el flag, no arreglar un fallo vivo»*. El flag llevaba **encendido desde el 06-ago**. Peor que un comentario obsoleto: era la **premisa de una decisión RGPD abierta** (si las filas de cartera cruzan al LLM). O sea que **la decisión ya estaba tomada por acción** mientras el issue seguía debatiéndola, y quien encendió el flag no vio ninguna restricción porque su issue no la mencionaba.

- Un fichero del repo **no puede saber** el estado de un panel de deploy, de una env de prod ni de una cuenta externa. Si hay que escribirlo: **fecharlo** («al 18-ago, según el panel») o **consultarlo**, nunca afirmarlo en presente.
- Distínguelo de [[un-comentario-que-afirma-una-invariante-es-una-deuda-de-test]]: aquello se arregla con un test; esto **no se puede testear** desde el repo — el remedio es la fecha, o un gate en el arranque que lea la env de verdad.
- Un ADR **no se reescribe**: registra qué se decidió y con qué información. Se le pone la fecha y la corrección al lado.
- Y al revés: si una decisión pendiente depende de un estado externo, **mídelo antes de re-litigarla** — puede llevar semanas resuelta de hecho.

🔁 **Reincidió: 4 sitios, 2 flags (31-ago).** Corregidos los tres primeros, el cuarto seguía —y era el peor: el `CLAUDE.md`, que se carga en **cada llamada API de cada sesión**, decía «el modelo NUNCA ha visto la conversación» con `AGENT_TRANSCRIPT_CONTEXT=true` en prod. La distinción que importa: la frase que **justifica** hace que *no actúes*; la que se presenta como **premisa medida** («hechos que hay que saber ANTES de tocar el prompt») hace que **diseñes para un prod que no existe**. Y el texto viejo induce el mismo error dos veces: al verlo deduje «decisión tomada por acción» —cierto la 1.ª vez, **falso** la 2.ª (ya autorizada)—. Arreglo: **no escribir el valor, nombrar la sonda** (`docker inspect` + el issue que lo mide). Un valor en un fichero que nadie re-mide envejece solo.

Ver [[un-control-que-un-documento-cliente-facing-afirma-necesita-registro]] · [[regla-en-docstring-no-impide-nada-partir-el-interface]]
