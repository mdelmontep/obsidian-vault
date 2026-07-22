---
title: Dependabot solo alerta pasivamente si no tiene dependabot.yml — no abre PRs solo
date: 2026-07-22
source: claude-code-session
tags: [github, dependabot, seguridad, ci]
---
GitHub activa el escáner pasivo de vulnerabilidades (pestaña Security →
Dependabot alerts) automáticamente en cualquier repo con lockfile — pero eso
SOLO avisa, no arregla nada. Sin un `.github/dependabot.yml` con
`version-updates` configurado, nadie abre el PR con el bump: las alertas se
acumulan hasta que alguien entra a mirar a mano (caso real: 12 vulns
acumuladas sin que nadie lo notara).

Son dos features DISTINTAS de Dependabot, fácil confundir:
- **Security alerts** (pasivo, automático, gratis, no requiere config) — solo
  notifica.
- **Version updates** (`dependabot.yml`) — el que de verdad abre PRs.

Fix: `.github/dependabot.yml` con `schedule: weekly` + `groups` (dev vs
prod-patches) para no inundar el repo de PRs sueltos por cada patch suelto.
Complementa (no sustituye) un trinquete local tipo
[[dependencias-npm-parcheadas-upstream-nunca-se-recogen-sin-npm-update-rutinario]]
que bloquee vulnerabilidades NUEVAS en pre-commit.
