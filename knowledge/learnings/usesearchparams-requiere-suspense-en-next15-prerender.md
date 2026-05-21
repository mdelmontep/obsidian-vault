---
name: usesearchparams-requiere-suspense-en-next15-prerender
description: useSearchParams() en client component requiere Suspense para no romper prerender en Next.js 15/16
metadata:
  type: feedback
---

Next.js 15+ obliga a envolver componentes que usan `useSearchParams()` en `<Suspense>` boundary durante el build de páginas con prerender. Sin Suspense: `Error occurred prerendering page → useSearchParams() should be wrapped in a suspense boundary`.

**Why:** Caso real 2026-05-21 — page `/invitacion` con `'use client'` + `useSearchParams` para leer `?org=` rompía el build.

**How to apply:** Patrón estándar — page default export es shell con Suspense, contenido en componente interno:
```tsx
export default function Page() {
  return (
    <Suspense fallback={<div className="auth-page-loading" />}>
      <Inner />
    </Suspense>
  )
}

function Inner() {
  const params = useSearchParams()
  ...
}
```
Vale para cualquier client component que use `useSearchParams`, `useRouter().query` análogos, o hooks que dependan de query string en primer render.
