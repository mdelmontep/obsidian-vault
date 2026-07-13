---
name: subida-en-lote-cliente-backoff-sobre-rate-limit-servidor
description: Subida en lote desde navegador contra endpoint con rate-limit per-user — sin reintento el excedente se pierde; el fix es Retry-After exacto + backoff cliente + panel de reintento
metadata:
  type: feedback
---

## El patrón que falla

Un cliente que sube N ficheros en lote (bucle/concurrencia) contra un endpoint `/api/*` protegido por `withApiAuth` (rate-limit per-user, p.ej. 120/min ingesta o 10/min conciliación) **sin reintento sobre 429**. Cuando el lote supera el tope/min, el excedente recibe `429` y **se pierde en silencio**: no crea fila, no entra en la cola, solo un toast efímero. Caso real FacturaIA (13/7): 130 facturas → 30 perdidas.

Ojo: una cola de fondo (OCR) absorbe el *procesado*, **no** la ráfaga de *subida HTTP*. Son tramos distintos.

## El fix (PR #874 + #876)

1. **Servidor**: el `429` de `withApiAuth` devuelve `Retry-After` **exacto** (PTTL real de la ventana Redis, campo `retryAfterMs` en `rateLimit()`) + `code: 'rate_limited'`.
2. **Cliente**: `fetchWithTransientRetry` (`src/lib/async/upload-retry.ts`) reintenta con backoff exponencial honrando `Retry-After` **solo** fallos transitorios (429 `rate_limited` + 5xx + red); NO reintenta topes de plan/org (mensual/diario) → esos se muestran como límite alcanzado.
3. **UX**: panel de resultado persistente (subidas / duplicadas / fallidas con motivo) + botón "Reintentar" que reintenta solo las fallidas (guarda el `File`).

Smoke prod verde: recuperación 149/150 (30 rate-limitadas reintentadas), `Retry-After: 52`/`60` + `code` confirmados en vivo. Tests unitarios cubren la política. Ver [[internal-fetch-res-ok-silencioso]].

## Follow-up (PR #878): subir-a-Storage-luego-insertar debe limpiar el blob si el insert falla

Al limpiar el smoke se destapó que `/api/upload` subía el fichero a Storage y, si el INSERT de `facturas`/`bandeja_ingesta` fallaba, borraba la factura pero **no el blob** → objetos huérfanos en el bucket. Las otras vías (whatsapp/email) ya lo hacían bien. Regla: **todo `storage.upload()` seguido de un INSERT debe borrar el blob (`remove([path]).catch()`) en cada rama de fallo del insert.** Un `.delete()` de la fila no basta.
