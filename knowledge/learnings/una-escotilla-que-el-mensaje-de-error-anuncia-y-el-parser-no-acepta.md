---
title: una escotilla que el mensaje de error anuncia y el parser no acepta es peor que no tenerla
date: 2026-08-15
source: claude-code-session agh-iberica
tags: [herramientas, testing, cli, metodo]
---
`~/.claude/bin/mutate` aborta cuando todas las apariciones de la cadena caen en comentarios, y su
mensaje ofrece la salida: *«dilo con `--permitir-comentario`»*. **Esa bandera no existía en el
parser** — solo la variable de entorno `PERMITIR_COMENTARIO=1`. Al pulsarla devolvía el `uso:` y
exit 1.

**Sobrevivió porque ningún test la aseveraba.** La suite cubría los cuatro veredictos y la
restauración, pero no **la única vía que la herramienta le ofrece al usuario cuando le dice que no**.
Coste: un contrafáctico hecho a mano y dudar de un resultado que era bueno.

👉 **Todo texto de error que promete una salida es una promesa ejecutable: hay que aseverarla.** Si
un mensaje dice «usa `--x`», tiene que haber un caso que corra `--x` y compruebe que hace algo.

Y el segundo defecto, del mismo arreglo: el parser eran **dos `if` encadenados**
(`[ "$1" = --a ] && shift; [ "$1" = --b ] && shift`), así que **solo funcionaba la bandera que iba
primera** y la segunda se leía como **el nombre del fichero** — en silencio, en una herramienta que
edita ficheros. Se cierra con un `while`/`case` y una rama `-*)` que **rechaza una bandera
desconocida nombrándola** en vez de tomarla por el argumento posicional.

Contrafácticos, los dos con recuento: quitar la bandera del parser → 2 fallidos; volver a los dos
`if` → 2 fallidos, uno de ellos el del orden.

Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] ·
[[una-lista-en-un-comentario-no-protege]].
