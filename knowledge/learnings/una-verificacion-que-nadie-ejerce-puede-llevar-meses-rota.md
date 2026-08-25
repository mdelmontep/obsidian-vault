---
title: una verificación que nadie ejerce puede llevar meses rota sin una sola alerta
date: 2026-08-25
source: agency-portal
tags: [webhooks, hmac, observabilidad, gotcha]
---
La verificación de firma del webhook de Retell del portal rechazaba el **100 %**
de las firmas reales desde el 22-jun (commit `4b3b628`): al desaparecer
`lib/webhook_auth` en el SDK 5.38 se reescribió a mano firmando **solo el
cuerpo**, y la fórmula real es `cuerpo + timestamp` — ver
[[retell-webhook-firma-hmac-body-mas-timestamp]].

Dos meses sin una alerta, y no por falta de logs: **desde el 5-may ningún agente
manda webhooks**, así que la rama rota no se ejecutaba. Lo que lo delató no fue
un error, fue un recuento por fuente: 2.539 filas `scheduled_sync` contra 105
`webhook`. Un camino que ya no recorre nadie no se rompe con ruido, se pudre en
silencio.

Regla: en una integración con dos vías (webhook + cron de reconciliación), la
proporción entre ambas **es una señal de salud**, no un dato de color. Si la vía
de tiempo real cae a cero y el cron lo tapa, nadie se entera hasta que el cron
falla también. Y al anclar el fix, hazlo con un vector del SDK oficial en un test
—reproducible en CI— antes que con una captura en vivo que caduca.
