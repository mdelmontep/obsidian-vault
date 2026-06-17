---
title: Decomiso bot de intención WhatsApp (issue 116) — plan
date: 2026-06-17
source: sesión flip emitirFactura (último flip Fase 2 Copiloto)
tags: [facturaia, copiloto, whatsapp, n8n, decomiso, fase2]
---

# Decomiso bot de intención WhatsApp (116) — plan

Plan read-only redactado tras cerrar el flip de `emitirFactura` (último flip fiscal de Fase 2). Receptor n8n `pqSWkDIHqmSVHotB`, nodo agente **"Agente Facturador"** (176 nodos). **No ejecutar sin OK** — toca prod n8n.

## Estado actual (2026-06-17)
- Acciones fiscales flipadas al Copiloto vía `accion_copiloto` y **LIVE + smoke verde**: marcar cobrada (a) · gasto (b) · email (c) · anular (d) · convertir (e) · **emitir (f)**.
- Preguntas de datos → `consulta_copiloto` (Fase 1).
- El flip de cada acción dejó su rama vieja **DORMIDA** en el prompt como red de revert.

## Qué SIGUE dependiendo del bot viejo (load-bearing — NO tocar)
1. **Router/parser central**: nodo code `Parsear y Calcular Totales` — despacha por `tipo` (accion_copiloto, consulta_copiloto, cambio_org, presupuesto, proforma, convertir…). Es el cerebro de routing, compartido por todo.
2. **Presupuesto / proforma**: NO flipados (no existe tool Copiloto `crearPresupuesto`/`crearProforma`). Fluyen por la cadena de emisión genérica `Preparar Datos Generar` → `Generar Factura` → `Crear Factura en BD` → `Enviar Documento PDF`.
3. `crear_doc_desde_movimiento`, cashflow inline (`get_cashflow_forecast`/`analizar_compra`), `cambio_org_solicitado`, small_talk/conversacion.
4. Tools de lectura `consultar_*` (catálogo/clientes/facturas/presupuestos) usadas por los flujos anteriores.

## Qué quedó "muerto" — pero solo INERTE
- **Prompt**: ramas factura/abono en `=== GENERAR DOCUMENTO ===`, `=== ABONOS ===`, `=== CONVERTIR_PRESUPUESTO ===`, y el mapping de keywords tipo:factura/abono/convertir. Ya no se alcanzan (la PRECEDENCIA enruta factura/abono/convertir → accion_copiloto).
- **Nodos de emisión**: `Generar Factura` / `Crear Factura en BD` / `Preparar Datos Generar` referencian `.tipo` y son **compartidos con presupuesto/proforma** → NO son dead, son load-bearing. Borrarlos rompe presupuesto/proforma.

## Conclusión (la que cambia el plan)
- El código "muerto" es **inerte**: cero coste runtime, el prompt nunca lo enruta. Beneficio de retirarlo = bajo.
- Los nodos de emisión son **compartidos** → no son borrables hasta flipar presupuesto/proforma.
- Las ramas dormidas son la **red de revert** de los flips recién hechos.
- **116 (retiro completo del bot) está BLOQUEADO** por la migración de presupuesto/proforma al Copiloto (Fase 3), no por emitir.

## Plan escalonado
- **Fase A — ahora: NO ejecutar nada.** Dejar las ramas dormidas como red de revert mientras los flips bakean (~1-2 semanas de uso real).
- **Fase B — tras bake, opcional, valor bajo: limpieza de prompt.** Retirar SOLO las secciones de prompt muertas (factura/abono/convertir) para acortar el prompt (~28K chars) y reducir mal-routing del LLM. Reversible (restaurar prompt), NO toca nodos. Requiere: backup + dry-run + **smoke de presupuesto Y proforma** (comparten esas secciones). Paso 0 de B: traza exacta de qué texto es tipo-específico vs compartido.
- **Fase C — bloqueada: retiro de nodos de emisión.** Solo cuando presupuesto/proforma tengan tool Copiloto propio y se flipen → entonces `Generar Factura`/`Crear Factura en BD`/`Convertir Presupuesto` quedan realmente dead y se podan. Esto ES Fase 3 del Copiloto, no "116 hoy".

## Recomendación
Reclasificar 116: **no es ejecutable ahora**. Convertirlo en "Fase B (limpieza prompt, tras bake) + Fase C (bloqueada por flip presupuesto/proforma)". El siguiente paso real de valor para acercar el decomiso es **diseñar `crearPresupuesto`/`crearProforma` como tools Copiloto** (Fase 3), no tocar el bot viejo.

Relacionado: flip artifacts en `feat/copiloto-flip-emitir` (commit `9e833c1e`) y PR #326.
