---
title: org GitHub Free + repo privado no puede proteger ramas (ni rulesets, ni forks)
date: 2026-06-16
source: claude-code-session
tags: [github, ci, seguridad, planes]
---

En una **organización en plan Free con repos privados** NO hay forma nativa de
impedir que una identidad con Write mergee a `main`:

- **Rulesets** → solo GitHub Team/Enterprise (doc: "applies... for customers on
  GitHub Team and GitHub Enterprise plans").
- **Protección de ramas clásica** en privados → también Team+ (en Free solo repos
  públicos).
- **Fork de repo privado** → bloqueado en Free ("You cannot fork a private
  repository... using GitHub Free") → adiós al workaround "bot trabaja desde fork".
- En GitHub **no se puede separar push de merge**: ambos requieren `contents:write`.
  Un token/cuenta que puede pushear ramas puede mergear PRs.

Implicación para bots/automatización (runner que abre PRs sin mergear): en Free la
garantía "nunca merge" solo puede ser **procedural** (el script nunca llama
`gh pr merge` + deny-list). Candado **duro** = subir a GitHub Team (~4 $/usuario/mes)
y usar ruleset con bypass solo para humanos. Verificar el plan antes de prometer
el candado duro. Ver [[facturaia-resolver-con-claude]].

**Update 2026-06-16**: `AgentesIA-MAdrid` pasó a **enterprise** → ruleset `Protect main`
activo (require PR+1 approval, bypass solo team `facturaia-maintainers`); el candado del
runner ya es por infra, no solo procedural. El learning sigue válido para orgs en Free.
