---
title: una aceptación no es señal positiva hasta que envejece sin ser contradicha
date: 2026-08-09
source: claude-code-session
tags: [agentic, hitl, evals, metricas, feedback]
---

Si un producto aprende de que el humano acepte lo que la IA propone, aprende del sello de goma:
una aceptación por pereza y una correcta **son idénticas en el instante en que ocurren**. Dejan
de serlo cuando el mundo reacciona. Así que la aceptación entra como **provisional** y sólo
alimenta golden set / gate / métrica cuando su ventana cierra sin contradicción:

- borrador enviado → 24 h; contradice que el humano mande un segundo mensaje corrigiéndose,
  o que el contacto señale el error;
- campo escrito por extracción → 7 d; contradice que alguien lo edite;
- cambio de estado → 24 h; contradice que vuelva atrás.

Complemento (no sustituto): **suelo físico de lectura** — longitud/250 ppm. Aceptar 900 caracteres
en 1,1 s es abstención, no positivo. Y el reloj arranca **al terminar el render**, no en la
petición: con streaming, medir desde la petición hace que todo parezca leído. Guarda las **dos**
marcas, no la resta, o no podrás descubrir que medías mal.

Señal derivada de primera clase: aceptación alta **con** contradicción diferida alta = firma sin
leer. El número que lo delata es el segundo.

Relacionado: [[gate-de-automatizacion-n50-al-95-no-sostiene-el-95-usa-cota-wilson]] ·
[[aceptar-sugerencia-hitl-debe-cerrar-decision-o-el-gate-no-abre]] ·
[[un-golden-set-que-se-nutre-de-produccion-necesita-troncal-inmutable]]
