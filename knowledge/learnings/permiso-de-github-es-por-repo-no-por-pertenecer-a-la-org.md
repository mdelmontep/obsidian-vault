---
title: el permiso de push es por repo, no por ser miembro de la org (y gh auth status no lo dice)
date: 2026-08-01
source: claude-code-session
tags: [github, gh-cli, permisos, diagnostico]
---

"Yo he mergeado con esta cuenta" no prueba nada sobre **este** repo: el permiso
es por repositorio. Caso real 01-ago — `mdelmontep` es `member` activo de
`AgentesIA-MAdrid` y tiene push en 9 repos (agency-portal, facturaia,
agh-iberica…), pero **no** en `agentesia-web` ni en `tufacturaia-web`. El push
murió con `403 Write access to repository not granted`.

`gh auth status` NO sirve para esto — enseña cuenta y scopes del token, no el
permiso efectivo. Preguntar a la API:

```bash
gh api repos/OWNER/REPO --jq .permissions          # {pull, push, admin, maintain}
gh api "orgs/ORG/repos?per_page=100" \
  --jq '.[] | select(.permissions.push) | .name'    # dónde SÍ puedo
```

Descartar antes de culpar al permiso: SSO pendiente (cabecera `X-GitHub-SSO` en
`gh api -i`) y scope `repo` del token. Si ambos están limpios y `push:false`, es
permiso de repo de verdad.

Salida sin tocar nada: con solo `pull` se puede **forkear y abrir PR**
(`gh repo fork --remote=false` → push al fork → `gh pr create --head user:rama`).
El merge lo sigue necesitando alguien con write. Arreglo de raíz:
`gh api -X PUT repos/OWNER/REPO/collaborators/USER -f permission=push` desde una
cuenta admin. Ver [[github-free-org-privado-sin-branch-protection-ni-rulesets]] · [[agentesia]].
