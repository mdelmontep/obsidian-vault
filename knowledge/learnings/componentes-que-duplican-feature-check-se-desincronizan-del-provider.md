---
title: componentes que duplican feature check se desincronizan del provider
date: 2026-04-21
source: claude-code-session
tags: [react, feature-flags, arquitectura, saas]
---

Cuando existe un `FeatureProvider` centralizado que resuelve features (override org > plan default > false), los componentes que hacen su propia consulta de features (RPCs individuales, fetch aparte) se desincronizan.

## Síntoma

Feature habilitada en el plan y visible en el admin, pero la UI del componente la muestra como "bloqueada".

## Causa raíz

El componente hace N llamadas RPC individuales a `org_has_feature()` en vez de consumir el contexto del provider. Si la RPC falla, el set local queda incompleto → feature aparece como no disponible.

## Caso real

`CanalesIngesta` en FacturaIA hacía 4 RPCs individuales por canal. Con plan Enterprise (todos los features habilitados), las tarjetas aparecían bloqueadas. Fix: reemplazar RPCs por `useFeatures()` del `FeatureProvider` existente.

## Regla

Si existe un provider/contexto de features, **siempre** usar su hook (`useFeatures()`, `useFeature(id)`). Nunca hacer queries directas a la BD desde componentes para verificar features. La única fuente de verdad client-side es el provider.
