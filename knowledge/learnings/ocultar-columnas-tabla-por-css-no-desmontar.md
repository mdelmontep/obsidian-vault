---
title: selector de columnas: ocultar por CSS (display:none), no desmontando th/td
date: 2026-07-14
source: claude-code-session
tags: [ui, frontend, tables]
---
Para un column-picker (mostrar/ocultar columnas estilo Holded/Notion), NO condicionar el render de `<th>`/`<td>` (desmontarlos). Ocúltalos con una clase CSS (`display:none`) sobre header + celdas de esa columna. Motivo: si desmontas, rompes el `colSpan` de filas agrupadas (cabeceras de mes), las medidas para sticky/scroll, y complica el orden/selección múltiple. Con `display:none` las celdas siguen en el DOM y todo lo demás (sort, bulk, totales, colSpan) sigue intacto.

Gotcha: si dos columnas comparten clase (ej. `col-date` para Fecha y Vto), no puedes ocultarlas por clase compartida → aplica la clase de oculto por-celda con un helper `hc(id)`.

Esenciales (Nº, Cliente, Total, Estado, acciones) = bloqueadas, no ocultables. Persistir el set oculto en localStorage por listado, leído en `useEffect` tras montar (no en init → hidratación SSR-safe). Scroll horizontal solo desktop (`min-width:641px`); en móvil sigue el colapso a tarjeta.
