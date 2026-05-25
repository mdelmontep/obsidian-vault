---
title: Audit con 3 agentes paralelos detecta vulnerabilidades cross-sprint
date: 2026-05-24
source: TuFacturaIA audit conciliación v3 (Sprints A-E + cashflow v2.2)
tags: [meta, audit, multi-agent]
---

# Audit con 3 agentes paralelos cierra blind-spots cross-sprint

Tras 6 commits en una sesión larga (Sprint A schema → B chips → C reglas → D tests → E UI gestión → fuzzy + cron), el código pasa typecheck/lint/build/tests y "parece bien". Pero acumula deuda invisible: vulnerabilidades sutiles, race conditions, A11Y, edge cases.

El truco: 3 agentes paralelos con perfiles disjuntos auditando los MISMOS archivos pero con foco distinto.

## Los tres perfiles (probados, funcionan)

**1. Security/Backend audit**:
- Multi-tenant isolation, IDOR, SQL injection, RLS policies.
- Detecta: campos sin chequear `estado='activo'`, queries sin filtrar por org_id, regex ReDoS, falta de Cache-Control no-store en datos sensibles.

**2. SQL correctness + math audit**:
- Lee migraciones completas y compara con la versión anterior.
- Detecta: edge cases (importe 0, NULL en arrays), exclusividad de bonuses (que no se sumen dos veces), umbrales borderline (≥80 vs >80), tie-break determinista en ORDER BY, triggers que falta cubrir UPDATE/DELETE.

**3. UX + A11Y audit**:
- Lee componentes React + globals.css.
- Detecta: WCAG AA contraste (calcula real), aria-label faltantes, role="tab"/"radiogroup" sin tabIndex, copy ambiguo, responsive mobile breakpoints.

## Por qué tres y no uno

Un agente "all-in-one" con todos esos focos en su prompt produce informe genérico y superficial. Cada perfil enfocado encuentra ~10x más cosas en su área.

En esta sesión encontraron:
- Agente 1: 2 vulnerabilidades ALTAS (`org_module_config` RLS sin estado='activo', client upsert sin org_id) + 1 MEDIA (UPSERT race).
- Agente 2: 2 bugs MEDIOS (falta UNIQUE INDEX en sugerencias para que ON CONFLICT DO NOTHING sea efectivo; trigger DELETE no resetea es_ambigua) + 1 inconsistencia documental (mig 155 dice 0..200, mig 156 corrige a 0..170).
- Agente 3: 4 issues A11Y (chips sin aria-label, tabs sin tabIndex, badge contraste 3.2:1 falla AA, palabras genéricas sin warning) + 2 UX (copy toggle confuso, tabla no responsive).

## Coste-beneficio

3 agentes en paralelo = ~3 min de wall clock + ~10K tokens cada uno. A cambio cierras ~30 hallazgos que de otra forma irían a producción.

Solo aplica si los cambios son grandes (>5 archivos tocados o >1 migración SQL). Para cambios chicos, 1 agente o ninguno.

## Prompts efectivos

Lo que funciona:
- Listar EXACTAMENTE los archivos a auditar al inicio (no "todo el cashflow").
- Listar entre 15-25 puntos NUMERADOS a verificar — cada agente devuelve hallazgos por punto. Más fácil de filtrar después.
- Pedir "✅ OK / ⚠️ Riesgo MEDIO / ❌ Vulnerabilidad ALTA" + citación archivo:línea + fix recomendado concreto.
- "Sé crítico — quiero production-ready, no compila".

Lo que NO funciona:
- "Audita la conciliación". Devuelve análisis vago.
- "Encuentra bugs". Devuelve cosas obvias.
- Pedir un único informe consolidado de un único agente — pierde la profundidad de las 3 perspectivas.

## Filtro de falsos positivos

~30% de los hallazgos son ruido. Ejemplos:
- "Falta validación de input length" (cuando el endpoint ya usa Zod).
- "Posible XSS en concatenación" (cuando es interpolación de string en SQL parametrizado).
- "Race condition" (cuando ya hay UNIQUE constraint cubriendo).

Lee TODOS los hallazgos, filtra por relevancia, aplica solo los que tengan evidencia real en código. ~60-70% acaban aplicándose.

## Conexión

Va con [[3-agentes-paralelos-auditoria-cambios-grandes]] y [[2-agentes-humanos-paralelos-detectan-jerga-tecnica-en-copy]] — patrones de multi-agente que confirman que la paralelización de perfiles supera al agente único.
