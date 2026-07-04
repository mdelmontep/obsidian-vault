---
title: no pidas elegir entre opciones que el usuario no puede probar todavía
date: 2026-07-04
source: claude-code-session
tags: [ux, onboarding, product, voice]
---

Un paso de onboarding/config que pide elegir una opción NOMBRADA que el usuario aún no puede experimentar es una elección a ciegas: no tiene criterio. Caso real: el onboarding de AGH ("Carlos", #76) pedía la voz por nombre —clara/diego/lucia— pero la síntesis (Retell #13) aún no está activa, así que nadie sabe cómo suenan.

Fix:
- Preguntar por el ATRIBUTO que sí puede decidir (voz femenina/masculina), no por el nombre interno.
- Ofrecer "me da igual" → asignar un default y dejar cambiarlo cuando la feature esté viva.
- Seguir aceptando el nombre explícito por si ya lo conoce o lo dicta.

Aplica a cualquier preferencia (voz, tema, plan, modelo) cuya vivencia real llega después. Relacionado con verificar el audio real antes de fijar voz: [[retell-custom-voice-label-no-garantiza-audio-real]].
