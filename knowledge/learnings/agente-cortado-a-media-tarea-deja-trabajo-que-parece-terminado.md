---
title: un agente cortado a media tarea deja trabajo que parece terminado y pasa el gate
date: 2026-08-13
source: claude-code-session facturaia
tags: [claude-code, subagentes, harness, metodo, verificacion]
---
Cuatro agentes murieron a la vez por límite de sesión de la cuenta (no por
fallo). El código quedó en sus worktrees y **parecía completo**. Al recogerlo:

- #1709: `syncAccountDiscountFromSubscription` escrita, importada y **nunca
  llamada**. El descuento no se persistía jamás. Typecheck y lint en verde.
- #1687: el endpoint devolvía un 409 explicando qué suscripción bloquea el
  borrado, y la UI tenía `if (res.ok)` **sin rama else**: rechazo mudo.
- #1699: daba por roto un componente correcto (ver
  [[intl-numberformat-grouping-difiere-node-icu-vs-browser-en-tests]]).

Ninguno lo habría cazado el gate: una función no llamada compila, y una rama
que falta no rompe ningún test que nadie escribió.

Al recoger trabajo interrumpido, **recorrer los criterios de aceptación uno a
uno contra el código**, no fiarse del gate ni del informe del agente. El último
mensaje del agente dice dónde se quedó y suele apuntar justo a la pieza que
falta ("ahora actualizo X para llamar a Y" = Y no se llama todavía).

Ver [[gate-parcial-a-subagentes-traslada-el-coste-al-recogedor]]
