---
title: una cita fichero:línea caduca en silencio, así que el gate que la vigila debe saber corregirla
date: 2026-08-18
source: obsidian-vault
tags: [documentacion, gates, metodo, mantenimiento]
---

Una referencia `fichero:línea` en documentación es correcta el día que se escribe y **falsa en cuanto alguien edita el fichero por encima** — sin que nada falle, sin que nadie lo note, y siguiendo pareciendo precisa.

**Medido.** Las citas de una lección caducaron **tres veces en el mismo día**, y ninguna de las tres por tocar la lección: quitar un import huérfano, añadir un bloque, limpiar código muerto. Nadie relacionaría esas ediciones con un documento.

**Fix en dos partes, y la segunda es la que importa:**
1. Un gate que, por cada cita, guarda **el fragmento de texto esperado** y comprueba que sigue en esa línea (±3). Comprobar solo que el fichero existe no prueba nada.
2. Que el gate sepa **arreglarlas** (`--corregir`) y actualice también **su propia lista de citas**. Un mantenimiento manual que hay que repetir cada vez que se toca el código es la garantía de que un día no se hará.

**Alternativa si no hay gate**: citar por símbolo (`función X en fichero.ts`), que sobrevive a los desplazamientos. Menos preciso, pero no miente.

Ver [[el-instrumento-devuelve-cero-sin-decir-que-no-ha-medido]] · [[una-lista-en-un-comentario-no-protege]]
