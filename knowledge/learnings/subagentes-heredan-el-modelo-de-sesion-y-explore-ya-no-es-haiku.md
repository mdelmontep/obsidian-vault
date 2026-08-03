---
title: los subagentes heredan el modelo de la sesión y Explore ya no corre en Haiku
date: 2026-08-03
source: claude-code-session
tags: [claude-code, subagentes, coste]
---
Dos fugas de coste en el frontmatter de los subagentes:

1. **`model` tiene default `inherit`.** Todo agente propio que no lo declare corre en el modelo de
   la sesión — 12 agentes de `facturaia` y `panel-tecnocloud` estaban en Opus con effort `high`,
   incluidos los que solo construyen. Los packs externos (SEO) sí traían `model: sonnet`, así que
   el contraste no se veía.
2. **El `Explore` integrado dejó de correr en Haiku** (Claude Code v2.1.198): hereda el modelo de
   la conversación, capado a Opus. Se recupera definiendo un subagente **de usuario** con ese
   nombre — tiene prioridad sobre el built-in y conserva su `model`.

Valores: `sonnet` · `opus` · `haiku` · `fable` · ID completo · `inherit`. Y existe **`effort`**
en el frontmatter (`low`…`max`), que sobrescribe el de la sesión: la palanca para no pagar `high`
en trabajo mecánico. Ver [[claude-code-gotchas]].
