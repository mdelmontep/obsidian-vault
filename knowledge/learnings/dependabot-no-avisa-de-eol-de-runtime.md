---
title: dependabot no avisa de fin de soporte, así que el runtime se muere en producción sin que salte nada
date: 2026-07-27
source: claude-code-session
tags: [infra, docker, node, seguridad, mantenimiento]
---

Dependabot vigila versiones nuevas y CVEs. **No vigila fechas de EOL.** Un runtime que
llega a fin de soporte no rompe nada el día que llega: simplemente deja de recibir
parches. Fallo silencioso por definición → solo lo caza algo que mire el calendario.

Caso real TuFacturaIA (27-jul): producción llevaba **88 días con Node 20** (EOL 30-abr) y
**117 con Alpine 3.20** (EOL 1-abr) sin que nadie se enterara. Se descubrió revisando a
mano una PR de Dependabot, no por un aviso.

Peor: la propuesta de Dependabot llevaba a `node:24-alpine3.20`, un tag **congelado desde
2025-05-26**. Habría cambiado de Node para caer en una base igual de muerta. Los tags
`<major>-alpine<x.y>` viejos siguen existiendo en Docker Hub aunque no se actualicen — que
el tag exista no dice nada.

Reglas:
- Un pin deliberado (aquí, Alpine fijado para congelar la línea de Chromium del PDF) es lo
  que más se pudre: nadie lo revisa porque "está decidido". Ponerle fecha de revisión.
- Check mensual contra `endoflife.date/api/{nodejs,alpine}.json` (público, sin auth),
  leyendo los `FROM` del repo, no una lista a mano.
- Alojarlo FUERA de la infra que puede caerse: un check de robustez dentro de GitHub
  Actions no vale si Actions está muerto. Ver [[actions-sin-billing-hooks-locales-unico-gate]].
- Al mover de Node comprobar el tag base en Docker Hub por `last_updated`, no por existencia.
