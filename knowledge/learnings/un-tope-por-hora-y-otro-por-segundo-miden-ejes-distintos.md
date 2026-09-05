---
title: un tope por hora y otro por segundo miden ejes distintos
date: 2026-09-05
source: mandadm
tags: [rate-limit, meta, api, arquitectura]
---

Un cubo de fichas que respeta el límite por segundo puede **agotar el presupuesto por hora en
minutos**, y al revés. No son el mismo límite expresado en otra unidad: son dos ejes.

Caso: Meta limita los private reply a comentarios de post/reel a **750 llamadas/hora por cuenta**
(≈0,2/s de media). Nuestro cubo iba a 2/s, que parece conservador al lado de los 100/s de la Send
API, pero permite 7.200/hora — casi diez veces el techo real. El código medía el eje equivocado y
ninguna prueba lo veía, porque todas eran ráfagas cortas.

Dos reglas que salieron de ahí:
- Si la fuente da un tope por hora o por día, **impleméntalo como presupuesto con diferido**, no lo
  conviertas a por-segundo dividiendo. La media no acota el pico ni el pico acota la media.
- Antes de fijar la constante, **comprueba de qué producto es el número**: los «2 llamadas/s» que
  arrastrábamos eran de la Conversations API de Meta, no de mensajería. Una constante debe citar su
  fuente, y la cita hay que releerla cuando el documento cambia.

Ver [[un-limite-por-ip-que-cuenta-todas-las-peticiones-anula-el-limite-por-credencial]]
