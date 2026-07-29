---
title: un nodo huérfano puede estar desconectado a propósito porque otro mecanismo ya lo cubre
date: 2026-07-29
source: claude-code-session
tags: [n8n, kommo, clinica-zen, auditoria]
---
Encontrar un nodo sin conexiones en un workflow activo invita a leerlo como un descuido —
"el agente promete un WhatsApp y ningún nodo lo envía, lo conecto". Pero la ausencia puede
ser la decisión correcta que alguien tomó antes: el efecto ya lo produce **otro sistema**
(un bot del Digital Pipeline, un trigger de BD, un cron externo) que no se ve desde el
workflow. Reconectarlo duplica el mensaje al cliente final.

Antes de conectar un huérfano, buscar el efecto en el OTRO lado y mirar su contador de uso.

Caso real (Clínica Zen): conecté `WA Confirmación Cita A/B` → salesbot `63814`. En Kommo ese
bot ya tenía **104 lanzamientos** con disparador "lead movido o creado en la etapa pENDIENTE
DE ASIGNAR" — exactamente lo que hace la rama de voz. Revertido. El contador de lanzamientos
del bot era la prueba, y no es consultable por API: hay que abrir la GUI.

Corolario: 0 lanzamientos también informa — los dos bots de recordatorio tenían 0, lo que
confirmó que nunca se habían ejecutado. Ver [[canal-nuevo-en-workflow-no-hereda-los-side-effects-de-la-rama-original]] · [[clinica-zen]]
