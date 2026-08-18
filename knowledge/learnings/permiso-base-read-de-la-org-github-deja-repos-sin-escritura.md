---
title: permiso base read de la org de GitHub deja repos sin escritura, y el 404 de collaborators despista
date: 2026-08-18
source: claude-code-session agentesia-web
tags: [github, permisos, org, gh-cli]
---

Un `git push` a un repo de la org devolvió `403 Write access not granted` con un token
que empuja sin problema a otros repos de **la misma org**. No es el token: es que el
permiso base de la org es *read* y la escritura se concede repo a repo.

**Cómo diagnosticarlo bien** — cruzar afiliaciones, no consultar el repo:

```bash
gh api "user/repos?affiliation=collaborator&per_page=100"        # concesión explícita
gh api "user/repos?affiliation=organization_member&per_page=100" # solo membresía
```

Correlación perfecta en el caso real: 10 como colaborador (todos `push:true`), 16 solo
por membresía (todos `push:false`).

**El falso amigo:** `gh api repos/<slug>/collaborators/<user>/permission` da `404` en
los repos sin escritura. Parece «no eres colaborador», pero ese endpoint *exige* push
para invocarse: el 404 es síntoma del mismo read-only, no una causa distinta.

Ojo también con los teams vacíos: uno llamado `<repo>-maintainers` puede tener
`repos_count: 0` y permiso `pull`, o sea no otorgar nada pese al nombre.

Arreglo (lo hace un **owner**): subir *Base permissions* a Write en
`organizations/<org>/settings/member_privileges`, o añadir al usuario como colaborador
Write repo a repo. Ver [[github-free-org-privado-sin-branch-protection-ni-rulesets]].
