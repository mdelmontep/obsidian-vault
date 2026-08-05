---
title: una decisión pendiente sin issue no está en ninguna cola
date: 2026-08-05
source: claude-code-session
tags: [metodo, proceso, tracking]
---
La regla de «todo hallazgo que merezca issue se abre» se aplica a los **bugs** y se olvida en las
**decisiones**. Y una decisión pendiente sin issue es peor que un bug sin issue: **no se prioriza, no
se asigna, no caduca — se hereda.**

Caso real (agh-iberica, 5-ago): la decisión de política de datos que bloqueaba una fase entera del
plan llevaba **25 días** existiendo sólo como una línea de prosa en el snapshot del proyecto
(«posponer el egress al LLM») y un comentario en una épica. Cada sesión leía «bloqueado por RGPD», no
tenía dónde ver **qué** había que decidir, y seguía adelante.

El issue de una decisión necesita cuatro cosas que una línea de prosa nunca tiene:

- **La pregunta en una frase.** Si no cabe en una, son varias decisiones disfrazadas.
- **Las opciones reales**, con lo que cada una desbloquea **y cuesta**. Aquí eran tres escalones, y
  el intermedio resultó ser un cambio de configuración, no una reescritura.
- **Quién la autoriza — y qué parte NO es nuestra.** El dato era de los clientes del cliente: ellos
  responsables del tratamiento, nosotros encargados. Sin eso, la conversación se tiene con la persona
  equivocada.
- **Criterio de cierre enumerado.** Sirvió el mismo día: llegó una respuesta que contestaba **una** de
  las cuatro casillas, y el criterio evitó cerrar el issue como si contestara las cuatro.

Dos trampas que vi:
- **Separar en el propio issue lo ya decidido de lo pendiente.** Aquí se confundía con un egress
  parecido aprobado un mes antes; sin separarlo, la conversación empieza por «pero ¿no sale ya?».
- **Comprobar la frase que todos repiten.** La prosa decía «cero egress» y el código repetía lo mismo
  en un comentario, pero **ya viajaban** datos al modelo por otra vía. Negociar sobre una descripción
  falsa del estado actual es la peor clase de acuerdo.

Hermana: [[la-linea-del-gate-no-dice-contra-que-base-se-midio]] — las dos son «lo escrito no coincide
con lo que pasa, y nadie lo comprueba».
