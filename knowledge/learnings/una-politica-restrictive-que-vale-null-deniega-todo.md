---
title: una política rls restrictive cuya expresión vale null deniega la fila, también en rutas que no querías cerrar
date: 2026-10-01
source: facturaia (ticket de soporte 188, mig 983 → 991, PR #3178)
tags: [postgres, rls, supabase, storage]
---
- Una política `AS RESTRICTIVE` se combina con AND a las permisivas; si su expresión da NULL, la fila se rechaza igual que con `false`.
- `NOT (bucket_id = 'x' AND (storage.foldername(name))[2] = 'carpeta')` parece "todo menos esa carpeta", pero con una ruta de UNA carpeta (`<org>/fichero.pdf`) el índice `[2]` es NULL → `NOT NULL` = NULL → deniega.
- Caso real: la mig 983 cerró el bucket `facturas` a toda subida con sesión durante un día en todas las orgs (`/api/upload` guarda en `<org>/<ts>-<nombre>`). Ningún test lo vio: service_role no pasa por la RLS y los de integración solo usaban rutas de dos carpetas.
- Fix: `IS NOT DISTINCT FROM 'carpeta'` (o `coalesce(...,'')`) en cualquier comparación con un elemento de array, un JSON opcional o una columna nullable dentro de una RESTRICTIVE.
- Test: medir cada FORMA de entrada (ruta plana, con subcarpeta, la carpeta cerrada, otra org) como `authenticated`, en INSERT y en UPDATE. En facturaia hay un candado estático: `scripts/__tests__/politica-restrictiva-sin-null.test.ts`.
