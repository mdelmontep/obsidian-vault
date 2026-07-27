---
title: un error de validación sobre un payload que arma la propia UI no es "revisa los campos"
date: 2026-07-28
source: claude-code-session
tags: [ux, copy, errores, api, facturaia]
---

Si el cuerpo de la petición lo construye el front a partir de lo que YA validó en pantalla, un
`validation_failed` / `invalid_input` del servidor es **un fallo nuestro, no del usuario**. Decirle
"Datos inválidos. Revisa los campos." le manda a buscar un error que no está ahí y que no puede
arreglar: en TuFacturaIA (2026-07-27) un modal de conciliación se quedó con ese aviso teniendo
todos los campos válidos, y el mensaje no daba ni un hilo del que tirar.

- El diccionario de errores debe distinguir **culpa del usuario** (importe fuera de rango, motivo
  corto) de **fallo de la aplicación**: "No hemos podido enviar la operación. Vuelve a intentarlo
  y, si sigue igual, escríbenos."
- Y el test que lo cubra debe **capturar la respuesta real** y meterla en el mensaje del fallo. Sin
  eso solo se ve el texto traducido de la UI y la causa cuesta una investigación entera que puede
  acabar sin conclusión (me pasó: cerré una hipótesis de signo que luego refuté reproduciéndola).

Corolario del mismo día: **una hipótesis de causa sin reproducir no es un diagnóstico.** El fallo
"conciliar a mano un pago" lo achaqué al signo canónico de una migración; al sembrar el caso exacto
el endpoint respondió 200 y creó la asignación correcta.

Ver [[codigo-error-de-dominio-es-estado-de-producto-no-error]] · [[cada-aviso-una-sola-superficie]] · [[facturaia]]
