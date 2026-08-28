---
title: retirar el worktree que le diste a un gate en marcha lo deja auditando otro checkout
date: 2026-08-19
source: claude-code-session facturaia
tags: [claude-code, worktrees, auditoria, harness]
---

Un gate multiagente al que se le pasa la ruta del worktree («el repo está en
`/Users/…/wt-X`») no falla si ese worktree desaparece a mitad: los agentes buscan el fichero por
su ruta relativa y **acaban leyéndolo en otro checkout del mismo repo**. El informe sale con
`ruta:línea` y con pinta de verificado.

Caso real: se mergeó el PR, se retiró el worktree como limpieza y el gate seguía corriendo. Su
síntesis dijo «commit auditado 785134406, en `/Users/…/wt-fb01-gclid`» — un worktree de OTRA
sesión. Los hallazgos eran correctos **por suerte**: esa rama acababa de nacer de `main` y estaba
en el mismo sha. Con un checkout dos merges por detrás, el gate habría auditado código que ya no
existe y sus «hallazgos verificados» serían fantasmas.

Reglas:
- La limpieza del worktree va **después** de que el gate termine, no en la misma tanda que el merge.
- En el informe, comprobar que la ruta que dice haber leído es la que le diste: si no coincide,
  `git -C <esa ruta> log -1` y verificar que el sha es el auditado antes de creerse nada.
- Y mejor: darle el **sha** además de la ruta, para que pueda comprobarlo él.

Es la misma clase de fallo que [[una-suite-en-verde-no-prueba-el-camino-real]]: el instrumento
contesta, pero no sobre lo que crees.

**Y la otra mitad, medida el 28-ago-2026 (tucrmia): el silencio no dice si el agente está vivo.**
Un subagente con 50 min sin escribir en su registro y sin contestar a `SendMessage` puede estar
DENTRO de una corrida larga (`npm run gate`, ~5 min y mucho más bajo carga): no escribe nada y no
atiende mensajes hasta su siguiente turno de herramienta. Lo di por muerto, le retiré el worktree
con `--force` y su gate murió con `GATE_EC=7` / `getcwd: cannot access parent directories`.
- Mirar si su **proceso** corre, no cuándo escribió por última vez.
- **`locked` en `git worktree list` es el aviso escrito**; `--force` sobre él es saltárselo.
- Si hay que rescatar su trabajo, **commitear en su rama es seguro y reversible**; retirar el
  directorio no lo es. Nada se perdió sólo porque el rescate cayó después de su última escritura.
