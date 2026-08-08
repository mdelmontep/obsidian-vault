---
title: un fichero de estado sin trackear no es memoria
date: 2026-08-08
source: claude-code-session
tags: [harness, tooling, gates, git]
---

Un gate que decide leyendo su propio histórico (`docs/plan/cierres.json`: "esta
dimensión lleva 3 cierres fallando, enciéndela") necesita que ese fichero esté
EN EL REPO. Si no lo está, vive en el worktree del día, muere con él y la
función no es que falle: **no existe**, en silencio, mientras el gate sigue
dando veredictos. Pasó entero el 8-ago — se registró el cierre y el registro
desapareció al retirarse el worktree.

Dos fallos que lo tapaban, los dos vistos:
- `writeFileSync` no crea el directorio padre. Si la carpeta no está en el repo,
  el primer registro muere con un ENOENT que parece de permisos.
- Un JSON con la forma equivocada (un `[]` escrito a mano para desbloquear)
  revienta con «Cannot read properties of undefined». Plántate con un mensaje
  legible y NO pises el fichero raro.

Regla: si un script lee un fichero para decidir, `git ls-files` tiene que
encontrarlo; y su escritura necesita `mkdirSync(dirname, {recursive:true})` más
un test que corra con el directorio ausente. Ver [[facturaia]].
