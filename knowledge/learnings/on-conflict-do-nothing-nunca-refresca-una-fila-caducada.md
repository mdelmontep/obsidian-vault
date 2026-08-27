---
title: on conflict do nothing nunca refresca una fila caducada y mata el dedup
date: 2026-08-27
source: centro-elphis
tags: [postgres, idempotencia, n8n]
---
Una tabla de idempotencia con `expires_at` y `ON CONFLICT (key) DO NOTHING` protege
bien... hasta que la primera fila caduca. Entonces la clave sigue existiendo, el
`INSERT` sigue devolviendo 0 filas, y **el dedup de esa clave queda muerto para
siempre**: cada evento pasa como si fuera nuevo.

En Elphis eran 26 claves en ese estado; una desde el 17-jul. Cada llamada del mismo
contacto abría un deal nuevo en el CRM. Nadie lo vio porque el síntoma es "de más",
no un error.

Patrón correcto — reclamar la ventana solo si venció:
```sql
ON CONFLICT (key) DO UPDATE
  SET expires_at = EXCLUDED.expires_at, created_at = NOW()
  WHERE tabla.expires_at < NOW()
```
Verificable con `BEGIN; … ROLLBACK;`: clave viva → `INSERT 0 0`, caducada → `0 1`.
Efecto lateral: `created_at` pasa a ser la ÚLTIMA reclamación, no la primera.
