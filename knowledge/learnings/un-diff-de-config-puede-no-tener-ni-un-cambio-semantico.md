---
title: un diff de config puede no tener ni un cambio semántico
date: 2026-09-24
source: facturaia
tags: [claude-code, harness, git, medicion]
---

Un hook avisó de que `~/.claude/settings.json` estaba sucio «y no lo escribió esta
sesión»: 15 líneas fuera, 15 dentro. Medido por claves en vez de por líneas, el
resultado fue **cero cambios**: mismo conjunto de claves, mismos valores. Las 15
líneas eran la propia CLI reescribiendo el fichero y moviendo el bloque
`skillOverrides` de la posición 25 a la 4. Confirmado con hash canónico
(`jq -S -c . | shasum`): idéntico en `HEAD` y en el árbol.

**Patrón:** en ficheros que reescribe una herramienta (settings, lockfiles, configs
generadas), el tamaño del diff no dice nada sobre el cambio. La pregunta «¿cambió
algo?» se contesta canonicalizando, no leyendo el diff. Y en un fichero con secretos
se mide **por rutas de clave, sin imprimir valores**.

**Ojo con el cero:** mis dos primeros `jq` daban 0 porque el patrón estaba mal
(`split(".")` se rompe con los índices de array). Un 0 se corrobora con una medida de
otra naturaleza antes de publicarlo — aquí, el hash.
Ver [[fia-gate]] · [[una-lectura-de-load1-no-acredita-una-ventana-de-medida]].
