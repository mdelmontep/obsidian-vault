---
title: el gate que corres aparte no incluye los trinquetes del pre-commit
date: 2026-08-14
source: claude-code-session
tags: [hooks, gate, git, harness, facturaia]
---

Commitear con `--no-verify` y correr «el gate» por separado NO es equivalente: `lint`,
`typecheck`, `build` y la suite no ejecutan los trinquetes de deuda, que viven solo en el
`pre-commit`. En FacturaIA se hizo en cuatro PR seguidos (el pre-commit tarda más que el
timeout del shell del agente) y entraron a `main` tres ficheros por encima del techo.

**Lo que multiplica el daño: un trinquete mide el ÁRBOL ENTERO** (`git ls-files`), no tu
diff. Así que a partir de ese merge el `pre-commit` abortaba **cualquier** commit del repo
—también uno que solo tocara un `.md`— y también en las sesiones paralelas. No es «dejé mi
rama sucia», es «bloqueé el repo».

Dos síntomas que despistan:
- Los trinquetes **por fichero** (inline-styles, deuda de diseño) marcan como alta lo que
  solo has MOVIDO al partir un fichero, aunque el total baje. Ahí regenerar el baseline es
  legítimo, pero **compruébalo antes con los totales del propio script**: si el global no
  sube, es movimiento; si sube, es adición disfrazada.
- El bloqueo aparece en un commit que no tiene nada que ver, así que se lee como fallo de
  lo que estabas haciendo.

**Arreglo durable**: los mismos trinquetes en el `pre-push`, que sí alcanza a un commit
hecho con `--no-verify`. Ruta absoluta (`$(git rev-parse --show-toplevel)`), o el `-f` falla
desde cualquier cwd que no sea la raíz y el bloque degrada a no-op en silencio. Ver
[[un-guard-envejece-por-partes-arregla-una-regla-y-sus-hermanas-siguen-rotas]] ·
[[gate-con-ruta-relativa-no-corre-desde-subdirectorio-y-sale-verde]]

**Variante peor (22-ago): el gate que corre ANTES del commit no valida lo que se publica.**
En el runner de tickets de FacturaIA, `gate()` medía el árbol de trabajo y el commit venía
después; entre uno y otro, `npm run deps:json` reescribía un fichero **tracked** que entraba
en el commit sin gatear, y en la ruta de merge `mig:renumerar` mutaba, commiteaba y pusheaba
otra vez **después** del gate. La comprobación de «punta remota == lo validado» comparaba
contra ese HEAD posterior: no existía ningún «HEAD validado». Regla: **el gate se mide sobre
el objeto que se publica** (commit ya hecho, `git rev-parse HEAD` guardado), no sobre el
árbol; si algo muta después, el gate certifica algo que ya no existe.
