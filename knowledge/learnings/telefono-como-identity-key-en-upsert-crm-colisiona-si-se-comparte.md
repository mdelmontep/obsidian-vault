---
title: teléfono como identity key en upsert de CRM colisiona si el número se comparte
date: 2026-07-22
source: claude-code-session
tags: [n8n, crm, clientify, upsert, elphis, anti-patron]
---

# Teléfono como identity key: colisiona si el número se comparte

**Caso real (Centro Elphis, `clientify-upsert-contact`):** dos contactos reales quedaron mezclados en Clientify porque el upsert matchea **solo por teléfono** y sobreescribe `first_name`/`last_name` sin comprobar si sigue siendo la misma persona (los emails, en cambio, se van sumando — nunca se pisan, así que el síntoma visible es "nombre nuevo + email viejo conviviendo"). Pasó dos veces: (1) una conversación posterior de otro familiar desde el mismo teléfono renombró el contacto; (2) `doctoralia-email-sync` mezcló dos reservas de personas distintas que compartían número.

**Por qué pasa en clínicas/centros de salud:** es habitual que un familiar reserve/escriba por el paciente, o que varias personas del mismo hogar usen el mismo móvil — el teléfono NO es un identificador 1:1 persona real, aunque en la mayoría de SaaS/CRM se trate como si lo fuera.

**Fix si se retoma:** no sobreescribir nombre a ciegas en el PATCH — si el nombre entrante difiere sustancialmente del existente, crear nota/alerta en vez de pisar, o pedir confirmación humana antes de renombrar un contacto con historial (deals abiertos).

**Aplica a**: cualquier cliente con upsert-por-teléfono en CRM (Clínica Zen, Simarro, EcoBox, Tecnocloud...) — no es específico de Elphis.

Relacionado: [[idempotencia-de-entidad-no-debe-gatear-notificacion-side-effect]]
