---
title: FacturaIA — superprompt auditoría integral del Centro Fiscal
date: 2026-07-10
source: claude-code-session
tags: [facturaia, fiscal, auditoria, prompt]
---

# Superprompt — Auditoría integral del Centro Fiscal (investigación + aplicada)

> Pegar tal cual en una sesión nueva de Claude Code con cwd `/Users/manueldelmonte/facturaia` (tras mergear `feat/fiscal-modelos-faltantes`). Diseñado para agentes paralelos + verificación adversarial. Presupuesto: sesión larga.

---

Audita el Centro Fiscal completo de TuFacturaIA con máximo rigor: los 9 modelos (303, 130, 390, 349, 111, 190, 115, 180, 347) más la pantalla del 131, sus plazos, exports, UI, captura de datos y composición entre modelos. **Auditoría READ-ONLY: hallazgos → issues locales en `issues/` (formato del repo), NUNCA fixes en esta sesión.** Cero especulación: cada hallazgo con archivo:línea + escenario concreto que lo dispara + severidad (crítico = importe/declaración errónea o pérdida de datos · medio = cuadre/UX engañosos · bajo = pulido/doc).

## Fase 1 — Investigación normativa fresca (NO confiar en los docs del repo)

Lanza agentes de research web independientes (solo BOE/sede AEAT) que verifiquen DESDE CERO, sin leer antes `docs/architecture/centro-fiscal-fuentes-oficiales.md`:
1. Órdenes vigentes y últimas modificaciones de: 303, 130, 390, 349, 111, 190, 115, 180, 347, 131. Especial atención a órdenes publicadas DESPUÉS de 2026-07-10 (el frente se verificó ese día; en dic-2026 es probable orden nueva que cambie 190/347 del ejercicio 2026).
2. Casillas/claves/plazos/tipos de retención de cada modelo + calendario del contribuyente vigente + BOE de días inhábiles del año siguiente si ya está publicado.
3. DESPUÉS: diff contra `centro-fiscal-fuentes-oficiales.md` §§1-11. Cada discrepancia = hallazgo (o confirmación de que el doc sigue vigente, dilo explícitamente).

## Fase 2 — Recomputación independiente de los calculadores

Por cada modelo, un agente que NO lea el calculador primero: lee solo la norma (fase 1) y los fixtures de `src/lib/fiscal/__fixtures__/`, computa A MANO el resultado esperado de cada fixture (casillas, registros, cuadres), y SOLO ENTONCES lo contrasta contra el output real del calculador (`npx vitest run` + leer los asserts de los tests). Divergencia test-vs-norma = hallazgo aunque el test pase (un golden test mal derivado se autovalida). Cubrir explícitamente: redondeos (half-up por factura vs por línea), signos de abonos, IVA excluido (111/115) vs incluido (347), umbrales por clave, periodicidad dinámica del 349, minoraciones del 130, arrastres/compensaciones (130/303).

## Fase 3 — Matriz de composición cross-modelo

Un agente construye la matriz completa de enrutamiento de una factura: {emitida/recibida} × {irpf_pct 0/>0} × {tipo_retencion: null/profesional/arrendamiento/trabajo} × {es_arrendamiento} × {es_intracom} × {territorio contacto ES/UE/EXTRA} × {estado} → ¿qué modelos la capturan, cuáles la excluyen, qué cuadre avisa? Verificar: cero dobles conteos (347↔349/190/180, 111↔115), cero agujeros silenciosos (combinación que no captura NADIE y ningún cuadre avisa), y que el mismo criterio de selección lo comparten trimestral y su derivado (190←111, 180←115, 390←303) vía función única, no duplicada.

## Fase 4 — Datos y persistencia

- Migraciones fiscales (146, 241, 246-250, 451, 452): CHECKs vs validaciones de app, RLS en cada tabla, seeds de `fiscal_plazos` contra `fechaPresentacion` (cross-check TS↔BD), numeración sin duplicados.
- Serialización bigint→string→UI en `extraDatos` (registros 190/180/347, fuentes 390): signos, >MAX_SAFE_INTEGER, undefined vs [].
- Estados de `fiscal_declaraciones` (borrador→cuadrado→exportado→presentado): ¿algún camino escribe sobre una presentada? ¿El cron de drift (`fiscal-recalcular-borrador`) respeta su guard de modelos 303/130? ¿`fiscal-generar-borradores` sigue limitado a 303/130 y al perfil correcto?
- Captura upstream: OCR (REGLAS 12/13, situación inmueble derivada 1/4), panel de ingesta, auto-approve (arrendamiento = línea roja). ¿Puede llegar a los calculadores una factura con datos fiscales inconsistentes que ningún cuadre detecte?

## Fase 5 — E2E aplicado con datos reales (org de test, `is_test=true`)

Con la app corriendo (local o sandbox): crear un juego de facturas conocido (profesional 15%, profesional 7%, nómina, alquiler 19% con y sin ref. catastral, intracom, extracomunitaria, abono, >3.005€ con un tercero) y verificar EN PANTALLA cada modelo del ejercicio: casillas exactas contra el cálculo a mano de la fase 2, cuadres esperados, navegación de periodos, export TXT de apoyo donde exista, pantalla de módulos con org en estimación objetiva, exoneración SII con `sii_activo=true`. Smoke contra BD prod: JAMÁS — solo org de test.

## Fase 6 — Verificación adversarial y cierre

Cada hallazgo de las fases 1-5 pasa por 2 verificadores independientes con lentes distintas (corrección normativa / reproducción en código) que intentan REFUTARLO; solo los confirmados se reportan. Entregables:
1. `issues/NNN-audit-fiscal-<slug>.md` por hallazgo confirmado (formato del repo, con severidad y escenario).
2. Informe artifact: matriz de la fase 3, resultado por modelo, hallazgos confirmados/refutados, y lista explícita de lo VERIFICADO como correcto (para no re-auditar).
3. Estado de los HITL conocidos: export posicional oficial pendiente en 111/190/115/180/347 (cuadres `export-oficial-pendiente`) — confirmar que siguen honestos; sandbox AEAT sigue pendiente de certificado.

Reglas duras: leer `CLAUDE.md` del repo antes de nada (inviolables) · read-only salvo `issues/` y el artifact · gate de referencia si dudas de un estado: `npm run lint && npm run typecheck && npx vitest run` · los tests Postgres se autosaltan sin BD (levantar compose local si quieres el backstop real).

---

Contexto previo (no re-derivar): frente implementado 2026-07-10, QA en https://claude.ai/code/artifact/9d211a05-2b01-4068-a165-859f0a364c4b · fuentes en `docs/architecture/centro-fiscal-fuentes-oficiales.md` §§6-11 · review adversarial previa ya corrigió: cron drift (guard 303/130), asimetría intracom 111/115, UI exoneración SII, situación inmueble en datos_extraidos. Hallazgo preexistente conocido sin tocar: test `registry-wired` (cron `ocr-dispatcher` sin case en admin).
