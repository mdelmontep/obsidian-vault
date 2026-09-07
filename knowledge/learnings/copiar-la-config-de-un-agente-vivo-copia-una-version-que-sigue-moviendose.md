---
title: copiar la config de un agente vivo copia una versión, y esa versión sigue moviéndose
date: 2026-09-07
source: elphis-psicologia
tags: [retell, agentes-voz, onboarding, configuracion, gotcha]
---
Elphis Psicología copió los knobs de audio de **Elphis Adicciones v5** el 25/08, y el repo lo
anotó como «se copia de Adicciones» — **sin la versión al lado**. Adicciones movió cuatro de
esos campos entre su v6 y su v8: `ambient_sound` a `null`, `voice_model` a `eleven_flash_v2_5`,
`responsiveness` 0,66→0,85, `interruption_sensitivity` 0,68→0,2 y `denoising_mode` a
`noise-and-background-speech-cancellation`.

Trece días después la frase del repo seguía pareciendo verdadera **describiendo algo que ya no
existía**, y el defecto salió por la vía cara: «suena embotellada» en la primera llamada real.

- Al copiar de otro cliente, **anotar la versión** junto al valor. «Es lo de X» sin versión no
  es un dato, es una fecha implícita.
- Antes de dar por bueno «esto es lo de X», pedir su config **viva** y diffear campo a campo
  (`get-agent/<id>` sin `?version` devuelve la última).
- Vale doble para `client-onboarding` y `pollo-costco`: clonan de un cliente que sigue vivo.

Ver [[create-or-replace-copiar-de-version-vigente]] · [[un-hallazgo-medido-en-otro-agente-viaja-el-mecanismo-nunca-el-porcentaje]]
