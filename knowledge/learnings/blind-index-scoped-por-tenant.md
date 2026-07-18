---
title: blind index para buscar sobre columna cifrada debe ir scoped por tenant
date: 2026-07-18
source: FacturaIA — auditoría cifrado, A6/A7 (matching de conciliación)
tags: [cifrado, blind-index, multitenant, rgpd, facturaia]
---

# Blind index (HMAC) = búsqueda por igualdad sobre dato cifrado, con scoping por org

Si cifras una columna con AES-GCM (nonce aleatorio) pierdes la búsqueda por igualdad (join/dedup/match). Solución estándar: **blind index** = `HMAC-SHA256(clave_indice, normalizar(valor))` en una columna aparte. Permite `WHERE col_bidx = $1` exacto; no permite LIKE/fuzzy.

Dos reglas que un security-review pilló:
- **Clave HMAC separada de la de cifrado** (dominios de riesgo distintos) y verificar que NO son iguales al cargar.
- **Scoping por tenant**: `HMAC(clave, org_id + ':' + valor)`, no `HMAC(clave, valor)`. Sin el `org_id`, el mismo IBAN en dos orgs produce el mismo bidx → cualquiera con acceso a la columna (o un dump) **correlaciona la misma cuenta entre tenants** sin descifrar. En SaaS multi-org bajo RGPD eso es un dato inferible que el cifrado pretendía eliminar.
- Cambiar el scoping o rotar la clave del índice después exige **re-backfill de todos los bidx** (uno nuevo no casa con los viejos) → decidirlo antes del backfill. Ver [[cifrado-columna-dual-write-degrada]].
