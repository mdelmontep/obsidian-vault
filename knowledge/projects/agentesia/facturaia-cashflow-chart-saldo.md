---
title: TuFacturaIA — Cashflow chart como saldo proyectado
date: 2026-05-26
source: sesión Claude
tags: [facturaia, cashflow, ui, producto]
---

# Cashflow chart → saldo proyectado

## Problema

En `/cashflow`, al conectar el banco con Tink (demo → 20.000€), el hero "Tienes ahora" muestra 20.598€ pero el gráfico principal sigue mostrando barras de ingresos/gastos en escala 0-2k€. **El usuario no ve recompensa por conectar el banco** y la pregunta mental que se hace ("¿llego a fin de año?") queda sin responder.

Hoy el gráfico responde a "¿cuánto entró y salió cada mes?" (flujo) cuando el autónomo se pregunta "¿cuánto voy a tener?" (saldo). Es contabilidad mostrada en lugar de tesorería.

## Hipótesis de producto

Lo que provoca el "ah, esto me interesa" en un autónomo / empresario es ver una **línea de saldo bancario proyectada** que parte del saldo actual (20.598€) y baja/sube mes a mes, cruzando 0 o no. Ver de un vistazo el runway. Lo que hacen Qonto, Pennylane, Holded en su dashboard de tesorería.

## Decisión

**Convertir el gráfico principal en una línea de saldo acumulado proyectado.** Las barras de ingresos vs gastos (flujo) pasan a vista secundaria.

## Diseño

### Gráfico principal (saldo proyectado)
- **Línea continua** de `saldoAcum` mes a mes (`src/lib/cashflow.ts` ya lo calcula en `CashflowMesExt.saldoAcum`).
- **Tramo real** (meses pasados + actual): línea sólida color `--fg` o `--brand-2`.
- **Tramo previsto** (meses futuros): misma línea pero color `--brand` y opacidad 0.6 o dasharray suave.
- **Zona bajo la línea**: área con gradiente `--brand` opacity .08 (igual que hoy el neto-area).
- **Línea 0€** visible siempre: si la curva la cruza, banda roja sutil debajo (`--danger` opacity .04) en los meses con saldo < 0.
- **Eje Y**: del mínimo (peorMes.saldoAcum si <0, o 0) al máximo (saldoInicial + algo de aire). Formato 20k / 15k / 10k / 5k / 0.
- **Pin de mes crítico**: ya existe (`criticalYm`). Se mantiene en el punto donde la línea toca el peor saldo. Texto cambia de "Mes más justo" a `–1.240€ en oct` o similar.
- **Punto "hoy"**: dot más grueso en el mes actual marcando dónde acaba lo real y empieza la previsión. Línea vertical "PREVISIÓN ▸" se mantiene.

### Anotaciones sobre la línea (el detalle que convierte)
Eventos clave del horizonte previsto:
- IVA / RETA estimados (events fiscales con prefijo `fiscal:`).
- Eventos puntuales no realizados (`cashflow_events`).
- Facturas con vencimiento futuro > umbral (ej. >2.000€).

Cada anotación es un pequeño tick vertical sobre la línea con tooltip al hover: `"23 jul · IVA Q2 −1.200€"`. Máximo 4-5 anotaciones para no saturar (priorizar por importe absoluto).

### Vista secundaria (flujo mensual)
Las barras ingresos vs gastos no desaparecen — se mueven a:

- **Tooltip al hover**: al pasar el ratón por un mes, popover con "Ingresos: 2.150€ · Gastos: 1.840€ · Neto: +310€".
- **Toggle pequeño** debajo del título del Panel: `Saldo | Flujo` (radio segmentado, default Saldo). Si el usuario quiere ver el flujo histórico, un click. No es el default.

Razón: los autónomos no tocan toggles, pero los contables sí. Saldo para la mayoría, flujo a un click para quien lo busca.

### Estado sin saldo configurado
Si `saldoIB.total === null` (no PSD2 ni manual): el chart actual (flujo de barras) se mantiene como fallback, con un overlay sutil "Indica tu saldo para ver la previsión de tesorería" + CTA al hero. La línea de saldo solo aparece cuando hay saldoInicial real.

## Cambios técnicos concretos

### Datos
- **Ya disponibles**: `CashflowMesExt.saldoAcum` existe (`src/lib/cashflow.ts:37`). No hay que tocar `buildCashflowData`.
- **Eventos para anotaciones**: ya están en `eventos` (state de `cashflow-view.tsx`). Hay que pasárselos al chart.

### `src/components/charts/cashflow-chart.tsx`
- Nuevo prop opcional `mode?: 'saldo' | 'flujo'` (default `'saldo'`).
- Nuevo prop opcional `eventos?: CashflowEvento[]` para las anotaciones (solo previsión).
- Nuevo prop opcional `saldoInicial?: number` para anclar eje Y y mostrar baseline.
- En modo `saldo`: renderizar polyline sobre `saldoAcum` en vez de bars. Reutilizar `criticalYm` para el pin (apuntando al saldoAcum del peorMes).
- En modo `flujo`: comportamiento actual sin cambios.

### `src/components/cashflow/cashflow-view.tsx`
- Estado local `chartMode: 'saldo' | 'flujo'` (default `'saldo'`).
- Pasar al `<CashflowChart>` el modo, los eventos y `saldoInicial`.
- Toggle segmentado debajo del `<Panel title="Flujo de caja detallado">`.
- Si `saldoIB?.total === null`: forzar modo flujo + overlay CTA.
- Cambiar título del Panel: "Saldo proyectado" (no "Flujo de caja detallado") cuando modo = saldo. Subtítulo: "Cómo evolucionará tu dinero los próximos 3 meses".

### `src/components/dashboard/dashboard-view.tsx`
Línea 575: también pasa `data={cashflow}` al chart. Decisión: ¿el dashboard usa modo saldo o flujo?
- **Propuesta**: dashboard también en modo `saldo`, sin toggle ni anotaciones (es resumen, no detalle). Reusa la curva. Mantiene los 4 KPIs alrededor.

## Anti-patrones a evitar

- **No** mezclar dos escalas (saldo + flujo) en mismo SVG — los 20k aplastan los 2k.
- **No** poner el toggle como pestañas grandes — segmented control discreto.
- **No** dibujar la línea desde 0 si hay saldo inicial — partir del saldo es justo el punto.
- **No** ocultar el flujo del todo — el contable lo pide. Por eso el toggle y el tooltip.
- **No** romper el dashboard mientras se cambia cashflow-view — son dos consumers.

## Criterios de éxito (smoke post-deploy)

1. Conectar Tink demo → "Tienes ahora" 20k → línea de saldo parte de 20k visiblemente.
2. La línea cruza 0 si los gastos previstos superan al saldo + ingresos → banda roja visible.
3. Hover sobre mes → tooltip con desglose ingresos/gastos/neto.
4. Toggle a "Flujo" → vuelve el gráfico de barras actual sin perder estado.
5. Sin saldo configurado → fallback al flujo + overlay CTA.
6. Dashboard `/` → línea de saldo en pequeño, sin toggle, sin anotaciones.

## Lo que NO entra en este cambio

- Modelado de saldo histórico diario (sigue siendo mensual).
- Comparativa con periodo anterior.
- Forecasting con IA (ya hay nudges deterministas en `narrative.ts`, no se tocan).
- Cambios en KPIs ni en panel de "Previsión de gastos".

## Riesgos

- **Lectura ambigua** si el usuario interpreta la línea como "lo que voy a ganar" en vez de "lo que voy a tener". Mitigación: título claro "Saldo proyectado" + subtítulo + eje Y en € absolutos, no relativos.
- **Eje Y dominado por saldoInicial alto** que aplaste variaciones: si saldo es 50k y movimientos son 2k, la curva parece plana. Mitigación: eje Y arranca en `min(saldoAcum) − padding`, no en 0, si el rango lo justifica. Decisión a validar visualmente.
- **Performance**: ninguno, mismos datos.

## Siguientes pasos

1. OK del usuario sobre esta spec.
2. Implementar `cashflow-chart.tsx` con `mode` + `eventos` + `saldoInicial`.
3. Integrar en `cashflow-view.tsx` con toggle + título dinámico.
4. Integrar en `dashboard-view.tsx` (modo saldo sin toggle).
5. Lint + typecheck + build.
6. Smoke con Tink demo. Iterar visual si el eje Y no funciona.

## Resultado final (2026-05-26)

**Iteración 1** (commit `d810e31`) implementó la spec tal cual: prop `mode='saldo'|'flujo'` + toggle segmentado. Funcional pero el user lo encontró "tosko" — el toggle era fricción innecesaria y dividía la lectura ("¿cuándo miro saldo, cuándo miro flujo?").

**Iteración 2** (commit `26cb553`) rediseñó a UN solo chart con dos bandas verticales (estilo TradingView price+volume):

- **Banda superior (72%)**: línea de saldo Catmull-Rom → Bézier (no quebradiza), tramo real `--fg` sólido + tramo previsto `--brand` punteado, área con gradient brand 22%→0%, banda roja sutil bajo 0, dot pulsante en mes "hoy", pin animado en peor mes con su saldo en €, anotaciones (máx 3) de eventos puntuales como ticks discretos sobre la línea.
- **Banda inferior (volume-style)**: mini-barras pareadas ingresos arriba (gradient brand) + gastos abajo (gradient slate), previstas a 45-55% opacidad. Eje 0 común con tick `±maxFlow` en JetBrains Mono.
- **Interacción**: hover line vertical + tooltip HTML flotante (saldo cierre · ingresos · gastos · neto coloreado), barras no-hovered al 55% para foco, animación entrada 120ms.
- **Compat sin saldo**: si no hay saldoInicial, banda flujo a altura completa, sin banda saldo. Layout no se rompe.
- Toggle eliminado, prop `mode` eliminada. Un chart, dos preguntas resueltas.

Lint clean (errores pre-existentes en `integrations-section.tsx` untracked NO míos), typecheck 0, build success.

**Aprendizaje meta**: cuando la UX exige al usuario elegir entre dos modos para ver datos relacionados, suele significar que el diseño debería integrarlos en una lectura única. La iteración 1 era correcta funcionalmente pero el toggle era el síntoma de la fricción real (dividir lo que el cerebro lee a la vez).
