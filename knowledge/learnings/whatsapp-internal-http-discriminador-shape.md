---
name: whatsapp-internal-http-discriminador-shape
description: Producer y caller internos desarrollan por separado → shapes discriminador divergen → todos los paths non-success silenciosos
metadata:
  type: feedback
---

## El bug

`callIngestaAndRespond` chequeaba `data.upsell`, `data.quota_exceeded`, `data.multi_org_pending` — ninguno de los tres era nunca `true` porque el endpoint `/api/internal/whatsapp/ingesta` devolvía `{ error:'quota_exceeded' }`, `{ error:'OCR feature no activa', reason:'feature_no_activa' }` y `{ error:'Org no encontrada', reason:'multi_org_pendiente' }` respectivamente. Los campos que el caller esperaba no existían. El resultado: TODOS los paths non-success caían al console.error de fallback (o simplemente a silencio total si el fallback también faltaba).

## Causa raíz

El producer (ingesta route) y el consumer (webhook caller) se desarrollaron en turnos diferentes sin un contrato explícito. El consumer asumió formas que el producer nunca devolvía.

## Regla

**Al escribir un caller interno, leer el cuerpo real que devuelve el endpoint** (Read del archivo, no el contrato mental). Al cambiar la response de un endpoint interno, grep los callers antes del commit.

Patrón correcto: el producer devuelve formas canónicas taggeadas (`{ multi_org_pending: true }`, `{ upsell: true }`, `{ error: 'quota_exceeded' }`); el caller las discrimina con `if (data.multi_org_pending)`, `if (data.upsell)`, `if (data.error === 'quota_exceeded')`.

## Señal de alerta

Caller con varios `if (data.algoCosa)` que nunca entran en producción pero tampoco fallan en tests → los mocks tienen `ok: true` hardcoded y nunca ejercen los paths non-success.

Ver también [[internal-fetch-res-ok-silencioso]]
