---
title: una migración ya aplicada en prod no se renumera aunque entre en main tarde
date: 2026-10-01
source: facturaia
tags: [supabase, migraciones, coordinacion, facturaia]
---
La regla «número con `mig:renumerar` justo antes del merge» tiene una excepción: si la
migración ya se aplicó en prod (db push antes del merge, por ejemplo para medir), su número
ya está en `schema_migrations`. Renumerarla a la siguiente libre deja dos versiones del
mismo SQL: `db push` da la vieja por hecha y aplica la nueva encima.

Caso: la 990 de #3112 estaba en prod; antes de que mergeara, entró la 991 de otro PR.
La 990 se mergeó DESPUÉS de la 991 conservando su número y `db push` quedó limpio.

Patrón: quien coordina la numeración pregunta «¿está aplicada en prod?» antes de dar la
orden de renumerar. Si sí, el número es fijo; que en main quede por debajo de una mayor es
inocuo. Relacionado: [[renumerar-migraciones-reescribe-referencias-de-migraciones-ajenas]].
