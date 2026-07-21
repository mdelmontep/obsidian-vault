---
title: Centro Elphis — HUB
date: 2026-05-18
source: investigación + onboarding firmado + discovery Clientify + propuesta enviada
tags: [cliente, agentesia, elphis, voz, whatsapp, retell, clientify, doctoralia, n8n, dokploy]
---

# Centro Elphis · HUB

Centro privado de tratamiento de adicciones en Madrid. Cliente Agentesia: paquete avanzado (voz Retell + chatbot WhatsApp + Clientify).

## Estado actual · 2026-07-21

- **Bot WhatsApp real VIVO** en 659 (Cloud API). 2026-07-21: **corregidos 4 fallos reportados por Alba en `chatwoot-event` + `book-and-notify` (desplegados y verificados E2E)**:
  - **Lock del orquestador liberado tras responder** (antes se retenía 15s por la extracción CRM → el 2º mensaje se descartaba = bot mudo tras dar el nombre + nombre vacío en Clientify + "Timed out" en Chatwoot) + reintento en `locked_busy`. Ver [[lock-conversacion-liberar-tras-responder-no-tras-trabajo-post]].
  - **Enlace primera visita por canal**: chat → texto libre **vía Chatwoot** (visible en bandeja + reenvío a WA por `send_to_meta`); voz → **plantilla `elphis_cita_link`** (fuera de ventana 24h). Ver [[whatsapp-fuera-ventana-24h-requiere-plantilla-hsm]].
  - **Retraso de 90 min (19-jul) diagnosticado: fue de Meta**, no del stack (n8n "Up 3 days", Traefik "Up 2 months"; diagnóstico vía API Dokploy sin SSH → [[dokploy-api-docker-getcontainers-estado-sin-ssh]]).
- **3 plantillas HSM APROBADAS** (WABA `3949824101978503`): `elphis_notif_interna` (`1003760889245568`), `elphis_recordatorio_24h` (`1052157190679924`), `elphis_cita_link` (`2263122474525415`, MARKETING). Token Meta en `op://Elphis/whatsapp elphis token EAA/credential`.
- **Monitor del portal**: servidor Elphis dado de alta en `/agency/infrastructure` ("En línea"). Acceso SSH al host resuelto (puerto 5251; pw root en op "ssh dokploy"; clave `dokploy_portal_monitor` + m.delmonte autorizadas). API Dokploy en `op://Employee/dokploy API Elphis/credential`.
- IDs WABA/credenciales en memory [[elphis-wa-cloud-api-migracion]]. Prompt afinado (17-jul): "nuestro director", paciente/familiar, `**`→`*`, reutiliza contexto. Chatwoot: 2 cuentas recepción admin.
- **Pendientes go-live:** (1) **rotar clave RSA `dokploy` + API key Dokploy** (expuestas en chat 2026-07-21) y `META_APP_SECRET` `723c1d…`; (2) DPAs Enrique, sesión 30min crisis, número directo recepcionista (Alba); (3) migrar GCal de pruebas al de Enrique. Ver [[bloqueantes-elphis]].

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
