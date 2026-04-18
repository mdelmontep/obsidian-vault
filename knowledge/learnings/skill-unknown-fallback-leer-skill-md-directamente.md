---
title: skill "unknown" → leer SKILL.md directamente con Read
date: 2026-04-16
source: claude-code-session
tags: [claude-code, skills, workaround]
---

Cuando la Skill tool de Claude Code devuelve "Unknown skill" pero el skill existe en disco, leer `~/.claude/skills/<nombre>/skills/<nombre>/SKILL.md` con la Read tool. El contenido carga igual y puede seguirse como guía.

Útil para skills instalados manualmente (clonados, copiados) que no aparecen registrados en el runtime. También sirve para inspeccionar el contenido de un skill antes de invocarlo.

Ejemplo real: `bencium-innovative-ux-designer` estaba en disco pero `Skill` tool no lo encontraba. Read directo del SKILL.md funcionó perfectamente.
