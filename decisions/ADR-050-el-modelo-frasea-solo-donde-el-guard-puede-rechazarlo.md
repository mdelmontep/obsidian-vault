---
title: ADR-050 — el modelo frasea solo donde el guard puede rechazarlo; donde no, la lectura se declara literal
date: 2026-08-07
status: accepted
tags: [adr, agh-iberica, llm, guardrails]
---

## Contexto
Un presenter LLM reformula la línea de introducción de una lectura ya redactada por código. Un guard
determinista (`isGrounded`) la rechaza si pierde hechos, pero solo sabe verificar **cuatro clases**:
conteo, polaridad, nombres propios y persona. Medido: puede cambiar «3 tareas **vencidas**» por «3
tareas **para hoy**» y el guard lo aprueba — otra pregunta, misma respuesta aparente.

## Opciones consideradas
- **A — ampliar la whitelist** con una regla por clase de hecho. Barata, y el `Record<Claim, Rule>`
  impide que la lista se desincronice del tipo. Pero: 4 clases en 3 semanas, y dos huecos más
  aparecieron en cinco minutos de sondeo. Rechaza «lo que ya nos mordió», no lo que puede pasar.
- **B — quitarle el lead al presenter.** Cierra la clase entera… y es **apagarlo**: el lead es lo
  único que tiene licencia para tocar.
- **C — por lectura**: la que pueda llevar un hecho no verificable declara su lead `verbatim`.

## Decisión
**C.** El mecanismo ya existía y no se usaba para esto; además corta **antes** de llamar al modelo,
así que no cuesta ni una llamada. Precio medido antes de aceptarla: de 11 lecturas, 3 pasan a
literal y **8 (73 %) siguen fraseándose** — el presenter conserva dominio real, no se apaga de tapadillo.

## Consecuencias
El criterio de aceptación es el del ADR-0005 del repo aplicado en serio: *el modelo redacta donde
existe una comprobación determinista capaz de rechazar su salida; donde no la hay, no redacta*. Una
whitelist incompleta **aparenta** cumplirlo. Queda pendiente medir la tasa real de rechazo en
producción (la señal existe y llega a las trazas; falta la credencial de API).
