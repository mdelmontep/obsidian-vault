---
title: un guard cuya aguja cubre una sola forma sintáctica se esquiva refactorizando
date: 2026-08-08
source: claude-code-session
tags: [guards, trinquetes, deuda-tecnica, regex, harness]
---

El trinquete de estilos en línea contaba `/style=\{\{/g`. Eso ve `style={{ … }}` y **no** ve
`style={cond ? {…} : undefined}` ni `style={fn()}`. El problema no era medir de menos (125 de 895, un
16 %): era que **sacar el objeto a una variable hacía desaparecer el estilo del radar sin quitarlo del
DOM**. Un guard que se rodea refactorizando, sin arreglar nada, no mide nada — y su verde se lee como
cobertura.

Cómo apareció: se añadió un `style={fn()}` deliberado, se documentó el `// runtime:` esperando que el
baseline subiera… y no se movió. El +1 real de ese commit lo aportaba OTRA línea. **Cuando tocas algo
que un trinquete debería contar, comprueba que el número se mueve; si no se mueve, el guard es el bug.**

Regla al escribir la aguja: apuntar al **semántico** (hay un `style=` con expresión), no a una de sus
formas. Y anclar para no cazar vecinos: `/(?<![\w-])style=\{/g` evita `data-style={x}`.

Dos consecuencias que hay que aceptar de golpe: el baseline salta (770 → 895) sin que nadie haya
añadido nada, y entran casos legítimos imposibles de migrar (`style={floatingStyles}` de floating-ui,
posicionamiento en runtime). Está bien: el baseline es un techo, no una lista de pecados.

Ver [[un-comentario-que-afirma-una-invariante-es-una-deuda-de-test]] · [[un-guard-sobre-el-minimo-no-acota-la-magnitud]]
