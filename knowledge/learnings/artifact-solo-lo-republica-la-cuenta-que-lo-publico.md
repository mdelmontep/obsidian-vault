---
title: republicar un artifact: el listado no basta — haz WebFetch de la URL antes de publicar
date: 2026-08-07
source: claude-code-session
tags: [claude-code, artifacts]
---
Un tablero republicado desde muchas sesiones acumuló **seis URL huérfanas**. Las reglas que se fueron
probando, y por qué las dos primeras no bastaban:

1. ~~«solo lo republica la cuenta que lo publicó»~~ — describe el síntoma, no da acción.
2. `Artifact({action:'list'})` antes de republicar. Evita mintar a ciegas, **pero la pertenencia al
   listado NO ES ESTABLE**: cambia entre sesiones del mismo día, en los dos sentidos. Una URL listada
   por la mañana puede no estarlo por la tarde, y al revés.
3. **`WebFetch` de la URL antes de publicar.** Es lo que desbloquea el republicado —si no, falla con
   «this session hasn't viewed the latest version»— y además **es lo único que enseña si la copia
   publicada va por detrás del fichero local**, que es el fallo silencioso de verdad: el tablero
   mintiendo por omisión mientras nadie mira.

Regla operativa: `WebFetch` → publicar con `url:` → si falla, `list` y elegir una que aparezca.
