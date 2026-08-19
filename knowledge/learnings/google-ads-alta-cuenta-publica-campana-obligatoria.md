---
title: el alta de una cuenta google ads publica una campaña sí o sí — pausar por api al segundo
date: 2026-08-19
source: facturaia
tags: [google-ads, marketing, browser-automation]
---

Una cuenta creada bajo MCC queda `CUSTOMER_NOT_ENABLED` (403 en toda la API) hasta
**completar el asistente de registro**, y el asistente no deja terminar sin publicar
una campaña con método de pago dentro. No hay camino "solo facturación".

Jugada que funcionó (TuFacturaIA, 19-ago): campaña semilla mínima (3 €/día, PAUSED no
existe como opción) → el usuario mete tarjeta → publicar → **pausarla por API en
segundos** (`campaignOperation update status PAUSED`) → gasto 0,00 €. El mutate FALLA
con `MUTATE_NOT_ALLOWED` mientras es borrador del wizard (`campaigns/new/...&draftId=`):
esperar a que exista como campaña real (GAQL `FROM campaign`) y pausar ese id.

Gotchas del wizard: valida la URL final EN VIVO (un apex con 404 = rechazo, usar un
subdominio que responda 200 y cambiarlo luego); los títulos que genera su IA traen
claims inventados (revisar antes de activar); y en los diálogos de assets (Angular)
una subida por CDP solo habilita «Guardar» si es **fresca en esa apertura del diálogo**
— reabrir y resubir el mismo fichero con otro nombre, no pelear con checkboxes.
