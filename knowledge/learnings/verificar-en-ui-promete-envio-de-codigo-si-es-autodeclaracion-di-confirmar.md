---
title: "verificar" en UI promete envío de código; si es autodeclaración, di "confirmar"
date: 2026-07-29
source: claude-code-session
tags: [ux, copy, rgpd, naming, frontend]
---
"Verificar teléfono/email" significa para cualquier usuario que sale un mensaje al titular con
un código. Si tu botón solo escribe un `*_validado_at` porque alguien de la empresa declara que
el dato es correcto, el verbo miente dos veces: el usuario teme haber notificado a su cliente,
y el término tapa que **nadie ha comprobado la titularidad** (relevante en RGPD: un tercero
certifica el contacto de otro).

Regla:
- Comprobación real con prueba (OTP, doble opt-in) → "verificar".
- Declaración de quien lo marca → "confirmar", y el aviso remata con "confirmarlo no envía
  ningún mensaje". La frase que mata el ticket es esa, no la explicación del mecanismo.
- El aviso empieza por el ÁMBITO ("solo para los recordatorios de cobro: ..."), porque quien no
  usa ese módulo cierra ahí.
- Cambia el vocabulario en TODAS las superficies del mismo gate (tooltips, modales, toasts) o
  quedan dos idiomas para el mismo concepto.

Caso real TuFacturaIA 2026-07-29 (ticket #103, PR #1348). Ver [[aviso-de-modulo-sin-gatear-por-feature-es-ruido-con-pinta-de-error]].
