---
title: el workaround que le funcionó al cliente no es la explicación de la causa
date: 2026-07-30
source: claude-code-session
tags: [soporte, debug, facturaia, stock]
---

"Ya está solucionado, lo guardé en borrador y lo volví a emitir" cierra el ticket
en la cabeza del cliente, no la investigación. Antes de darlo por resuelto, explicar
POR QUÉ funcionó — el mecanismo puede ser otro bug.

Caso TuFacturaIA (ticket #117, Chivite): emisión bloqueada por falta de stock en la
partida. Guardar y reabrir el borrador "lo arregló". No entró género: cero
movimientos de entrada ese día en la org. Lo que pasó es que al reabrir, el editor
rehace el autopick FEFO y REASIGNA la partida de la línea. O sea, el workaround
cambiaba datos por debajo sin decirlo.

Cómo comprobarlo barato: en la tabla de movimientos de la magnitud implicada, buscar
si hubo alguna entrada entre el fallo y el éxito. Si no la hubo, lo que cambió es el
estado del documento, y ahí está la explicación real.

Corolario: el usuario que dice "salí de la sesión y volví a entrar y sigue igual"
está dando un dato de diagnóstico — la causa es un dato, no la sesión.
