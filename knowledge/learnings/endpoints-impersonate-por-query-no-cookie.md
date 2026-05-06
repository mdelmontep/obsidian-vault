---
title: endpoints con superadmin impersonando deben aceptar query param org_id, no fiar en cookie
date: 2026-05-06
source: claude-code-session
tags: [nextjs, auth, multi-tenant, gotcha]
---

El middleware de Next.js para impersonate (cookie `impersonate_org`) la **borra en cada navegación sin `?impersonate=` en URL**. Pattern habitual del proxy:
```ts
} else if (!impersonateOrg) {
  supabaseResponse.cookies.delete('impersonate_org')
}
```

Cookie no es fuente fiable para endpoints API. Patrón robusto:

1. Endpoint acepta `?org_id=...` query param
2. Valida con `isSuperadmin()` antes de usarlo
3. Cookie como fallback secundario (legacy)

```ts
async function effectiveOrgId(request: Request) {
  const url = new URL(request.url)
  const queryOrgId = url.searchParams.get('org_id')
  if (queryOrgId && UUID_RE.test(queryOrgId) && await isSuperadmin()) return queryOrgId
  // fallback a cookie...
  return getOrgId() // del usuario
}
```

Cliente debe construir `?org_id=` cuando `useOrg().isImpersonating === true`.

Caso real facturaia: 3 commits debugando hasta detectar `plan: "enterprise"` en consola al impersonar Starter (cookie ya borrada por middleware).
