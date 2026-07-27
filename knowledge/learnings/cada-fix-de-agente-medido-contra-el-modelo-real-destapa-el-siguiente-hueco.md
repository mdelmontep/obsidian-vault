---
title: cada fix de un agente, medido contra el modelo real después de mergear, destapa el siguiente hueco de sí mismo
date: 2026-07-27
source: claude-code-session
tags: [agentes-conversacionales, verificacion, testing, evals, methodology]
---
En un lote de 8 fixes sobre una llamada real (agh-iberica), **tres huecos nuevos aparecieron solo al ejecutar la conversación con el modelo real DESPUÉS de mergear** — ninguno lo veían los tests deterministas, todos verdes:

1. Arreglado el modo `last` de un read → el modo `detail` **del mismo read** seguía con el mismo fallo (narraba una fecha futura como pasada). Un fix por rama del `switch`, no por conducta.
2. Tapado que el ruido de ASR se colara como **alta de cliente** → el modelo lo metió como **cuerpo de una nota**. La guarda era específica de un `kind`; **el ruido busca cualquier hueco donde caber**.
3. El propio assert del arnés estaba mal: prohibía mencionar el fragmento de ruido, cuando la conducta correcta era **preguntar por él nombrándolo** (callarlo = descartar datos en silencio).

**Cómo trabajar con esto:**
- Un fix de conducta no está verificado hasta ejecutar la conversación completa con el modelo real **sobre el código ya mergeado**. Los tests deterministas prueban el camino que imaginaste; el modelo elige otro.
- Al tapar una vía por la que un dato basura se convierte en escritura, **enumera las demás vías** (todos los `kind` que aceptan texto libre) en el mismo cambio, o la siguiente pasada te lo encuentra.
- Cuando un turno sigue rojo tras el fix, la primera hipótesis debe ser **el assert**, no el código: el arnés se escribió antes de saber cuál era la conducta correcta.
- Escala real medida: 35/43 checks → 38/45 tras tres rondas; los rojos que quedaron eran huecos de prompt ya declarados, no sorpresas.

Ver [[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]] · [[escribir-en-una-fuente-y-leer-de-otra-hace-que-el-agente-se-contradiga]]
