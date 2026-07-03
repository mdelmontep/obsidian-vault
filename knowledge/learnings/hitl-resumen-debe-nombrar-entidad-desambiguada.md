---
title: un gate HITL solo protege si el resumen nombra la entidad que un campo desambigua
date: 2026-07-03
source: claude-code-session
tags: [agentic, hitl, diseño, agh-iberica]
---

Feature: campo opcional que elige SOBRE QUÉ entidad se actúa cuando hay varias
candidatas ("la oportunidad de Dragados" con N abiertas → `opportunityTitle`). Dos
trampas que una auditoría adversaria cazó (ambas rompían la promesa):

1. **El resumen de confirmación debe renderizar ese campo.** Si la línea HITL dice
   "actualizar la oportunidad de «Dragados»" sin nombrar CUÁL, el humano confirma a
   ciegas y no puede atrapar una mala resolución. Regla: el summary muestra todo campo
   que cambie *qué entidad* se toca, no solo la acción.
2. **No hagas early-return del caso único antes de aplicar el filtro opcional.**
   `if (candidatas.length===1) return found` ANTES de filtrar por el campo → si el
   usuario nombró otra y solo hay una, se ignora el nombre y se escribe sobre la que
   no era, en silencio. El campo nombrado MANDA siempre: si no casa → clarify.

Match por inclusión normalizada tolera abreviaciones de voz ("Java"→"Perfiles Java").
Primo de [[hitl-reresolver-nombre-id-en-execute-no-inyectar-en-prepare]].
