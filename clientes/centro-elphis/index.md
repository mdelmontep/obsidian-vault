---
title: Centro Elphis — HUB
date: 2026-05-18
source: investigación + onboarding firmado + discovery Clientify + propuesta enviada
tags: [cliente, agentesia, elphis, voz, whatsapp, retell, clientify, doctoralia, n8n, dokploy]
---

# Centro Elphis · HUB

Centro privado de tratamiento de adicciones en Madrid. Cliente Agentesia: paquete avanzado (voz Retell + chatbot WhatsApp + Clientify).

## Estado actual · 2026-06-18

- **Chat WhatsApp y voz Retell funcionando E2E** con número de pruebas Agentesia (`+34 910 05 49 50`). Cerebro del bot completo (router-ia, registrar-lead, agenda, Clientify).
- **Bloqueante go-live activo · conexión del número real a Meta.** El `659 877 708` figura **"Sin conexión"** en Meta (WABA `349202490218983`, modo "App de WhatsApp Business"). Hasta conectarlo a la Cloud API **no se pueden crear las plantillas HSM**. Diagnóstico previo (tarjeta caducada, 2026-06-12) quedó OBSOLETO: la tarjeta ya es válida (VISA `*1716`), negocio Aprobado, rol OK.
- **Causa real = coexistencia sin completar.** El número se usa a diario en la app WhatsApp Business → único camino es **coexistencia** (conecta a la API sin sacarlo del móvil). Requiere escanear/confirmar desde el móvil del 659. La app "Elphis" de Agentesia NO ve este WABA (vive en otro Business `463746404062650`) → se delega al cliente vía la app del móvil.
- **Acción en curso:** email enviado a **Pablo Rubio** con paso a paso autónomo para conectarlo desde la app (Ajustes → Herramientas para la empresa → "Registrarse con Facebook"). Detalle técnico completo en `/Users/manueldelmonte/elphis/CLAUDE.md` (bloque "Bloqueante creación plantillas — REDIAGNOSTICADO 2026-06-18"). Ver [[bloqueantes-elphis]].
- **Diseño técnico cerrado.** Documentado en `/Users/manueldelmonte/elphis/CLAUDE.md` y reflejado en este vault.
- Credenciales Clientify en memory: [clientify-elphis-api](~/.claude/projects/-Users-manueldelmonte/memory/clientify-elphis-api.md).

## Datos clave del cliente

- Web: https://centroelphis.com
- Sede: C/ O'Donnell 32, Bajo C, 28009 Madrid
- Teléfono público: **659 877 708** (mismo voz y WhatsApp)
- Doctoralia: https://www.doctoralia.es/clinicas/centro-elphis (52 reseñas, 5.0)
- Instagram: @centroelphis
- Razón social: KISAMU S.L., CIF B88269022, reg. sanitario CS16658
- Director y firmante: **Enrique Sanz** («Kike» en Clientify)
- Contacto operativo: **Alba Orgaz**, +34 687 448 210, alba.orgaz@centroelphis.com
- AgentesIA owner: **Borja Chivite**, bgchivite@agentesia.madrid

## Conversión y audiencia

- Conversión clave: agendar **primera visita informativa gratuita** (30 min, con Enrique Sanz).
- ~50% de quien contacta es un familiar, no el paciente. El bot pregunta pronto: «¿La consulta es para ti, o para un familiar o conocido?».

## Documentos del proyecto

- [[contexto-cliente-elphis]] · perfil, tono, audiencia, datos para personalizar el bot
- [[arquitectura-elphis]] · stack completo, diagrama lógico, SoT por entidad, riesgos
- [[clientify-discovery-elphis]] · auditoría del CRM existente: pipeline IDs, users, limitaciones técnicas
- [[propuesta-pdf-elphis]] · entregable PDF para Borja y Dani, identidad visual, polish aplicado
- [[protocolo-crisis-elphis]] · Teléfono de la Esperanza como derivación principal, triggers, sesgos
- [[bloqueantes-elphis]] · estado completo: resueltos, bloqueante real, pendientes Alba, pendientes Enrique
- [[dpas-rgpd]] · DPAs pendientes con Retell, OpenAI, Meta (parking hasta cerca del go-live)
- [[ADR-001-doctoralia-google-calendar]] · decisión arquitectónica: GCal como puente, no API Doctoralia

## Stack en una línea

Clientify (CRM) · Chatwoot self-hosted (inbox + handoff) · Meta Cloud API (WhatsApp) · Retell + ElevenLabs castellano (voz) · n8n + Supabase dedicados en Dokploy actual · Google Calendar de Enrique como puente con Doctoralia.

## Protocolo de crisis · resumen

Ideación suicida → transferencia directa al **Teléfono de la Esperanza (717 003 717)**. WhatsApp: plantilla `elphis_aviso_crisis` reproduciendo el texto firmado del onboarding (717, 024, 112, urgencias). Ver [[protocolo-crisis-elphis]] para detalle.

## Plan de fases

0. Infra Dokploy (stacks `n8n-elphis`, `supabase-elphis`, cuenta Chatwoot Elphis).
1. agenda-service sobre Google Calendar.
2. clientify-service (upsert por phone E.164).
3. Chatbot WhatsApp MVP con número de pruebas Agentesia.
4. Agente de voz Laura (Retell + tools + post-call webhook + transfer Teléfono de la Esperanza).
5. Sync inverso, recordatorios, formulario web.
6. Hardening, DPAs firmados, validación Enrique, migración al 659 877 708 real.

Estimación: 3-4 semanas entre arranque y go-live.

## Relacionado

- [[clinica-zen]] · patrón replicable previo (Retell + Kommo + n8n). Aquí cambia el CRM y se añade Chatwoot.
- [[agentesia]] · agencia.
