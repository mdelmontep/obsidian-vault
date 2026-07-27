---
title: documenta la divergencia con un test verde que la afirma, no con un rojo permanente
date: 2026-07-27
source: claude-code-session
tags: [testing, auditoria, arquitectura, deuda-tecnica]
---

Al auditar N implementaciones que deberían decidir igual (4 pipelines de auth en facturaia), la tentación es escribir tests de lo que *debería* pasar y dejarlos rojos "para señalar el bug". Error: un rojo permanente se normaliza en dos días, deja de leerse y encima rompe el gate de pre-commit para todo el equipo.

Alternativa (characterization testing): afirmar el comportamiento **actual aunque sea el indeseado**, con nombre y comentario explícitos:

```ts
// DIVERGENCIA CONOCIDA (auditoría 2026-07-27, hallazgo B2).
// Se afirma el comportamiento ACTUAL, no el deseado. Si este test se pone
// rojo, alguien unificó el criterio: decidir cuál gana y alinear los cuatro.
it('DIVERGE: withApiAuth acepta rol de una membresía invitada', ...)
```

La suite queda verde y la divergencia pasa de "disciplina" a artefacto ejecutable: cambiarla obliga a una decisión consciente. Funcionó en la práctica — dos tests `DIVERGE:` saltaron el mismo día porque otro agente arregló lo que documentaban.

Complemento útil: un test de arquitectura con allowlist justificada (toda `route.ts` usa un wrapper conocido o está en la lista) que falle también cuando una entrada **se pudre**. Cubre el modo de fallo que ningún test de comportamiento ve: la ruta nueva que no llama a nadie.

Ojo al reverso: [[test-verde-puede-codificar-el-bug-como-esperado]].
