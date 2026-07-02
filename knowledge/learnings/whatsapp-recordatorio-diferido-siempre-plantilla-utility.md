---
title: recordatorio/notificación programada por whatsapp → siempre plantilla utility
date: 2026-07-02
source: claude-code-session
tags: [whatsapp, meta, recordatorios, plantillas]
---

WhatsApp Cloud API: fuera de la **ventana de 24h** (la abre un mensaje entrante del
usuario) solo se pueden enviar **template messages**; el texto libre falla (131047
re-engagement / 131026 undeliverable). **No hay endpoint** para saber si estás dentro de
la ventana — solo el `timestamp` del último inbound, que tendrías que trackear tú.

Patrón para recordatorios/notificaciones **programados** (que casi siempre disparan fuera
de la ventana): **asumir el peor caso y usar SIEMPRE plantilla** (funciona dentro y fuera).
Evita trackear `last_inbound_at`. Categoría **UTILITY** (no marketing/auth): recordatorio
pedido por el usuario, no promocional — gratis dentro de ventana, tarifa utility fuera.

La plantilla es **config, no texto**: `template_name` + `language_code` + params `{{n}}`
ordenados, pre-aprobada por Meta. El sistema guarda eso, no la frase. Canales sin ventana
(Telegram) → texto libre. Sanear params (Meta rechaza `\n` o 4+ espacios seguidos).
