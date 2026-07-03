---
title: FacturaIA — Export gestoría v1.5 (spec/prompt de la siguiente iteración)
date: 2026-07-03
source: claude-code-session
tags: [facturaia, fiscal, export, spec]
---

Prompt entregado a Manu el 2026-07-03 (tras mergear el tren #653/#654/#657/#658). 5 workstreams, en orden; multi-agente + plan corto + OK antes de codificar; PRs pequeños apilados; auditoría 3-agentes al final + resumen ELI5.

1. **Validación Pre303 (HITL)** — generar XLSX AEAT real de FacturaIA Sandbox (2T 2026), validar offline contra plantilla LSI v9.0 (posiciones, Decimal(12,2), dd/mm/yyyy, fichero `Ejercicio+NIF@Nombre`), checklist paso a paso para que Manu lo importe en Pre303 con certificado; iterar el serializador si falla. Registrar resultado en el hub.
2. **Asientos de diario PGC** (diseño ADR-036) — columna `cuenta_contable` en clientes/proveedores (mig NNN al abrir PR) + defaults en `org_module_config` fiscal (430/400/700/600/472/477/4751) + autoasignación 430.0001… al exportar. Serializador `formato=asientos` (fecha, asiento, cuenta, concepto, debe, haber; test de cuadre debe=haber). Emitida = 430x/700x/477x (+4751x IRPF); recibida = 600x/400x/472x.
3. **Datos no capturados** — epígrafe IAE en perfil_fiscal (wizard + Settings), flag `bien_inversion` en recibidas (aprobación + editor), prorrata en perfil (default 100). Criterio de caja NO (régimen bloqueado) — solo hueco documentado. Cablear cada dato al serializador AEAT con test.
4. **IA "Revisa mi export"** — botón en Avisos (+card /informes) que abre el copiloto con los avisos como contexto y tools: completar NIF/nombre vía VIES (`src/lib/fiscal/vies.ts`), listar facturas sin líneas con deep-link, re-generar export. Patrón preview/commit; nunca modificar sin confirmación.
5. **WhatsApp fase 1** — intención "mándame el libro del 2T" → deep-link firmado de un solo uso (HMAC+TTL, patrón vincular Slack). Adjuntar fichero = fase 2 (análisis de seguridad aparte). Gate: feature fiscal + rol del user vinculado.

Referencias: `src/lib/fiscal/export/{export-contable,load-facturas-contables,aeat-libros-xlsx}.ts`, route `/api/fiscal/[ejercicio]/export-contable`, plantilla oficial parseada en la cabecera de `aeat-libros-xlsx.ts`, [[ADR-036-export-contable-libro-registro-sin-pgc]].
