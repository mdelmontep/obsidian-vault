---
title: next.js app router layout no recibe el pathname en servidor
date: 2026-06-15
source: claude-code-session
tags: [nextjs, app-router, auth, guards]
---

Un `layout.tsx` server component NO tiene acceso al pathname actual (no hay
`usePathname` en servidor, y el layout no recibe params de ruta). Por eso no
sirve para un guard que necesita comparar "dónde estoy" contra "dónde debería
estar" (resume de wizard, role-aware redirect por step).

Patrón correcto: helper compartido `getState(userId)` + `redirectTarget(state)`,
y un guard POR PÁGINA que hace `if (target !== currentPathLiteral) redirect(target)`.
Cada página pasa su propia ruta como string literal. El layout solo hace lo
global (sesión → /login). La página índice redirige al step calculado.

Caso real: onboarding TuFacturaIA (`src/lib/onboarding/state.ts` →
`guardOnboardingStep('/onboarding/perfil')`). Evita meter al guard en el layout.
