---
title: facturaia — histórico eventos (2026-06-16 a 2026-07-13)
date: 2026-07-13
tags: [facturaia, historico, eventos]
---

## 2026-06-16 · Informes de analítica 089-092 (CERRADO, en prod)

PRD `issues/prd-informes-analitica.md` (análisis comparativo vs Holded). 4 informes colgados del hub `/informes` (tarjetas, sin tocar sidebar):
- **Ventas**: por cliente/producto/mes, margen sobre coste de stock + cobertura, narrativa determinista, descuento global aplicado. KPI principal "Ventas emitidas (base, sin IVA)" + secundario **"Pendiente de emitir"** (borradores, solo si count>0).
- **Gastos**: por proveedor/categoría/mes. KPI "Gasto aprobado (base, sin IVA)" + secundario **"Pendiente de aprobar"** (recibidas en `sin_aprobar`, solo si count>0).
- **Objetivos**: tabla `objetivos` (mig **296**, RLS + 4 políticas + CHECK facturación-sin-categoría), CRUD gateado propietario|admin, sugerencia determinista desde histórico, widget dashboard.
- **Actividad**: REUTILIZA `AuditoriaSection`/`buildAuditFeed`; **feed acotado por rol en la capa de datos** (`viewerScope`: admin/propietario/superadmin → equipo; resto → solo lo suyo). Cierra exposición cross-usuario pre-existente del endpoint compartido.

Server-side `/api/informes/*` + helpers puros `src/lib/informes/*`. Tool copiloto `getInformeVentas` (reusa `buildVentasReport`). Manuales usuario+admin actualizados.

**Auditoría multi-agente** (seguridad/correctitud/frontend/composición) + correcciones: dark-mode (tokens `--line`/`--bg-elev`), trim categoría, `.limit()` determinista, validación sugerencia, truncated flag, descuento global, inline-styles→CSS Modules, **doble "€ €" en KPIs** (`fmt()` ya incluye €).

**Decisión abonos**: informes + dashboard + copiloto `getKPIs` los EXCLUYEN (`tipo_documento='factura'`) — la anulación deja la origen en `anulada`; contar el abono negativo restaría 2× → "Facturado" negativo falso. El 303 sí los incluye (correcto fiscalmente). Bug `getKPIs` (incluía abonos) corregido (`a3493b12`).

**Verificado**: 176+ tests, lint+typecheck+build limpios. Playwright (login real) read+write-path verdes en prod, 0 residuo. Mig 296 aplicada a prod (`db push --include-all`, iba por detrás de 297). Bug `proveedores.empresa` (no existe columna; sí en `clientes`) cazado y fijado → [[proveedores-no-tiene-columna-empresa-asimetria-clientes]].

Commits en main: `d2fcc81b` (barrido por sesión paralela 088) + `fe346a29` + `7c52cbad` + `a3493b12` + `858f79fa` + `954dd181`.

---

## 2026-06-24 · Bug recibidas "no se puede cumplimentar NIF proveedor"

Ticket soporte Pescados Chivite (proveedor francés SARL HUITRES GEAY, NIF vacío en recibida `pendiente`). **Causa**: `saveEdit` (`facturas-view.tsx`) bloqueaba TODO guardado fuera de `sin_aprobar`, mezclando datos fiscales del documento (inmutables, RD 1619/2012) con datos maestros del proveedor (nombre/NIF, del contacto).

- **#464**: completar nombre/NIF del proveedor vinculado se permite en cualquier estado de la factura; los campos fiscales siguen restringidos al estado editable.
- **#467**: si la recibida no tiene proveedor (`proveedor_id` NULL — 29 en prod, OCR sin emisor), `ensureProveedor` hace find-or-create (NIF identidad fuerte, nombre respaldo; espejo del emparejado de la bandeja de ingesta) y vincula el id a la factura. Antes el nombre/NIF tecleados se descartaban en silencio.

Spec E2E de regresión `tests/e2e/smoke/recibidas-completar-nif.spec.ts` (2 casos, verde en localhost con seed/cleanup vía service-role en org sandbox). lint+typecheck+build limpios. Ambos PRs MERGED a main (`178ecf55`, `44063312`).

### Stock — descuento por lotes (ticket Chivite, 2026-06-25)

- **#488 + mig 388**: ventas de productos con `gestiona_lotes` no descontaban stock — el motor `aplicar_movimientos_lotes` exigía `lote_id` y fallaba en silencio (`raise warning + continue`) cuando no llegaba; varios bordes lo descartaban (Zod no-strict en `POST /api/facturas`, schema `.strict()` en `PATCH`, payload UI, schema API v1). Fix de raíz: **auto-FEFO en el motor** (consume partidas por caducidad/entrada con split; sobreventa→excepción, nunca silencio) como single source of truth para todos los canales (web/API/voz/copiloto) + propagación de `lote_id` en los bordes como defensa en profundidad. Reconciliación one-off de las 3 facturas ya emitidas de Chivite (A2026-0001/0002/0003). Desplegado y verificado en prod (smoke 3/3 + test FEFO transaccional). Learning [[motor-con-input-requerido-debe-defaultear-no-fallar-mudo]].

### Hitos 2026-06-28 → 07-04 (migrados desde `00-home/facturaia-historico-detallado.md`, fork duplicado consolidado 2026-07-05)

2026-06-28 · fix duplicar factura: copia líneas+presentación (`unidad_medida`, `cantidad_presentacion`), nunca hereda `lote_id` (#578) + test regresión e2e + invariante CLAUDE.md (#580). Ticket Dani 3eb1aec3.

2026-06-30 · PR #607 — «Convertir en recurrente» en menú `…` lista de emitidas + overlay panel en modal detalle (gateado módulo SEPA) + refactor ingesta justificante a state machine keyed por item. Ticket Borja.

2026-06-30 · Presupuestos propios detectados en OCR (issues `ingesta-presupuesto-001..006`, `40a6b0c3`+`810aa86c`): `doc_type='presupuesto'` local a `ocr-process` (sin ensuciar el `DocType` compartido con conciliación), descarte+`tipo_generado` reutilizado, migración `presupuesto_id`, endpoint `crear-presupuesto` idempotente con guard de duplicado y cierre de race, CTA en ingesta-view. Smoke real cazó y arregló 2 bugs de prompt; clasificación queda pendiente de validar con un presupuesto real (no solo el fixture sintético). Ver [[mock-no-actualizado-tras-refactor-io-rompe-suite-sin-aviso]] (de paso arreglé la suite de tests rota).

2026-07-01 · Ticket rápido (PRs #620-#635, #631, #637) — emisión proactiva de factura simplificada sin movimiento bancario, para cobro en efectivo/Bizum al momento. Fase 1 web (endpoint + modal standalone + entrada sidebar/generar + PDF/email) y Fase 2 Copiloto (`emitirTicket`). Fix same-day tras QA visual del usuario: `estado` quedaba `pendiente` sin marcar cobrado (contaminaba KPIs/cashflow/vencidas) + inputs/select sin estilo canónico `form-input`. Verificado en real contra sandbox. Ver [[documento-dinero-ya-cobrado-debe-marcarse-cobrada-explicito]].

2026-07-02 · **Migración clientes Supabase tipados COMPLETA (PR #648, mergeado con review 8-ángulos)** — `createAdminClient`/`createServerSupabase`/browser → `SupabaseClient<Database>`; 341 errores→0 en 12 commits gate-verdes (alias tipado incremental), suite 4320 tests, `as any` src 29→10. **10 bugs prod destapados** (clase 42703 silencioso): worker VeriFACTU no-op desde 05-18, emails branding fallback, duplicar v1 404, is_admin nunca concedido, fallback PDF email, export fiscal sin NIF, getURLPDF presupuestos, /api/health modo lectura, audit admin global, rama muerta sourceTable. Nuevos `zod-json.ts` + `database-overrides.ts`. Decisiones pendientes → gotchas.md (§VeriFACTU, §Auth). Merge `--admin` (revisión delegada por Manu). Ver [[supabase-tipar-admin-client-global-cascada-300-errores]] · [[supabase-select-columna-inexistente-falla-query-entera-42703]] · [[supabase-gen-types-numeric-override-bigint-string]].

2026-07-03 · **Exportación contable para gestorías COMPLETA (tren #653/#654/#657/#658 mergeado)** — libro registro normalizado (1 fila por factura × tipo IVA, XLSX 3 hojas + CSV `;`/coma, IRPF prorrateado con ajuste de céntimo, degradación por hoja Avisos) + **formato oficial AEAT** (plantilla LSI v9.0 de la sede, importable en Pre303 y A3 sin mapeo) + /informes conectado al endpoint (fix TZ rangos −1 día, columna IVA=total−base, resumen con floats, cards muertas) + deep-link en copiloto. De regalo: **fix Libro IVA roto en prod** (500 permanente, columnas x100 inexistentes) + loader compartido con paginación max-rows y chunking `.in()` + `isOrgInTrial` con regla fiscal server-side. QA: Playwright 6/6, verificación numérica independiente al céntimo (export ≡ casillas 303 en pantalla ≡ recompute BD), auditoría 3-agentes con fixes. Merge `--admin` (OK Manu). Pendiente: deploy+smoke prod, Pre303 HITL. Ver [[ADR-036-export-contable-libro-registro-sin-pgc]] · [[facturaia-export-gestoria-v15]].

2026-07-03 (tarde) · **QA post-deploy export gestoría: 7 PRs mergeados+desplegados** (#661 visual detalle sin hueco + menús canónicos row-menu + chevron + alturas ancladas · #662 orden intent multi-org · #676 builders lazy `void` + ojo facturas cableado a `?factura=` + céntimos-string tool/v1 · #678 estimación IVA en vivo · #679 trimestre_actual + formato es-ES · #680 respuesta dual a-presentar/en-curso · #681 anti-anclaje ABIERTO). Bot WhatsApp curado en 3 capas (ver incidents); verificación final por el endpoint interno real: "2T 2.100,20 € vence 20/07 + 3T 35,32 € acumulados". Reset del hilo de Manu (100 mensajes). Deploys por autodeploy verificados por timestamp.

2026-07-04 · **Auditoría `audit_log` Bloques 1-3 CERRADOS (7 PRs: #685/#690/#691/#693/#694/#696/#698)** — mapeo previo (Explore agent, grep exhaustivo) encontró ~0 de 25 endpoints/RPCs de conciliación con `logAgentAction`; decisión tomada: explícito en cada endpoint, no ampliar `feed.ts` a leer `module_events`. Bloque 1 seguridad crítica (2FA/security-policy, teléfono sin OTP, merge destructivo clientes/proveedores, NIF onboarding), Bloque 2 API v1 (clientes/proveedores/presupuestos/catálogo/stock), Bloque 3a+3b conciliación completa (mutaciones directas + 9 RPCs, incluido el soft-delete de movimiento que no tenía NINGÚN rastro). Hallazgo grave post-merge: 27 `accion` de conciliación salían en formato máquina (`movimiento_bancario.delete`) para actor `human` porque la UI de Ajustes→Auditoría renderiza `accion` literal (sin humanizer) — solo se detectó con smoke visual real de la pantalla, no verificando inserts en BD; PR #698 lo corrigió + añadió 11 entidades a `ENTIDAD_LABEL`. Merge `--admin` en los 3 PRs contra `main` (ruleset de 1-aprobación bloquea auto-review de tu propio PR, no relacionado con CI). Ver [[trigger-audit-solo-registra-sesion-humana]]. Bloque 4 (cobros/recurrentes/remesas/settings menores) queda pendiente, baja prioridad.

### Datos y backups fases 3-4 — smoke prod completo (2026-07-05)

**MERGEADO a main 2026-07-04, 4 PRs `--admin`** — #692 limpieza de exports caducados (enum `expired`) + endurecimiento runner · #695 higiene/aislamiento PDFs por org · #697 puente gestoría **a3 SUENLACE.DAT + SII XML** (validado byte-a-byte + xmllint contra XSD AEAT, tarjeta en Ajustes›Datos) · #699 **cierre de cuenta = BLOQUEO** (nunca DELETE; gracia 72h; mig 429 en prod; trigger anti-borrado; audit append-only). Cron `account-closure-apply` en Dokploy (scheduleId `_ceKyBGW6-tNGxE8briwd`, `0 3 * * *`).

**Smoke prod 2026-07-05 (completo)**: (1) descarga a3 SUENLACE.DAT — 151 registros, ISO-8859+CRLF, todas las líneas 255 chars exactos (ancho fijo correcto) · SII emitidas XML (83KB, `xmllint` OK, `SuministroLRFacturasEmitidas`, 132 registros) · SII recibidas XML (12KB, OK, 18 registros). Ubicación: `/settings?tab=datos` → "Export para gestoría (a3/SII)". (2) ciclo cierre de cuenta con org de test desechable (`6d9aa0f4`, 0 facturas, aislada): `account_closure_grace_until` forzado al pasado → `runManually` del cron vía API Dokploy → `account_closed_at`/`account_closure_applied_at` poblados (bloqueo real), fila y datos intactos (nunca DELETE, trigger `trg_prevent_org_delete_with_fiscal_docs` confirmado en `pg_trigger`), `cron_runs` verde (`triggered_by: dokploy`, corre también solo cada día 01:00 UTC sin intervención) — org de test revertida a estado original tras verificar. (3) `data-export-runner`: 60/60 `success` en la última hora (corre cada minuto), tabla `data_export_jobs` vacía (nada caducado que limpiar hoy).

Nota metodológica: `psql` directo se cuelga en este entorno (probable bloqueo de puerto Postgres del sandbox) — usar el tool MCP `mcp__supabase__execute_sql` para queries read-only contra prod en su lugar.

### Dedup NOTES.md CERRADO — 5 PRs adicionales (2026-07-05, #757-761)

`calendario` (dayISO/truncate16), `cashflow` (psd2BancosLabel), `ingesta` (normalizeNif/normalizeProvName), `conciliacion` (memo porRevisarMovs + matchesTransferFilter); `generar-view` resultó no-op al coincidir byte a byte con #756 de sesión paralela. Las 9 duplicaciones idénticas de la auditoría, resueltas. Mecanismo: 5 worktrees + build/QA localhost/verificación `state=MERGED` por PR.

### Ingesta — desplegable «⋯» canónico + copy de error OCR en español (2026-07-10, #813)

Dos fixes de bandeja detectados por Manu en prod (captura): (1) el menú «⋯» de `BulkBar` (selección múltiple) y `ActionBar` (por-doc) usaba un `overflow-pop` casero → migrado al patrón canónico `useAnchoredMenu` + `.row-menu`/`.row-menu-item` (mismo que fiscal/equipo); CSS muerto `.overflow-*`/`.ab-overflow-pop` eliminado. (2) La bandeja mostraba el `last_error` técnico crudo (`max_attempts_reached: status_502`, escrito por el worker de la cola OCR) → helper `ocrErrorLabel()` traduce a copy español; el crudo queda en el `title` para soporte. Mergeado `--admin` + **verificado en prod** por comportamiento (DOM: menú con clase `row-menu` no `overflow-pop`; cero `status_502` crudos). Manuales revisados: no requieren cambio (mismos ítems/acciones).

### Drawer «Personalizar» del Resumen sobre el shell canónico (2026-07-10, #819)

Ticket `678aa22c` (Borja): el panel de personalización del dashboard se veía "demasiado transparente" — era un drawer a mano con `var(--bg-elev)` (60% translúcido en skin glass) sin `backdrop-filter` ni scrim. Migrado a `ui/drawer.tsx` (glass-panel + sheen + scrim + focus trap + ESC + aria-modal), −97 líneas; el module.css queda solo con presets/toggles. Override `.body.body` (clase doblada) porque el orden de bundle entre CSS Modules no está garantizado — primer consumidor de `bodyClassName`. Verificado en localhost con e2e+smoke (captura antes/después en artifact). Merge `--admin` tras gates locales verdes.

### Ajuste global de fondos al abrir drawers/modales (2026-07-10, #821)

Follow-up del #819 a petición de Manu: `--glass-bg-panel` +20% de opacidad y `--scrim-bg`/`--scrim-fallback-bg` ∓20% en los 4 bloques de tema (base+freebie × light+dark) — el panel se ve más sólido y el fondo detrás más claro. Solo `tokens.css`; aplica a todos los drawers/popovers/modales (fuente única). QA visual localhost claro+oscuro aprobado antes del merge.

### Sesión de cierre de pendientes (2026-07-13)

Triaje: el hub NOW/WIP estaba muy stale — decenas de PRs marcados 🔴/🟡 ya MERGED (verificado por `gh pr view`: #754 #766 #767 #771 #772 #781 #798 #799 #811 #841 #866 #869 + wa-fase #700/#701/#702). Trabajo real:
- **PR #871 (totales, follow-up de #869)** — `subtotalLinea` exportado como sede única y usado en `PATCH /api/facturas/[id]` sin redondear; el editor de borrador persistía el subtotal redondeado por línea (drift ±1 cént. vs XML VeriFACTU que suma crudo por grupo). Gates verdes + test de regresión. **Pendiente: merge de Manu (=deploy).** Ver [[totales-multilinea-redondeo-por-grupo-de-iva-una-sede]].
- **Rama `feat/copiloto-ux-markdown-ancho-botones` = CRUFT** — contenido íntegro ya en main vía PR #841 (mergeado 12-jul, v32 plegado, main en v33); confirmado con `git range-diff`. Borrada local+remota.
- **PR #825 (Centro Fiscal)** — estaba 43 commits por detrás de main. Merge de `origin/main`, resuelto conflicto trivial de import (MessageFeedback+AssistantMarkdown coexisten) + 3 errores de integración (`ejercicio` a `CuadreResolverDrawer` en detalle 180/190/347, igual que 349). Gates verdes (typecheck/lint/build, 5049 tests; único fallo ajeno = `registry-wired`, crons `ocr-dispatcher`/`copiloto-insights` sin cablear en admin). **MERGEADO `--admin --squash` (bypass autorizado por Manu).** Migs 452/453 aplicadas a prod (Manu lanzó `db push --include-all` por el gate de producción; verificadas: columna `situacion_inmueble` + `fiscal_plazos` 111/115/180/190/347) ANTES del merge (orden: schema antes que deploy). #871 también mergeado `--admin`. Smoke prod fiscal pendiente tras deploy.
- **PR #872 (crons)** — cableados `ocr-dispatcher` + `copiloto-insights` en el switch `loadHandler` de `/api/admin/crons/run` (estaban en CRON_REGISTRY sin case → "Run Now" 500 + test `registry-wired` rojo, único fallo de la suite en main). Mergeado `--admin --squash`. Suite verde.
- **Limpieza de worktrees**: de ~20 a 5. Borrados 14 verificados como merged (0 ahead) o squash-merged (PR MERGED confirmado por `gh pr view`: #641/#754/#851/#787/#798/#772). Conservados: `saltedge-psd2` (#610 draft), `fix-gestor-externo-ux` + `informes-selector` (trabajo real sin PR, flageados en hub WIP), `agent-a80ef300` (detached huérfano). Cuidado con el falso positivo de squash (`ahead>0` ≠ sin mergear) → ver [[git-merge-base-is-ancestor-falso-negativo-con-squash]].


## 2026-08-08 · Las 12 quejas de UI de Obras (#1546 + #1550)

Doce defectos visuales del presupuesto de obra y del pedido, todos cerrados. Lo que merece
recordarse son las tres cosas que aparecieron al verificarlos con medidas en vez de a ojo, ninguna
pedida:

1. **La recepción de albarán rotulaba «Material» en casi toda recepción real.** Traía el catálogo
   completo con `GET /api/obras/materiales` para traducir `material_id`, y ese endpoint pagina a 50:
   **50 de 11.595** en la org de pruebas, y el material de la 1ª línea de un pedido real no estaba en
   esa página. Fix por eliminación: `getPedidoDetail` ya devolvía `material_denominacion`.
   → [[resolver-label-nombre-en-cliente-contra-endpoint-paginado-cae-al-uuid]]
2. **El trinquete de estilos en línea se podía esquivar** sacando el objeto de `style={{…}}` a una
   variable. Aguja a `/(?<![\w-])style=\{/g`, baseline 770 → 895 (125 que ya existían y no se veían).
   → [[un-guard-cuya-aguja-cubre-una-sola-forma-sintactica-se-esquiva-refactorizando]]
3. **Una «fuente única» de formateo dentro de un módulo `server-only`**, que por construcción no
   podía serla: export sin consumidor mientras cada pantalla concatenaba a mano. Silencioso — un
   export sin usar compila. → [[crypto-modulo-server-only-bloquea-scripts-cli-extraer-primitivas]]

Lo entregado: densidad unificada en `--control-h-md` (36 px) en toda la app, `ColumnPicker` sobre la
rejilla de costes (18 columnas → las que quieras; cada una descontada resta su ancho + 6 px de hueco,
de 768 a 122 px de exceso), cabecera y filas con `subgrid` para que no puedan desalinearse, y la
unidad de medida en las cuatro pantallas del pedido con fuente única de resolución
(`lib/obras/unidad-material.ts`) y de formateo (`lib/obras/unidad-formato.ts`).

El gate corrió 4 rondas: la 2 salió **no listo** con 2 bloqueantes. En la 4, `datos` agotó los
reintentos de `StructuredOutput` y `codigo` devolvió `"test"` como resumen — registrado en
`cierres.json` por lo que corrió de verdad, no por lo que se invocó.
→ [[dos-salidas-contradictorias-no-son-un-mecanismo-hasta-que-lo-reproduces]] · artifact `d50dd108`

### Cifras completas del catálogo de IET (medido 07-ago-2026, en prod por organización)

Corrige un diagnóstico anterior que decía «falta el tiempo de MO en 7.683 materiales»: no faltaban
tiempos, faltaba el catálogo. Los 7.683 de su org son **dos tarifas de fabricante y nada más**:
SIMON 6.387 + GENERAL CABLE 1.296. Su catálogo de trabajo real vive en la org sandbox
`Obras tufacturaia sandbox`, del volcado de WAPI del 21-jul: **11.595 materiales con 7.871 tiempos de
MO** y **3.945 unidades de obra con 13.083 líneas**.

Cobertura ponderada por uso: **0,9 %**. De las 59.220 líneas de material de sus 2.380 presupuestos
históricos, solo **525** apuntan a un material que hoy existe en su org. Casan **433 por
`cod_almacen` (5,6 %)** y el casado es real: mismo artículo con distinta nomenclatura. Lo que SÍ está
correcto en su org son los **745 tipos de mano de obra** con sus horas.

### 2026-08-08 · La fila del pedido en móvil (#1541/#1551), y una falsedad que casi shipeo

Resuelto y en `main` (`bc90dcd8`). Se documenta aparte por dos cosas, y ninguna es el CSS:

1. El trabajo vivía en un stash etiquetado **«restos-obsoletos»** con 78 líneas razonadas que no
   estaban en ninguna rama. No fiarse de la etiqueta: mirar el contenido.
2. De una anomalía al leer ese stash inferí un mecanismo de git («`refs/stash` es por worktree»),
   lo escribí en cuatro documentos y estuve a punto de shipear un hook con él. **Era falso**, y lo
   refutó un repo de prueba de 60 segundos. Lo que sí sobrevivió, porque estaba medido, es la regla
   6 de `git-guard.sh`: `worktree remove` con cambios sin commitear, con 5 casos en su suite.

Crónica y diff → [[facturaia-pedido-movil-390-issue-1541]] ·
[[dos-salidas-contradictorias-no-son-un-mecanismo-hasta-que-lo-reproduces]]

---
title-evento: empaquetado y circuito de cobro — los 15 PR mergeados y en producción
date: 2026-08-14
---

Cierre de la tanda de las specs #1678 (integridad del cobro) y #1679 (empaquetado y modo
prueba): **15 PR mergeados**, sus issues cerrados y las migraciones **679-687 aplicadas y
verificadas por catálogo** en prod (columnas de descuento en `organizations` y
`billing_accounts`, `plan_limits.cuentas_bancarias` 3/10, `plans.empresas_incluidas`=2 en
Plus, `conciliacion` habilitada en Pro). Más **#1754** (PR #1766): el panel de admin ya
decide con el plan efectivo en las tres lecturas que quedaban fuera de #1696, y
`pickEffectivePlan` normaliza el embed cuando llega como array de uno.

**Las tres decisiones que esperaban a Manuel, respondidas**: límite de cuentas bancarias
3 Pro / 10 Enterprise aprobado; baseline del trinquete de `registry.ts` subido a conciencia
(contrapartida = #1751, partir el fichero); `CONTEXT.md` §Dominio fusionado quedándose las
dos mitades (la corta aporta anclajes de implementación, la larga el porqué), y ADR-013 gana
la decisión que faltaba: ningún tier incluye complementos.

**Lo que cazaron las auditorías antes de mergear**, ninguno detectable por el gate: un cron
que iba a mandar email de severidad alta **en cada impago normal** (72 h de gracia con la
suscripción en `past_due`); dos `UPDATE` sin leer su `error`, con un cupón de importe fijo
violando el CHECK en silencio; ids en `snake_case` enseñados al cliente en el modal de bajada
de plan; una incidencia de webhook que no la cerraba nada nunca; una card que se escondía
entera si fallaba su GET; y un CHECK que se vendía como candado cerrando una sola dirección.

**Deuda abierta con número**: #1750-#1759. **Raíces de lo que queda**: #1702 (checkout
genérico de complementos) y #1712 (la matriz de empaquetado), las dos arquitectura.

Aprendizajes: [[pre-push-que-typechequea-con-next-build-no-mira-los-tests]] ·
[[renumerar-migraciones-reescribe-referencias-de-migraciones-ajenas]] ·
[[stripe-sin-account-tax-ids-la-factura-sale-sin-nif-del-emisor]] ·
[[conflicto-rebase-json-generado-regenerar-no-mergear-a-mano]] ·
[[claude-code-agentes-worktree-failure-modes]]

## 2026-08-15 · Spec #1678, circuito de cobro con eventos reales de Stripe

🟢 **Spec #1678 cerrado y el circuito probado con eventos REALES de Stripe (15-ago)** — CLI emparejado con `acct_1Td5cc`, modo test, misma versión de API que live (**caduca 12-nov-2026**). Probados mirando el efecto en BD: impago de complemento y recuperación, disputa, reembolso, reactivación e idempotencia. **Salieron dos fallos que la suite no veía**, ya en prod: **#1788** (pausar el cobro no suspendía; la reactivación pasa a mirar el motivo, mig 693) y **#1789**. Cerrados también #1773 y el PR 1/4 de #1702. Queda **#1686, tuyo**. [[stripe-pause-collection-no-emite-subscription-paused]] · [[ADR-052-persistir-el-motivo-de-la-suspension-de-cobro]]

## 2026-08-18 · T1 item 1 cerrado: contrato de `requires_recalc` y un endpoint retirado

🟢 **#1888, #1889, #1890, #1891 en prod (18-ago)** — el recuento de partida estaba mal: no eran «5 de 7 lectores hechos», eran **4 de 7** (la vista de detalle ya leía el flag desde #1219/#1237/#1303, y `hub-timeline` + `historico-trimestres` son una fila del inventario, no dos).

De las tres que faltaban: **`share` queda como excepción declarada, sin 409** (la página de gestoría evalúa el flag en cada render, así que ya avisa en vivo y cubre el caso que un bloqueo al compartir no cubriría: que caduque *después*). **`explicar` se niega con 409** — el panel ya traducía ese código con el copy exacto, escrito antes que el guard; el primer intento fue añadir un campo al sobre y **no lo leía nadie**, el mismo «cero consumidores» por el que se retiró el endpoint. **`calendario` se retiró**, no se arregló: 0 consumidores por grep del literal, aristas de madge y ausencia de test; la UI lee `fiscal_plazos` directo. Sobrevivió porque `huerfanos.md` lo salvó con un «tiene 20 consumidores» falso (ese documento fallaba en **2 de 2** falsos positivos comprobables).

El `declMap` no era puntual: `hub-timeline.tsx` y `proximo-plazo-card.tsx` hacían `Map.set()` sin guarda sobre un array ya ordenado `num_secuencia DESC`, así que ganaba **siempre** la fila superada. Y aparecieron **dos lectores ciegos que el inventario no tenía**: `v1/fiscal/iva-trimestral` (lo consume agency-portal) y el tool `consultarIvaTrimestral` del copiloto, que además devolvían dos filas contradictorias por trimestre. Todo latente hoy: nada escribe `num_secuencia > 1`.

Contrato en `src/lib/fiscal/__tests__/contrato-lectores-requires-recalc.test.ts` con el detector en `contrato-lectores.ts` (17 tests de dientes, límites escritos en su docblock). Smoke en prod con agent-browser: **409** en «Explícame» sobre una declaración caducada con el copy visible, 200 en una sana, y en la API pública el **2T `cuadrado` con `requires_recalc:true`** — el caso peligroso, visible por fin. Ocho mutaciones, ocho víctimas. Suite sobre main mergeado 12.982/0.

Queda abierto el **punto 4, la deriva de perfil**: decisión de arquitectura, no parche. → [[un-gate-derivado-del-repo-necesita-guarda-contra-su-propia-ceguera]] · [[next-typed-routes-validator-stale-tras-cambio-de-rama]] · [[pipe-a-tail-enmascara-el-exit-code-del-comando]]
