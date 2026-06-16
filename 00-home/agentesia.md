---
title: agentesia
date: 2026-05-07
tags: [cliente, agentesia]
---

# Agentesia (interno)

La empresa. agency-portal + ticketing chatbot + integración con TuFacturaIA + Slack canvases.

## Estado

- **agency-portal** (Borja como reviewer) — Next.js, integra con TuFacturaIA via API v1 (HMAC webhooks + outbox + Stripe-style sync)
- **Chatbot ticketing** desplegado en `89B9QN23hOHDq6oP` n8n
- **Slack workspace** activo, canvases por proyecto

## Próximos hitos

1. **agency-portal PR #86 + #87 — review Borja + deploy** (NOW) — #86 hotfix: la llamada a OpenAI en el onboarding no estaba en try/catch → un fallo tumbaba el webhook con 500 silencioso y el bot quedaba mudo; ahora degrada + audita `onboarding.llm_call_failed`. #87 feature: módulo "secretaría virtual con jerarquía" para HGH Ibérica (asistente interno por comercial + visibilidad del responsable sobre su equipo), validado con dry-run real. Independientes, 4 checks verdes. Detalle [[Stack/onboarding-whatsapp]]
2. **agency-portal PR #54 + #55 pendientes pushear** (NOW) — #55 audit actor passthrough, #54 base lista. Tras merge: regen types.gen.ts + quitar 3 `as never` + migration `quotes.converted_facturaia_factura_id`
3. **agency-portal PR #72 onboarding sync+md+web — smoke pendiente** (NOW) — primer onboarding WhatsApp cerrado (ecobox) destapó tres bugs: sync no escribía nada, `.md` perdía info, bot no preguntaba web pese a estar en notas. Fix en rama `fix/onboarding-sync-and-md-fidelity`. Smoke en próximo cliente real. Detalle [[Stack/onboarding-whatsapp]]
4. **agency-portal PR #73 factura nueva prerellena fiscal del cliente — smoke pendiente** (NOW) — al crear factura desde detalle de cliente o vía combobox de destinatario, el bloque "Datos fiscales · Destinatario" salía vacío aunque el cliente tenía los 6 campos guardados (razón social, NIF/CIF, dirección, ciudad, CP, país). `page.tsx` cargaba `getAgencyClientDetail` pero sólo pasaba name/email al form; combobox tampoco copiaba `recipient.fiscal` aunque venía cargado. Fix: pasar `FiscalData` y phone vía `defaultRecipient`, inicializar `recipientFiscal` desde ahí, y en `handleRecipientChange` copiar fiscal + abrir collapsible. Detalle [[Stack/agency-portal-forms-prefill]]
5. **Test ticketing con cliente real** (NEXT) — pedir teléfono al cliente "Soporte técnico" + verificar respuestas TICKET_CREATED/APPENDED/ERROR_NO_CLIENTE. Limpiar workflow temporal `a96XVFKX4WujMCKW`

## Bloqueos / esperando a terceros

- Borja: review PR #54 y #55 cuando se pusheen
- Borja: review PR #86 (hotfix onboarding 500) y #87 (secretaría virtual HGH) → desplegar tras merge

## Links rápidos

- [Github org](https://github.com/AgentesIA-MAdrid)
- [agency-portal](https://github.com/AgentesIA-MAdrid/agency-portal)
- Slack #pro-facturaia, #pro-agentesia
- Canvas Panel TuFacturaIA: F0AV38CHYSJ

## Histórico de hitos

- 2026-05-02: integración API v1 ↔ agency-portal viva en prod (7 PRs apilados + 7 fixes auditoría)
- 2026-06-16: onboarding WhatsApp caído — cuenta OpenAI sin saldo (`429 insufficient_quota`) → webhook 500 silencioso, bot mudo. Diagnóstico vía ejecuciones n8n. Recargado el saldo (revive sin deploy) + PR #86 para que no muera en silencio. Feature secretaría virtual HGH (PR #87) lista y validada con dry-run.
