---
title: facturaia — snapshot de poda del hub 2026-07-25
date: 2026-07-25
tags: [cliente, facturaia, historico]
---

Poda del `## NOW` del hub [[facturaia]] a 2026-07-25: las 38 entradas ya cerradas (✅) que se habían acumulado en NOW, movidas aquí literalmente. Cubren 2026-06-30 → 2026-07-25 (Obras completo, unificación UI, Centro Fiscal, billing/cupones, Slack, seguridad npm, ticket-runner, conciliación/import de extractos, API v1 de Obras).

## NOW cerrado a 2026-07-25

- ✅ **Conciliación: parcial en recibidas + import XLS/XLSX + 3 bugs reales de import EN PROD (7 PRs #1187-#1194, 23-jul)** — probado con extracto real de Agentesia Lab (.xls legado BIFF, SheetJS vía CDN propio por CVEs de npm). Bugs cazados en el propio dogfooding: dedup por existencia (no conteo) perdía comisiones repetidas el mismo día; cabecera "F. Valor"/"F. Operativa" no se detectaba (normalización inconsistente entre dos matchers); 90 tests preexistentes rotos en main (`connection()` Next 16 sin mock + varios). De paso: drawer al 40% + wizard "¿qué es este cobro?" con ejemplos. **Pendiente/idea en curso**: botón "volver a buscar sugerencias" por movimiento individual (hoy solo hay recalculo global) — evaluar. Ver [[hash-dedup-necesita-indice-secuencial-para-movimientos-repetidos]] · [[matching-texto-header-debe-normalizar-igual-en-ambos-lados]] · [[sheetjs-xlsx-npm-abandonado-cves-usar-cdn-propio-version-fijada]].
- ✅ **ticket-runner — smoke funcional CONFIRMADO 2×, 2026-07-24**: **PR #1198** (ticket real de Borja "permitir crear cliente sin dni", NIF opcional al crear cliente) y **PR #1199** (nuevo ticket, `bandeja_ingesta.fuente_account` — muestra qué buzón de email recibió cada documento cuando una org tiene varios conectados) — ambas con diff correcto, ambas en **draft** al fallar su propio gate typecheck (self-diagnosticado en el PR body — deps `xlsx`/`jsdom` del sandbox, no del repo), **nunca auto-mergearon**. Revisadas, verificadas localmente (lint/typecheck limpios; build falla solo por `.env` ausente en el worktree de review, no por el código) y mergeadas a mano. Confirma end-to-end el fix de PR #1182 (23-jul). **Hallazgo aparte**: #1199 traía su propia migración numerada `553`, la misma que #1111 acababa de fijar — 2º choque de numeración el mismo día → **fix sistémico**: `.githooks/pre-push` ahora aborta el push si detecta el mismo nº NNN en 2 migraciones distintas contra `origin/main`. Ver [[facturaia-migracion-numero-duplicado-536-553]].
- ✅ **ticket-runner — time tracking: sesiones sí llegaban bajo "Manuela" pero con `project=ticket-xxxxxx` en vez de "facturaia" (PR #1200, 2026-07-24, CERRADO)** — `resolveProject()` usaba el basename del worktree efímero (`mkdtempSync`), no el repo real; fix prioriza `REPO_SLUG` del entorno del runner. Mergeado directo (solo tocaba `facturaia`, no el panel), **redeploy manual + Autodeploy activado** en el servicio `ticket-runner` de Dokploy (estaba apagado), y **16 filas históricas reescritas** en `work_sessions` (agency-portal) de `ticket-xxxxxx` a `facturaia` vía PATCH directo a PostgREST. Ver [[hook-en-worktree-efimero-no-debe-derivar-nombre-de-basename-cwd]].
- ✅ **Seguridad — auditoría de vulnerabilidades npm COMPLETA (PRs #1157/#1159/#1177, 12→22-23 jul)** — 12→2 vulnerabilidades. sharp 0.34.5→0.35.3 (CVE libvips, `overrides` para forzar copia única pese al `optionalDependency` de next) con QA exhaustiva en Alpine/musl (binding nativo, rotación real de píxeles, build standalone, servidor arrancado — ver [[npm-overrides-necesario-cuando-dependencia-fija-optionaldependency-vieja]]); de paso se coló y cerró un CVE real de next (16.2.9→16.2.11, 3 high: bypass middleware/proxy, 2×SSRF), verificado sin regresión. **Quedan solo 2 en `.audit-baseline.json`**: `@hono/node-server`/`@modelcontextprotocol/sdk`, bloqueadas upstream. Ver [[dependencias-npm-parcheadas-upstream-nunca-se-recogen-sin-npm-update-rutinario]] · [[trinquete-baseline-bloquea-solo-lo-nuevo-patron-reusable]].
- ✅ **306 tests rotos por `revalidateTag`/Cache Components (E4)** — diagnosticado y cerrado en PR #1181 (mismo día). Detalle en §E4 más abajo.
- ✅ **Obras — «Toda la obra»/ficha/certificación: pulido UX + bugs reales** (push directo a main, 2026-07-21) — 9 commits tras dogfooding de Manu (desplegable Responsable, barra de certificación fija, árbol Estructura persistente, tooltips, fix doble símbolo €). [[resolver-label-nombre-en-cliente-contra-endpoint-paginado-cae-al-uuid]] · [[css-grid-cabecera-y-filas-en-contenedores-distintos-auto-no-sincroniza]]
- ✅ **Obras — «Toda la obra»: Fases 1-2 + BLOQUE P1 del follow-up COMPLETO** (2026-07-21, PRs #1112-#1117 + #1121 retención garantía) — árbol multi-presupuesto, certificar por selección, smoke prod verde. [[obras-endpoints-n+1-paralelizar]] · [[levantar-supabase-local-en-facturaia-config-puertos-analytics-dup519]] · [[db-push-remote-versions-not-found-es-checkout-stale-o-num-duplicado-no-repair]]
- ✅ **Obras — nombres de componente por UUID + modales adaptables** (#1103/#1106, EN PROD 2026-07-20) — resolución server-side del nombre de material (antes UUID crudo) + modales a ancho fluido acotado. [[resolver-label-nombre-en-cliente-contra-endpoint-paginado-cae-al-uuid]]
- ✅ **Obras — Calendario (barras/festivos) + sistema de diseño en 5 olas EN PROD** (7 PRs #1042-#1048, 2026-07-19) — calendario tipo Google Calendar + festivos nacionales + tokens semánticos por rol unificados. [[worktree-qa-next-standalone-symlink-node-modules]]
- ✅ **Obras — IA + WhatsApp + MCP COMPLETO** (7 PRs, desplegado, 2026-07-19) — paridad de obras en copiloto (generar/explicar/imputar/pedidos) + 15 tools MCP `obras:read/draft`. [[namespace-v1-reservado-user-token-para-sacar-campo-del-contrato-api-key]] · [[copiloto-entidad-tabla-propia-necesita-tool-busqueda-y-regla-en-prompt]]
- ✅ **Botón «Ask» glass + spark real (topbar + Copiloto)** — PR #1054 MERGEADO (2026-07-20) — réplica del Glass Button 2.0 de Figma vía Figma MCP. [[figma-mcp-community-bloqueado-vs-editable]]
- ✅ **Sidebar rail plegado: centrado + tooltips por icono** — PR #1010 MERGEADO (2026-07-19).
- ✅ **Obras — polish UI + auditoría de mejoras EN PROD** (PRs #1005+#1006+mig 513, 2026-07-19) — kit `src/components/ui/` + N+1 presupuestos a RPC batch. [[cap-en-id-set-que-alimenta-agregacion-infra-reporta-en-silencio]] · [[aplicar-migracion-por-psql-y-registrar-version-cuando-el-cli-supabase-esta-bloqueado]]
- ✅ **Módulo Clasificador OCR: gate real de `auto_categorizar` + métricas de aprendizaje** — PR #990 MERGEADO (2026-07-18). [[defensa-cableada-vs-codigo-muerto]]
- ✅ **Cashflow a base caja + capa «Vencimientos»** — PR #986 MERGEADO (2026-07-17), fix saldo duplicado devengo+caja. [[cashflow-forecast-base-caja-no-mezclar-devengo-con-vencimiento]]
- ✅ **Calendario: aclarar cobros/pagos del día = vencimientos** — PR #987 MERGEADO (2026-07-17).
- ✅ **Dashboard: KPIs vacíos en Vista cliente** — PR #988 MERGEADO + mig 495 (2026-07-17). [[impersonate-client-stubbea-rpc-datos-de-rpc-vacios-en-vista-cliente]]
- ✅ **Registro standalone + onboarding en claro + validación en vivo** — PR #984 MERGEADO (2026-07-17). [[facturaia-multiples-dialectos-input-field-generico-rompe-fuera-de-contexto]]
- ✅ **Iconos de marca reales para integraciones** — PRs #973/#975 MERGEADOS (2026-07-17). [[react-hooks-static-components-lookup-dinamico]]
- ✅ **Dedup OCR proveedores/clientes** — PR #965 MERGEADO+DESPLEGADO (2026-07-17, mig 467+468). [[advisory-lookup-en-funcion-compartida-debe-ser-opt-in]]
- ✅ **Clase 42703 CERRADA en TODO `src/**`** — en prod (2026-07-16, #944/#961/#964/#969). [[facturaia-historico-detallado]] · [[facturaia-erradicar-casts-supabase-42703]]
- ✅ **Unificación UI COMPLETA — los 4 Frentes** — en prod (2026-07-16, 11 PRs #953-#963). [[facturaia-historico-detallado]]
- ✅ **Cierre de pendientes (2026-07-13)** — 3 PRs #871/#825/#872 MERGEADOS. [[facturaia-historico-detallado]]
- ✅ **Centro Fiscal auditado a fondo** — PR #825 MERGEADO + migs 452/453 en prod (2026-07-13). Smoke pendiente: ver §Smoke tests pendientes. [[facturaia-historico-detallado]]
- ✅ **Sistema de cupones de descuento** — 5 PRs MERGEADOS + migs 437-439 en prod (2026-07-07). Pendiente acción Manu: crear el primer cupón real desde `/admin/descuentos`. [[stripe-coupon-no-es-tecleable-necesita-promotion-code]] · [[worktree-add-sin-cd-bash-cae-en-checkout-principal]] · [[facturaia-historico-detallado]]
- ✅ **Auditoría billing Stripe (suscripción)** — PR #777 MERGEADO + mig 436 en prod (2026-07-07). [[stripe-subscription-item-resolver-por-price-no-por-indice]] · [[facturaia-historico-detallado]]
- ✅ **Export gestoría v1.5** — CERRADO, en prod y verificado con datos reales (2026-07-03). Único pendiente: Pre303 HITL (bloqueado sin certificado). [[facturaia-export-gestoria-v15]] · [[facturaia-historico-detallado]]
- ✅ **PR #640 — 5 docs legales compliance pulidos** — MERGEADO (2026-07-02). Pendiente acción Manu: envío real a FNMT/OpenAI/Anthropic/abogado/seguro. [[facturaia-historico-detallado]]
- ✅ **Smoke /soporte (sandbox, 2026-07-02)** — carga con empty-state (bug del Dashboard arreglado). [[facturaia-historico-detallado]]
- ✅ **Auditoría de cobertura de tools de agente (MCP/copiloto/v1/web)** — 4 PRs (#890-#893) en prod (2026-07-14). Frontera fiscal intacta y blindada. [[capacidad-en-dos-capas-tool-mas-gate-endpoint-verificar-paridad-o-queda-muerta]] · [[facturaia-historico-detallado]]
- ✅ **Plan consolidación WhatsApp/copiloto (post G5)** — PR #705 MERGEADO A MAIN (2026-07-05). `cobro_stripe` gated off, sin riesgo en prod. [[payment-link-importe-congelado-revalidar-pendiente-al-conciliar]] · [[stripe-connect-signup-gotcha-crear-cuenta-conectada]] · [[facturaia-historico-detallado]]
- ✅ **Integración Slack — LIVE EN PROD** (#002-007b, migs 406-411) — lecturas+escrituras con autoría `agent:slack`, vinculación de identidad. Ver ADR-009 · manual-admin §9. [[facturaia-historico-detallado]]
- ✅ ~~Registro branded + onboarding (PR #256/#258)~~ — ciclo antiguo superado por el rediseño de #984. [[facturaia-historico-detallado]]
- ✅ **Iniciativa agéntica S7+G6 CERRADA** (2026-06-30) — batch recordatorios headless + config por-org + crons `mcp-dcr-cleanup`/`copiloto-recordatorios-batch` verificados. [[facturaia-historico-detallado]]
- ✅ **G5 — Desacople copiloto↔n8n — CUTOVER COMPLETO** (2026-06-30) — envs+webhook Meta en Dokploy, canary y smokes verificados. [[facturaia-historico-detallado]]
- ✅ **Botón «Enviar a Conciliación» (Bandeja IA) reconectado** (2026-06-30) — endpoint huérfano portado y reescrito, smoke real verificado. [[ocr-clasificacion-doc-type-no-factura-sin-campos]] · [[facturaia-historico-detallado]]
- ✅ **Dropzone «Importar extracto bancario» (/conciliacion) CERRADA** — 2 PRs (#1148/#1151, 2026-07-22), pieza glass compartida + fix de hueco muerto. [[next-typed-routes-validator-stale-tras-cambio-de-rama]]
- ✅ **API v1 Obras — 15 endpoints documentados en `openapi.json`, drift-guard cerrado (PR #1192, 2026-07-23)** — hallazgo al arreglar tests rotos preexistentes: los endpoints reales bajo `/api/v1/obras/*` (obras, pedidos, presupuestos, instaladores, materiales, partes, albaranes, salidas, informes) eran invisibles al SDK del portal. Hecho en worktree tras perder el primer intento (agente en background editando `main` compartido, ver [[claude-code-sesiones-paralelas-mismo-repo-colisiones-git]]).

---

## Módulos IA de `/agentes` — detalle cerrado de la auditoría (movido del hub, 2026-07-25)

La auditoría de los 9 módulos y su plan de 27 slices están en el repo: `issues/PRD-modulos-ia-config.md`,
`issues/modia-000-indice.md` y `issues/modia-0NN-*.md`. Lo que queda cerrado y sale del hub:

- **Los tres P0 tal como se describieron**: (1) el `PATCH /api/modules/[id]` reemplazaba el jsonb entero de
  `org_module_config` (13 escritores) → guardar la config de tesorería borraba el saldo bancario inicial
  manual y la previsión se recalculaba desde 0 €; **cerrado en main** por otra sesión. (2) 13 ajustes
  `implemented:true` sin consumidor, incl. `guardar_historial` (prometía no persistir y persistía),
  `alerta_bajo_minimo` y el trío `regimen_iva`/`periodicidad_iva`/`estimacion_irpf`, duplicado divergente
  de la tabla `perfil_fiscal`; los dos primeros cableados en main (`7f0ff046`, `debbdc28`), el trío sigue
  abierto en `modia-012`. (3) la cadencia de cobros solo se validaba en cliente y la RPC elegía nivel con
  cascada `>= d3` primero → con 90/3/7 el primer aviso al cliente final era el de "procedimientos de
  reclamación formales"; auditado contra prod (`modia-024`): **0 orgs afectadas, daño teórico**.
- **Reverificación tras el merge de SEPA (#1201)**: de 27 citas fichero:línea, 26 exactas y 1 corregida.
  #1201 ya había adelantado parte del plan (NumberField/Input, vaciar-no-guarda-0, aria-describedby,
  empty state con 403/error, gate por rol).
- **Dos fixes de main que salieron de paso**: `/admin/onboarding` se prerenderizaba y llamaba a
  `createAdminClient()` en build-time, tumbando el build entero y haciendo imposible satisfacer el
  `pre-push` (`f1b3d3b3`); y 2 tests rojos preexistentes por un mock que no seguía a la RPC batch del
  #1111 (`5a9e130f`).
- **Vulnerabilidad high `brace-expansion` GHSA-mh99**: parche INALCANZABLE, probado (5.x rompe
  `minimatch@3`); aceptada en baseline con explotabilidad nula verificada, 18 entradas documentadas,
  `audit:check` verde. Ver [[aviso-con-parche-publicado-puede-tener-el-parche-inaplicable]].
