---
title: migrar un submodal a <Modal> común choca con el escape/focus que ya coordina su contenedor
date: 2026-07-14
source: claude-code-session
tags: [frontend, modales, refactor, ux]
---
Un submodal centrado que vive DENTRO de un contenedor (drawer, wizard) que ya
maneja Escape/focus a mano (p. ej. "si hay submodal abierto, Escape lo cierra a
él primero, no el drawer") NO se migra sin más al componente `Modal` común:
`Modal` añade su PROPIO listener de Escape + focus-trap + click-outside, que se
solapa con la coordinación del contenedor → doble cierre (Escape cierra submodal
Y contenedor a la vez) o focus roto al restaurar.

Antes de migrar: grep del contenedor por `Escape|keydown|focus`. Si lo coordina
a mano → o se deja el submodal como está, o se refactoriza el contenedor para
cederle ese control a `Modal` (con QA del anidamiento). Caso real FacturaIA:
`movimiento-detail-drawer/*` (conciliación) — la Fase 3 del audit Jakob los dejó
fuera por esto; reconfirmado en Block C (PR #880). Ver [[facturaia]].
