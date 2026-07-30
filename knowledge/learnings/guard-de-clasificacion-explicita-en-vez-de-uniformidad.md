---
title: cuando la asimetría es correcta, el guard no exige uniformidad — exige clasificación explícita
date: 2026-07-30
source: claude-code-session agh-iberica
tags: [tests, arquitectura, metodo]
---
Un decorador se aplicaba **a mano**, item a item, en un fichero de wiring: unas lecturas envueltas y
otras no. La asimetría era **correcta** y estaba razonada en un comentario (las listas se frasean; las
fichas y la agenda se dejan literales). El problema: al ser una decisión manual en un **imán de
conflicto**, un merge combinado puede perder un `present(` y **nada falla** — el código sigue
funcionando, solo pierde una propiedad en silencio.

El reflejo malo es forzar uniformidad («que todo vaya envuelto»): rompe una decisión buena. El bueno es
**quitar la tercera opción**. El test exige que cada item esté *clasificado*: envuelto, o declarado en
una allowlist **con su motivo escrito**. Olvidarlo deja de ser posible; el criterio sigue siendo tuyo.

Tres detalles que lo hacen funcionar:
- **El motivo es el entregable**, no un adorno: es lo que hace la exención revisable dentro de un año.
  Un test que exija `reason.length > 40` evita el placeholder.
- **Guard de entradas muertas**: una exención cuyo item ya no existe deja pasar sin clasificar al item
  real que la sustituya. Se comprueba en las dos direcciones.
- **El mensaje de fallo nombra el escenario, no el hecho**: «si esto salta tras resolver un conflicto
  de X, es que se perdió un `present(` al combinar». Quien lo vea de madrugada no lo reconstruye.

Verificarlo rompiéndolo en ambos sentidos (quitar un envoltorio; declarar un exento inexistente). Un
guard que nunca se ha visto fallar es una afirmación. Ver
[[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]] · [[regla-en-docstring-no-impide-nada-partir-el-interface]].
