---
title: en un ON CONFLICT, COALESCE no filtra un jsonb {"k":null} y el WHERE veta el UPDATE entero
date: 2026-09-08
source: centro-elphis
tags: [postgres, idempotencia, upsert, n8n]
---
Patrón de caché/idempotencia: `INSERT … ON CONFLICT (key) DO UPDATE SET response =
COALESCE(EXCLUDED.response, tabla.response)`. Dos trampas medidas:

- **`'{"deal_id":null}'::jsonb IS NULL` es falso**, así que el COALESCE no protege: una escritura
  fallida PISA el valor bueno y envenena la clave hasta que caduque. Filtro correcto:
  `COALESCE(NULLIF(EXCLUDED.response,'{"deal_id":null}'::jsonb), tabla.response)`.
- **Añadir `WHERE tabla.expires_at < NOW()` al DO UPDATE no es la opción conservadora**: veta el
  UPDATE completo (`INSERT 0 0`), así que una clave envenenada queda irreparable toda la ventana.
- Renovar `expires_at` en cada escritura tampoco: la ventana no caduca nunca mientras haya tráfico.
  Semántica correcta para «un episodio»: `expires_at = CASE WHEN tabla.expires_at < NOW() THEN
  EXCLUDED.expires_at ELSE tabla.expires_at END`, y `created_at` con el mismo CASE.
- Ninguna ventana sustituye a comprobar el estado real del objeto cacheado antes de escribirle.
