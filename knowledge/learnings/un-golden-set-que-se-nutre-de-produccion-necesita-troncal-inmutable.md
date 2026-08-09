---
title: un golden set que se nutre de producción necesita troncal inmutable y un corte por calendario
date: 2026-08-09
source: claude-code-session
tags: [evals, agentic, metricas, calidad]
---

Cosechar casos de prueba del uso real es lo más barato que existe (el caso se **deriva** de lo que
el humano dejó: los parámetros que corrigió, la clase que puso, la acción que deshizo — nadie lo
escribe). Y es exactamente por eso que el conjunto deriva hacia lo que el modelo **ya hace**.

Tres reglas que lo cortan:

- **Troncal humano inmutable**: los casos escritos a mano, el corpus adversarial y el caso de
  "confirmación obligatoria" por cada acción destructiva no se borran, no se editan y **son la
  referencia contra la que se decide retirar algo**. Los cosechados, tope de proporción (60 %).
- **Sólo se auto-promueve lo de verdad objetiva** (invariante violado: confirmación ausente,
  inyección que escribió, cifra sin fundar). Lo de criterio va a curación humana. Promover solo lo
  de criterio ES el bucle.
- **El corte**: correr el troncal por calendario contra producción. **Troncal a la baja mientras la
  aceptación sube** es la firma del bucle comiéndose a sí mismo → congelar la cosecha (no el
  producto) y avisar.

Y dos detalles que muerden: el **juez** se fija a una versión concreta (si juez y juzgado se mueven
a la vez, la métrica se mueve sin que el producto se mueva), y un caso cosechado **lleva datos
reales del cliente** → es de su organización y no sale de ella.

Relacionado: [[una-aceptacion-no-es-senal-hasta-que-envejece-sin-ser-contradicha]] ·
[[evals-de-modelo-real-oscilan-agregar-corridas-y-baseline-con-margen]] ·
[[una-suite-de-evals-cuesta-llamadas-por-prompt-mide-el-cache-antes-de-proponerlo]]
