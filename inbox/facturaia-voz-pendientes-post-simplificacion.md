---
title: facturaia voz pendientes post simplificacion
date: 2026-04-26
source: claude-code-session
tags: [facturaia, voz, whatsapp, pendientes]
---

# FacturaIA — Pendientes tras simplificación workflow de voz

El workflow de voz funciona e2e (audio → agente → resumen → botones → confirmar → factura + PDF por WhatsApp). Pendientes antes de considerar producción:

## CRÍTICO
- **Verificar que funciona para TODAS las orgs** — no solo la de test. Cada org debe:
  - Ser detectada correctamente por el lookup de org (matching por número remitente)
  - Tener su `template_config` cargada para que el PDF use la plantilla seleccionada
  - El PDF debe subirse al bucket correcto de Supabase Storage (`{org_id}/factura/{num}.pdf`)
  - El `documento_url` debe actualizarse en la factura de la org correcta
- **Comprobar que OCR facturas recibidas sigue funcionando** — el workflow receptor v2 reemplazó el v1, la rama de imagen/documento NO se ha testeado con el nuevo workflow
- **Verificar rama presupuestos** — solo se ha testeado facturas, no presupuestos (`tipo: 'presupuesto'`)

## IMPORTANTE
- **Mejorar textos de los mensajes WhatsApp** — actualmente son genéricos:
  - Resumen: formato básico con emojis, podría ser más profesional
  - Confirmación: "Factura X creada correctamente. Ya la puedes ver en tu dashboard." — añadir total y link directo
  - Error: mensajes genéricos que no ayudan al usuario
  - Caption del PDF: "Factura generada por voz." — incluir número y total
- **Actualizar manuales usuario y admin** con el flujo de voz simplificado

## LIMPIEZA
- Limpiar facturas/presupuestos duplicados creados durante testing en la BD
- Eliminar campo `pdf_error` del response de `/api/voice/generate` cuando sea estable
- Eliminar campo `detail` del error de series (debug temporal)
- Desactivar/archivar sub-workflows antiguos en n8n (Voice Process, Voice Confirm, Voice Correct)
