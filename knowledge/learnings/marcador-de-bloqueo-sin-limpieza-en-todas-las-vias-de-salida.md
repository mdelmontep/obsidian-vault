---
title: un marcador de bloqueo necesita limpieza en TODAS las vías de reapertura
date: 2026-08-12
source: claude-code-session
tags: [diseño, state-machine, postgres]
---
Si un gate escribe un estado-marcador («bloqueada_por_tope»), hay que
enumerar TODAS las vías por las que el paso vuelve a abrirse y limpiar el
marcador en cada una — no solo en la acción de desbloqueo explícita.

Caso real (TuFacturaIA mig 670→671): la pieza bloqueada solo se restauraba
al aprobar una extensión, pero el gate también reabría por el reset natural
del ámbito (día/mes siguiente) o por subir el límite base. Por esas vías el
run se servía con la pieza aún bloqueada: el estado interno se filtraba al
consumidor externo y los marcadores quedaban huérfanos para siempre.

Patrón de arreglo: hacer del PASO la limpieza («servir es el evento de
desbloqueo», en la misma transacción), no de cada causa. Y el smoke debe
medir la vía implícita (reset temporal), no solo la explícita (aprobar).
