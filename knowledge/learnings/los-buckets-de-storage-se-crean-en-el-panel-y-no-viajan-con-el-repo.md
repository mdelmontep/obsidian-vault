---
title: los buckets de storage se crean en el panel y no viajan con el repo
date: 2026-08-12
source: claude-code-session
tags: [supabase, storage, migraciones, infra, reconstruccion]
---
Un bucket se da de alta con dos clics en el panel de Supabase, así que casi nadie escribe la
migración. El resultado es infraestructura que existe **solo en producción**: una base reconstruida
desde el repo nace sin ella y la app falla en un sitio que no la menciona.

Medido en TuFacturaIA: de 4 buckets, 2 (`facturas`, `logos`) no los creaba ninguna migración —solo
`feedback-screenshots` y `data-exports`—. En staging, `POST /api/upload` devolvía
`500 {"error":"Bucket not found"}`, o sea que ese entorno **no podía guardar ni un PDF de factura ni
un logo**. El síntoma llegó por un test que esperaba una región `[role=status]` que nunca aparecía.

Daño colateral que no es ruidoso: mientras faltó el bucket las facturas **se crearon igual y sin
PDF** (30 de 31). La subida falla y la creación del documento no aborta — razonable, pero invisible.

Patrón: al reconstruir un entorno, comparar `storage.buckets` origen vs destino, no solo tablas. Y
la migración con `ON CONFLICT DO UPDATE` es no-op en el entorno que ya lo tiene.

Ver [[facturaia]] · [[aplicar-migraciones-a-prod-antes-del-merge-caduca-la-reserva-de-numero]].
