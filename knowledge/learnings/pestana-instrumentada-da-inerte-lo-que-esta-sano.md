---
title: una pestaña instrumentada da por inerte una app que está sana
date: 2026-08-22
source: facturaia
tags: [react, nextjs, hidratacion, ppr, metodo, medicion]
---
Conducir el navegador con la extensión abre la pestaña en segundo plano (`document.visibilityState === "hidden"`). Ahí React hidrata `<html>`, el `<head>` y el div raíz — **17 nodos de 1519** — y el resto se queda en el fallback de ruta, sin error en consola. Se lee exactamente como una caída de producción.

El mismo build, con login real y un Chromium limpio vía Playwright: **1476 / 1575** nodos hidratados, 0 fallbacks, y la interacción que "no funcionaba" pasando 6 de 6.

Trampa que costó una reapertura de issue: en el HTML servido, **dos `<template id="B:n">` con sus `<div hidden id="S:n">` y un solo `$RC(` NO son síntoma**. La sesión que sí hidrata recibe exactamente los mismos marcadores; es el patrón normal de PPR. Descartados también por medición, no por razonamiento: service worker, su caché, la caché HTTP y los bytes de los 19 chunks (idénticos a la red).

Regla: antes de declarar caída por lo que ve un navegador instrumentado, reprodúcelo en uno limpio. Y si el "control" de la comparación no hidrata tampoco, comprueba que no sea un 404 — el mío lo era. Ver [[playwright-domcontentloaded-no-espera-hidratacion-rsc]].

Añadido 26-ago, el mismo fallo con dos instrumentos peores. El discriminador más barato **no es un navegador limpio, es la BD**: filas con `actor_type = 'human'` en `audit_log` posteriores al deploy prueban que la app hidrata para gente real sin abrir nada (aquel día, la propia activación por `POST` un minuto después del deploy). Y ojo al selector: consultar `input[type=radio]` en un repo donde todo control es un componente de `ui/` (`<Segmented>` con `role="radio"`) devuelve **0 nodos**, y 0 nodos se lee como "todo deshabilitado y nada marcado". La avería la fabricó el instrumento, dos veces.
