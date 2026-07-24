---
title: "FacturaIA — Conciliación v4: plan maestro"
date: 2026-07-25
source: auditoría propia + revisión adversarial de 3 agentes (Postgres/fiscal · record-linkage/eval · producto/riesgo)
tags: [facturaia, conciliacion, plan, matching, sepa, irpf]
---

# Conciliación v4 — Plan maestro

Repo: `/Users/manueldelmonte/Projects/facturaia`. Auditoría 2026-07-25.
Revisado y corregido por 3 agentes adversariales. **Las correcciones están incorporadas; los errores del borrador se documentan en §7 para que no se repitan.**

Relacionado: [[facturaia]] (hub) · `docs/architecture/conciliacion-copiloto-spec.md` (spec original, parcialmente caducado) · `docs/architecture/agentic-ocr-conciliacion.md` (§0.bis decisiones del grill agéntico) · `docs/architecture/conciliacion-referencia-holded.md` (**caducado: su tabla de mapeo de 2026-06-12 ya no refleja el código**).

---

## 0. Estado de concurrencia (leer ANTES de tocar nada)

Tres worktrees vivos sobre el mismo repo a 2026-07-25:

| Worktree | Rama | Qué toca | Consecuencia para este plan |
|---|---|---|---|
| `~/Projects/facturaia` | `main` | lote `issues/modia-*.md` (27 issues, módulos IA config) + `src/lib/modules/config.ts` | **No usar este checkout.** |
| `~/Projects/facturaia-conciliacion` | `fix/conciliacion-lote-julio` | `conc-fix-001` (signo `importe_aplicado` + `mirror_factura_match_to_nn` + CHECK), `conc-fix-002` (**reescribe `compute_sugerencias_for_movimiento` verbatim desde 547 con guard de capacidad**) | **BLOQUEANTE.** F1.1/F1.3 reescriben la MISMA función. Hay que partir de SU versión, no de la 547. |
| `~/Projects/facturaia-sepa` | `feat/sepa-modulo-config` | `src/lib/sepa/{remesa,pain008,pain001,validators}.ts`, `src/lib/modules/catalog.ts`, `config.ts` | **BLOQUEANTE.** El fix de SEPA (§PR-0c) y el `umbral_auto_conciliacion` en `catalog.ts` chocan. |

Reglas de convivencia:
1. Worktree nuevo propio desde `origin/main`: `git worktree add ~/Projects/facturaia-matching -b feat/conciliacion-importe-cobrable origin/main`.
2. **No tocar** `src/lib/sepa/*`, `src/lib/modules/catalog.ts`, `src/lib/modules/config.ts` hasta que `feat/sepa-modulo-config` mergee.
3. **No tocar** `compute_sugerencias_for_movimiento` ni `mirror_factura_match_to_nn` ni `movimiento_factura_asignacion` hasta que `fix/conciliacion-lote-julio` mergee.
4. Migraciones: numerar **al abrir el PR**, no al crear la rama. Última secuencial 2026-07-25: `554`. Hay 2 ramas con migraciones en vuelo → `ls supabase/migrations | tail` justo antes del PR y verificar duplicados tras el merge (`git ls-files supabase/migrations | grep -oE '/[0-9]{3}_' | sort | uniq -d`).

---

## 1. Los hallazgos, corregidos

### H1 — `facturas.total` no es el importe que el cliente transfiere
- `src/lib/documents/totales.ts:94` → `total = round2(baseNeta + iva)`. IRPF **no** se resta.
- `src/components/templates/template-types.ts:387` → el PDF imprime `total = base + iva − retencion`.
- `src/lib/documents/compose.ts:249-251` → `total` es el importe que firma **VeriFactu**.
- `grep -rn "irpf|retencion_garantia" supabase/migrations/*concilia*.sql` → **0 hits**.
- **Fórmulas (corregido, esto estaba mal en el borrador):**
  - IRPF: sobre la **BASE** → `round(base × irpf_pct/100, 2)`. Convención canónica ya fijada en `src/lib/fiscal/calculadores/v1/111.ts:134` (half-up por factura). Cuadrar con ella o el 111 y la conciliación divergirán.
  - Retención de garantía: sobre el **TOTAL con IVA** → `compose.ts:204` `round2(total × pct/100)`. Calcularla sobre la base da ~17-21% de menos.
- **También afecta a `presupuestos`**: `presupuestos.irpf_pct` existe (mig `165:17`), `234:72,81` persiste `total` e `irpf_pct` por separado, y `547:239-241` compara `COALESCE(p.total_eur, p.total)`. Mismo bug.
- **Blast radius, clasificado:**
  - **Dinero que sale de la app hacia un tercero (P0, arreglar ya):** `src/lib/sepa/remesa.ts:195,272,386` → `pain008.ts:173 <InstdAmt>`: se **adeuda al cliente el bruto**. Con IRPF 15% son 150 € de cobro indebido por factura, con exposición a R-transaction y al mandato. `src/lib/cobros/orchestrator.ts:196-197`: el recordatorio por email/WhatsApp reclama el importe equivocado, con la firma de la org detrás.
  - **Informativo (P2, a deuda):** `src/lib/cashflow.ts:177`, MCP `services/mcp-server/facturas.ts:92,115`, `analytics.ts:27,51`.
  - **Correcto por diseño fiscal, NO tocar:** 303 (base+IVA), VeriFactu, 111/190/347/130 (declaran la retención aparte con la fórmula correcta).
- **Inviolable: `facturas.total` no se toca nunca.**

### H2 — El motor que muta estado fiscal es el único sin medición
`supabase/migrations/370_agentic_decisions.sql:19` → `CHECK (dominio IN ('ocr','categorias'))`. Todo el aparato shadow→gate→activo→degradación existe y excluye matching. Evals sólo del Copiloto. Umbral 80 no configurable.

### H3 — Techo estructural: candidato por importe, texto sólo reordena
`547:266` importe fuera de tolerancia → `RETURN 0` (puerta dura). `547:475-476` `ORDER BY ABS(pendiente − importe) LIMIT 5`.

### H4 — Señal estructurada capturada y tirada
`movimientos_bancarios.referencia` se rellena en los 3 caminos y **el motor no la lee** (sólo `descripcion`, `547:290`). `psd2/tink.ts:277-285` devuelve `raw` y se descarta. `import-parser.ts:794` MT940 ignora `?32/?33` (nombre contraparte). `:831` OFX pierde `NAME` si hay `MEMO`.

### H5 — El aprendizaje está muerto
Sólo modal manual opt-in (`sugerencias-factura-mov-modal.tsx:74` → `learn-rule-modal.tsx`). La conciliación manual (`asignar_manual`, mig 269) **no aprende nada**. `veces_confirmada` no se usa en el scoring (`547:322-334`). Rechazos con `reason:'otro'` hardcodeado (`:93`).

---

## 2. Los dos invariantes que salieron de la revisión

**INV-1 (crítico, dos agentes lo encontraron por separado): relajar la puerta de importe abre auto-marcado sin señal de importe.**
Hoy score ≥80 es inalcanzable sin puntos de importe porque todo lo demás hace `RETURN 0`. Con penalización graduada, `num_doc(35)+cif(30)+regla(30)=95 ≥ 80` auto-marcaría cobrada una factura desde un movimiento de importe arbitrario. El `RAISE EXCEPTION` de mig 371 protege el número 80, no el invariante.
⇒ **La relajación aplica SOLO a generación y sugerencia. La ruta de auto-marcado exige `breakdown.importe > 0` obligatorio**, más candidata única y margen ≥15. Dos umbrales con nombre distinto: `umbral_sugerencia` / `elegible_auto`. Guard anti-regresión propio que verifique el invariante, no el número.

**INV-2: nada retroactivo se auto-marca.** No existe concepto de ejercicio cerrado en el repo (`grep -rn "ejercicio_cerrado|cierre_contable|periodo_cerrado"` → 0 hits). Auto-marcar fija `fecha_cobro`, entra en cashflow, en el KPI "Cobrado" y **cancela recordatorios de cobro**. Un cliente puede ver cambiar números de un ejercicio ya presentado. ⇒ Todo lo que F1.1 destape sobre facturas antiguas es **HITL obligatorio**.

---

## 3. Secuencia de PRs

### PR-0a — `importe_cobrable` (columna generada). Sin dependencias, cero conflicto.
Ningún consumidor cambia: sólo la columna + tests. Es la pieza compartida por todo lo demás, probada en aislamiento.

```sql
ALTER TABLE facturas ADD COLUMN importe_cobrable_eur NUMERIC(14,2)
  GENERATED ALWAYS AS (...) STORED;
```
- **No** función `STABLE` en plpgsql: es caja negra para el planner (coste por defecto, sin inlining, una llamada por fila) y va a ir en `WHERE` y `ORDER BY` dentro de 4 triggers `FOR EACH ROW`. Columna generada STORED = columna normal para el planner.
- No puede referenciar `total_eur`/`base_eur` (Postgres prohíbe generada→generada): reexpandir la conversión. **Verificar la dirección de `tipo_cambio` contra mig `173:110-121` antes de escribir** (`total * tipo_cambio` vs `/`).
- Orden de redondeo: redondear la retención en la divisa del documento y **luego** convertir, para cuadrar al céntimo con el PDF y con el 111. Documentar como invariante.
- Abonos: el signo sale solo (`base=-1000, total=-1210, irpf=15` → `-1210 − (-150) = -1060`). Test que lo fije.
- Misma columna en `presupuestos`.
- Índice `(org_id, tipo, importe_cobrable_eur) WHERE deleted_at IS NULL`.
- ⚠️ `ADD COLUMN ... GENERATED ... STORED` **reescribe la tabla y toma ACCESS EXCLUSIVE**. Medir el tiempo sobre el tamaño real de `facturas` en prod antes del `db push`.
- Retención de garantía **NO va en la columna**: va por `LEFT JOIN obras_retenciones ON factura_id AND estado='retenida'` (`UNIQUE(factura_id)`, mig `538:89` → join 1:1; `importe_retenido` ya es el euro snapshoteado). Razón decisiva: `538:72` tiene `estado IN ('retenida','liberada')` — al liberarse, **el cliente paga ese importe**, y un pct estático en `facturas` haría ese cobro inconciliable para siempre. Además duplicar el dato viola single-source-of-truth.
- Si el acoplamiento core→Obras molesta: vista de núcleo `retenciones_no_fiscales_activas(factura_id, importe)`, 5 líneas. Revisar `docs/architecture/dependency-map.md` antes.
- **Precondición**: endurecer `src/lib/obras/facturar-obra.ts:61-68` — hoy el INSERT en `obras_retenciones` es best-effort (`console.error` y sigue), así que la factura puede quedar con el bloque impreso en el PDF y sin fila en el ledger. Se va a convertir en fuente de un importe de cobro.
- Nombres: tres conceptos, tres nombres. `total` (fiscal) · `importe_cobrable` (lo que transfiere el cliente) · `pendiente_cobrable` (= `importe_cobrable − garantía_retenida − Σ ABS(mfa activas)`). La ambigüedad de nombres es el vector de error más probable.
- Tests: IRPF 7/15/19, garantía 5%, ambas juntas, IRPF+divisa, abono con IRPF.
- ⚠️ Bug preexistente a decidir antes de codificar: con IRPF **y** garantía simultáneos, el "Importe total a pagar" del PDF ignora el IRPF (`compose.ts:204,208` deriva de `composed.totales.total`, que es `baseNeta+iva`, mientras `template-types.ts:387` resta IRPF por su cuenta). Hay que fijar cuál es el número correcto.

### PR-0b — Cobros deja de reclamar el bruto. P0, daño a un tercero, hoy.
`src/lib/cobros/orchestrator.ts:196-197` consume `importe_cobrable`. No muta estado fiscal, no dispara triggers, no necesita backfill ni shadow.

### PR-0c — SEPA deja de adeudar el bruto. P0 pero BLOQUEADO por concurrencia.
`src/lib/sepa/remesa.ts:195,272,386`. **Esperar a que `feat/sepa-modulo-config` mergee**, o coordinar con esa sesión para que lo aplique ella. Es un cobro indebido en producción: no dejarlo caer en el olvido por el bloqueo.

### PR-0d — Dedup intra-lote en el path `con external_id`. Pérdida de datos activa.
`movimientos-insert.ts:64-111` filtra contra BD pero no intra-lote → `23505` → el reintento fila-a-fila (`:88-102`) cuenta la 2ª como `skippedDup++`. Mismo bug que el comentario de `:117-130` documenta como ya corregido en el otro path. Con MT940/OFX donde dos movimientos reales comparten `?20`/`FITID`, se pierde dinero en silencio.
**Smoke con datos reales ANTES del fix** (inviolable: nada de arreglar a ciegas un path de dinero).

### PR-1 — Matching con importe cobrable + telemetría. Depende de `conc-fix-002` mergeado.
- **Partir de la versión de `conc-fix-002`, no de la 547.**
- `calcular_score_match_doc` + prefiltros + los dos `auto_mark_*` puntúan contra `pendiente_cobrable`.
- **`conciliacion_candidatas_manual`: la versión viva es `278:364`, NO la 270.** La 270 usa `f.total` crudo; la 278 la pasó a `COALESCE(total_eur,total)`. Partir de la 270 revierte el fix de divisa (issue 059) y **aquí no hay guard anti-regresión** (el de 371 sólo cubre los 3 automarks).
- `capacidad-movimiento.ts` **no** hay que tocarlo: no consume `facturas.total` (sólo `importe`, `mfa.importe_aplicado`, `resto_importe`).
- **F1.2 en el mismo PR**: leer `referencia`. `normalizar_texto_match(coalesce(descripcion,'') || ' ' || coalesce(referencia,''))` para nº-doc, nombre y CIF. Una línea, el mejor ratio valor/esfuerzo del plan. Riesgo: `referencia` a veces lleva el `external_id` → falsos positivos si un ID coincide con un nº normalizado. Mitigar con longitud mínima (ver PR-2, `≥5` o `≥4` con prefijo no numérico) y medir con los fixtures.
- **Telemetría (F0.1 reducido) en este mismo PR**, no en una fase previa: `CHECK (dominio IN ('ocr','categorias','matching'))`. Escribir **desde el trigger SQL**, no desde TS: el auto-mark es SQL y es justamente el camino que hay que medir; el mismo `tx` hace el denominador completo (cero decisiones perdidas → cero sesgo).
  - Envolver el INSERT en `BEGIN ... EXCEPTION WHEN OTHERS THEN RAISE WARNING ...; END;`. Un fallo de observabilidad **no puede** abortar el import de un movimiento.
  - `agentic_decisions.zona` es `NOT NULL CHECK (verde|ambar|rojo)` (`370:23`): definir el mapeo score→zona **en la propia migración** o el INSERT falla.
  - Añadir `score_raw INTEGER`: `547:502` persiste `LEAST(score/100, 1)`, así que **todo score ≥100 se guarda como 1.0** y el histórico no sirve para calibrar. `motor_version` como clave dentro de `score_breakdown`/`valor_ia`, sin columna nueva.
  - El cierre (`confirm`/`reject`/`asignar`/`revert`) sí en TS: son endpoints.
  - **Reescritura retroactiva obligatoria**: desvincular / `bulk-revert` / `automarks/revertir` dentro de 30d **reabre** la decisión ya cerrada y la marca `correccion`. En matching el error se descubre después; sin esto el fallo es invisible por diseño.
- **INV-2**: nada de backfill automático. El recomputador histórico (`internal/conciliacion-recompute-sugerencias/route.ts:44-49`) filtra `score_breakdown IS NULL` → sólo toca legacy pre-155, de las que ya no queda ninguna. ⇒ **F1.1 por sí sola no arregla a ningún cliente actual**: los triggers son `AFTER INSERT`. Hace falta un recomputador acotado y explícito (por org, por rango, disparado a mano, generando **sólo sugerencias**), nunca un `UPDATE facturas SET estado=estado` (dispara `auto_mark_*` fila a fila; `pg_trigger_depth()>1` de `371:68` no protege de un UPDATE de primer nivel).
- Rollback escrito **antes** del deploy: `CREATE OR REPLACE` de vuelta + limpieza de las `pending` generadas en la ventana. La palanca de emergencia que ya existe es `auto_marcar_cobradas` en `org_module_config` (`catalog.ts:169`, leída en `371:82-83`) — apaga el auto-marcado, no la generación.
- Feature flags internos: `matching_importe_cobrable`, `matching_blocking_multiple`. (⚠️ `catalog.ts` bloqueado por la sesión SEPA → meterlos cuando se libere, o en tabla propia.)

### PR-2 — Desacoplar el import, luego blocking múltiple.
**Orden invertido respecto al borrador: desacoplar va PRIMERO.** `movimientos_bancarios` tiene 4 triggers `AFTER INSERT FOR EACH ROW` (`061:139`, `101:164`, `109:276`, `116:179`); pasar de 1 bloque a 4 con dedup y top-K multiplica el trabajo síncrono por ~3-4× dentro de la transacción de import. Si se hace al revés, el import de ficheros grandes revienta por timeout.
⚠️ Al desacoplar hay que **reescribir el criterio de selección del cron** (`score_breakdown IS NULL`) o los movimientos nuevos se quedan sin sugerencia. F3.6 no es UX: es un cambio de arquitectura del pipeline.

Bloques, en orden de retorno:
- **B5 — importe exacto SIN ventana de fecha** (o 180d). Hoy B1 exige ±`ventana_dias` (30). Un pago a 75 días con importe exacto es invisible, y en B2B español (60-90d + retraso) esto es **probablemente un agujero de recall mayor que el de retenciones** y mucho más barato. Empezar por aquí.
- **B2 — referencia. Como igualdad indexada, no como substring.** El borrador pedía "facturas cuyo `normalizar_num_match(num)` aparece en el texto del movimiento": eso es *reverse LIKE* (aguja variable, pajar fijo) y **un GIN pg_trgm no puede responderlo** → seq scan de todas las facturas de la org con una llamada a función por fila, dentro del import. Correcto: extraer los tokens del movimiento **una vez** con `regexp_matches`, y luego `WHERE normalizar_num_match(f.num) = ANY(v_tokens)` con `CREATE INDEX ON facturas (org_id, normalizar_num_match(num))`. Viable porque `normalizar_num_match` es **IMMUTABLE** (`155:194-197`). Exacto, O(log n), sin trgm.
  Suelo de longitud: `≥5`, o `≥4` con prefijo no numérico. Hoy `"0142"` matchea media contabilidad.
- **B6 — IBAN de contraparte exacto**, bloque de primera clase (tras capturarlo), no dentro del fuzzy. Es la mayor ganancia de precisión del plan y no necesita IA.
- **B3 — contraparte fuzzy.** El trgm GIN, si se quiere, va sobre `clientes/proveedores` (patrón ya establecido en `168:79-83`), **no** sobre `movimientos_bancarios` (hoy no hay ningún índice trgm ahí).
- **B7 — subset-sum N↔1** (una transferencia paga 3 facturas del mismo cliente). El bloque de importe nunca lo genera. Acotar a contraparte identificada y ≤8 facturas abiertas, sólo HITL. Si no cabe, que sea decisión explícita, no omisión.
- Forma: **un solo CTE** `WITH b1 AS (...LIMIT 10), b2 AS (...) ... SELECT DISTINCT ON (factura_id) FROM (b1 UNION ALL b2 ...)`. Cuatro `FOR ... LOOP` en plpgsql impiden cualquier reordenación del planner y obligan a dedup manual.
- Explosión: LIMIT 10/bloque, **tope global 25 pares puntuados por movimiento**, K=5 persistidas, tie-break estable (`f.id ASC`, ya está: es lo que hace reproducible la eval). Etiquetar el bloque de origen en la sugerencia (`origen` B1..B7) o no se puede medir recall por bloque ni matar el que sólo hace ruido.
- **Penalización negativa, no "menos positiva"** (si no, dos señales débiles superan a una fuerte): `−25` si `diff > 2×tol`, `−40` si `diff > 10×tol`; `importe > pendiente_cobrable × 1,5` sin razón de sobrepago → capar por debajo del umbral de sugerencia.
- **INV-1 aquí.** Y `umbral_auto_conciliacion` configurable (70-100, default 80) — ⚠️ `catalog.ts` bloqueado por SEPA.
- Sobre el `RAISE EXCEPTION` de `371:413-415`: **es un bloque `DO $$` de un solo uso, ya ejecutado. No hay conflicto y NO se debe editar** (editar una migración aplicada crea drift contra `schema_migrations`). Lo correcto: dejar 371 intacta y **replicar el guard actualizado en la migración nueva**, verificando el invariante INV-1, no el número 80.
- **F1.4 — parcial explícito.** Si `imp < pendiente_cobrable` y hay señal fuerte, sugerir parcial con "quedarán N € pendientes". Escritura ya existe (269/272/273). **Nunca auto-confirmar. HITL siempre.**

### PR-3 — Aprendizaje. Depende de PR-2.
- **F2.1 — aprendizaje implícito en servidor**, enganchado en `confirmar_sugerencia`, `asignar_manual` y `conciliar-doc`. Tokens con `normalizar_texto_match()`, stopwords bancarias subidas a SQL (lista de `learn-rule-modal.tsx:36-41` + `PAGO/TRANSFERENCIA/RECIBO/ADEUDO/BIZUM/COMPRA/TARJETA/SEPA`). Si hay IBAN de contraparte, aprender el IBAN: determinista, no ambiguo.
- **Cortar el auto-refuerzo lavado por un click.** Ponderar por origen: `asignar_manual`/`conciliar-doc` (lo encontró el humano) = **+1**; `confirmar_sugerencia` donde **la regla ya aportaba puntos** = **+0**; `confirmar_sugerencia` sin aporte de regla = +1 pero no puede ser la única vía a la madurez. Sin esto: motor propone → humano confirma → +30 → madura → auto-marca → fin de la señal humana. En 3 clicks un patrón erróneo es permanente.
- **Ambigüedad relativa (BLOQUEANTE de F2.1, no opcional).** Hoy `marcar_reglas_ambiguas` (`155:796-815`) pone `es_ambigua = count(distinct contraparte)>1` para **todas** las filas de `(org, token)`, binario, ignorando `veces_confirmada`. Con minado masivo, un token basura aprendido **una vez** para B desactiva silenciosamente una regla confirmada **50 veces** para A. Corregir: regla activa si concentra ≥80% de las confirmaciones del token y tiene ≥3 absolutas; una de 1 confirmación nunca invalida una de ≥3. Añadir `origen ∈ ('explicita','implicita')`, gana la explícita. Suelo de longitud **≥6** para tokens auto-minados.
- **Decay por oportunidades falladas, no por calendario.** 6 meses sin activación es normal en un cliente que factura 2 veces al año. Degradar cuando la contraparte tuvo conciliaciones y la regla no disparó, o disparó y fue corregida. Calendario como red gruesa a 18-24 meses. Alternativa barata: ventana = mediana del intervalo entre facturas de esa contraparte × 3.
- **Localizar la regla que empeora**: contadores `veces_aportada` y `veces_seguida_de_correccion`; job nocturno desactiva las de `veces_aportada ≥ 5 AND ratio > 0,30` y escribe en `conciliacion_reglas_eventos`. Sin esto `auto_accuracy` agrega el daño y no lo localiza.
- **F2.3 reglas negativas — DESPUÉS de F1.4** y ampliando `RechazoRazon` antes. Hoy es `'importe_incorrecto' | 'no_es_la_misma' | 'otro'`, e `importe_incorrecto` es precisamente el caso que F1.4 convierte en **legítimo** (parcial): aprender de ahí penalizaría parciales correctos. Añadir `es_parcial`, `otra_fecha`. Reglas: aprender sólo de `no_es_la_misma` **con `rejected_by IS NOT NULL`** (excluye los `rejected` que genera el trigger de mig 267 M5); exigir **2** rechazos del mismo `(token, contraparte)`; penalización **acotada, resta puntos, nunca suprime la candidata** (un mis-click no puede esconder un match para siempre y ser indepurable); caducidad **90 días**.

### PR-4 — Pesos y gate. Depende de PR-3.
- **Fuera regresión logística + Platt/isotónica** (el borrador lo pedía; era un error: la logística ya emite probabilidad, Platt es para márgenes SVM/ensembles, e isotónica con unos cientos de positivos sobreajusta escalones al ruido).
- **Dentro: pesos Fellegi-Sunter estimados por conteo.** Las 6 señales ya son binarias/ternarias. Estimar `m_i = P(coincide | match)` y `u_i = P(coincide | no-match)`; peso `= log2(m_i/u_i)`. Se estima contando con unos cientos de casos; se persiste como ~12 números en una tabla; es un `SELECT`+suma en SQL sin modelo en el camino crítico; es explicable señal a señal (justo lo que ya renderiza `score-reasons.ts`); y **reduce al esquema aditivo actual**, así que sustituye 40/15/10/5/35/25/30/30 sin reescribir el motor. Y corrige por construcción el problema de H3: en orgs con muchos importes idénticos `u(importe_exacto)` es alto y el peso baja **solo**.
- **Calibración = tabla de precisión empírica por tramo de score** (tramos de 10), no una curva ajustada. Mostrar N: "de las sugerencias con esta puntuación, 92 de 100 acertaron (N=137)". **No mostrar porcentaje con N<30** → "aún midiendo". Degrada con dignidad, no hay modelo que versionar.
- **Pesos globales + un modificador por org sin etiquetas.** Con 6 señales harían falta ~100+ matches etiquetados por org; casi ninguna los tendrá, y pesos por org exigirían **evals por org** (imposible por tamaño de muestra). Pero la mayor varianza entre orgs es la de H3, y se calcula **sin etiquetar nada** desde la propia tabla: `p_dup = fracción de facturas abiertas cuyo importe coincide (±0,50 €) con otra factura abierta de la org`. Con `p_dup` alto, baja el peso de importe y sube el de nº/CIF/IBAN. Es literalmente el `u_i` de FS estimado por org: un número, determinista, sin modelo.
- **Gate, con los números corregidos.** El `≥50 @ ≥0,95` del doc agéntico no sostiene lo que afirma: Wilson 95% para p̂=0,95, n=50 → **[0,851 , 0,984]**, un intervalo compatible con el criterio de *cierre*. A n=50, "≥0,95" es "≤2 errores": una org realmente al **90%** tiene **11,2%** de probabilidad de abrir el gate; una realmente al 95% tiene **7,5%** de ser degradada por ≥3 errores en 20. Y el sweep corre **a diario** sobre ventana móvil → test repetido sin corrección: a lo largo de meses ambos falsos veredictos pasan de posibles a casi seguros. La histéresis 95/90 protege del ruido de la señal, no del **ruido de muestreo**.
  Correcciones: **cota inferior de Wilson**, no estimador puntual. Abrir con **≥100 decisiones resueltas y ≤1 corrección**. Afirmar **"≥90% con 95% de confianza"**, no "≥95%". Sweep **semanal**, condición sostenida en 2 sweeps, **cooldown de 14 días** entre cambios de estado. Umbral propio para matching (muta estado fiscal y propaga a cobros; no puede compartir el de categorías). **Veto duro**: un solo auto-mark erróneo con efecto visible al cliente cierra el gate sin mirar la tasa.
  **Descontar el sello de goma**: excluir del denominador las confirmaciones en bloque (`closeCategoriaDecisionsBulk` marca todo el lote como `'aceptacion'`) y las hechas a <3 s de abrir el modal. Excluirlas, no contarlas como fallo.
  **Silencio = no etiquetado, nunca aceptación.** Publicar `cobertura = resueltas / decisiones_totales` y **no abrir el gate con cobertura < 0,30**.
  En modo activo el muestreo es la única fuente insesgada: al 8% de 600 auto-marks/mes = 48 auditados → detecta una caída a 85%, **no** a 93%. Decirlo explícitamente para que nadie afirme "monitorización al 95%".

### PR-5 — UX. Sólo lo que de verdad falta.
**Ya existe en producción, borrado del plan** (el borrador lo dio por pendiente leyendo el doc de Holded de junio en vez del código):
- Aprobar/descartar **inline en la fila**: `conciliacion-view.tsx:1315-1379` (`s.inlineSugActions`, `confirmInline`/`rejectInline`, cuarentena, `stopPropagation`).
- **Progreso %** por movimiento: `:1087` (`<th>Progreso</th>`) + `:1264-1287` (`progresoPctMovimiento`). Ya documentado en `manual-usuario.md:920`.
- **Motivo humano**: `src/lib/conciliacion/score-reasons.ts:18-38` (`reasonsFromBreakdown`/`topReason`), renderizado en `sugerencia-card.tsx:114-121,298-305`, `movimiento-detail-drawer.tsx:1044` e inline en `conciliacion-view.tsx:1321`. Documentado en `manual-usuario.md:740-752`. Sólo queda el string `motivo` de `547:504`, cosmético.

Lo que sí falta:
1. **Tres secciones separadas** (auto-conciliadas a revisar / sugerencias / sin candidato). El spec lo declaró inviolable (`conciliacion-copiloto-spec.md:317`) y hoy es tabla única con `Segmented` + `FilterChip`. Headers colapsables: `<button aria-expanded>` + **`<Icon name="chevron*">`**, no el triángulo Unicode del spec (inviolable: nunca emojis).
2. **Búsqueda libre.** No existe. El spec la pide (`:361` "Buscar por concepto o referencia"), `ToolbarSearch` ya está construido, es estándar en Holded y Xero, y para quien tiene 3.000 movimientos vale más que cualquier otra cosa de esta lista. **Una hora de trabajo.**
3. **Ordenación de columnas**: `SortableTh` existe y la tabla no lo usa.
4. **Migrar a los compartidos** (deuda que cualquier trabajo nuevo aquí amplifica): `src/components/conciliacion/filter-chip.tsx:1-23` reimplementa lo que ya hay en `src/components/ui/filters.tsx:1-40`; `src/components/ui/bulk-bar.tsx` existe y **no se usa** pese a que ya hay `bulk-confirm`/`bulk-revert` (`conciliacion-view.tsx:862,885`); `por-revisar-cta.tsx:33-49` usa `<button>` crudo con `style` inline en vez de `<Button>`; la vista no importa `ListToolbar`/`ToolbarSearch`/`ColumnPicker` — es el único listado grande del producto que no usa el toolbar canónico.
5. **Copy**: `por-revisar-cta.tsx:29` → `"Categorías propuestas automáticamente — confirma o cámbialas con un clic."` incumple `copy-humano.md` dos veces (raya con espacios + "con un clic" como frase-plantilla). Una línea.

**Recortado del plan:**
- **Cash coding**: fuera. Vista nueva entera, el mayor foco de riesgo de inviolables (una rejilla de controles inline invita a `<select>`/`<input type=date>`/`<input type=checkbox>`, los tres prohibidos), y su valor depende de tener muchos movimientos sin categoría, que `ia_auto_categorizar` (default true, `catalog.ts:172`) ya resuelve en gran parte.
- **KPI de precisión al cliente**: fuera. Contradice una decisión de producto ya razonada **y comentada en el código**: `por-revisar-cta.tsx:8-10` cita a Buell & Norton para justificar mostrar el trabajo concreto pendiente en vez de un % de precisión agregado. Un "92%" sólo abre "¿y el 8%?". La tarjeta cross-org en `/admin/ia-ops` sí: es interna.

### Deuda apuntada (no bloquea)
- camt.053: **fuera, con condición de disparo escrita**: primer cliente cuyo banco sólo ofrezca camt.053, o cuando el segundo de los cinco grandes retire MT940. Añade cobertura de formato, no precisión; el 80% de la ganancia de contraparte la da leer `?32/?33` en MT940 y dejar de tirar `NAME` en OFX, por el 5% del coste.
- `?32/?33` MT940 + `NAME` OFX + `counterparties`/`merchantInformation` de Tink (ampliar `TinkTransactionRaw`) + columnas `contraparte_nombre` / `contraparte_iban_{enc,bidx,mask}` (patrón A6, mig 519) / `end_to_end_id`. Habilita B6.
- `compute_sugerencias_for_factura` con presupuestos (asimetría de 547).
- KPI `sin_cobrar_30d_count` por vencimiento y excluyendo las ya casadas (`conciliacion-view.tsx:349-354`).
- Corregir el comentario de `src/lib/documents/types.ts:153`: dice que `irpf_pct` "sí resta del total"; es cierto para el total del PDF, falso para `facturas.total`.
- Consumidores informativos de H1: `cashflow.ts:177`, MCP `facturas.ts:92,115`, `analytics.ts:27,51`.

---

## 4. Evaluación: método de agente-2, tamaño de agente-3

Los dos revisores chocaron y la resolución es adoptar **el método del riguroso con el tamaño del pragmático**, porque el método es gratis (sólo cambia cómo se construyen los fixtures) y el tamaño no lo es.

**Fuera: corpus de 200-300 pares etiquetados desde datos de cliente.** Es una semana de trabajo, requiere un export anonimizado que el plan no diseñó (¿qué org? ¿con qué base legal?), y **F1.1 no lo necesita**: no es un cambio de calibración, es un bug de definición. No hace falta un gate con histéresis para saber que 1.060 ≠ 1.210.

**Dentro: 40-60 fixtures dirigidos, con el método correcto.**
- **Unidad = el movimiento**, no el par. Con pares no se puede medir "propuso la equivocada" ni "no propuso ninguna".
- **Clase "no debe proponer nada" ≥25%**: transferencia interna, anticipo, comisión bancaria, nómina, devolución. Sin ella, PR-2 sube recall proponiendo más y parece gratis. Es el guardarraíl principal del blocking múltiple.
- **Cuotas por familia**, ~5 casos cada una: IRPF 7/15/19, garantía, parcial, comisión/pronto pago, N facturas mismo importe, remesa N↔1, divisa, **pago tardío >30d** (B5), sin candidato legítimo. Sin cuotas, 250 casos fáciles dan 97% y no prueban nada.
- **La verdad-terreno del recall NO está en `conciliacion_sugerencias`** (conjunto condicionado por el motor: circular). Está en `movimiento_factura_asignacion`: cada enlace creado por un humano vía `asignar_manual`/`conciliar-doc` es un caso que el motor falló o nunca propuso, observable hoy, retrospectivamente, con **coste de etiquetado cero**. Excluir de esa fuente los creados vía `confirmar_sugerencia`.
- **Negativos gratis**: para cada movimiento con enlace conocido, toda otra candidata es negativo verdadero. Sin etiquetar nada.
- **Nunca usar `status='rejected'`** como negativo: mig 267 §M5 marca `rejected` las pending de un movimiento soft-borrado, `expires_at` purga a 30d, y `rejection_reason` está hardcodeado a `'otro'`. No significa "el humano dijo no".
- **Leakage**: `calcular_score_match_doc` (`547:322-334`) consulta las reglas aprendidas de la org viva. Con PR-3, **cada positivo del corpus tendrá una regla apuntando a su etiqueta** → la eval reportaría memorización pura. Antídoto: parámetro **`as-of`** en el scoring que excluya reglas aprendidas después de la fecha del movimiento. **Es cambio de PR-1, no de PR-3**: sin él nunca se podrá medir el aprendizaje. Y reportar cada métrica **dos veces**: con reglas y con reglas desactivadas.
- **El test es apareado, no dos muestras.** El motor es determinista → v1 y v2 sobre el MISMO corpus congelado → **McNemar / binomial exacta sobre los flips**, no dos estimaciones de precisión. Con 50 casos, 5 flips en la misma dirección da p=0,031: detectable. Un "no bajar de la baseline" sobre un estimador puntual parpadearía cada vez que se añade un caso.
- **Dos gates asimétricos**: (a) *veto por ítem* — cualquier flip nuevo del tipo "auto-marcada la factura equivocada" bloquea el PR, independientemente del porcentaje (muta estado fiscal, no es asunto de 2 pp); (b) *regresión global* — bloquea si `regresiones − mejoras ≥ 3` con p<0,05.
- **Con n≈50 sólo se detectan flips, no se estima precisión a ±2 pp.** Declararlo en el README del corpus para que nadie afirme lo contrario. (Para ±2 pp sobre p≈0,95 harían falta ~456 decisiones auto; para ±3 pp, ~203.)
- **Dónde corre**: `vitest.integration.config.ts` (Supabase local, SQL real, determinista — ya tiene `automark-score.test.ts`), **no** `vitest.evals.config.ts` (explícitamente no-determinista, con LLM real, "NO va en CI normal"). Llamar a las **funciones SQL reales**: si se reimplementa el scoring en TS, se mide un motor distinto del de producción. Para ser gate de CI de verdad hay que montar el job docker que ese config ya reconoce como pendiente.
- Congelar y versionar: `corpus_v1` + hash en el test. Pinear `tolerancia_euros` y `ventana_dias` en la org de eval o el config mueve los resultados.
- Pseudonimización que **preserve la señal**: mapa determinista por entidad conservando forma (longitud, estructura de tokens). Cero IBAN reales en el repo.
- Sesgo residual (movimientos que nadie concilió nunca, inobservables): acotarlo con una auditoría ciega de 100 movimientos `sin_candidato` nunca conciliados → estimación de la bolsa silenciosa a ±10 pp. Suficiente para distinguir 5% de 40%.

---

## 5. Lo que NO se hace
- **Embeddings / pgvector** (PR-B2 del spec): no, hasta agotar la señal determinista. Un embedding no rescata un candidato que el prefiltro nunca generó.
- **LLM en el camino crítico del matching**: no. Auditable, gratis y explicable vale más que un punto de recall cuando se muta estado fiscal.
- **Tocar `facturas.total`**: nunca.
- **Subir el umbral antes de tener telemetría**: no.
- **Backfill masivo vía `UPDATE facturas`**: nunca (dispara `auto_mark_*` fila a fila).

---

## 6. Fuera del código
- **Manuales** (el borrador no los mencionaba y el CLAUDE.md lo exige): `manual-usuario.md:748` dice *"Muy probable (≥80 puntos): se concilia automáticamente"* → el umbral configurable la vuelve falsa. `:742-752` documenta los tramos 80/50/30 → PR-2/PR-4 los mueven. `:919-920` documenta filtros → PR-5 los reorganiza. Sección nueva de retenciones. `manual-admin.md`: la clave `umbral_auto_conciliacion`.
- **Qué se le dice al cliente cuyas retenciones nunca se conciliaron**: **no** un aviso proactivo tipo "llevábamos meses fallando". Sí, cuando aparezcan sugerencias sobre facturas antiguas, decir el porqué en la sección ("Hemos revisado tus facturas con retención de IRPF y encontramos N posibles cobros") y **nunca auto-marcarlas**. Convierte el bug en un momento de valor en vez de en una confesión.
- **Canvas Slack `F0AV38CHYSJ`** antes del deploy de PR-1: una línea de qué cambia y cuál es la palanca de apagado. **Aviso a Borja: no** — sólo si toca agency-portal, y esto es todo tufacturaia ([[feedback_borja_notificaciones]]).
- `Stack/incidents.md` si algo se torna en producción.

---

## 7. Errores del borrador (para no repetirlos)
1. **Fase 3 escrita contra `conciliacion-referencia-holded.md` (junio) en vez de contra el código.** Tres de seis puntos ya estaban en producción. Lección: el doc de mapeo competitivo caduca; el componente no. Verificar features contra el componente, siempre.
2. Retención de garantía: se asumió "sobre la base". Es **sobre el total con IVA** (`compose.ts:204`).
3. Se dio `conciliacion_candidatas_manual` por vigente en la 270. La viva es la **278**.
4. Se propuso **editar el `DO $$` de la migración 371 aplicada**. Eso crea drift; hay que replicar el guard en la migración nueva.
5. Se listó `capacidad-movimiento.ts` como consumidor de `facturas.total`. No lo es.
6. Se olvidó `presupuestos` en H1.
7. Se propuso `importe_cobrable` como función `STABLE` en prefiltros y `ORDER BY`. Va como **columna generada STORED**.
8. Se propuso GIN pg_trgm para un *reverse LIKE* que un trgm no puede responder.
9. Se propuso regresión logística + Platt + isotónica. Fellegi-Sunter por conteo es más simple, más barato, explicable y reduce al esquema actual.
10. Se dio por bueno el gate `≥50 @ 0,95` del doc agéntico. Estadísticamente no sostiene lo que afirma.
11. Se ordenó blocking múltiple **antes** de desacoplar el import. Es al revés.
12. Se aparcó el fix de SEPA/cobros en "blast radius a documentar". Es un cobro indebido a un tercero, en producción, hoy.
13. No se contempló que **F1.1 sin recomputador no arregla a ningún cliente actual** (los triggers son `AFTER INSERT`).
14. No se detectó INV-1 (auto-marcado sin señal de importe al relajar la puerta). Lo encontraron dos revisores por separado: es el hallazgo más importante de la revisión.
