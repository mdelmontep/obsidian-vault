---
title: un guard envejece por partes — arreglas una regla y sus hermanas siguen con el mismo defecto
date: 2026-08-12
source: claude-code-session agh-iberica
tags: [claude-code, hooks, harness, auditoria, metodo]
---
`git-guard.sh` tenía cuatro reglas. La **1** aprendió el 8-ago a partir el comando por segmentos
(`;`, `&&`, `||`, `|`) *«para no cazar un `--hard` que pertenezca a otro comando del compuesto»* —
con su comentario y su caso. Las reglas **2, 5 y 6 se quedaron con la forma vieja**, y el 12-ago
mordieron las tres:

- **2** (force push): pedía «hay un push» Y «hay un `--force`» en el comando entero, sin exigir que
  fueran el mismo → `worktree remove --force x; push --delete y` bloqueaba. Falla **cerrado**.
- **5**: el filtro era un glob de subcadena, así que `checkout` dentro de un **nombre de fichero**
  lo activaba y el segmento entero pasaba por lista de rutas. Falla **cerrado**.
- **6**: `tail -1` sobre el comando entero cogía el último token, no la ruta → `worktree remove
  --force <sucio> && echo listo` **no bloqueaba**. Falla **ABIERTO**, y ésta no me había mordido
  nunca: salió de auditar las hermanas, no de un síntoma.

**Why:** el arreglo de una regla no se propaga a las de al lado, y el comentario que lo explica se
lee como historia del fichero, no como deuda pendiente. Cuando un guard te dé un falso positivo,
**el bug no es el caso: es la forma de matchear**, y hay que buscarla en las otras reglas.

**How to apply:** al tocar una regla de un guard, pasa su nueva forma por las hermanas y **mide cada
una** (invocar el hook con el JSON a mano cuesta segundos). Y al arreglar, **una mutación por pieza**:
aquí `head -1` ya cubría los dos casos de la regla 6, así que la segmentación quedaba sin medir —
en vez de declararla equivalente, el caso que la discrimina (dos `remove` en un compuesto, el sucio
delante, donde el `sed` greedy salta al último).

⚠️ **Y una copia VIEJA de un guard es peor que no tenerlo.** El mismo día: `.claude/hooks/git-guard.sh`
del repo era un subconjunto de hace semanas del global —que ya corre ahí igualmente—, con `git reset
-q --hard` **pasando** por comparar una subcadena literal. No añade protección, sí falsos positivos
propios, y sobre todo **confianza falsa**: quien lee ese fichero cree que el repo prohíbe algo que no
prohíbe. Un guard duplicado se sincroniza o se borra; dejarlo divergir es lo peor de las dos.

**No es solo de hooks** (Elphis, 17-ago): el `invalid input syntax for type bigint: "null"` se arregló el
12-ago con `NULLIF` en `Persist ids conv_state` y **su gemelo `Upsert conv_state` se quedó como estaba**, con
`onError: continueRegularOutput`. Resultado: `conversation_state` llevaba **semanas sin escribir una sola fila**
y el bot iba sin memoria, sin un solo error visible. El síntoma que lo destapó no era de base de datos («el bot
vuelve a preguntar el motivo»), así que nadie miró ahí. Dos queries que comparten forma son hermanas aunque
estén en workflows distintos: al arreglar una, **grep de la otra**.

Hermana: [[dokploy-secret-guard-falso-positivo-variable-local-con-nombre-sensible]] — el otro modo,
un guard que invierte su incentivo y te empuja justo a la conducta peligrosa.
