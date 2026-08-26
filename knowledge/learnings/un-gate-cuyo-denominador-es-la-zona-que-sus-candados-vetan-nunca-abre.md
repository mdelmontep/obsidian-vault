---
title: un gate cuyo denominador es la zona que sus propios candados vetan nunca abre
date: 2026-08-26
source: facturaia
tags: [agentes, gates, harness, medicion, ocr]
---
El gate agéntico abre `shadow→activo` con **≥50 decisiones de zona verde resueltas y acierto ≥95%**. Medido en prod sobre el dominio `ocr`: **328 decisiones, 241 ámbar + 87 rojo, 0 verdes**. Nunca ha habido una. Con 0 verdes el acierto es `null`, `evaluarGate` devuelve `mantener / sin_volumen_medido` y el panel dice lo mismo que diría una org que empezó ayer: "aprendiendo". Contraste en el mismo sistema: `categorias` acumuló 112 verdes de 131 y su gate abrió solo.

Regla 1: en un gate de promoción, medir la **distribución de motivos de bloqueo**, no el contador. "0 de N en la zona que habilita" no es aprendizaje lento, es bloqueo estructural, y su telemetría es idéntica.

Regla 2, la que casi me costó un bug: **un histograma de motivos sobre decisiones que abarcan un cambio de código mide dos sistemas distintos.** `requiere_confirmacion_stock` salía en 296 de 328 (90%) y parecía el tapón evidente que había que quitar. Pero hasta el #2037 (21-ago) la consulta medía el PLAN en vez del inventario real, así que disparaba en 8 orgs. Filtrando `created_at >= '2026-08-21'` aparece 13 veces y **todas de la única org con inventario**, donde el veto es portante: el 98% de sus bandejas las mapea un humano antes de aprobar, así que auto-aprobar no movería stock mal, dejaría de moverlo — y la factura saldría de la bandeja sin que ese mapeo llegue a ocurrir nunca. Quitarlo habría sido meter el bug, no arreglarlo.

Antes de tratar un contador agregado como estado presente: `git log` del fichero que lo produce y volver a medir desde esa fecha. Ver [[gate-de-automatizacion-n50-al-95-no-sostiene-el-95-usa-cota-wilson]] (el mismo gate, por el lado del muestreo) y [[dos-castigos-por-el-mismo-evento-hacen-inalcanzable-el-estado-bueno]] (el candado que sí era el freno real).
