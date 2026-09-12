---
title: filtrar las opciones de un desplegable por un predicado convierte lo inválido en «ninguno»
date: 2026-09-12
source: facturaia
tags: [react, ui, formularios, validacion, marketing]
---

`opciones = catalogo.filter(esServible)` con un `value` guardado hace meses tiene un tercer estado
que nadie modela: **el valor existe, pero ya no pasa el predicado**. Ni vacío ni elegido: por el
hueco entre los dos.

Síntomas a la vez, ninguno con pinta de bug (FacturaIA #2683, estudio de pieza): el `<Select>` pinta
el **UUID crudo** —su fallback para un `value` sin opción—, los controles dependientes desaparecen
como si no hubiera selección, y el botón de enviar **sigue activo**, encolando lo que el endpoint
niega con 409. El plan estaba bien; lo que cambió fue el catálogo.

- **El veredicto se IMPORTA del endpoint**, no se reescribe: si la ruta publica predicado y frase
  juntos, el aviso dice lo mismo que el rechazo dirá.
- **La opción muerta entra en la lista**, rotulada, para que el botón sea una frase y no un UUID; el
  envío se bloquea aparte.
- **Nunca sustituirla sola**: cambiar en silencio lo que alguien aprobó es peor que parar.

Mismo síntoma, otra causa: [[resolver-label-nombre-en-cliente-contra-endpoint-paginado-cae-al-uuid]] (allí el catálogo está incompleto por paginación; aquí, completo y la fila excluida a propósito).
