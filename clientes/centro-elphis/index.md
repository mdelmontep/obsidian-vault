---
title: Centro Elphis — HUB
date: 2026-05-18
source: investigación 10 agentes + decisiones Manu
tags: [cliente, agentesia, elphis, voz, whatsapp, retell, clientify, doctoralia, n8n, dokploy]
---

# Centro Elphis

Centro de tratamiento de adicciones en Madrid. Cliente Agentesia: paquete voz + chat + CRM + agenda.

## Datos del cliente

- Web: https://centroelphis.com
- Sede: C/ O'Donnell 32, Bajo C, 28009 Madrid
- Teléfono público 24h: **659 877 708**
- Doctoralia: https://www.doctoralia.es/clinicas/centro-elphis (52 reseñas, 5.0)
- Instagram: @centroelphis (1.1k, muy activa)
- Modalidades: ambulatorio · centro de día · residencial (partners) · online
- Adicciones cubiertas: alcohol, cocaína, benzo, ludopatía, compras, sexo, trabajo
- Equipo: terapeuta + psicóloga + psiquiatra colaborador externo
- Conversión clave: **primera cita gratuita** (CTA recurrente)
- Audiencia: ~50% paciente, ~50% familiar (el bot debe distinguir y adaptar)
- Posible nicho LGTBI+ (mencionado en listados terceros como loottis.com)

## Documentos

- [[contexto-cliente-elphis]] — perfil, tono, audiencia, datos para personalizar bots
- [[arquitectura-elphis]] — stack completo, single source of truth por entidad, diagrama
- [[agente-voz-elphis]] — diseño Retell, tools, anti-alucinación, edge cases
- [[chatbot-whatsapp-elphis]] — Chatwoot + 360dialog + handoff humano + plantillas HSM
- [[workflows-n8n-elphis]] — catálogo workflows + Postgres auxiliar + smoke tests
- [[dokploy-deploy-elphis]] — stacks, orden, rollback, coste
- [[bloqueantes-elphis]] — 8 inputs pendientes con el cliente
- [[ADR-001-doctoralia-google-calendar]] — por qué GCal y no API Doctoralia

## Estado actual (2026-05-18)

- Fase de **diseño + arquitectura cerrada**.
- Repo local: `/Users/manueldelmonte/elphis/` con `CLAUDE.md` operativo.
- Pendiente: confirmar 8 bloqueantes + arrancar Fase 0 Dokploy.

## Relacionado

- [[clinica-zen]] — patrón replicable previo (Retell + Kommo + n8n). Aquí cambia: Clientify en vez de Kommo + Chatwoot + GCal.
- [[agentesia]] — agencia.
