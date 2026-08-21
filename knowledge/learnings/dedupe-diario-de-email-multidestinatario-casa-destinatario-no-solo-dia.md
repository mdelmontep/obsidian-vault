---
title: un dedupe diario de email multidestinatario casa destinatario, no solo día
date: 2026-08-12
source: claude-code-session
tags: [email, notificaciones, dedupe, patron]
---
Un aviso «máximo 1/día» que se manda a N buzones y dedupea GLOBALMENTE («¿ya salió hoy?»)
silencia el reintento en fallo parcial: si A recibe y B falla, el siguiente run ve la fila
`sent` de A y no reintenta a B — el retry solo funciona si fallaron TODOS. Latente mientras
N=1, explota al añadir el segundo destinatario.

Fix: el dedupe casa `(destinatario, día)` contra el log de envíos, no solo el día. Reglas que
lo acompañan: `failed` no cuenta (reabre el reintento de ESE buzón), `pending` sí cuenta
(en vuelo; el sweep de zombies lo pasa a `failed` y se reabre solo), y el «día» se calcula en
la MISMA timezone que el schedule del cron, no en UTC.

Ojo también a la idempotencia del wrapper de envío: la de `sendEmail` en FacturaIA cubre solo
5 min — no sirve de dedupe diario, solo de cinturón anti doble-click.

Caso real: cron `marketing-revision-aviso` (facturaia #1647, PR #1670); lo cazó la review de
dos ejes antes del merge, con test de fallo parcial (`T5b`).

Corolario (21-ago, FB-09 #2034): si el contenido del email es de un PERIODO (informe semanal),
el dedupe se ata al periodo (`semana_inicio` en `payload_meta`), no al día del envío — un retry
del cron al día siguiente recalcula el MISMO periodo y el dedupe de «hoy» no ve el envío de ayer:
reenvío íntegro. La idempotency key también lleva el periodo, no la fecha.
