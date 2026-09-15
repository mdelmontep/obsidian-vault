---
title: un error que nombra exactamente lo que falta no es una caída: relee el esquema del parámetro
date: 2026-09-15
source: agh-iberica
tags: [diagnostico, mcp, herramientas, sesgo]
---
> ⚠️ El nombre de este fichero es de una primera versión cuya premisa era FALSA («el canal
> se cayó»). Se conserva el nombre porque ya estaba commiteado y citado; lo que vale es el
> título de arriba.

`slack_send_message` devolvió `no_text` seis veces. Bisecté el CONTENIDO —longitud,
mrkdwn, enlaces, comillas, no-ASCII, hasta un texto de 21 caracteres— concluí «la
herramienta está caída», lo escribí como learning y mandé un reporte de bug. El
parámetro obligatorio se llama **`message`**; yo pasaba `text`. El campo llegaba vacío y
`no_text` decía literalmente eso. Otra sesión lo resolvió al primer intento.

Dos señales que ignoré, y son las que valen:
1. **El nombre del error describía la causa.** Antes de bisecar el contenido, releer el
   esquema del parámetro (`ToolSearch select:<tool>` cuesta una llamada).
2. **«Funcionaba antes en esta misma sesión»** era premisa falsa: los envíos buenos
   llevaban otro formato. Sostuvo todo el diagnóstico sin comprobarse.

Regla: con un error de forma (`no_X`, `missing_Y`, `invalid_Z`), el primer contrafáctico
es el ESQUEMA, no el dato. Bisecar el contenido solo prueba cosas sobre el contenido.

Ver [[un-instrumento-que-devuelve-cero-para-todo-no-es-un-dato]].
