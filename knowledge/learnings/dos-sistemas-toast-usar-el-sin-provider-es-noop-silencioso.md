---
title: con dos sistemas de toast, usar el que no tiene provider en esa área = no-op silencioso
date: 2026-07-03
source: claude-code-session
tags: [react, nextjs, frontend, gotcha, facturaia]
---

FacturaIA tiene DOS toasters: `ToastContext` (`@/components/ui/toast`, `useToast`)
montado solo en `(dashboard)` y design-system, y **sileo** (`<AdminToaster/>`)
montado en `(admin)`. `useToast` crea el contexto con default
`{ toast: () => {} }` → llamar `toast(...)` fuera de su provider **no lanza, no
muestra nada** (silencioso). Vivió así en 6 superficies admin (feedback, emails,
documents, cobros…): los toasts nunca se veían y nadie se enteró.

Regla: en `(admin)` usar `sileo.success/error(...)` (o el helper `adminToast`);
en `(dashboard)` usar `useToast`. Al escribir un toast, confirmar qué toaster
monta el layout de ESA área — no asumir un único toaster global.

Detección: `grep useToast <árbol-de-esa-área>` + revisar el `layout.tsx` del
route-group. Un contexto React con default no-op esconde el bug (compila y corre).
Relacionado: [[next-build-lock-huerfano-hace-fallar-pre-push-hook]].
