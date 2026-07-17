---
title: Centro Elphis — Estado de bloqueantes
date: 2026-05-18
source: tras envío de propuesta a Borja y Dani
tags: [elphis, bloqueantes, todo, decisiones]
---

# Estado de bloqueantes · Centro Elphis

## ✅ RESUELTO 2026-07-17 — conexión nº real (era bloqueante desde 2026-06-30)

Negocio KISAMU verificado + cliente OK → **vía A (migración)**: borrar cuenta en la app móvil → alta OTP en WhatsApp Manager → `register` con PIN → suscribir webhook → repuntar env n8n. **659 en Cloud API + bot WhatsApp real E2E funcionando.** IDs nuevos: WABA `3949824101978503`, phone_number_id `1166319609905823`, app `1332761645647854`. Detalle en memory [[elphis-wa-cloud-api-migracion]]. Ver [[whatsapp-conectar-numero-propio-en-movil-a-cloud-api]].

**Nuevos pendientes derivados:** (1) rotar `META_APP_SECRET` `723c1d…` (expuesto en captura) + actualizar Dokploy env/`.env`; (2) plantilla HSM para reservas por **voz** (business-initiated sin ventana 24h → texto libre falla; crear Utility + rama en book-and-notify). Ver [[whatsapp-fuera-ventana-24h-requiere-plantilla-hsm]].

## Resueltos por el onboarding firmado o por decisión Manu

- Horario del centro: L-V 9-21, S 9-15, cerrado dom + festivos. Atención 24h solo pacientes en proceso.
- Servicios y precios (KB del bot): completos en el onboarding §2. Ver [[propuesta-pdf-elphis]] §3.
- Persona contacto operativo: Alba Orgaz.
- Firmante: Enrique Sanz, administrador KISAMU S.L.
- Número WhatsApp público: 659 877 708 (mismo que voz).
- Nombre y tono del agente: Laura, tuteo respetuoso, empático y cálido.
- Modelo handoff: WhatsApp interno al equipo + transferencia SIP a recepción cuando piden humano en horario.
- Agenda: Google Calendar de Enrique como puente con Doctoralia (su API está cerrada a clínicas individuales). Ver [[ADR-001-doctoralia-google-calendar]].
- Protocolo de crisis: Teléfono de la Esperanza (717 003 717) como derivación principal. Ver [[protocolo-crisis-elphis]].
- Clientify: API key + pipeline IDs descubiertos. Ver [[clientify-discovery-elphis]].
- Meta WhatsApp: arrancamos con número de pruebas Agentesia, migramos al 659 877 708 cuando esté validado.
- Google Calendar: arrancamos con calendar propio Agentesia, conectamos el de Enrique en go-live.
- Doctoralia API: descartada por ahora.

## Bloqueante real (decide el arranque)

**Chatwoot self-hosted en Dokploy como inbox WhatsApp + handoff humano**. ¿OK o preferimos otra solución? Pendiente respuesta de Borja y Dani tras lectura de [[propuesta-pdf-elphis]].

## Pendiente con Alba (no bloquea Fase 0)

1. **Spiroox**: dos admins externos (Laura Spiroox, Pepe Framis) con acceso completo a Clientify. ¿Tienen automatizaciones activas que no debamos pisar? Confirmar antes de crear custom fields o tocar pipeline.
2. **Número directo de la recepcionista**: el onboarding dice «ella tiene número propio» pero no lo escribe. Es el destino del WhatsApp interno cuando el bot deriva caso no-ingreso.
3. **IMAP `info@centroelphis.com`**: NO es cuenta Google — es email de dominio propio. Necesito host IMAP del hosting (probar `mail.centroelphis.com`), puerto y contraseña real. La que pasó Alba (`psw`) no conecta. Mientras, `doctoralia-email-sync` (n8n `3mykMD5qzQLUHDC1`) está importado pero desactivado.
4. **Formulario web**: ¿la web `centroelphis.com` tiene formulario activo hoy? ¿A dónde llegan los datos? ¿Quieren además widget de chat embebido?
5. **Meta Business Manager**: ¿cuenta API ya creada? ¿negocio verificado? (campos vacíos en onboarding §4).
6. **Custom fields Clientify**: confirmar que podemos crear los necesarios sin pisar nada. Lista mínima en [[clientify-discovery-elphis]].

## Pre go-live con Enrique (no bloquea desarrollo)

1. **Lista cerrada de triggers de crisis**: frases ambiguas tipo «estoy harto», abstinencia aguda con riesgo médico real (delirium tremens, retirada benzo), quién revisa post-llamada los disparos. Sesión 30 min antes del go-live. Ver [[protocolo-crisis-elphis]].
2. **DPAs RGPD**: Retell, OpenAI, Meta. Los gestiono yo (templates, revisión), firma Enrique como administrador KISAMU S.L. Bloquea poner pacientes reales, no desarrollo. Ver [[dpas-rgpd]].
3. **Plantillas HSM WhatsApp**: redacción final de las 6 plantillas Elphis, validar copy con Alba antes de subir a Meta. Lista en [[propuesta-pdf-elphis]] §7.

## Relacionado

- [[index|Centro Elphis HUB]]
- [[propuesta-pdf-elphis]]
- [[arquitectura-elphis]]
