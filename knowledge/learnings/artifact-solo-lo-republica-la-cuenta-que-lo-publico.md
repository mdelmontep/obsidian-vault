---
title: republicar un artifact: el listado no basta — haz WebFetch de la URL antes de publicar
date: 2026-08-07
source: claude-code-session
tags: [claude-code, artifacts]
---
Un tablero republicado desde muchas sesiones acumuló **seis URL huérfanas**. Las reglas que se fueron
probando, y por qué las dos primeras no bastaban:

1. `Artifact({action:'list'})` antes de republicar. Evita mintar a ciegas, **pero la pertenencia al
   listado NO ES ESTABLE**: cambia entre sesiones del mismo día, en los dos sentidos. Una URL listada
   por la mañana puede no estarlo por la tarde, y al revés.
2. **`WebFetch` de la URL antes de publicar.** Es lo que desbloquea el republicado —si no, falla con
   «this session hasn't viewed the latest version»— y además **es lo único que enseña si la copia
   publicada va por detrás del fichero local**, que es el fallo silencioso de verdad: el tablero
   mintiendo por omisión mientras nadie mira.

**Y el 10-ago, la vuelta que remata la regla: las URL ALTERNAN, en menos de una hora.** Una se
republicó con éxito a mediodía y a la hora daba 404 no transitorio; otra que esa mañana no contestaba
—ya dada por huérfana— aceptó la republicación. Publicar desde la conversación que creó la URL
tampoco la salva.

Regla operativa, **sin memoria de lo que pasó la vez anterior**: `list` → `WebFetch` de la candidata →
publicar sobre la que conteste → mintar nueva sólo si ninguna contesta. Cada vez, entera.

**Y un `/login` a media sesión rompe TODO lo publicado antes (19-ago)**: los artifacts quedan en la
cuenta vieja (403 «not a writer» al republicar, y misma-ruta ⇒ misma URL vieja). Salida: copiar el
HTML a OTRA ruta de fichero y publicar como artifact nuevo, y actualizar los enlaces ya pegados en
PRs/Slack con un comentario — los viejos pueden no abrir para la cuenta nueva.

**27-ago: también los BORRAN, y entonces el `list` engaña por partida doble.** De dos publicados el
mismo día, uno seguía listado y el otro había desaparecido; al republicar por su ruta, el tool devolvió
`artifact-deleted` y **cortó el enlace de la sesión** («do not pass its url again»), así que ni siquiera
se puede reintentar sobre esa URL. De ahí la regla que faltaba, preventiva: **la evidencia que va a
sobrevivir a la sesión no se cita como enlace a un artifact.** El cuerpo de un PR ya mergeado y el
histórico del vault duran años; el artifact, no. El artifact es el extra visual — lo que se prueba se
escribe en texto donde queda.
