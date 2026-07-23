---
title: g5a-005 — Plan de decomisión del Agente Facturador (n8n)
date: 2026-07-04
source: sesión Claude Code (auditoría + plan)
tags: [facturaia, n8n, g5, seguridad, decomision]
---

# g5a-005 — Decomisión del Agente Facturador en n8n

Workflow: **FacturaIA — WhatsApp Receptor v2** (`pqSWkDIHqmSVHotB`, n8n.tufacturaia.com), 184 nodos, `active:true`.
Backup previo (sin secretos, credenciales por referencia): `~/facturaia/ops/n8n-backups/facturaia-whatsapp-receptor-v2-pre-g5a005-2026-07-04.json`.

## Evidencia (audit cerrado)
- **0 tráfico real** del Agente Facturador en la ventana retenida (2026-06-27→29): las 21 ejecuciones con el agente activo son SOLO de testers internos (Manu `34617314938`, Sory `34661253928`). Cero remitentes externos.
- Receptor sin ejecuciones desde **2026-06-29** (coherente con el cutover del webhook Meta → Next.js del 30/06).
- Deuda confirmada: los toolCode leen `$env.SUPABASE_SERVICE_ROLE_KEY` y pegan a Supabase REST **sin role/feature gating**. No hay secreto hardcodeado en el export (todo por env/credencial).

## Nodos a ELIMINAR (segundo cerebro + deuda)
- `Agente Facturador` (langchain.agent), `OpenAI GPT-4o` (lmChatOpenAi), `Memoria Postgres` (memoryPostgresChat), `Think` (toolThink).
- **16 toolCode** con SERVICE_ROLE_KEY directo: `consultar_catalogo`, `consultar_clientes`, `consultar_facturas`, `consultar_presupuestos`, `consultar_presupuesto_detalle`, `get_cashflow_forecast`, `registrar_gasto_rapido`, `analizar_compra`, `crear_cliente`, `crear_proveedor`, `consultar_vencimientos`, `consultar_iva_trimestral`, `consultar_retenciones_irpf`, `consultar_perfil_empresa`, `consultar_recibidas`, `consultar_proveedores`.
- Post-proceso acoplado al JSON del agente (evaluar 1:1 antes de borrar): `Parsear y Calcular Totales`, `Totales OK?`, y el sub-flujo de generación desde el JSON del agente (`Leer Ultimo JSON Agente` → `Preparar Datos Generar` → `Generar Factura` …) — SOLO si el copiloto in-house cubre ya ese camino (crear/emitir por texto).

## Nodos que SE QUEDAN (no tocar)
- Toda la rama media: OCR (`Preparar Datos Ingesta`, `Subir a Storage`, `Disparar OCR`…), voz (`Transcribir Whisper`, `Parsear Transcripcion`…). Usan SERVICE_ROLE_KEY legítimamente como worker media-bound (Capa B).
- STOP/opt-out, delivery status, idempotencia, phone-state guard.
- `Confirmar Copiloto` (ya existe → puente parcial de confirmación al copiloto in-house).

## Diseño del relay de texto (objetivo)
`Preparar Texto Agente` (resuelto org/usuario) → **HTTP POST `/api/internal/whatsapp/copiloto`** (service-auth) → enrutar el **discriminador** de la respuesta:
- `{ reply:true, text }` → `Enviar Resumen WhatsApp` (texto).
- `{ confirm:true, summary, pending_id }` → `Enviar Botones WhatsApp` (Confirmar/Cancelar) — el confirm consume vía el raíl pending-action existente.
Sin razonamiento LLM en n8n para texto: n8n queda como transporte puro.

## Ejecución (IRREVERSIBLE — requiere OK de Manu)
1. Backup ✅ (arriba).
2. **Hacerlo con la skill `n8n-workflow-surgical-edit`** (edición quirúrgica por nodo, no regenerar el workflow entero — nunca sin backup del env).
3. Staged: primero desconectar la entrada al `Agente Facturador` y cablear el relay; validar con el número tester; luego borrar los nodos huérfanos (agente + 16 toolCode + modelo + memoria).
4. Smoke post-cambio: (a) texto real desde el tester → respuesta in-house; (b) voz y OCR intactos.
5. Confirmar `active:true` y `git`/backup del workflow resultante.

## Riesgos
- El post-proceso de texto (Totales/Generar) está acoplado al shape del agente; si el copiloto no cubre 100% crear/emitir por texto, hay que mantener puentes o cerrar gaps antes de borrar.
- Es un workflow LIVE de 184 nodos: editar por nodo, validar por tramos, no “recrear”.

## EJECUTADO — 2026-07-04 (con OK de Manu)

**Hallazgo que cambió el plan**: auditoría del flujo antes de tocar reveló que el workflow estaba **100% fuera del camino**. El webhook de Meta apunta a Next.js (`/api/whatsapp/webhook`) y Next.js maneja texto/voz/OCR **in-house** sin reenviar nunca a n8n (confirmado por código + test `NO reenvía a N8N_MEDIA_WEBHOOK`). El "relay de texto" del plan era innecesario: no hay tráfico que relayar. El único riesgo vivo era el **webhook público sin auth** (`/webhook/whatsapp-tufacturaia`, `authentication:none`) fronteando los 16 toolCode con `SERVICE_ROLE_KEY` sin gating. Decisión (Manu): **escalonado desactivar + borrar nodos** (en vez de recablear un relay a la nada).

**Ejecución (vía API n8n, por tramos):**
1. `POST /workflows/pqSWkDIHqmSVHotB/deactivate` → `active:false`. Verificado: `POST /webhook/whatsapp-tufacturaia` → `404 not registered`. Superficie SERVICE_ROLE_KEY cerrada, reversible.
2. Smoke: app viva (307), webhook Next.js vivo (GET verify → 403 token malo; POST → 200 in-house), n8n confirmado inactivo. WhatsApp in-house intacto.
3. `PUT /workflows/pqSWkDIHqmSVHotB` con 164 nodos (borrados los 20: Agente Facturador + 16 toolCode + OpenAI GPT-4o + Memoria Postgres + Think). 0 referencias residuales. Solo se rompió la conexión muerta `Preparar Input Agente → Agente Facturador`. Workflow queda `active:false` (decomisionado).

**Backups**: `~/facturaia/ops/n8n-backups/facturaia-whatsapp-receptor-v2-post-g5a005-decomision-2026-07-04.json` (post) + `...pre-g5a005-2026-07-04.json` (pre), ambos en `~/facturaia/ops/n8n-backups/`.

**Nota**: la skill referida en CLAUDE.md como `n8n-workflow-surgical-edit` no existe con ese nombre; la edición quirúrgica se hizo por API n8n directa (GET→editar copia local→validar→PUT). Nodos huérfanos pre-existentes NO tocados (IF Detectar Frase Cobro, Lookup Cobro Pendiente, etc. — ya desconectados antes). El workflow inactivo con 164 nodos podría borrarse entero más adelante si no se quiere conservar histórico.
