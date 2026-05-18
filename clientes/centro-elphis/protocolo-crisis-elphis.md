---
title: Centro Elphis — Protocolo de crisis (riesgo vital)
date: 2026-05-18
source: onboarding firmado §3 + decisión Manu post-propuesta
tags: [elphis, crisis, rgpd, protocolo, bot, regla-dura]
---

# Protocolo de crisis · Centro Elphis

Aplica cuando el usuario expresa **ideación suicida o intención de hacerse daño** en cualquier canal (voz, WhatsApp).

## Origen y evolución de la decisión

1. **Onboarding firmado por Enrique Sanz (4 mayo 2026)**: derivar a **Teléfono de la Esperanza (717 003 717)** o al **024** (línea de atención a conducta suicida). Texto literal del onboarding:
   > «Actualmente estás hablando con un agente y no podemos atender tu petición. Si te encuentras en una situación de riesgo, te pedimos que contactes con el teléfono 024 (línea de atención a la conducta suicida), 112 o te dirijas a un servicio de urgencias médicas.»

2. **Override inicial Manu (descartado)**: transferir directo al 112.
3. **Decisión final Manu (vigente)**: respetar el onboarding firmado · **Teléfono de la Esperanza es la primera derivación**, son operadores profesionales especializados en escucha emocional 24h. El 112 queda como red de emergencia general.

## Implementación en voz (Retell)

- Nodo `crisis_detected` con prioridad sobre cualquier otro intent.
- Detección por triggers (lista pendiente cerrar con Enrique, ver §triggers).
- Frase fija ≈ 2 s: *«Te paso ahora mismo con el Teléfono de la Esperanza, no cuelgues. Son profesionales especializados que pueden ayudarte.»*
- Acción: `transfer_call(destination="717003717", mode="cold")`.
- Sin filler, sin read-back, sin recoger datos.
- Post-call webhook → notifica al equipo Elphis al **659 877 708** con resumen + transcript URL para seguimiento posterior.

## Implementación en WhatsApp

Donde no hay transferencia posible, reproducir texto literal del onboarding como plantilla HSM `elphis_aviso_crisis`:

> «Actualmente estás hablando con un agente y no podemos atender tu petición. Si te encuentras en una situación de riesgo, te pedimos que contactes con el Teléfono de la Esperanza (717 003 717), el 024 (línea de atención a la conducta suicida), el 112, o te dirijas a un servicio de urgencias médicas.»

Tras enviar:
- Pausar bot (atributo Chatwoot `bot_paused=true`).
- Notificar al equipo Elphis al 659 877 708.
- La conversación queda asignada a humano.

## Triggers de crisis · pendiente cerrar con Enrique

Lista inicial propuesta (a validar antes del go-live):

- «suicidarme», «quitarme la vida», «matarme», «no quiero seguir», «hacerme daño», «tirarme», «ahorcarme», «pastillas para acabar».
- Variantes con verbos en futuro/condicional.

**Casos ambiguos a discutir con Enrique** (sesión 30 min antes del go-live):
- Frases tipo «estoy harto», «no puedo más», «no quiero seguir así», «no veo salida» · ¿son crisis o no?
- Pasado: «intenté suicidarme hace años» · ¿es crisis activa?
- **Abstinencia aguda con riesgo médico** (delirium tremens, sobredosis cocaína, retirada benzo) · ¿también van al Teléfono de la Esperanza o tienen protocolo distinto?
- Quién en su equipo revisa post-llamada los disparos para validar el corte.

## Riesgo si falla la detección

- Falso positivo: corta una conversación normal y deriva al Teléfono de la Esperanza. Coste reputacional bajo, vida no en juego.
- Falso negativo: bot sigue conversando con alguien en crisis real. Coste alto.

Sesgo de diseño: **preferir falsos positivos a falsos negativos**.

## Relacionado

- [[index|Centro Elphis HUB]]
- [[arquitectura-elphis]]
- [[bloqueantes-elphis]]
