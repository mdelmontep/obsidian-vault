---
title: comparar por tamaño no ve un artefacto servido desde otra versión
date: 2026-08-27
source: elphis-psicologia
tags: [verificacion, n8n, retell, prompts, guardianes]
---
Al emitir la v2 de un documento firmado, cinco textos generados que viven fuera del
repo (nodos de n8n, `general_prompt` de Retell) quedaron desalineados. **Dos de los
cinco pesaban exactamente lo mismo antes y después**: solo cambiaba la línea de
versión dentro del artefacto. Un guardián que comparase longitudes les habría dado
verde estando servidos desde otra versión del documento.

- Un artefacto que vive en un panel se compara **carácter por carácter** con el del
  repo, nunca por tamaño ni por «contiene la frase clave».
- Cambiar la versión suele ser un reemplazo de igual longitud (`v1 · 21 de agosto`
  → `v2 · 27 de agosto`), así que el caso peor es el más probable, no el raro.
- Corolario para el arnés: mutar el artefacto **sin cambiar su longitud** es la
  mutación que discrimina. La que añade texto la pasa cualquiera.

Ver [[un-comando-de-reparacion-corrido-desde-un-checkout-viejo-repara-a-la-version-vieja]].
