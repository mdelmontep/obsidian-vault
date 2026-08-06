---
title: facturaia — histórico detallado
date: 2026-05-31
tags: [cliente, facturaia, historico]
---

Índice del histórico de FacturaIA. El contenido pesado vive partido en los ficheros de abajo (uno por snapshot de poda del hub, más uno de eventos puntuales con fecha propia). El hub vivo y actual es [[facturaia]].

- [[facturaia-historico-snapshot-2026-05-31]] — snapshot fundacional del hub (contenido original del archivo desde su creación): log cronológico en blockquotes (~2026-05-16 a 2026-07-19), foto congelada del hub a 2026-05-31 (Estado actual, NOW, Smoke, WIP, Progreso en vivo, NEXT, LATER, Decisiones, Bloqueos, Seguridad, Stack, credenciales, histórico de hitos) y la Auditoría SaaS 2026-05-29.
- [[facturaia-historico-snapshot-2026-06-15]] — dos podas del hub del mismo día: "dieta del hub" (Estado/NOW/PRIORIDADES/Progreso en vivo/Decisiones/Histórico de hitos) y "purga hub" (NEXT/Smoke/Bloqueos/WIP cerrados movidos).
- [[facturaia-historico-eventos]] — entradas de evento puntual con fecha propia en el header, 2026-06-16 a 2026-07-13 (informes de analítica, bug NIF proveedor, stock por lotes, hitos 06-28→07-04, dedup NOTES, ingesta, drawers, cierre de pendientes).
- [[facturaia-historico-snapshot-2026-07-15]] — poda del NOW del hub a 2026-07-15.
- [[facturaia-historico-snapshot-2026-07-23]] — poda más reciente del hub a 2026-07-23 (Obras: certificación/ficha/adicionales/retención de garantía, modales adaptables, nombres por UUID).
- [[facturaia-historico-snapshot-2026-07-25]] — poda del NOW del hub a 2026-07-25: 38 entradas cerradas (Obras completo, unificación UI, Centro Fiscal, billing/cupones, Slack, seguridad npm, ticket-runner, import de extractos, API v1 Obras).
- [[facturaia-historico-snapshot-2026-07-27]] — poda del 27-jul: 12 entradas cerradas del NOW (gate del 26-jul y sus remates, vigilante externo, lote conciliación, retención del copiloto, Obras, VeriFactu, coste LLM, prompt caching, auditoría Fable 5, cola OCR, UX de ingesta).
- [[facturaia-historico-snapshot-2026-07-28]] — poda del 28-jul: 10 entradas cerradas del NOW (IVA negativo de presupuestos, `/api/health` con versión real, ticket de vencimiento de IET, panel `/admin` sin falsas incidencias de precios + `proxy.ts`, gate del 26-jul y sus remates, lote de conciliación).
- [[facturaia-historico-snapshot-2026-07-29]] — dos podas del 29-jul: la de la mañana y, al cierre, 11 entradas más del NOW (área de tickets y su fuga de mensajes internos, avisos de respuesta del cliente, impersonación en listados, VeriFactu, coste LLM, prompt caching, auditoría Fable 5, cola OCR, UX de ingesta, recurrentes).
- [[facturaia-historico-snapshot-2026-07-30]] — poda del 30-jul: los 4 smokes de prod que Manu ya verificó (runner, OCR de nº de factura y RAEE, condiciones de pago en PDF, impersonación tras `proxy.ts`).

## Módulo Obras — entrada retirada de `top-of-mind` el 03-ago-2026

**Módulo Obras (mini-ERP instalaciones, sustituye WAPI) EN PRODUCCIÓN.** Núcleo + FASE 2 + **FASE 3 (PR #999, 18-jul)** mergeados a main y con smoke prod verde. FASE 3 = decisiones de Natalia: coste MO fiel (tarifa por instalador, precio hora especial por obra, dieta default, calendario mensual de partes), módulo **Herramientas** (foto+event log+alta por WhatsApp vía copiloto), corregir descuento/precio desde recibida, **proforma a origen** (informe PDF, NO createDocument, ADR-obras-001), generar pedido desde presupuesto con expansión de UO, chip recibido X/Y. Migs 471-511 reconciliadas (schema_migrations local==remote). `/fia-cierre` cross-issue cazó 2 bloqueantes que los gates por-issue no vieron (`.or()` sin entrecomillar en tools copiloto con test mock no-op → ver [[postgrest-or-no-escapa-delimitadores]]; clave React/dedup rota al componer olas). **Org REAL de Natalia**: "Instalaciones Eléctricas y de Telecomunicación, S.A." (`b9d5d6f7-…`, is_test=false, creada 16-jul, miembro `administracion@iet.es`). Sembrado el catálogo de **745 tipos M.O.** (copiado del Sandbox, suma horas 3826,901 idéntica, 18-jul). Docs `docs/architecture/obras/fase3-plan-decisiones.md` + ADRs 001/002/003.

## Obras — IA/WhatsApp/MCP: dos entradas retiradas de `top-of-mind` el 03-ago-2026

Ambas describen trabajo ya EN PROD (19-20 jul). Se retiran del arranque porque su narrativa
(2.750 chars) se pagaba en cada sesión; los smokes que seguían pendientes quedan en una línea
del `top-of-mind`.

- **TuFacturaIA — Obras-IA: 14 issues + hardening/QA + confirmación de enriquecimiento EN PROD (obras-060..086 + #1094/#1096/#1097, 20-jul)** — descripción auto + clasificador M.O. + presupuesto conversacional, todo desplegado (incl. fix Telematel columnas, tope-1000 diff, drag-scroll ratón, desglose precio con MO). **Confirmación de enriquecimiento HECHA** (mig 529): la descripción IA ya no se ve al cliente sin OK; bandeja de sugerencias (aceptar/rechazar desc + tipo MO). **Precio con MO** (#1098-#1100): desglose con tooltip "cómo se calcula", suma cuadrada, y FIX de fondo — material sin proveedor se valoraba a 0 (catálogo entero a 0 € tras importar Telematel); ahora coste = base de tarifa ×(1+margen), mig 530 recalculó prod. **Desglose auditable por componente** (#1102 + fix #1105, migs 531/532, 20-jul): cada línea muestra su aportación (€/h "Aporta") + efecto del descuento (bruto→neto) + tooltip; `/fia-cierre` cazó un bug de precio-0 en UO con sub-UO vacía (array sin COALESCE + parse estricto) → arreglado y verificado en vivo. **Pendiente:** smoke prod presupuesto conversacional WhatsApp + que Manuel confirme visualmente los precios recalculados tras el deploy de #1100 (smoke P0.4 `test:integration` de `uo-calcular-desglose` ✅ verde 2026-07-21). [[facturaia]]

- **TuFacturaIA — Obras: IA + WhatsApp + MCP COMPLETO (7 PRs #1018/#1024/#1027/#1031/#1026/#1028/#1033, 19-jul)** — copiloto (generar presupuesto NL / explicar precio / insight desvío + imputar parte / aceptar presup. / pedidos / salida / recepción albarán), multimodal (enrutado por intención, factura default seguro), MCP paridad obras (15 tools read+write draft, `/api/v1/obras/*` user-token-only, guard api_key→404). **MCP redeployado 3× a mano, 48→64 tools verificado**. Aditivo, doble-gated, sin frontera fiscal, revisiones adversariales limpias, 3.3 rebasada sin revertir ajeno. **Smokes pendientes (Manu)**: WhatsApp + MCP con token. Follow-ups CERRADOS 19-jul: umbral margen configurable (#1035), single-source copiloto pedido/albarán (#1038), OCR estructurado del adjunto + clasificación por visión (#1039). **20-jul (+smoke real WhatsApp)**: manuales (#1041), negrita `**`→`*` (#1060), **resolución tolerante de entidades** (#1068, prompt v34: materiales fuzzy + obra/proveedor/instalador AND-palabras + `buscarMaterialesObra` + fix generador; causa raíz = el copiloto usaba `buscarCatalogo` genérico ciego a `obras_materiales`, ver [[copiloto-entidad-tabla-propia-necesita-tool-busqueda-y-regla-en-prompt]]). Mig 523 aplicada. E2E verificado en BD: parte (210 €). **Pendiente Manu (tras deploy #1068)**: pedido/salida/albarán + foto factura-sin-caption→factura. Ver [[namespace-v1-reservado-user-token-para-sacar-campo-del-contrato-api-key]]. [[facturaia]]

## Retiradas del dashboard en el cierre del 06-ago (ya cerradas, engordaban el arranque)

- **[03-ago, #1514] Prod y repo reconciliados: 626…637 contigua, sin duplicados** — obras-095 se mergeó sin renumerar a conciencia: sus migraciones ya estaban aplicadas y moverlas habría dejado `schema_migrations` con las dos numeraciones. Regla: con un PR paralelo en medio manda la BD, y se valida con `uniq -d` sobre los números, no mirando el hueco. Ver [[el-hueco-libre-de-migraciones-puede-estar-ya-ocupado-en-produccion]]
- **[03-ago, #1513, mig 637] Latido del runner de tickets, en prod y verificado** — sin cola, un runner muerto era idéntico a uno ocioso (4 h muertas el 02-ago). El sello va dentro del claim, no en un healthcheck aparte que también se puede quedar sin desplegar. Ver [[dockerfile-que-lista-modulos-uno-a-uno-mata-el-servicio-sin-fallar-el-build]]
- **[03-ago, `obras-095`, #1514, ADR-obras-008, migs 630-636] El descuento cuelga del fabricante, en prod** — clave `(org, proveedor, familia, marca)`, gana la más específica y un material sin marca no hereda. Desbloqueó `obras-091`. Al aplicar no se movió ni un precio: el ADR predecía 11.595 materiales subiendo y esa sandbox tenía 0 enlaces material-proveedor. Ver [[una-prevision-de-impacto-que-no-mira-el-join-que-conecta-sobreestima]]
- **[08-jul, #802, mig 449] Cutover de la cola de OCR, resuelto** — cron `ocr-dispatcher` dado de alta y verificado. Lo que quedaba vivo (el smoke) sigue en la sección Smoke del hub.


## Movido del hub en el cierre del 2026-08-06 (poda por trinquete de contexto)

- ~~PR #851 (v1 rechaza `tipo:'abono'`)~~ ✅ **RESUELTO 2026-07-13** — decisión Manu: agency-portal NO crea abonos vía `POST /api/v1/facturas` → mergeado (`d5bb63a4`). Canal correcto = `POST /v1/facturas/{id}/anular`.
<!-- RESUELTO 2026-06-22 (verificado por screenshot): Supabase Auth URL Config OK — Site URL = https://app.tufacturaia.com + 5 redirect URLs (app.tufacturaia.com/**, /invitacion, /invitacion?org=*, /api/auth/callback, /api/auth/callback?type=*). NO se añade localhost:3000 a un proyecto PROD (superficie de ataque innecesaria; el wildcard de prod ya cubre, y el reset usa admin.generateLink con URL propia). Cerrado. -->
- **Reempaquetado planes — casi cerrado** (act. 2026-06-26): mig 399 (#509) + Fase 2B (#513) aplicadas a prod ya cubrieron ~~grandfathering~~ ✅ (PASO 1, override `source='grandfathered'`), ~~Starter canónico 14€~~ ✅ (PASO 0, reconciliado desde 19), ~~sidebar candado~~ ✅ (#513). **Queda vivo**: (1) ~~crear prices Stripe live de Plus~~ ✅ hechos y activos (verificado 29-jul por API); (2) verificar que `stock` en beta no se cobra como add-on de pago (mig 399 PASO 6 tocó incoherencias de add-ons — confirmar). Detalle: [[facturaia-reempaquetado-planes]]


### Pagadores fase 1 — cerrada 2026-08-06 (migs 640→645, PR #1520)

Ledger `factura_pagos` para cobros sin movimiento bancario, `factura_cobros_resumen` como fuente única de la suma, `recompute_factura_estado` como único escritor del estado. Historial de cobros en la ficha y señal `pagador` en el score de conciliación.

Tres incidencias de la propia fase, todas encontradas por el gate de cierre y corregidas:

- **mig 643** — la 641 había hecho `GRANT EXECUTE ... TO authenticated` sobre `factura_cobros_resumen`, SECURITY DEFINER sin filtro de org: PostgREST la exponía con el anon key del bundle. Reproducido en prod. 6ª reincidencia del patrón → cerrado además con el hook `revoke-guard`.
- **mig 644** — la 640 convirtió `facturas.estado` en derivada sin backfill: 1.385 de 1.403 cobradas volvían a `pendiente` con `fecha_cobro` a NULL en cualquier recálculo (15 de 15 medidas). 1.312 filas de respaldo.
- **mig 645** — el backfill de la 644 se acotó con `pendiente_eur > tolerancia` y su verificación preguntaba lo mismo, así que se validó a sí misma: quedaban 99 de 108 negativas cayendo (88 emitidas históricas con total negativo + 7 abonos + 4 vencidas), no «7» como se reportó al muestrear las 60 más recientes. `target_eur` pasa a `ABS(...)` y 95 filas más de respaldo.

Estado final verificado sin muestrear: 1.444 cobradas/pagadas de producción recomputadas, 0 cambian de estado.

### Lo que destapó el /fia-cierre de la fase 1 (06-ago, PR #1520 mergeado en 00862a33)

Trece dimensiones en paralelo. Cuatro defectos gordos, los cuatro reproducidos en producción antes de tocarlos y ninguno cazado por una revisión humana:

- **Fuga cross-tenant de LECTURA** (mig 643): la 641 concedió `factura_cobros_resumen` a `authenticated`; PostgREST la exponía con el anon key del bundle. 6ª reincidencia del patrón → cerrada además con el hook `revoke-guard` en pre-commit.
- **1.407 cobradas a un trigger de volver a `pendiente`** (migs 644+645): la 640 convirtió `estado` en derivada sin backfill. Y el primer backfill se verificó con el mismo predicado que lo filtró, así que dejó 99 negativas fuera diciendo que quedaban 0.
- **Escritura cross-tenant** (mig 646): la política validaba `org_id`, la columna que el atacante escribe, y nada ataba `factura_id`. Un usuario podía marcar cobrada la factura de otra empresa.
- **Doble clic = doble cobro**: el guard de concurrencia vivía de que ese UPDATE escribiera `estado`, y al pasar a derivada dejó de serializar. 2.662 € sobre una factura de 1.331.

Verificación final sin muestrear: 1.444 cobradas/pagadas de prod recomputadas, 0 cambian. Suite Playwright: 125 pasan, incluidas las tres de conciliación (el camino bancario).

### Ledger fase 1 — cierre completo 06-ago (PRs #1520 + #1522)

PR #1520 mergeado con un bloqueante a sabiendas (código preexistente, las migs ya estaban en prod). Al revisar las 9 ramas/worktrees con trabajo sin mergear, encontré el checkout raíz con 3 días de WIP suelta (56 ficheros) mezclando dos cosas: una versión anterior y con bugs de trabajo YA mergeado (contraste AA, orden de providers, CSS movido a módulo compartido — descartada, verificada archivo a archivo), y una feature real sin equivalente en main (SkeletonTable en Obras+dashboard, fix `opsa` en agentes, docs de `cron_runs`, y el hook `/fia-cierre` que se disparó de verdad sobre mí en esta misma sesión). La real se organizó en 5 commits atómicos y se mergeó como PR #1522.

Al hacer inventario de las 87 ramas locales sin worktree, dos métodos rápidos (`git cherry`, diff de tres puntos) dieron falsos positivos por el mismo motivo: ninguno compara árboles actuales, y este repo hace squash-merge. Con el método correcto (árbol actual vs árbol actual, solo en los ficheros tocados), las 87 salieron confirmadas redundantes — 3 de ellas eran borradores anteriores de un informe QA que main ya tiene completo, así que mergearlas habría sido un retroceso. Ver [[tres-puntos-y-git-cherry-mienten-en-ramas-squash-mergeadas]].

Queda abierto el issue #1521: `importar_emitida_externa` es un tercer escritor de `facturas.estado` que regenera la misma mina que las migs 644/645 acabaron de desactivar. Prompt de continuación entregado con el fix ubicado línea a línea.

**Issue #1521 cerrado el mismo 06-ago (mig 647, PRs #1523+#1524).** Fix calcado del patrón de la 644: inserta la fila de ledger en el único punto donde convergen las dos ramas de `importar_emitida_externa` (antes del `INSERT INTO lineas_factura`), y deja de escribir `estado`/`fecha_cobro` a mano. Verificado en los dos sentidos con `supabase/tests/647_importar_emitida_externa_ledger.validate.sql` (patrón de la 470: org de prueba propia + rollback interno). **El pooler de Postgres (5432/6543) daba timeout desde la máquina de desarrollo** (ver [[supabase-pooler-timeout-isp-fallback-dashboard]]), así que la migración se aplicó y verificó a mano por el SQL Editor del dashboard en vez del `psql`+`BEGIN…ROLLBACK` habitual — mismo resultado, un paso más manual. Reconciliado además `supabase_migrations.schema_migrations` sin CLI: diff bidireccional por SQL puro (`string_agg` de versiones remotas vs `ls supabase/migrations/` local) confirmando 609=609 antes de cerrar. Con esto el bloque "ledger de cobros y pagadores" (#1519/#1520/#1521) queda cerrado del todo.
