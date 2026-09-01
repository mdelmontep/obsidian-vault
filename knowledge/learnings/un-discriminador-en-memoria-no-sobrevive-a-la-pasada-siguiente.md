---
title: un discriminador que solo vive en memoria no sobrevive a la pasada siguiente
date: 2026-09-01
source: agency-portal
tags: [cron, batch, observabilidad, alertas]
---
Al recoger un lote de la Batch API, los jobs cuyo transcript ya se había purgado se marcaban `failed`
y se sacaban de la lista de emparejado. Sus líneas de resultado **sí venían** en la respuesta del
proveedor, así que caían en «no corresponden a ningún job» y salían por Slack como huérfanos. Se
arregló con un `Set` de ids descartados… que solo conocía lo descartado **en esa invocación**.

Un lote grande se parte en varias pasadas, y el job rendido en la primera ya no vuelve a salir en la
consulta (no está `submitted`). Su línea la sigue devolviendo el proveedor durante semanas → cada
pasada posterior lo redenunciaba.

El discriminador durable es **el motivo que ya se persistió**: se relee el `last_error` con un prefijo
constante, filtrando por el lote — **una consulta por lote, no una por línea**. Si esa lectura falla,
se dice en `failures` y se sigue con el comportamiento viejo; perder la recogida de un lote ya pagado
sería peor que el ruido.

Patrón: cualquier estado que decida «esto ya lo expliqué» entre pasadas de un cron tiene que vivir en
la fila, no en el proceso. Ver [[una-fila-de-log-por-evento-y-pasada-con-cron-de-ventana-crece-a-miles-al-dia]].
