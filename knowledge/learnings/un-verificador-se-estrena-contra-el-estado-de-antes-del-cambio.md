---
title: un verificador se estrena contra el estado de ANTES del cambio; si no sale rojo, mide otra cosa
date: 2026-09-14
source: centro-elphis
tags: [guardianes, verificacion, n8n, metodo]
---

Escrito el verificador de una migración en prod, correrlo primero contra una ejecución
**anterior** al cambio cuesta un comando y es la única prueba de que su criterio discrimina.

Ahí se cazó que el criterio no valía: usaba `__sin_aviso`, una bandera que el nodo emite
**tanto cuando todo va bien como cuando no pudo mirar** — el caso que la migración podía
provocar. Una bandera que significa «OK» y «no sé» a la vez no es un criterio.

El que discrimina es un campo que **solo existe en el camino sano** (aquí `revisadas`,
el contador de llamadas leídas), más el código HTTP y la forma de la respuesta. Misma
razón por la que el latido no sirve de verificación: se escribe también cuando falla.

Corolario: si el verificador sale VERDE contra el estado viejo, no lo estrenes — arréglalo.

Ver [[migrar-un-endpoint-deprecado-cambia-la-forma-y-el-consumidor-lo-calla]] ·
[[un-checker-que-se-pone-rojo-por-la-razon-equivocada-es-peor-que-no-tenerlo]]
