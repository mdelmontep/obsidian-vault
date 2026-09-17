---
title: un 404 no dice si la ruta está desplegada; el content-type sí
date: 2026-09-17
source: facturaia
tags: [deploy, api, nextjs, verificacion]
---

Para comprobar si una ruta de API nueva está VIVA en producción, un 404 no vale como respuesta:
significa a la vez «esa ruta no existe en el build desplegado» y «la ruta existe y el recurso que
pediste no». Son conclusiones opuestas y el código de estado es el mismo.

**Lo que discrimina es quién redactó el cuerpo.** En Next, una ruta inexistente la sirve el
framework con la página 404 (`content-type: text/html`); una ruta que existe la sirve tu handler, y
responde JSON. Medido el 17-sep-2026 contra prod, con un id inventado:

- ruta real → `404` · `application/json` · `{"error":"Not found"}` → **el handler corrió, está
  desplegada**
- ruta inventada → `404` · `text/html` · `<!DOCTYPE html>` → no existe

Dos pares en la misma llamada, uno de control, y se lee en un vistazo. Sirve igual para saber si un
deploy ya trae tu PR sin tener que crear datos ni buscar un id válido.

Corolario: no confundas esto con saber QUÉ commit corre. Si el contenedor no recibe una variable con
el SHA (`DEPLOY_COMMIT` y compañía), la propia app no lo sabe y lo reporta como `null`, así que
«¿está mi código vivo?» solo se contesta por conducta, como aquí, o por la hora de arranque.

Ver [[un-guard-nuevo-se-mide-contra-los-datos-que-ya-existen]] · [[facturaia]]
