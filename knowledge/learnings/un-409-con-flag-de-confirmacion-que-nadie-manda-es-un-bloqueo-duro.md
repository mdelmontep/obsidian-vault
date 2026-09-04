---
title: un 409 con flag de confirmación que ninguna pantalla manda es un bloqueo duro
date: 2026-09-04
source: facturaia
tags: [api, ux, guardarrail, revision]
---

Un guardarraíl que responde 409 «confírmalo y vuelve» solo es un guardarraíl si **alguna
superficie manda de verdad el flag**. Si el backend lo acepta y ninguna pantalla lo envía,
lo entregado es un muro: el documento no se puede aprobar por ningún camino, y los tests
del backend están verdes porque el flag existe en el `BodySchema`.

FacturaIA lo ha pagado tres veces (`duplicado_sin_confirmar`, `albaranes_sin_cruzar`,
`coste_desviado_sin_confirmar`). Lo que lo evita:

- La lista de flags vive en **un solo módulo** que construye el `RequestInit`
  (`aprobar-recibida-request.ts`), no repartida por cada vista.
- Un candado que extrae las claves **enteras** del `BodySchema` del endpoint y compara con
  ese módulo. Ojo: `toContain('confirmar_coste')` casa con `confirmar_coste_x` y da verde
  sobre el desajuste que existe para cazar — medido por mutación, sin víctima.
- Y contar las superficies: en esta app son tres (ficha, listado, bandeja), y la bandeja
  además necesita su rama ANTES del genérico o el 409 se lee como «ya estaba aprobada».
