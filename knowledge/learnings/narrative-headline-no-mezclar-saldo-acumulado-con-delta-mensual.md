---
title: Narrativa de forecast — NUNCA mezclar "saldo acumulado del peor mes" con "delta neto vs mes anterior" en la misma frase
date: 2026-05-24
source: bug copy cashflow v2.1 detectado por usuario + 2 agentes humanos
tags: [ux, copy, cashflow, contabilidad, narrative]
---

## Bug detectado

El módulo Cashflow IA mostraba:

```
Punto de riesgo en el horizonte
Ago: -2435 € saldo negativo previsto
⭐ IA  Ago mejora 714 € vs Jul porque: ...
```

El usuario y los 2 agentes humanos pararon en seco: *"si Agosto es el peor mes y está en negativo, ¿cómo puede 'mejorar'?"*.

## Causa raíz

El bloque mezclaba **dos métricas distintas** en la misma tarjeta:

1. **"Ago: -2435€"** = `saldoAcum` del mes (importe acumulado a fin de mes).
2. **"Ago mejora 714€ vs Jul"** = `delta neto mensual` (Ago.neto − Jul.neto).

Numéricamente eran compatibles (Jul gastaba más que Ago, por eso el "neto mensual de Ago" era menos negativo que el de Jul), pero **conceptualmente son dos historias distintas**:

- La primera dice "vas a acabar agosto en rojo".
- La segunda dice "en agosto te entra/sale algo menos que en julio".

Ambas pueden ser verdad a la vez y aun así confundir al lector. El cerebro lee "mejora" e ignora el contexto.

## Regla aprendida

**Una tarjeta = una historia.** Si quieres comparar mes con mes anterior, hazlo en otra zona (un sparkline, una tendencia visual). En el bloque de "este mes" cuenta SOLO lo que pasa ese mes:

✅ **"En agosto te faltarían 2.435€ para cubrir tus gastos. Los ingresos previstos (1.200€) no llegan para los gastos previstos (3.635€)."**

❌ "Punto de riesgo en el horizonte. Ago: -2.435€. Ago mejora 714€ vs Jul porque..."

## Implementación

En `narrative.ts`:

```ts
// MAL (antiguo):
export function narrativeHeadline(n: MonthNarrative, prevMes: string | null): string {
  const verb = n.deltaNeto < 0 ? 'cae' : 'mejora'
  const ref = prevMes ? `vs ${prevMes}` : 'respecto al mes anterior'
  return `${n.mes} ${verb} ${fmtEur(Math.abs(n.deltaNeto))} ${ref} porque:`
}

// BIEN (nuevo, commit da34f6c):
export function narrativeHeadline(n: MonthNarrative): string {
  if (n.enRiesgo && n.faltaParaCubrir !== null) {
    return `En ${n.mesLargo} te faltarían ${fmtEur(n.faltaParaCubrir)} para cubrir tus gastos.`
  }
  return `${n.mes} cierra con ${fmtEur(n.saldoAcum)} de margen.`
}
```

La firma cambió — eliminé el `prevMes` porque ya no se necesita. Si en el futuro quieres comparativa entre meses, ponla en una **zona separada** ("Tendencia 3 meses: -200€ menos que la media") con un sparkline aparte.

## Test de regresión

```ts
it('headline NO menciona mes anterior ("vs", "mejora", "cae")', () => {
  const headline = narrativeHeadline(narrativeEnRiesgo)
  expect(headline.toLowerCase()).not.toMatch(/mejora|cae|vs |delta/)
})
```

## Cross-ref

- Detectado por usuario + Lucía + Marcos en [[2-agentes-humanos-paralelos-detectan-jerga-tecnica-en-copy]].
- Fix en commit `da34f6c` `src/lib/cashflow/narrative.ts`.
- Patrón aplicable a CUALQUIER tarjeta de KPI con explicación: una métrica, una historia. Si necesitas comparar, contexto aparte.
