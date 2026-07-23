---
title: TuFacturaIA — Factura de anticipo con IVA propio (spec futura)
date: 2026-07-24
source: chat análisis + 2 rondas de agentes (fiscal/arquitectura/UX + adversarial)
tags: [facturaia, fiscal, verifactu, conciliacion, anticipos, roadmap, later]
---

# Factura de anticipo con IVA propio — spec para implementación futura

> **Estado**: LATER — no iniciado, no priorizado. Anotado para cuando haga falta (típico en obras/reformas/proyectos largos con anticipo formal).
> **No confundir** con el sistema YA EN PRODUCCIÓN de "anticipo a cuenta" (`276_conciliacion_anticipos.sql`, tabla `anticipo`, `registrar_anticipo`/`aplicar_anticipo`): ese vincula un movimiento bancario a un contacto SIN generar documento fiscal, y luego lo aplica a una factura ya existente vía `movimiento_factura_asignacion`. Sigue siendo válido y no se toca. Esta spec es para cuando el cliente necesite una **factura real con IVA** del anticipo cobrado.

## Problema de negocio

Un cliente de TuFacturaIA cobra un adelanto de SU cliente antes de completar el trabajo. Necesita: (a) poder emitir una factura real del anticipo (con IVA, numerada como cualquier factura), y (b) que al facturar el trabajo completo, ese anticipo se descuente correctamente sin duplicar ni descuadrar el 303/VeriFactu.

## Por qué NO es un tipo de documento nuevo

VeriFactu (Orden HAC/1177/2024) no tiene una clave `TipoFactura` para "anticipo" — solo F1/F2/R1-R5. Un anticipo cobrado se factura como **F1/F2 normal**, serie A/S de siempre, vía `createDocument()` sin ningún caso especial. La numeración/huella/encadenamiento son los de cualquier factura.

## El mecanismo correcto (verificado contra el motor real, no en abstracto)

**Descartado tras verificación**: "restar solo del total, no de la base" — suena fiscalmente prudente pero es **incorrecto para este código**. `465_verifactu_huella_fechahorahuso.sql` calcula `CuotaTotal = total - base` **directamente en SQL**. Si se toca `total` sin tocar `base` en la misma proporción, la cuota de IVA declarada a la AEAT queda matemáticamente falsa y la factura incumple el desglose obligatorio (RD 1619/2012 art. 6.1.d-e: `Total ≠ Base + Cuota`).

**Mecanismo correcto**: la deducción del anticipo es una **línea normal con `cantidad` negativa**, al `iva_pct` **congelado** del anticipo original (no el tipo vigente en la factura final — así se declara correctamente un anticipo cobrado a un tipo distinto si hubo cambio impositivo entre medias). `calcularTotales()` (`src/lib/documents/totales.ts`) ya agrupa líneas por `iva_pct` en un `Map` y construye `total = baseNeta + iva` — **ya soporta tipos de IVA mixtos dentro de una factura** (no hace falta ningún caso especial: una cantidad negativa fluye por el mismo cálculo y el invariante `Total = Base + Cuota` se mantiene siempre, porque no se calculan por separado).

## Bug real que esto destapa (no lo encontró ningún agente, solo trazar el signo a mano)

`src/lib/documents/anular-factura.ts:262` construye las líneas del abono así: `cantidad: Math.abs(Number(l.cantidad))`. Asume que **todas** las líneas de una factura normal son positivas (cierto hoy: el 100% de las facturas existentes solo tienen líneas positivas). Con una línea de anticipo de `cantidad` negativa dentro de una factura normal, ese `Math.abs()` la aplanaría a positivo ANTES de que `buildLineasFactura(lineas, sign=-1)` le aplique el signo del abono — el abono generado **no revertiría correctamente la línea de anticipo** (el cliente no recuperaría el crédito al anular la factura final).

**Fix necesario**: quitar el `Math.abs()` en esa línea (inofensivo hoy porque todo es positivo; deja de serlo con este cambio, y hace falta preservar el signo real para que `buildLineasFactura` invierta bien tanto las líneas normales como la de anticipo).

## Schema mínimo (sin columnas de "total ajustado")

- `facturas.es_anticipo boolean default false` — metadato para UI/listas ("¿qué facturas son anticipos?"), sin efecto fiscal.
- `lineas_factura.anticipo_factura_id uuid null references facturas(id)` — marca qué línea es una deducción y de qué factura de anticipo viene. Permite calcular "cuánto del anticipo ya está aplicado": `SUM(ABS(subtotal)) FROM lineas_factura WHERE anticipo_factura_id = X AND factura_id IN (facturas activas, no anuladas)`.
- Función/trigger `SECURITY DEFINER` + `REVOKE FROM PUBLIC/anon` (patrón `133_conciliacion_fiscal_hardening.sql` / `265_conciliacion_guard_capacidad_movimiento.sql`) que garantice `Σ aplicado ≤ anticipo.total` con lock antes de insertar la línea — mismo patrón que los guards de capacidad/overpayment ya existentes en conciliación.
- Regla de scope v1: el anticipo solo se aplica a una factura final en la **misma moneda** — evita la complejidad de congelar tipos de cambio cruzados (limitación consciente, no bug; el resto del sistema multidivisa ya congela `total_eur` por factura individual, esto simplemente no lo cruza entre dos facturas).

## UX (validado en la ronda de agentes, no re-litigar)

- **Un solo punto de entrada**: NO dos botones separados para "a cuenta sin factura" vs "factura de anticipo con IVA" — el usuario no debe tener que saber esa distinción fiscal de antemano. Modificar el modal `AnticipoModal` existente (drawer de conciliación bancaria) para preguntar, en el momento del cobro: *"¿Necesitas emitirle una factura de este anticipo?"* → No: flujo actual sin cambios. Sí: crea la factura real.
- Solo desde conciliación bancaria (donde llega el cobro) — no en 3 sitios (nueva factura, ficha cliente, etc.): es el único momento en que el sistema ya conoce importe/contacto/fecha sin que el usuario teclee nada.
- En el editor de la factura final (`/generar`): si el cliente tiene facturas `es_anticipo=true` sin aplicar del todo (misma moneda), aviso + botón "Aplicar anticipo" que inserta la línea negativa. Poder **quitarla mientras la factura sigue en borrador** (antes de emitir) — imprescindible, aplicar mal un anticipo sin poder deshacerlo obliga a anular y reemitir.
- Copy de la línea (la ve el cliente final del emisor, no solo el emisor): con fecha, no con jerga de código interno — `"A cuenta del anticipo cobrado el 12/03 (factura A-0045): −300,00 €"`.
- Falta pantalla/lista "Anticipos pendientes de aplicar" (badge en ficha de cliente + aviso en el editor) — sin esto el usuario cobra el anticipo, factura, y se olvida de que queda dinero cobrado sin descontar.

## Único bloqueante real sin resolver

Si el desglose de IVA de VeriFactu (`src/app/api/verifactu/process/route.ts`, agrupado por `iva_pct`/exención) admite un tramo con **cuota negativa** dentro del mismo documento sin que el XML sea rechazado por la AEAT. No se puede verificar sin probarlo contra el validador real (entorno de pruebas AEAT) o consultarlo con un asesor fiscal — bloqueante antes de implementar, mismo criterio que el resto de huecos VeriFactu ya pendientes del proyecto (encadenamiento por-obligado).

## Proceso de esta spec (nota meta, por si se repite el patrón)

Esta spec pasó por 3 versiones antes de llegar a la correcta:
1. Boceto inicial sin verificar contra el motor real.
2. "Restar solo del total, no de la base" — sonaba fiscalmente prudente (evita duplicar la declaración del 303) pero es incorrecto para ESTE código: nadie había leído que `CuotaTotal = total - base` se calcula literalmente en SQL en el trigger de huella.
3. Correcta — solo salió al pedir una revisión **adversarial** explícita ("intenta romper el plan leyendo el código real") + trazar el signo línea por línea a mano contra `anular-factura.ts`.

Lección: para preguntas fiscales en este proyecto, razonar desde la ley en abstracto no basta — hay que verificar contra el trigger/RPC real que efectivamente calcula lo que se declara a Hacienda.
