---
title: persistir el error en su tabla no basta si ninguna superficie lo lee
date: 2026-08-06
source: claude-code-session
tags: [observabilidad, integraciones, whatsapp, proceso, agh-iberica]
---

La regla de [[integracion-en-jsonb-tabla-generica-pierde-observabilidad]] resuelve la mitad:
tabla dedicada con `status` + `last_error`/`_at`. La otra mitad —que alguien LEA esa columna— no
la garantiza el schema, y sin ella el fallo sigue siendo invisible.

Caso AGH (06-ago, #952): el digest semanal llevaba **un mes sin entregar ni un mensaje**. La
plantilla de WhatsApp no existía en Meta (`132001`). Todo estaba correctamente persistido en
`last_delivery_status='error'` + `last_error` — porque una auditoría previa había **predicho ese
escenario exacto** («si `dispatch` lanza, *template rechazado*, no hay señal durable») y añadido
esas columnas a propósito. El instrumento era el correcto y el fallo duró un mes igual. La consulta
que lo destapa cabe en una línea y nadie la había corrido nunca.

- El PR que añade observabilidad entrega también **quién la lee**: alerta, panel o consulta en el
  runbook. Sin lector, el hallazgo no está cerrado — es un log efímero con más pasos.
- Auditando una feature con entrega externa (WhatsApp, email, webhook), la **primera** consulta es
  el estado de entrega en la BD, antes de leer código: distingue «nunca funcionó» de «se degradó».
- Busca el **control que discrimina**: aquí, que los recordatorios sí se entregaban por el mismo
  dispatcher descartó credencial, sender y cola de golpe.
- **Sonda de WhatsApp Cloud API**: antes de sospechar del sender, pregunta a Meta qué plantillas
  existen — `GET /{WABA_ID}/message_templates` con el token de la propia app. Confirma el fallo desde
  el otro lado, y si el `GET` funciona el token ya tiene `whatsapp_business_management`, o sea que el
  alta también es scriptable. Todo aviso proactivo cae fuera de la ventana de 24 h → **siempre**
  plantilla aprobada, nunca texto libre.

Ver [[observabilidad-nueva-destapa-bugs-viejos-en-silencio]] · [[ejecucion-en-verde-no-prueba-el-efecto]]
