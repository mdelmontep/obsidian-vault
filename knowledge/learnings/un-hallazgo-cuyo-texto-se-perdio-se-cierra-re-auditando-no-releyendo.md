---
title: un hallazgo cuyo texto se perdió se cierra re-auditando su territorio, no releyendo el registro
date: 2026-08-15
source: claude-code-session
tags: [metodo, auditoria, harness, tucrmia]
---
Doce supervivientes de auditoría llevaban diez días «abiertos». Al ir a drenarlos: **ninguno tenía
enunciado escrito en ninguna parte** — existían sólo dentro de los números «14 sobreviven» y «17
confirmados». Los dos que sí tenían fichero y línea ya estaban arreglados.

Iba a ordenar «drena primero, audita después» y era al revés: **no hay nada que leer**, así que
volver a auditar ese territorio con las mismas lentes **ES** su cierre — lo que siga siendo real
reaparece con su enunciado, y lo que no reaparezca no era deuda. Contarlos cero sin eso sería el
cero por omisión que el campo existe para impedir.

**Y la causa de que se repita está en el comando, no en el descuido**: el que registra la auditoría
(`--registrar <nº> <lentes>`) **no escribe el campo `abiertos`**, así que cada entrada nueva nace en
`null` y regenera el agujero. Un registro cuyo comando de escritura omite el campo que lo hace
honesto produce «no consta» para siempre.

Fix: al registrar, rellenar ese campo **en el mismo commit**, con una nota de qué lo compone.
Regla: si un contador puede existir sin el detalle que lo justifica, acabará existiendo sin él.

Ver [[un-hallazgo-que-solo-vive-en-el-resumen-no-existe]] · [[la-tabla-existe-y-nadie-le-escribe-no-es-lo-mismo-que-no-existe]]
