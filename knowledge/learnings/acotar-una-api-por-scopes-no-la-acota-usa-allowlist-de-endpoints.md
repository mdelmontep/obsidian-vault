---
title: acotar una api pública por scopes no la acota — mide la intersección y usa allowlist de endpoints
date: 2026-08-17
source: claude-code-session
tags: [api, gating, planes, seguridad, facturaia]
---

Para dar acceso ESTRECHO a un integrador, el reflejo es «que su clave lleve solo los
scopes que necesita». No funciona: los scopes son gruesos y varias rutas comparten uno.

Medido en TuFacturaIA sobre las 50 rutas `/api/v1` (issue #1844): con los scopes que el
CRM necesitaba —`clientes:*`, `presupuestos:*`, `facturas:*`— quedaban abiertos además
`proveedores/*` (comparte `clientes:read/write`), `catalogo/*`, `fiscal/iva-trimestral`,
`fiscal/retenciones`, `resumen`, `clientes/top`, `facturas/recibidas/*`, `anular`,
`marcar-cobrada` y `buscar`. Con `facturas:read` se veía el IVA trimestral.

El patrón que sí acota: **allowlist de endpoints evaluada en el wrapper común**, contra la
etiqueta que cada ruta ya declara. Ventaja decisiva: una ruta nueva **nace fuera**, así que
la superficie no crece por olvido.

Dos trampas al implementarlo:
- La etiqueta es texto libre → renombrarla deja la entrada muerta y cierra el endpoint en
  producción con un 403 silencioso. Hace falta un test que cruce la allowlist contra las
  etiquetas reales del árbol de ficheros.
- El 403 debe distinguir «no tienes acceso» de «tu derecho no llega a esta ruta»; con un
  texto único mandas a comprar plan a quien ya tiene el que necesita.

Antes de diseñar el derecho, **mide la intersección**: lista el scope de cada ruta y mira
qué se cuela. No es derivable leyendo el gate. Ver [[capacidad-en-dos-capas-tool-mas-gate-endpoint-verificar-paridad-o-queda-muerta]].
