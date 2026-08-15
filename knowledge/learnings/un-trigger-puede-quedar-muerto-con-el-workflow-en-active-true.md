---
title: un trigger puede quedar muerto con el workflow en active true
date: 2026-08-15
source: claude-code-session
tags: [n8n, imap, observabilidad, watchdog, elphis]
---
Cuando un trigger de conexión persistente (IMAP, colas) se cae en runtime, n8n tiene **dos
caminos** y solo uno se recupera solo:

- `addQueuedWorkflowActivation` → reintenta indefinidamente con backoff. Log: *"Will try to reactivate"*.
- `handleTriggerRuntimeFailure` → **desregistra** el trigger y reintenta 5 veces
  (`TRIGGER_ACTIVATION_MAX_ATTEMPTS`). Si se agotan: `logger.error` y **nada más**. No vuelve a
  avisar (el error workflow se llama UNA vez) y el workflow **sigue con `active: true`** en la BD.

O sea: `active: true` no prueba que nadie esté escuchando, y un umbral tipo "avisar si se repite
N veces" nunca dispararía.

**La sonda es `POST /api/v1/workflows/{id}/activate`**: no es ciega — si el trigger no puede
abrir la conexión responde **400 con la causa** (`getaddrinfo ENOTFOUND ...`); un 200 prueba que
quedó registrado y conectado. Por eso un watchdog que hace desactivar → activar → releer es a la
vez reparación y verificación, sin sondas artificiales ni correos de prueba.

Exigir las **dos** condiciones: `activate` = 200 **y** `active: true` al releer — si el activate
falla, el workflow se queda desactivado, peor que al empezar.
Ver [[ejecucion-en-verde-no-prueba-el-efecto]] · [[n8n-api-activate-es-POST-no-PATCH]]
