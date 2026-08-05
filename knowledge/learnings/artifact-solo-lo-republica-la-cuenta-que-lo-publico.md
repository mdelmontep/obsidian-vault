---
title: un artifact de Claude solo se puede republicar desde la cuenta que lo publicó
date: 2026-08-05
source: claude-code-session — tablero de TuCRMIA
tags: [claude-code, artifact, gotcha]
---

`Artifact` con `action: publish` y `url:` de un artifact existente falla siempre con
«could not verify the target page is not a review page (... served to you as a public
(non-member) reader ...)» si la sesión actual usa una cuenta DISTINTA de la que lo
publicó originalmente — no es un fallo transitorio de la plataforma, es que esa cuenta
no es la dueña. Confirmado con cinco reintentos idénticos, con y sin `?org=`.

No hay mecanismo para transferir la propiedad ni para que otra cuenta gane permiso de
publish sobre un artifact ajeno (compartir desde el menú da solo lectura). Salidas
reales:
1. Republicar desde la cuenta original.
2. Publicar una URL nueva desde la cuenta actual y actualizar la referencia donde se
   documente esa URL (el contenido fuente en el repo no se pierde; solo cambia el link).

Antes de asumir "fallo de la plataforma" tras 2-3 reintentos idénticos con el mismo
error, preguntar si el artifact se publicó alguna vez desde otra cuenta/sesión.
