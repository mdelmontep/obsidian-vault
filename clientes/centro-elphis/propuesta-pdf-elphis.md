---
title: Centro Elphis — Propuesta técnica PDF
date: 2026-05-18
source: documento generado para Borja y Dani
tags: [elphis, propuesta, pdf, entregable]
---

# Propuesta técnica PDF · Centro Elphis

Documento interno AgentesIA enviado a Borja y Dani para validar arquitectura antes de arrancar la Fase 0.

## Archivo

- **PDF**: `/Users/manueldelmonte/elphis/Propuesta_CentroElphis_AgentesIA.pdf` (15 páginas, A4)
- **Fuente HTML**: `/Users/manueldelmonte/elphis/propuesta-elphis.html`
- **Backup pre-polish**: `/Users/manueldelmonte/elphis/propuesta-elphis.pre-polish.html`
- **Assets**: `/Users/manueldelmonte/elphis/assets/logo-full.png` + `logo-iso.png`
- **Render**: Chrome headless → PDF A4

## Identidad visual aplicada

- Logos AgentesIA versión gradient (Recurso 7 + Recurso 8): violet → cyan.
- Tipografías: **Syne** titulares · **DM Sans** cuerpo · **JetBrains Mono** IDs técnicos.
- Paleta OKLCH con neutrales tintados violeta (chroma 0.005–0.01).
- Color strategy: **Restrained** (acento gradient ≤ 10% superficie).

## Contenido del documento

1. **Portada** — eyebrow «Plan Avanzado», título, subtítulo, contexto del CRM (1.807 contactos · 1.334 deals).
2. **Cambios sobre el paquete estándar** — tabla delta vs Pollo Costco (CZ/Simarro).
3. **Datos del cliente** — extraídos del onboarding firmado: KISAMU S.L., sede, contacto, servicios + precios completos.
4. **Auditoría CRM** — pipeline IDs reales, users, limitaciones de Clientify vs Kommo. Ver [[clientify-discovery-elphis]].
5. **Agente Laura · voz y chat** — configuración derivada del onboarding (nombre, voz, saludo, desvío 3 tonos), diferenciación de interlocutor, información reservada.
6. **Handoff humano y crisis** — tres caminos: petición humano en horario (transfer SIP), notificación interna fuera de horario, crisis vital (Teléfono de la Esperanza 717 003 717). Ver [[protocolo-crisis-elphis]].
7. **Agenda y plantillas** — Google Calendar como puente con Doctoralia, recordatorios, catálogo de plantillas adaptado al vertical adicciones.
8. **Decisiones y arranque** — bloqueante (Chatwoot sí/no), confirmaciones para Alba, plan de fases.

## Polish aplicado (4 agentes paralelos)

Refinado con la skill `impeccable` · comando polish.

- **Tipografía**: escala modular 1.25, font-feature-settings (kern, liga, cv11, ss01, tnum), tracking ajustado por nivel, text-wrap balance/pretty.
- **Espaciado**: base 4pt, regla espacio-antes > espacio-después en títulos, `page-break-inside: avoid`, clases `.dense`/`.airy` por página.
- **Color**: paleta OKLCH, neutrales tintados, bans eliminados (side-stripe borders, gradient text en h1, hero-metric template).
- **Microtipografía**: 0 em-dashes restantes, comillas españolas «», `&nbsp;` en teléfonos y unidades, en-dash en rangos, slop eliminado.

Detalle de los patches: `/tmp/polish-agent-typography.css`, `/tmp/polish-agent-spacing.css`, `/tmp/polish-agent-color.css`, `/tmp/polish-agent-microtype.md`.

## Decisión que el documento solicita

Una sola que bloquea el arranque:

- **Chatwoot self-hosted en Dokploy como inbox WhatsApp y handoff humano** (recomendado) frente a otra solución de bandeja.

Lo demás son confirmaciones operativas (Alba) o pre go-live (Enrique). Ver [[bloqueantes-elphis]].

## Cómo regenerar el PDF

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf-no-header \
  --print-to-pdf="/Users/manueldelmonte/elphis/Propuesta_CentroElphis_AgentesIA.pdf" \
  --virtual-time-budget=12000 \
  "file:///Users/manueldelmonte/elphis/propuesta-elphis.html"
```

## Relacionado

- [[index|Centro Elphis HUB]]
- [[arquitectura-elphis]]
- [[clientify-discovery-elphis]]
- [[protocolo-crisis-elphis]]
- [[bloqueantes-elphis]]
- [[dpas-rgpd]]
