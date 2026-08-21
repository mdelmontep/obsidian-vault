---
title: un fallo transitorio guardado en una columna se lee después como veredicto
date: 2026-08-21
source: facturaia
tags: [resiliencia, diseno-datos, ocr]
---

El proveedor de tipos de cambio falló unos segundos mientras se procesaban 100 facturas en dólares. Ese "no hay tipo de cambio" de unos segundos se **escribió** en la fila (`bandeja_ingesta.tipo_cambio_fuente` a null) y todo lo que vino detrás lo leyó como respuesta definitiva: 22 documentos imposibles de aprobar durante días, con un aviso que mandaba a un botón que dice "Próximamente".

- Un null de origen transitorio y un null de "esto no aplica" son indistinguibles al leerlos. Si guardas el resultado de una llamada de red, guarda **por qué** o no lo guardes.
- El guard que consume el dato tiene que poder **reintentar en el momento de decidir**, no solo mirar la columna.
- Reintento con backoff en el cliente HTTP: necesario, no suficiente. El daño no fue el fallo, fue persistirlo.
- Un mensaje de bloqueo nunca puede señalar a una acción que la interfaz no ofrece.

Ver [[cerrar-un-ticket-automaticamente-no-es-responder-a-quien-lo-abrio]]
