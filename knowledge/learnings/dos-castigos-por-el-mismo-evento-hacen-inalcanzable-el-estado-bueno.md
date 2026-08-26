---
title: dos guardas que castigan el mismo evento hacen inalcanzable el estado que protegen
date: 2026-08-26
source: facturaia
tags: [postgres, triggers, confianza, diseño, agentic]
---
La confianza de un proveedor en el OCR exigía **dos** cosas: `facturas_ok >= 3` **y** ninguna
corrección en 30 días. Y el trigger que detectaba una corrección hacía **las dos**: ponía el
contador **a 0** y rearmaba la ventana. Una sola corrección borraba el historial *y* abría la
cuarentena, así que un proveedor con 12 facturas limpias necesitaba 3 aprobaciones nuevas
**más** 30 días de silencio. No maduró nunca ninguno.

Fix (mig 755): el contador **decrementa** (`GREATEST(facturas_ok - 1, 0)`); la ventana sigue
rearmándose, que es su trabajo. Cada guarda castiga una vez.

Regla: si dos condiciones independientes gobiernan un estado, **un evento debe mover una sola**.
Si el mismo hecho penaliza las dos no tienes dos guardas, tienes una multiplicada — y el umbral
efectivo no es el escrito en el código.

Se detecta sin leer el trigger: contar cuántas entidades alcanzaron el estado bueno alguna vez.
Cero con meses de tráfico = el umbral no está calibrado, está roto.
Ver [[postgres-guard-transition-no-persiste-en-recompute-chain]].
