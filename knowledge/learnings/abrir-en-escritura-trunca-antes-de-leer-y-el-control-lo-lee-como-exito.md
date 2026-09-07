---
title: abrir en escritura trunca antes de leer, y el control lo lee como éxito
date: 2026-09-07
source: obsidian-vault
tags: [python, scripting, agentes, verificacion, datos]
---
`open(p,'w').write(edita(open(p).read()))` **destruye el fichero**. Python evalúa
primero el objeto cuyo método llama, así que `open(p,'w')` trunca a 0 bytes; solo
después corre `open(p).read()`, que ya lee vacío. Escribe `''`. Y si la función
lanza una excepción, el fichero se queda a 0 igual, porque el truncado ya ocurrió.

Lo caro no es el borrado, es el **control**: yo comprobaba «¿ha desaparecido la
entrada?» con `grep -c "Ticket 138"` y salía `0`, que es exactamente lo que
esperaba de un borrado correcto. Un fichero vacío da 0 a **cualquier** grep, así
que la verificación confirmaba el éxito de lo que acababa de destruir. Me llevé
223 KB de histórico y 151 KB de hub por delante, y en sesión llegué a acusar a
otra sesión de haberlo pisado.

Patrón: leer entero, **cerrar**, y solo entonces escribir —
`with open(p) as f: t=f.read()` … `with open(p,'w') as f: f.write(nuevo)` — y que
el control mida **tamaño**, no ausencia: `assert len(nuevo) > 100000`. Un check de
ausencia no distingue «lo quité» de «no queda nada».
Ver [[un-conteo-con-grep-falla-en-silencio]] ·
[[un-resultado-vacio-no-es-un-hecho-hasta-que-miras-el-exit-code]].
