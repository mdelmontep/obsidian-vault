---
title: una pista puesta detrás de un gate que el caso afectado no cumple no existe
date: 2026-08-01
source: claude-code-session
tags: [ux, producto, frontend]
---
Al añadir un aviso que explica «cómo se hace esto», comprueba **por dónde llega el usuario del caso
que lo motivó**, no solo que el texto se renderice. Un aviso correcto colocado tras una condición que
ese usuario no cumple es invisible.

Caso TuFacturaIA: el aviso «los importes están mal → elimínala y vuelve a aprobar el documento» se
puso en el editor bloqueado del listado. A ese editor solo se llega por el botón **«Completar
datos»**, que aparece si faltan datos del proveedor (`hasMissingFields`). El caso del ticket era el
contrario: proveedor bien, cantidades mal → nunca veía la pista. Se movió al **detalle de la
factura**, que es lo que el usuario abre.

- Lo cazó conducir prod, no los tests: el menú de la fila real solo ofrecía Marcar pagada, Duplicar,
  Descartar y Eliminar. Ninguna entrada al editor.
- Gatear el aviso por la acción a la que manda (aquí, que el borrado esté disponible) para no
  señalar un botón que no está.
- Ojo al smoke: impersonando como superadmin puede no resolverse el rol de la org y el modal esconde
  las acciones de escritura → verificar en una org donde el usuario sea miembro de verdad.
