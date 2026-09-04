---
title: un gate cuyo fuente es copia de lo desplegado caduca, y nadie se entera de que está en rojo
date: 2026-09-04
source: centro-elphis
tags: [n8n, testing, metodo, harness]
---

El código de un Code node vive en el servidor de n8n, no en git. Si el gate lo prueba desde una
**copia local** (`normalizar.js`, `preparar.js` junto al test), esa copia caduca en cuanto alguien
edita por API o por la UI — y el gate deja de medir lo que corre.

- Elphis, 4-sep: al sincronizar las copias con lo desplegado, el gate del 15-ago salió con **18
  fallos**. Llevaba en rojo desde el 27-ago, la fecha del cambio que rompió el circuito de avisos: se
  editó el nodo y no se corrió. Nadie ve un gate que nadie ejecuta.
- Orden correcto al tocar un workflow ya desplegado: **GET del workflow → volcar los `jsCode` a los
  ficheros del gate → correr en verde → editar → correr → PUT**. Si el primer paso sale rojo, el bug
  ya estaba ahí y no es tuyo.
- El caso de test también caduca: el de Elphis usaba `message = '<codigo>'` sin detalle, forma que ya
  no existía en producción. **Fijar el payload real capturado de una ejecución**, no uno plausible.
- Sin repo git en la carpeta, `~/.claude/bin/mutate` se niega («esto no es un repo git»): el arnés se
  monta a mano con copia + restauración, y conviene endurecer los `check` contra `null` o el mutante
  revienta el test y el recuento miente. Ver [[n8n-parte-el-mensaje-de-error-en-el-primer-dos-puntos]].
