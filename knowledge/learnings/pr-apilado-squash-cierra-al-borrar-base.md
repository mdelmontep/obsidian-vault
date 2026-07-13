---
title: PR apilado + squash-merge de su base + borrar rama → el apilado se auto-cierra y no se reabre
date: 2026-07-13
source: claude-code-session
tags: [git, github, workflow]
---
Al squash-mergear el PR base y borrar su rama, GitHub **auto-cierra** el PR apilado
(su base dejó de existir) y NO deja reabrirlo ni cambiarle la base
("Cannot change the base branch of a closed pull request"). Además el apilado arrastra
los commits ORIGINALES de la base — el squash crea un commit nuevo distinto, así que el
diff del apilado vs main muestra de más.

Fix: rebasar el apilado con `git rebase --onto origin/main <sha-base-vieja>` (replaya SOLO
sus commits propios sobre main, descartando la base ya integrada), correr gates, y abrir un
PR **nuevo** a main. Mejor aún: mergear el base y rebasar el apilado ANTES de borrar la rama
base. Cada merge a main de un repo con auto-deploy = un deploy; ojo al orden.
Ver [[audits-cross-pr-vs-per-pr]].
