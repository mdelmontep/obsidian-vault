---
title: openapi-fetch ternary rompe narrowing — r.response.status aparece como `never`
date: 2026-05-01
source: claude-code-session
tags: [typescript, openapi-fetch, narrowing, sdk]
---

`openapi-fetch` (cliente generado por openapi-typescript) tipa el resultado por path. Cuando la llamada se elige con un ternario, TS no narrowea la unión de tipos pesados:

```ts
const r = isFactura
  ? await fia.GET('/facturas/{id}/pdf', {...})
  : await fia.GET('/presupuestos/{id}/pdf', {...})
// r.response.status → never
// r.data → never
```

Fix: split en if-else con dos llamadas literales. Cada rama narrowea limpio:

```ts
if (isFactura) {
  const r = await fia.GET('/facturas/{id}/pdf', {...})
  return NextResponse.redirect(r.data.url, 302)
} else {
  const r = await fia.GET('/presupuestos/{id}/pdf', {...})
  return NextResponse.redirect(r.data.url, 302)
}
```

Aplica a cualquier SDK con tipos genéricos profundos cuando la operación es condicional.
