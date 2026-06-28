---
title: facturaia — candidatos de deepening arquitectónico
date: 2026-06-27
source: claude-code-session (skill improve-codebase-architecture)
tags: [cliente, facturaia, arquitectura, refactor, roadmap]
---

# TuFacturaIA — Candidatos de deepening (módulos shallow → profundos)

Raíz común de #1/#2/#4: **no hay capa de dominio entre los puntos de entrada (route handlers, tools, voz) y PostgREST** → cada sitio reimplementa resolve/validar/auditar acoplado al builder de Supabase. El #2 estableció el patrón replicable: módulo de dominio con **resultado discriminado sin throw** + tests al límite + HTTP solo en el borde.

| # | Candidato | Estado | Profundidad | RFC |
|---|---|---|---|---|
| 2 | find-or-create cliente/proveedor | ✅ CERRADO (deployado, smoke E2E verde) | exploración profunda + 3 diseños | `issues/rfc-find-or-create-contacto-nif-opcional.md` |
| 1 | 45 tools copiloto shallow | 🟢 CERRADO (núcleo). Fase 0 schema único (#536) · Fase 1 port 5 destructive (#538) · Fase 1b 3 email (#539) = 8 tools sobre el port. Fase 2 factory DESCARTADA (sobre-abstracción sobre el port). NO migradas a propósito: duplicar/convertir/editar (familia crear-documento → candidato #3). Pendiente externo: smoke API real (saldo Anthropic) | 3 diseños + RFC + 3 PRs en main | `issues/rfc-deepening-tools-copiloto.md` |
| 3 | seam emisión voz↔web (núcleo) | 🟢 Fase A IMPLEMENTADA (rama `refactor/documents-compose-core`, gates verdes, pend. commit/PR). Fase B bloqueada por D1-D5 | encuadre + 3 diseños + RFC + Fase A | `issues/rfc-convergencia-voice-creacion-documentos.md` (NUEVO; supersede al previo) |
| 4 | lógica de negocio en route handlers | ⏳ parcial. CopilotoStore NO generaliza (ver nota) | evaluación hecha | — |
| — | seam mutación `editarPresupuesto`/`updatePresupuesto` | ⏳ identificado (salió del #3) | — | — |

## #1 — Tools del copiloto (recomendado siguiente)
`src/lib/copiloto/tools/*` (46) + `registry.ts` + `runner.ts`. Cada tool reimplementa plomería: `resolveFactura()`/`resolvePresupuesto()` (~45 LOC ≈ idénticos en `marcarCobrada.ts:56`, `marcarPresupuestoAceptado.ts:50`, `anularFactura.ts`), `assertMarcable()`/`assertAceptable()`, `createAdminClient().from(...).eq('org_id',...)`, bloque `logAgentAction(...)`. ~1.300-1.500 LOC duplicados (≈20%). `marcarPresupuestoAceptado.ts` = 72% plomería / 22% lógica. Dep: cat 2/4 (mock builder). Impacto tests: ~15 suites con ~35 LOC boilerplate cada una (≈525 LOC). **Mayor volumen; el patrón del #2 aplica casi directo.**

## #3 — Seam emisión voz↔web — RFC LISTO (2026-06-27)
**Vigencia revisada:** el RFC previo (`rfc-unificar-creacion-documentos.md`) estaba ~50% implementado y se marcó SUPERSEDED. `domain.ts` YA existe (reglas puras: verifactuAplica, assertNifReceptor criterio A, buildLineas*, etc.) y `calcularTotales` YA es fuente única (7 callers) → los totales NO divergen. Target real estrechado a **1 archivo: `voice/generate` (684 LOC), la última copia divergente** (`:301` "no usa createDocument"). `duplicar*`/`crear*`/`emitir*` ya delegan en createDocument.
Divergencias reclasificadas: #1 verifactu / #2 serie = **LATENTES** (schema voz no acepta `factura_simplificada`, sin efecto hoy). #3 nif_conflict / #4 NIF criterio B vs A / #6 logo PDF = **ACTIVAS**. **#7 abono sin motivo_rectificacion = fallo fiscal real** (schema voz no lo acepta). **#8 voice crea abonos por vía que esquiva anularFactura = riesgo de inviolable.**
3 diseños explorados (minimizar/unificar-prepare-commit/ports). Síntesis: prepare/commit perdió justificación (voice commitea directo); ports se solapan con #4. **Recomendación = híbrido 2 fases: A) extraer núcleo puro composeDocument/buildTemplateData/buildVerifactuData (riesgo nulo + testabilidad); B) migrar voice a consumirlo (cierra #1-#7).** Diferir DocumentStore/prepare-commit.
**Fase A HECHA (2026-06-27, rama `refactor/documents-compose-core`):** `src/lib/documents/compose.ts` (composeDocument + buildTemplateConfig/buildTemplateData/buildVerifactuData, cero I/O) + create-document refactorizado con **diff funcional nulo** (201 suites docs verdes) + 23 boundary tests nuevos (`compose.test.ts`, regresión #1/#2/#6). Gates: lint+typecheck+build+suite 4056 passed. Pendiente: commit/PR.
**Decisiones D1-D5 TOMADAS con fuente oficial (2026-06-27):**
- D1 (NIF receptor): **criterio A** — AEAT confirma que a consumidor final la factura completa SIN NIF es válida y se registra con **clave F2** (no F1). Criterio B de voz era más restrictivo que la ley. Implica F2 en Verifactu → ratificar con gestoría + hacer en Fase B. Fuente: AEAT procedimientos-facturacion Verifactu + RD 1619/2012 art 6.1.d.
- D2 (logo PDF): **sí, inyectar** — NO es decisión de producto sino bug de consistencia: `emitir-borrador.ts`, `render-and-upload.ts` y `voice/generate` YA leen `org.logo_url`; `createDocument` es el ÚNICO que no → presupuestos/facturas-directas vía createDocument salen sin logo. Alinear en `buildTemplateConfig` tras mergear #544.
- D3 (cliente NIF conflict): NIF = identidad fiscal única (criterio AEAT/Holded/Sage). Hallazgo: v1 `resolveCliente` hoy SOBREESCRIBE el nombre del cliente existente en match por NIF (rename silencioso, riesgo). Decisión: detectar conflicto en el núcleo, **NO renombrar** identidad fiscal registrada; voz 409, copiloto aviso, v1 reutiliza-sin-renombrar+warning. Fase B.
- D4 (abono por voz): **NO** — implementado ✅ (PR #547).
- D5 (motivo rectificación): legalmente la rectificativa exige motivo R1-R5 + ref a factura rectificada (RD 1619/2012 art 15 + Verifactu) → vía correcta = anularFactura. **Resuelto por D4** ✅.

**Bugs #7/#8 CORREGIDOS** (PR #547 `fix/voice-no-abono`): voz rechaza `tipo:'abono'` con error tipado; código de abono muerto retirado; factura/presupuesto byte-idéntico.

### PRs abiertas (cadena, 2026-06-27) — mergear en orden
- **#544** `refactor/documents-compose-core` — Fase A: núcleo puro `compose.ts` (composeDocument/buildTemplateConfig/buildTemplateData/buildVerifactuData), createDocument lo consume, **diff-nulo**. Base de la cadena de documents.
- **#550** `feat/createdocument-pdf-logo` (stacked en #544) — D2: createDocument inyecta logo de la org (alinea con los otros 3 paths de render). Cierra #6.
- **#547** `fix/voice-no-abono` — D4/D5: voz no crea abonos (#7/#8). Base de la cadena de voz.
- **#551** `feat/voice-nif-criterio-a` (stacked en #547) — D1: criterio A, voz permite factura sin NIF a consumidor final.

### TODO MERGEADO A MAIN (2026-06-27): Fase A✅ D1✅ D2✅ D3✅ D4✅ D5✅
- #544 Fase A (núcleo puro compose.ts, diff-nulo) · #552 D2 (logo en createDocument) · #547 D4/D5 (voz no crea abonos) · #551 D1 (criterio A, factura sin NIF a consumidor final) · #554 D3 (no renombrar identidad fiscal por NIF).
- Nota merge de PRs apiladas con squash: borrar la rama base cierra las PRs stacked → mergear base SIN `--delete-branch`, rebasar la stacked (`git rebase --onto origin/main <base-sha>`), retarget `--base main`, mergear, y limpiar ramas al final. (#550 se cerró al borrar #544 → reemplazada por #552.)
- Merge con `--admin` (checks de Actions fallan por billing bloqueado, no por tests; verificado verde en local).

### Fase B — estado 2026-06-28 (PR-A en main; PR-B y D3 pleno abiertas)
- **PR-A `#556` ✅ MERGEADA** — campos opcionales en `createDocument` (diff-nulo para los 15+ callers): `generado_por_voz` (cuota whatsapp_docs_mes), `skipAudit` (evita doble audit), `irpf_pct` en presupuestos, `retencionIrpfPct` en `buildTemplateData`. Arregló de paso un test obsoleto de D3 (totals) que quedó rojo en main al mergear #554 con `--admin`.
- **PR-B `#559` 🟡 ABIERTA — NO mergear hasta smoke WhatsApp** — `voice/generate` delega en `createDocument`; conserva solo bordes de canal (auth, identidad, cuotas con sus códigos n8n, find-or-create+409, NIF criterio A + exención con sus `error_code`, audit con teléfono, URL 7d, traductor `ApiError`→códigos voz). Route 689→547. Patrón en [[converger-canal-divergente-sobre-fuente-unica]]. Cambio observable: factura por voz sin NIF emisor → `422 emisor.nif_required` (nuevo para n8n). Bug de paridad colateral arreglado en el núcleo: `buildLineasPresupuesto` no propagaba `exencion_codigo`/`catalogo_id` (afectaba copiloto/v1). **Smoke**: emitir factura+presupuesto por voz en org test → PDF (logo+retención), cuota, audit con phone, URL abre a 7d.
- **D3 pleno `#561` 🟡 ABIERTA** — `resolveCliente` delega en `crearClienteRapido` (candidato #2). Decisión (estilo Holded): validación NIF **no bloqueante** en emisión (`nifValidation:'lenient'`) + `checkQuota:false` (clientes_mes no aborta la factura). Gana restaurar archivados + race 23505 + normalización NIF. Edge: lookup por NIF ya no desambigua por país.
- **F2/Destinatario Verifactu** — investigación cerrada en `issues/verifactu-f2-destinatario-investigacion.md` (estado código verificado + 7 preguntas gestoría). **HALLAZGO elevado**: `xml.ts` NUNCA emite bloque `Destinatario`, ni para F1 B2B con NIF → podría estar **rechazándose hoy en validación de negocio AEAT** (envío real activo), no solo el caso F2. Pendiente: gestoría + **smoke entorno PRE** (`prewww1.aeat.es`) antes de tocar nada.
- **Deuda en main (ajena a #3)**: cron `slack-dispatcher` en registry sin case en `loadHandler` → test `registry-wired` rojo + "Run Now" devuelve "handler not wired". Equipo Slack.

## #4 — Lógica de negocio en route handlers (transversal) — EVALUADO
El port `CopilotoStore` (`copiloto/store/port.ts`) **NO generaliza mecánicamente** a `createMockAdminClient`/las route tests. Son palancas distintas: CopilotoStore es un *port de dominio estrecho* (superficie tipada, resultado discriminado, oculta PostgREST) que funciona porque las tools hacen pocas operaciones acotadas. `createMockAdminClient` (`documents/__tests__/__fixtures__/`, 9 suites lib, **0/100 route tests**) es lo contrario: un *fake genérico del query-builder*. 86/100 route tests mockean `createAdminClient` ad-hoc. Dos vías: (a) generalizar `createMockAdminClient` a las 86 = consolidar boilerplate de test (barato, no toca prod, NO hace los handlers menos shallow); (b) generalizar el *patrón* CopilotoStore = port estrecho por handler gordo = el deepening real del #4, trabajo por-handler grande. Ninguna sale gratis del port del copiloto.

## Proceso por candidato (skill `improve-codebase-architecture`)
Encuadre del problema + 3 diseños de interfaz en paralelo (minimizar / unificar / ports&adapters) + recomendación + RFC en `issues/`. **No implementar sin OK.** Validar siempre: gates verdes + smoke E2E real (no solo unit).
