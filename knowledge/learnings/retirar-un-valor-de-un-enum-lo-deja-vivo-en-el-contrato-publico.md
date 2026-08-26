---
title: retirar un valor de un enum lo deja vivo en el contrato público
date: 2026-08-26
source: facturaia
tags: [api-design, openapi, drift, espejos]
---

Un estado vive en TRES sitios: el espejo TS, el `CHECK` de la migración y la spec
OpenAPI publicada. El test de espejo ataba **dos**. Al retirarlo (nadie podía
escribirlo ya) TS y SQL quedaron limpios y la spec siguió ofreciéndolo a los
consumidores externos como valor válido y como filtro aceptado.

El patrón: un espejo con N caras y un candado que mide N−1 no protege,
tranquiliza. Al retirar un valor, **cuenta las caras** (`grep` del literal en todo
el repo: spec y fixtures incluidos) antes de darlo por hecho.

Fix: el test camina el JSON de la spec buscando **todos** los enums que contienen
algún valor del eje, afirma cuántas listas hay y compara cada una con el espejo
TS — una lista nueva rompe el test en vez de divergir en silencio.
Ver [[openapi-spec-mantenido-a-mano-deriva-del-handler]].
