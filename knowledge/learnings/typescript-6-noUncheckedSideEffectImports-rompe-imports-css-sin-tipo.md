---
title: typescript 6 activa noUncheckedSideEffectImports por defecto y rompe imports css sin tipo
date: 2026-07-08
source: claude-code-session
tags: [typescript, vite, migration]
---

Al subir TypeScript a la major 6, `noUncheckedSideEffectImports` pasa a **true por defecto**. Cualquier `import "./styles.css"` (side-effect, sin binding) que antes compilaba sin más empieza a fallar si no hay una declaración de tipo para `*.css`.

Fix en origen (no relajar el flag): añadir `declare module "*.css" {}` en el `vite-env.d.ts` del proyecto (mismo patrón que trae `vite/client` para otras extensiones). No hace falta tocar `tsconfig`.

Aplica a cualquier proyecto Vite+React que migre a TS 6 con imports CSS sueltos.
