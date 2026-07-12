---
title: facturaia-copiloto-siguiente-nivel
date: 2026-07-12
source: análisis estratégico + diagnóstico prod (read-only)
tags: [facturaia, copiloto, ia, roadmap, gestorias]
---

# Copiloto IA — siguiente nivel (roadmap por tiers)

Análisis de "dónde pasamos al siguiente nivel" del copiloto, ayudando a autónomos,
pymes y **gestorías**. Decisión Manuel 2026-07-12: **Tier 0 + Tier 1 en paralelo ya**;
Tier 2 (gestorías + fiscal) documentado aquí como importante-cuanto-antes.
Ver también `docs/architecture/copiloto-modelo-escalado.md` (escalado a Opus, diferido)
y el NEXT del hub (fases 1b/6). Contexto de código en [[facturaia-conciliacion-copiloto-spec]].

## Diagnóstico de adopción (prod `lahqlyaxvobqjgdiftag`, read-only, 2026-07-12)

**El motor va MUY por delante de la demanda.**
- Vida entera: **118 threads, 362 mensajes, 126 tool-calls, solo 3 orgs con acciones** —
  y las 3 son internas (AgentesiaLab, tecnocloud, Borja, AgenteIA PRUEBA). Uso real de
  terceros ≈ **cero**. Pico junio (107 msgs, casi todo pruebas), julio cayendo.
- **Telemetría a medio cablear** (columnas existen, INSERT no):
  - `copiloto_tool_calls.cost_usd` → **NULL en todas** (no medimos coste/turno).
  - `copiloto_mensajes.aborted` → **siempre 0** (nunca se escribe).
  - `copiloto_tool_calls.destructive` → **0 en 126 filas**, pero `pending_action` tiene
    **48 destructivas consumidas** → inconsistencia (ejecuciones destructivas no se
    registran bien en `tool_calls`).
  - `copiloto_feedback` → **VACÍA** (👍/👎 ni conectado en UI ni escritura; tabla+mig ya existen).
- Señales de calidad (poco volumen, pero visibles):
  - **`listarClientes` 56% OK** (bug real, la tool más rota) · `getCliente` 86% · `getFactura` 90%.
  - Gate de confirmación: **48 consumidas / 12 canceladas (20%) / 24 abandonadas (29%)** →
    el humano-checker funciona, pero ~1 de cada 3 propuestas se abandona (fricción del flujo de botones).
  - Uso **100% lectura/consulta**; casi nunca brazo ejecutor.

**Conclusión estratégica:** no gold-platear el motor de un coche que nadie conduce.
Medir por qué no se usa (descubribilidad / confianza / caso-de-uso killer) va **antes**
de más capacidad. Pero varias capacidades de abajo SON lo que dispara adopción.

## Tier 0 — Fundaciones de medición (barato, desbloquea decidir con datos)

Objetivo: dejar de optimizar a ciegas. **No es montar telemetría, es TERMINAR de cablear la existente.**
1. **Cablear los INSERT que faltan** — ✅ **PR #847** (abierto 2026-07-12, pendiente QA+merge):
   `cost_usd` a `copiloto_usage_increment` en los 3 canales + pricing gpt-5.2 (antes caía a
   gpt-4o-mini, −10-20×); audit de destructivas en `confirmPendingAction` (hueco: emitir/anular
   no dejaban fila en `copiloto_tool_calls`); WhatsApp ahora escribe `tool_calls` (no lo hacía);
   fix `.or()` de listarClientes/Proveedores (coma en razón social rompía el filtro) + desenmascarar
   error. `aborted` real → **diferido** (requiere plumbing de abort SSE; va con el panel 0.3).
2. **Feedback 👍/👎** (fase 1b) — ✅ **PR #852** (abierto 2026-07-12): mig 455 generaliza
   `copiloto_feedback` (solo-negativo → sentiment up/down + índice único msg/user); endpoint
   `POST /api/copiloto/feedback` con verificación de propiedad + upsert; componente `MessageFeedback`
   (👎 revela chips de motivo). Iconos thumbs añadidos. types a mano (gen cuelga). Pendiente `db push` mig 455.
3. **Panel de calidad conversacional** en `/admin/ia-ops` (junto al de OCR/enrich existente):
   % turnos que cierran sin agotar `MAX_TOOL_LOOPS`, % confirmaciones abortadas/canceladas,
   tools con peor `success` (hoy `listarClientes` 56%), coste/turno, feedback negativo reciente.
4. **Eval set vivo minado de prod**: script que convierte turnos reales (`copiloto_mensajes` +
   `copiloto_tool_calls`) en casos golden candidatos → curación manual → crece más allá de los 14.
5. **Fix `listarClientes`** (56% OK) — bug concreto que el diagnóstico ya señala.
6. Consolidar strings de modelo (duplicados en `runner.ts` / `llm/client.ts` / `admin/llm/route.ts`)
   antes de meter más modelos (deuda que marca `copiloto-modelo-escalado.md`).

## Tier 1 — Proactividad + multimodal (retención, infra ya existe)

1. **Motor de insights proactivo** (fase 6): el endpoint `/api/internal/copiloto/proactive`
   y el headless G6 ya existen. Falta el **motor que decide qué merece un empujón**:
   - Fiscal: "se acerca el 20, tu IVA estimado es X, te faltan N facturas de gastos".
   - Cobros: "cliente lleva 45 días sin pagar, ¿le mando recordatorio?".
   - Gastos: "detecté un gasto recurrente sin factura".
   - **Decisión producto 2026-07-12 (Manuel):** vigilar los **4 eventos** (fiscal IVA/modelo,
     cobros/impagados, gasto recurrente sin factura, cashflow negativo proyectado). Canal =
     **campanita in-app por defecto + digest opt-in** (email/WhatsApp solo si el usuario lo activa).
     Evitar duplicar el aviso de cobros con el cron `copiloto-recordatorios-batch` existente.
2. **Multimodal en el runner**: hoy el OCR va por pipeline aparte (bandeja), el copiloto NO
   "ve" el documento. Claude y gpt-5.2 son multimodales. Salto: foto de ticket → "¿lo registro
   como gasto de vehículo?" en el MISMO turno conversacional, sin pipeline desconectado.

## Tier 2 — IMPORTANTE, cuanto antes, con buen plan

### 2A · Modo gestoría multi-cliente (mayor upside comercial)

**El mayor multiplicador y el mayor hueco de mercado.** Una gestoría maneja 50-200 clientes;
el copiloto hoy es mono-org (multiempresa es para el mismo dueño). Un gestor con copiloto
agéntico maneja 3× clientes.

Plan:
- **Vista cartera**: el copiloto opera sobre los N clientes del gestor, no una org.
  "¿Qué clientes no me han pasado facturas este mes?", "prepárame el 303 de estos 12",
  "¿quién tiene el IVA sin cuadrar?".
- **Trabajo por lotes conversacional** (recordatorios masivos ya existe como tool — extender patrón).
- **Reusar MCP server draft-only** (`services/mcp-server/`): el gestor PREPARA borradores,
  el cliente/gestor emite. Encaja con la postura "el agente nunca emite fiscalmente autónomo".
- **Modelo de datos**: relación gestoría↔clientes (¿membresías existentes?, ¿nueva entidad
  "despacho"?). Auth: rol `gestor_externo` ya existe en `OrgRole` — punto de partida.
- **Riesgo**: RLS y aislamiento entre clientes de la cartera; un fallo aquí filtra datos entre empresas.

### 2B · Copiloto fiscal (el diferenciador, el de más riesgo)

De "facturación con chat" a **asesor fiscal**. Hoy manipula datos (IVA trimestral *calculado*)
pero NO responde "¿puedo deducir esta comida?", "¿módulos o estimación directa?", "¿qué modelo presento si...?".

Plan:
- **Base de conocimiento normativa** (AEAT / RD / casos) + **RAG con citas** (aquí SÍ hay
  caso para embeddings/pgvector — la decisión anti-RAG actual es correcta solo para el corpus
  de clientes/catálogo, no para normativa ni documentos).
- **RAG de documentos** además de normativa: contratos, condiciones de proveedor, PDFs adjuntos
  ("¿qué dice el contrato con este proveedor sobre plazos?"). Y **agregación histórica** sobre
  miles de facturas (trigram no llega: "¿cuánto le facturé a X en material el año pasado?").
- **Responsabilidad legal**: dar consejo fiscal tiene riesgo → citas obligatorias, disclaimers,
  y probablemente "sugiere, no afirma". Decisión de producto + posiblemente legal antes de lanzar.
- Encaja con el add-on **Centro Fiscal IA** (14,90 €/mes) ya existente → [[facturaia-centro-fiscal-ia]].

## Segmentación (para qué sirve cada tier a cada cliente)

- **Autónomos** → simplicidad + proactividad (Tier 1) + entrada foto/voz sin fricción. Gestor de bolsillo.
- **Pymes** → analytics conversacional + workflows de cierre (Tier 1 + acciones compuestas).
- **Gestorías** → cartera multi-cliente (Tier 2A). Donde "más IA" = "más clientes por gestor".

## Deuda/decisiones abiertas

- ¿Escalado a Opus por "loops agotados" (Propuesta A de `copiloto-modelo-escalado.md`) entra
  cuando lleguen las acciones compuestas / planes largos? Diferido a H2, sin evidencia aún que lo dispare.
- Fases 3 (routing) y 4 (memoria) YA descartadas por evidencia (gpt-5.2 no se confunde; 1 sola
  memoria en toda la plataforma). No reabrir sin datos nuevos.
