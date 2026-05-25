---
title: etag por path con upsert mutable devuelve 304 indefinido
date: 2026-05-26
source: claude-code-session
tags: [debugging, cache, http, anti-pattern, storage]
---

Si un endpoint sirve un blob **mutable** desde un almacén que permite upsert sobre el mismo path (Supabase Storage, S3, GCS, R2) y calcula el ETag como función del path (`W/"${path}"`, o `etag = md5(path)`), el navegador recibe **304 Not Modified indefinidamente** tras una regeneración. El comentario "los archivos son inmutables por path" es la trampa: lo son hasta que alguien hace upsert.

Síntomas: el usuario "regenera X" y dice que no cambia nada. Curl con `If-None-Match` devuelve 304 con el ETag viejo. Curl sin ese header devuelve el blob nuevo. El CDN del provider sí invalida en upsert pero el browser cache local sigue stale por ETag.

**Fix**: ETag fuerte = `"sha256-<base64(slice 22)>"` del buffer real + `Cache-Control: private, no-cache`. El navegador siempre revalida, el ETag permite 304 cuando el hash coincide y 200 cuando cambia. Coste: download del blob siempre, hash trivial (μs).

Caso real FacturaIA 2026-05-26: `/api/documents/file/route.ts` servía PDFs de facturas con ETag `W/"${path}"`. "Regenerar PDF" hacía upsert sobre `${orgId}/factura/${num}.pdf`. Storage actualizado, BD actualizada, browser servía el PDF viejo. Commit fix `87d08e7`. Ver [[cache-invalidation-artifacts-emitidos]] y [[pdf-adjunto-email-vs-link-frozen-blob]].
