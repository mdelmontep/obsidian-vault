---
title: endpoint que muta varias tablas debe invalidar TODOS los dominios cacheados que tocó
date: 2026-07-23
source: claude-code-session
tags: [nextjs, cache-components, use-cache, code-review]
---

Al añadir `use cache` dominio por dominio (E4 en TuFacturaIA), es fácil arreglar
la invalidación mirando SOLO el dominio que estás trabajando ahora mismo, y
olvidar que un mismo endpoint puede mutar tablas de OTROS dominios ya
cacheados. Caso real: un endpoint de reseed de datos borraba e insertaba
`facturas`, `clientes`/`proveedores` Y `presupuestos` en una sola request,
pero cuando se cacheó Presupuestos solo se añadió
`revalidateTag(presupuestosCacheTag)` — dejando Emitidas/Recibidas, Clientes
y Dashboard sirviendo datos borrados hasta expirar su TTL.

**Por qué no lo cazó el mapeo per-dominio**: cada ronda de E4 mapeaba "qué
mutaciones tocan MI dominio", no "qué otros dominios toca ESTE endpoint
concreto que ya estoy tocando". Un endpoint multi-tabla necesita el checklist
completo de invalidación de TODOS los dominios cacheados que sus escrituras
afecten, no solo el que motivó el cambio.

**Fix / blindaje**: al cachear un nuevo dominio, grep de endpoints que
mutan MÁS de una tabla relevante (`.delete()`/`.insert()`/`.update()` sobre
2+ tablas en la misma función) y verificar que invalidan TODOS los tags de
dominio que ya existan para esas tablas, no solo el nuevo. Lo cazó
`/fia-cierre` (dimensión BD) en una auditoría posterior al merge, no el
mapeo original.
