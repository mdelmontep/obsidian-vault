---
title: formulario parcial + UPSERT de fila completa borra columnas no enviadas (pérdida silenciosa)
date: 2026-06-10
source: claude-code-session
tags: [backend, supabase, data-loss, forms]
---
Un formulario que solo edita un SUBCONJUNTO de columnas + un endpoint que hace UPSERT de la fila ENTERA defaulteando los campos ausentes (`?? false`/`?? null`) = **borra silenciosamente** las columnas que el form no muestra, en cada guardado. Caso real (TuFacturaIA perfil_fiscal, audit composición): la pestaña Settings no mostraba `recargo_equivalencia`/`roi_activo`/`vivienda_pre2013`/`rendimiento_neto`; al guardar el perfil se reseteaban a default → cálculo 303/130 erróneo. El bug NO está en ningún archivo aislado: emerge de la interacción form-parcial × upsert-full-row × valores backfilleados.
**Fix**: el mapper preserva — `payload.campo ?? existing.campo ?? default` (lee la fila actual antes del upsert). `??` solo cae en nullish, así que un `false` explícito del form SÍ sobreescribe; un `undefined` (campo no enviado) conserva el valor previo.
Detectarlo: tras un PR que toca un form sobre tabla con más columnas que el form, preguntar "¿qué columnas NO están en el form y qué les pasa al guardar?". Es típico tras unificar fuentes de verdad (JSONB→tabla). Ver [[triggers-bd-sync-son-antipatron]] · [[cache-invalidation-artifacts-emitidos]].
