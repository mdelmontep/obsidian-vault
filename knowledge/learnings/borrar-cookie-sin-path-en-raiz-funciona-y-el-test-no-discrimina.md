---
title: borrar cookie sin path funciona en paths de un nivel y el test no discrimina
date: 2026-08-21
source: facturaia
tags: [cookies, testing, rfc6265, jsdom]
---
El default-path del RFC 6265 para una página en `/cookies` o `/registro` (un
solo nivel) es `/`: un borrado `Max-Age=0` SIN `Path=` alcanza igualmente a la
cookie escrita con `Path=/`. Consecuencia doble:
1. En prod no hay bug mientras las páginas vivan a un nivel (a dos niveles,
   `/legal/cookies`, sí se crea la cookie fantasma y la original sobrevive).
2. Un test que asierta el ESTADO final de `document.cookie` tras borrar «se
   pone verde» aunque mutes el borrado quitándole los atributos: cree
   discriminar el `Path` y no lo hace (medido con mutate: 5/5 verdes con la
   mutación viva).
Fix del test: spy sobre el setter de `document.cookie`
(`Object.getOwnPropertyDescriptor(Document.prototype, 'cookie')`) y assert de
la cadena LITERAL escrita (`nombre=; Max-Age=0; Path=/; SameSite=Lax`). Con eso
la mutación cae (víctima verificada). El comentario del test debe decir qué
capa discrimina qué: estado final ≠ atributos de escritura.
