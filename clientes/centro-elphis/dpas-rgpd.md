---
title: Centro Elphis — DPAs RGPD pendientes
date: 2026-05-18
source: conversación Manu, requisito legal art. 28 RGPD
tags: [elphis, rgpd, legal, dpa, go-live, pendiente]
---

# DPAs pendientes de firmar antes del go-live

**No bloquea desarrollo. SÍ bloquea poner el bot en producción con pacientes reales.**

## Qué hay que firmar

Contrato de Encargado de Tratamiento (DPA, art. 28 RGPD) con cada proveedor externo que procese datos personales de pacientes de Elphis. Datos de salud = categoría especial (art. 9), riesgo regulatorio alto.

- Responsable del tratamiento: **Centro Elphis (KISAMU S.L., CIF B88269022)**. Firma: Enrique Sanz (administrador).
- Encargados a contratar:
  - **Retell AI** → procesa voz + transcripción. Contacto: `privacy@retellai.com`. DPA accesible en https://retellai.com/legal.
  - **OpenAI** → procesa texto del paciente para clasificación de intents (si se usa GPT en el router IA). Autoservicio: https://openai.com/policies/data-processing-addendum (se firma desde el panel del workspace).
  - **360dialog** → procesa mensajes de WhatsApp. Contacto: `dpo@360dialog.com`. Empresa alemana, suele responder rápido.

## Procedimiento

1. Solicitar template por email a cada uno.
2. Revisar (ubicación de datos UE, retención, subprocesadores, brechas).
3. Pasar PDFs a Manu → **firma Enrique Sanz**, no Borja (el responsable es Elphis, no Agentesia).
4. Archivar copia digital recuperable en Drive Agentesia, carpeta cliente.

## Estado

**Pendiente. Manu decidirá cuándo lanzar los emails — de momento no.** Recordatorio para activar antes del primer paciente real.

## Riesgo si se omite

- AEPD puede multar a Elphis (hasta 4% facturación / 20M€).
- Por contrato Elphis-Agentesia el coste cae corresponsable en Agentesia.

## Relacionado

- [[index|Centro Elphis HUB]]
- [[bloqueantes-elphis]]
- [[arquitectura-elphis]]
