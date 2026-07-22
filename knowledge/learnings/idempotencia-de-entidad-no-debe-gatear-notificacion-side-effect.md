---
title: guard de idempotencia de una entidad (deal/registro) no debe gatear el side-effect de notificar
date: 2026-07-22
source: claude-code-session
tags: [n8n, idempotencia, notificaciones, elphis, anti-patron]
---

# Idempotencia de entidad ≠ idempotencia de notificación

**Bug real (Centro Elphis, `registrar-lead`):** un guard anti-doble-deal en Clientify (`idempotency_log` key `deal-open-<contact_id>`, TTL 30 días) estaba conectado ANTES del nodo que dispara WhatsApp+email. Resultado: cualquier contacto recurrente dentro de esos 30 días (la mayoría de "llámame ahora" reales) no generaba ni deal duplicado NI notificación — el equipo no se enteraba durante hasta un mes. Además, `should_notify` dependía de `was_created` (solo true en la rama "crear deal nuevo"), así que ni siquiera la rama "mover deal existente" notificaba.

**Causa raíz:** dos ejes de idempotencia con semántica distinta compartiendo el mismo guard: (1) no crear un deal duplicado en el CRM (correcto, TTL largo, por contacto) vs (2) no reenviar el mismo aviso interno dos veces por un retry (debería ser TTL corto, por evento/mensaje). Usar el guard de (1) para bloquear (2) apaga el side-effect que el negocio sí quiere siempre.

**Fix:** separar las dos keys en la misma tabla `idempotency_log`: `deal-open-<contact_id>` (30d, gatea solo creación/movimiento de deal) y `notif-<destino>-<contacto>` (60min, gatea solo el envío WA/email, con `ON CONFLICT DO UPDATE ... WHERE expires_at < NOW()` para no bloquear para siempre si expira y no se ha purgado). El nodo de notificación cuelga de `destino !== 'none'`, no de si el deal es nuevo.

**Regla general:** antes de reusar un guard anti-duplicado existente para gatear un nuevo side-effect, pregunta "¿el TTL/scope de este guard tiene sentido para lo nuevo que quiero bloquear?". Si no, key nueva con su propio TTL — no acoples.

Relacionado: [[update-atomico-no-acopla-liberacion-critica-con-metadata-cosmetica]] · [[dedup-key-no-debe-incluir-contenido-volatil]]
