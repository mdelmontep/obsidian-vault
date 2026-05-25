---
title: Prompt — Auditoría integral del dashboard de TuFacturaIA
date: 2026-05-13
source: sesión claude code
tags: [facturaia, auditoria, dashboard, prompt-reutilizable, ia, benchmarking]
---

Prompt reutilizable para correr en una sesión limpia (idealmente `/model opus`). Audita exactitud numérica + oportunidades de mejora + arquitectura escalable + benchmarking competitivo, todo bajo la óptica de **diferenciación por IA** (no IA como feature aislada).

Pensado para correr periódicamente (cada trimestre o tras cambios grandes en dashboard/métricas). El entregable es un informe en `docs/audits/dashboard-audit-YYYY-MM-DD.md` — no se toca código en esa pasada.

Relacionado: [[facturaia]] · [[facturaia-integracion-api-v1-portal]]

---

# Prompt

**Auditoría integral del dashboard de TuFacturaIA: exactitud numérica + oportunidades de mejora + arquitectura escalable + benchmarking competitivo (con foco en diferenciación por IA)**

Quiero una revisión profunda en cuatro dimensiones del dashboard de TuFacturaIA (vistas de cliente Y panel de admin/superadmin). TuFacturaIA se diferencia de la competencia (Holded, Quaderno, Contasimple, Sage…) **explotando IA como capa principal del producto, no como feature aislado**: agentes conversacionales por WhatsApp/voz, OCR inteligente, predicciones, auto-categorización, sugerencias proactivas, asistente IA en cada vista. Todo el análisis debe leerse bajo esa óptica — dónde la IA puede convertir un número estático en una acción, una alerta o una recomendación.

Las cuatro dimensiones:

1. **Corrección numérica** — todo número que se muestra debe ser matemática y fiscalmente correcto.
2. **Oportunidades de mejora** — qué métricas faltan, qué UI es mejorable, dónde la IA puede convertir datos en insight accionable.
3. **Arquitectura escalable** — cómo centralizar la capa de métricas/agregados para que añadir un KPI o un agente nuevo no requiera tocar 5 sitios.
4. **Benchmarking competitivo** — qué hacen Holded y Quaderno mejor (y peor) que nosotros, y dónde la IA es nuestro foso defensivo.

---

## PARTE 1 — Auditoría de exactitud numérica

### Alcance

Auditar TODOS los números, sumas, KPIs y agregados visibles en:

**Lado cliente:**
1. **Dashboard `/`** — KPIs (facturado, pendiente, vencido, cobrado), charts (cashflow, donuts, sparklines, ranked bars), métricas mensuales/YTD.
2. **`/emitidas`** — totales tabla, contadores por estado, sumas base/IVA/total.
3. **`/recibidas`** — totales gasto, IVA soportado, pendientes de aprobar.
4. **`/informes`** — modelo 303 (IVA), 130 (IRPF), 347 si existe.
5. **`/cashflow`** — entradas, salidas, neto, predicciones.
6. **`/clientes`** — facturado, pendiente, gasto por cliente (calculados runtime).
7. **Modales de detalle factura** — totales, retenciones IRPF, recargo equivalencia, multi-IVA.

**Lado admin/superadmin (`/admin/*`):**
8. **Dashboard admin** — métricas globales multi-org (orgs activas, facturas/mes, MRR, uso de módulos IA).
9. **`/admin/modules`** — métricas de adopción por módulo IA.
10. **`/admin/orgs`** — KPIs por organización.
11. **`/admin/api-keys` / `/admin/webhooks`** — tráfico, tasas de error.

### Qué verificar para cada número

1. **Origen exacto** — archivo:línea de la query/agregación. Distinguir BD vs cliente vs derivado.
2. **Filtros obligatorios**:
   - `org_id` correcto (admin: cuidado con leaks cross-tenant)
   - Emitidas: `estado NOT IN ('borrador','anulada')`
   - Recibidas: `estado NOT IN ('sin_aprobar','disputada')`
   - Rango de fechas: distinguir fecha emisión / fecha cobro / fecha vencimiento
   - Signo de abonos (importe negativo)
3. **Coherencia entre vistas** — "facturado del mes" del dashboard = suma `/emitidas` filtrada al mismo mes. Modelo 303 IVA repercutido = SUM(iva) emitidas no-borrador no-anulada del periodo.
4. **Estados derivados** — "vencida" no siempre es estado almacenado. Verificar fórmula y aplicación uniforme.
5. **Lógica duplicada** — `total = base + iva` calculado en 2 sitios con redondeos distintos = descuadre céntimos.
6. **Edge cases**: retenciones IRPF, recargo equivalencia, multi-IVA, abonos rectificativos, multi-moneda, org vacía, org pre-feature.
7. **Admin específicos**: ¿se filtran orgs `is_test=true`? ¿incluyen orgs eliminadas/suspendidas?

### Metodología

1. Lista componentes y data sources (`src/components/dashboard/`, `src/app/(dashboard)/page.tsx`, `src/app/emitidas/`, `src/app/admin/`).
2. Por cada KPI: componente → fetch → endpoint/RPC → SQL → tabla.
3. **Ejecuta SQL real** vía MCP Supabase contra org de prueba con datos. Compara UI vs `SELECT SUM(...)`. Reporta delta.
4. Bugs conocidos del repo:
   - Filtro borradores/anuladas en agregados (regla CLAUDE.md)
   - Columnas calculadas referenciadas como BD (`facturado`, `pendiente`, `gasto` en clientes)
   - Sincronización con triggers (race conditions)

---

## PARTE 2 — Oportunidades de mejora (con IA como vector principal)

Para cada vista, propón mejoras agrupadas por: **(a) métricas faltantes**, **(b) UI/UX**, **(c) capa IA encima del dato**.

### Métricas faltantes — cliente

- **Cashflow predictivo**: DSO (días promedio cobro), DPO (días pago), gap tesorería 30/60/90d.
- **Calidad cartera**: % cobradas en plazo, top morosos, edad media deuda.
- **Concentración**: % facturado top 3 clientes, riesgo de dependencia.
- **Eficiencia operativa**: tiempo borrador → emitida, % emitidas API/UI/voz, tasa OCR exitoso.
- **Cumplimiento fiscal**: countdown a 303/130, alertas Verifactu sin firmar, huecos en numeración.
- **Comparativas**: MoM, YoY, vs media móvil 3m, % desviación.

### Métricas faltantes — admin

- **Salud plataforma**: tasa error webhooks, latencia p95 API v1, % cron ok.
- **Adopción módulos IA**: % orgs usando OCR/Cobros/Anti-fraude, time-to-first-use.
- **Cohortes**: retención por mes alta, churn signals (orgs con caída >50% MoM).
- **Revenue**: MRR por plan, ARPU, expansion revenue (add-ons IA), LTV.
- **Health score por org**: composite uso + volumen + módulos + errores.
- **Coste IA por org**: tokens consumidos OCR/asistente/voz, margen vs precio del plan.

### Mejoras de UI/UX

- Drill-down: cada KPI clicable → lista filtrada que lo compone.
- Tooltips con fórmula: "¿qué incluye este número?".
- Skeleton loaders coherentes vs `0` mientras carga.
- Comparativas inline (▲ +12% vs mes anterior) en cada KPI.
- Empty states informativos vs `0€` mudo.
- Mobile: ¿el dashboard es usable en móvil?
- Densidad: ¿charts redundantes consolidables?
- Accesibilidad: contraste, lectores de pantalla en SVG.

### Capa IA encima del dato — donde nos diferenciamos

Por cada vista auditada, proponer **al menos una capa IA accionable**. Ejemplos:

- **Dashboard**: "Resumen ejecutivo de tu mes" generado por LLM en lenguaje natural arriba del dashboard, con 3 puntos clave + 2 acciones recomendadas. Refresh diario.
- **Cashflow**: predicción de tesorería a 60d con LLM/modelo estadístico que aprende del histórico — "tienes riesgo de gap el 14 de junio, te faltan 4.200€; envía recordatorio a estos 3 clientes morosos para evitarlo".
- **Emitidas**: detector de anomalías ("esta factura es 3x el promedio de este cliente, ¿confirmas?"), sugerencia de fecha vencimiento óptima por cliente según histórico de cobro.
- **Recibidas**: auto-categorización contextual (módulo D ya planeado), detección duplicados, alerta de subida de precio recurrente del mismo proveedor.
- **Informes**: pre-revisión IA del modelo 303 antes de presentar — "detectamos 2 facturas sin IVA repercutido que deberían tenerlo, revisa".
- **Clientes**: scoring de cliente (probabilidad de pago a tiempo, ticket medio esperado, churn risk), sugerencia de upsell.
- **Admin**: alertas proactivas IA — "la org X tiene caída del 60% MoM, posible churn, propón intervención".
- **Asistente conversacional contextual**: en cada vista, panel "pregúntale a tu IA" pre-rellenado con contexto de la pantalla — el usuario puede preguntar "¿por qué ha subido mi pendiente este mes?" y la IA responde con datos reales + acción.
- **Acciones por voz/WhatsApp desde el dashboard**: "envíame un resumen por WhatsApp cada lunes" generado y enviado por el agente.
- **Auto-redacción de mensajes de cobro**: en vez de mostrar "5 facturas vencidas", mostrar "5 facturas vencidas — pulsa para que la IA redacte y envíe el recordatorio personalizado a cada cliente".

Para cada propuesta IA: **valor cliente**, **coste técnico (S/M/L)**, **dependencias (datos, prompts, infra)**, **diferenciación vs Holded/Quaderno**.

### Mejoras de funcionamiento

- Caché: ¿se recalculan agregados en cada navegación? Materialized views o `revalidate`/SWR.
- Realtime: KPIs que se actualicen al llegar factura nueva (Supabase Realtime).
- Background jobs: pre-cómputo nocturno de cohortes, predicciones, resúmenes IA.
- Exportación: CSV/Excel de cualquier vista filtrada.

---

## PARTE 3 — Arquitectura escalable

### Diagnóstico
1. Mapa de la capa de métricas hoy: ¿cuántos sitios calculan "facturado del mes"? Lista archivos.
2. ¿`/api/modules/[id]/metrics`, dashboard, informes, cashflow comparten código o duplican?
3. Acoplamientos peligrosos: lógica fiscal repetida.
4. Performance: N+1, falta de índices `(org_id, fecha, estado)`.
5. **Capa IA**: ¿dónde viven los prompts? ¿hay un "metrics-to-LLM" reutilizable? ¿caché de respuestas IA por org+periodo para no quemar tokens?

### Propuesta arquitectónica (a evaluar)

**A — Capa servicios métricas (`src/lib/metrics/`):**
- Función pura por KPI: `getFacturadoMes(orgId, mes)`, `getPendiente(orgId)`, `getCashflow(orgId, rango)`.
- Filtros fiscales encapsulados: `excludeBorradorAnulada()`, `signoAbono()`.
- Tipos `Metric<T>` con `value`, `delta`, `trend`, `breakdown`.
- Tests unitarios con fixtures.

**B — Vistas materializadas Postgres:**
- `mv_facturas_mensuales`, `mv_cashflow_diario`, `mv_admin_org_health`.
- Refresh incremental con triggers o cron.

**C — Event sourcing ligero:**
- `module_events` ya existe parcialmente.
- Agregados por suma incremental, auditoría natural.

**D — Capa IA unificada (`src/lib/ai/insights/`):**
- `generateMonthlySummary(orgId)`, `predictCashflowGap(orgId, days)`, `detectAnomalies(orgId)`.
- Cada función: input métricas estructuradas (capa A) → prompt versionado → respuesta cacheada (`org_id + tipo + periodo + hash_input`).
- Versionado de prompts en repo, evals automáticos, fallback graceful si LLM falla.

**E — Híbrida (probable):**
- Servicios puros (A) como única API interna de números.
- MVs (B) para queries pesadas, directas para baratas.
- Capa IA (D) consume A, no SQL crudo — separa "cálculo" de "narrativa".
- Realtime Supabase para invalidar caché cliente y disparar re-cómputo IA.

### Entregable arquitectónico

ADR en `docs/architecture/decisions/ADR-NNN-metrics-and-ai-layer.md`:
- Estado actual con números (duplicaciones, archivos tocando métricas, dónde viven prompts hoy).
- 4-5 opciones contrastadas con pros/contras.
- Recomendación con plan de migración por fases (no big bang).
- Criterios éxito: latencia p95, cobertura tests métricas, # sitios calculando "facturado", coste IA por org/mes, % insights IA con feedback positivo.

---

## PARTE 4 — Benchmarking competitivo: Holded y Quaderno

Análisis comparativo centrado en dashboard, métricas y diferenciación IA. Investiga ambas (web pública, capturas de docs, demos, reviews G2/Capterra, foros). No te bases solo en marketing — busca screenshots reales y reviews de usuarios.

### Por cada competidor, documenta

**Holded** (ERP español, foco PYME):
1. Cómo es su dashboard principal — KPIs arriba, charts, densidad informativa.
2. Métricas que tienen y nosotros no.
3. Qué hacen mejor en UX (drill-down, filtros, mobile).
4. Qué hacen peor (carga, claridad, accesibilidad).
5. **Capa IA**: ¿asistente? ¿OCR? ¿predicciones? ¿feature aislada o integrado?
6. Pricing del tier con dashboard avanzado.
7. Reviews recurrentes sobre su dashboard.

**Quaderno** (facturación + tax compliance internacional):
1. Mismo análisis. Su fuerte es tax automation/multi-país, dashboard más simple.
2. Especial atención al reporting fiscal (303 equivalente, IVA intracomunitario).
3. **Capa IA**: probablemente menos que Holded.

### Tabla comparativa final

| Dimensión | TuFacturaIA hoy | Holded | Quaderno | Gap / Oportunidad |
|---|---|---|---|---|
| KPIs en dashboard | ... | ... | ... | ... |
| Cashflow predictivo | ... | ... | ... | ... |
| OCR inteligente | ... | ... | ... | ... |
| Asistente conversacional | ... | ... | ... | ... |
| Agente WhatsApp/voz | sí | no | no | **Nuestro foso** |
| Auto-categorización IA | ... | ... | ... | ... |
| Anomalías/alertas IA | ... | ... | ... | ... |
| Modelos fiscales | ... | ... | ... | ... |
| Mobile UX | ... | ... | ... | ... |
| API pública | sí v1 | sí | sí | ... |
| Webhooks | sí | sí | sí | ... |
| Multi-org / agencias | sí | parcial | no | ... |

### Conclusiones del benchmarking

1. Dónde estamos por delante — features IA que ellos no tienen.
2. Dónde nos copian fácil — features IA que cualquiera puede añadir en 6 meses (OCR básico).
3. Dónde tenemos foso real — agente conversacional integrado al ERP, multi-canal, contextual.
4. Dónde estamos detrás — features no-IA que ellos pulen mejor (UX, mobile, ecosistema integraciones).
5. 3 movimientos prioritarios que combinan diferenciación IA + cierre de gaps no-IA.

---

## Entregable global

Informe en `docs/audits/dashboard-audit-YYYY-MM-DD.md`:

1. **Resumen ejecutivo** — top 5 hallazgos críticos (bugs fiscales > UX > arquitectura > diferenciación).
2. **Parte 1: KPIs auditados** — tabla (vista, KPI, archivo:línea, SQL, valor UI, valor SQL, ok/ko).
3. **Parte 1: Bugs encontrados** — severidad, repro, fix.
4. **Parte 2: Oportunidades** — agrupadas por vista, con (a) métricas (b) UX (c) capa IA, esfuerzo (S/M/L), impacto (alto/medio/bajo).
5. **Parte 3: ADR capa métricas + IA** — propuesta completa con fases.
6. **Parte 4: Benchmarking** — tabla comparativa + conclusiones + 3 movimientos prioritarios.
7. **Roadmap** — ya / sprint próximo / 3 meses, dejando claro qué movimientos amplifican nuestra ventaja en IA.

**No toques código todavía.** Solo audita, mide, investiga competencia, propón. Usa MCP Supabase para BD real, lee código directo, busca screenshots reales de Holded/Quaderno, no asumas nada.
