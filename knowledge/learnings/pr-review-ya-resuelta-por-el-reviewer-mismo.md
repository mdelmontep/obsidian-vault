---
title: review de PR puede estar stale si el reviewer pusheó fixes propios
date: 2026-05-05
source: claude-code-session
tags: [git, github, workflow, code-review]
---

Antes de "actuar" sobre items bloqueantes de una review, hacer `git log origin/<rama-pr> -5`. El reviewer puede haber aplicado los fixes él mismo en un commit posterior y la review quedó stale.

Mapear cada item ↔ commit antes de empezar a tocar nada. Reactuar sobre items ya resueltos = revertir trabajo del reviewer y arrastrar conflictos al rebase.

Caso: PR #54 agency-portal — Borja posteó review con 4 bloqueantes, luego los aplicó él mismo en commit `58e0ef0` y cambió la base de la rama. La review siguió visible pero solo quedaba pendiente confirmar 1 cosa nuestra (PDF empresa/nombre).

Señales de que la review está stale:
- El reviewer dice en chat "lo arreglé yo en X" pero la UI de GitHub aún muestra "Changes requested"
- Hay commits del reviewer en la rama del PR posteriores al review submit
