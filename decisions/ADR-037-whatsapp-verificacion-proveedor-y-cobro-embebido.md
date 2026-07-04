---
title: ADR-037 — TuFacturaIA: verificación de proveedor externo por WhatsApp y proveedor de cobro embebido
date: 2026-07-04
status: accepted
tags: [adr, facturaia, whatsapp, seguridad, pagos]
---

## Contexto
Plan de consolidación WhatsApp/copiloto (post G5): (1) un tercero no-miembro puede mandar una foto de factura al WhatsApp de la empresa — hay que decidir cómo verificar que el número es realmente ese proveedor antes de autoclasificar; (2) cobro embebido en el mensaje de factura/recordatorio — hay que elegir proveedor de pago. Cerrado vía `/grill-me` autónomo (usuario delegó las decisiones recomendadas).

## Opciones consideradas — verificación proveedor
- **A — OTP al proveedor** — cierra la suplantación de raíz, pero un tercero sin cuenta no completa un flujo OTP para mandar un ticket; fricción mata la feature.
- **B — Confirmación manual del admin** — cero infra nueva, mismo patrón ya usado (`clientes.telefono_validado_at`); depende de que el admin esté atento.
- **C — Solo match por NIF extraído en OCR** — determinístico y sin fricción, pero el NIF de un proveedor real no es secreto (aparece en sus propias facturas) → spoofable.

## Opciones consideradas — cobro embebido
- **A — Stripe Connect (Standard)** — reutiliza la cuenta Stripe ya montada y el patrón de verificación de webhook del repo; cierra conciliación automática. Coste: cada org necesita onboarding Connect (KYC).
- **B — Redsys/Bizum** — más nativo en España, pero cero infraestructura existente en el repo; SDK/docs de conciliación notablemente peores.
- **C — Link genérico manual por org** — cero esfuerzo, pero no cierra el ciclo (alguien tiene que marcar cobrada a mano).

## Decisión
Verificación: **B**, con **C** como pre-filtro de UX (sugiere el proveedor si el NIF coincide, pero la confirmación del admin sigue siendo obligatoria). Cobro: **A**, Stripe Connect Standard.

## Consecuencias
- Un remitente no verificado NUNCA autoclasifica — el documento se procesa (OCR corre igual) pero queda `pendiente_verificacion_remitente` hasta que el admin confirme o rechace. Tabla dedicada `proveedor_whatsapp_pending`, no JSONB.
- Cobro embebido v1 NO incluye Bizum ni pagos parciales vía Stripe; queda como posible v2.
- Cada org que quiera cobro embebido pasa por onboarding Connect — fricción aceptada conscientemente por cerrar conciliación automática.
