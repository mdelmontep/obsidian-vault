---
title: ADR-052 — persistir el motivo de la suspensión para decidir quién puede reactivar
date: 2026-08-15
status: accepted
tags: [adr, facturaia, billing, stripe]
---

## Contexto

Arreglar #1788 (pausar el cobro en Stripe no suspendía la cuenta) exigía también
reactivar al despausar. Pero `change_billing_status` no guardaba POR QUÉ se
suspendió una cuenta, así que cualquier señal de «esto ya está bien» servía de
llave maestra: un cobro recuperado o una reanudación devolvían el acceso a una
cuenta suspendida por DISPUTA. El agujero ya existía antes del issue.

## Opciones consideradas

- **A — Persistir el motivo** (columna + parámetro en la RPC): reactivar exige que
  el motivo encaje. Toca el núcleo de la máquina de estados y lleva migración.
- **B — Solo suspender, sin reactivación automática**: cierra el acceso-sin-cobro
  sin tocar nada más, pero deja al cliente en solo-lectura hasta el siguiente
  cobro con éxito, que con `behavior=void` pueden ser semanas.
- **C — Reactivar por `previous_attributes`** sin motivo: arregla el issue tal cual
  y acepta a sabiendas resucitar cuentas con disputa abierta.

## Decisión

**A**. Vocabulario cerrado (`impago`, `disputa`, `cobro_pausado`, `manual`) con
CHECK en BD y espejo TS. Un motivo NULL cuenta como «no reactivable»: ante la
duda, no dar acceso. Coste asumido: migración sobre la RPC del cobro (693).

## Consecuencias

Cada camino que suspende declara su motivo, y quien no lo declare deja la cuenta
sin reactivación automática — por eso el parámetro es obligatorio en el handler.
La guarda aprieta **solo** `suspended`: desde `grace_period` o `expired` se
reactiva igual que antes, porque ahí no hay motivo que consultar (lo detectó la
suite al romper la reactivación de #1690). Una disputa pasa a exigir decisión
humana desde el panel de admin, a propósito.
