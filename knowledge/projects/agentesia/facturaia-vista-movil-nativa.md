---
title: TuFacturaIA — vista móvil nativa (Home + tabs)
date: 2026-07-14
source: claude-code-session
tags: [facturaia, frontend, mobile, spec]
---

# Vista móvil nativa TuFacturaIA

**Estado (2026-07-14):** alcance decidido (Home + TODAS las tabs nativas), sin código. Prompt de plan para Fable 5 listo abajo → lanzar en otra sesión y revisar el plan antes de tocar código. [[facturaia]]

## Contexto rastreado
- La app HOY es solo responsive; NO hay vista móvil dedicada.
- Existió `src/components/mobile-view.tsx` (270 líneas, leía org/usuario/facturas/ingesta reales; tabs: home, fact, add, chat/IA, user/empresa). Borrado como código muerto (0 importadores) en commit **`b98e635a`**. Recuperar: `git show b98e635a^:src/components/mobile-view.tsx`.
- CSS huérfano vivo: `src/components/mobile-view.module.css` + clases `.mobile-*` / `.m-*` en `src/app/globals.css` (~línea 5132, "===== MOBILE DEVICE =====").
- CRÍTICO: el componente viejo dibujaba marco de teléfono FALSO (notch + status bar "9:41" + batería). En la vista REAL eso NO va (el SO ya pinta su barra) → solo contenido a pantalla completa + tabbar fija con safe-area.
- Arrancó como "añade la status bar al login" (mockup decorativo, artifact aprobado) → derivó a "hazla como vista móvil real".

## Prompt para Fable 5 (modo plan, no escribe código)

```
Eres el arquitecto técnico de TuFacturaIA (Next.js 15 App Router + Supabase). Tu ÚNICA
salida es un PLAN DE IMPLEMENTACIÓN por fases/PRs. NO escribas código de producción,
NO edites archivos: solo el plan. Ruta del repo: /Users/manueldelmonte/facturaia.

## Objetivo
Construir una VISTA MÓVIL NATIVA real de la app (no el marco-mockup decorativo): un home
tipo app + todas las tabs como pantallas móviles nativas, enganchada al dashboard cuando
el viewport es de móvil (~≤767px). Referencia de diseño aprobada: un mockup de home
(saludo, hero de importe, KPIs, próximos vencimientos, tarjeta de ingesta, tabbar inferior
con botón + central). Debe leer datos reales de Supabase.

## Estado actual (verifícalo, no lo asumas)
- La app HOY es solo responsive; NO existe vista móvil dedicada.
- Existió `src/components/mobile-view.tsx` (270 líneas, leía org/usuario/facturas/ingesta
  reales, tabs: home, fact, add, chat/IA, user/empresa). Se borró como código muerto
  (0 importadores) en el commit b98e635a. Recupéralo con:
  `git show b98e635a^:src/components/mobile-view.tsx`
- Su CSS quedó huérfano: `src/components/mobile-view.module.css` y las clases `.mobile-*`
  / `.m-*` en `src/app/globals.css` (busca "===== MOBILE DEVICE =====", ~línea 5132).
- CRÍTICO: el componente viejo dibujaba un marco de teléfono FALSO (notch + status bar
  "9:41" + batería). En la vista REAL eso NO va (el SO ya pinta su barra). Hay que
  renderizar solo el CONTENIDO a pantalla completa + tabbar fija con safe-area
  (`env(safe-area-inset-bottom)`).

## Contexto del repo que DEBES leer antes de planificar
- `CLAUDE.md` y `AGENTS.md` (inviolables del proyecto).
- `docs/architecture/gotchas.md` (§Auth, §OCR, §Notificaciones), `ARCHITECTURE.md`,
  `docs/architecture/dependency-map.md`.
- Estructura de rutas: `src/app/(dashboard)/` (dashboard, emitidas, recibidas, clientes,
  informes, cashflow, ingesta, generar, agentes, settings, ...). Layout:
  `src/app/(dashboard)/layout.tsx` → `layout-server.tsx`.
- `src/app/(dashboard)/page.tsx` (home actual desktop), `src/components/layout/` (sidebar,
  topbar, icon.tsx), `src/lib/types.ts` (Factura, EstadoEmitida/Recibida),
  `src/components/ui/estado-pill.tsx`, `src/lib/format.ts`.
- `src/app/tokens.css` (variables de tema light/dark).

## Inviolables que el plan debe respetar (del CLAUDE.md)
- Type-safety E2E: strict, 0 `any`, cliente Supabase tipado, parse-don't-validate en bordes.
- Iconos SOLO `<Icon name>` de `src/components/layout/icon.tsx`; NUNCA emojis Unicode.
- Colores/tipografía por tokens: `--brand #3D7BF5`, Filson Soft (display), Switzer (UI),
  JetBrains Mono (cifras tabulares).
- `EstadoPill` debe cubrir cada estado; acciones por estado según reglas.
- Feature gating vía `useFeatures()`, nunca RPC directa en componente.
- Endpoints con sesión → `withApiAuth`; nada de gate global de teléfono.
- QA en localhost (claro+oscuro) + artifact antes/después obligatorio; PR, nunca push
  directo a main.
- Migraciones NNN_ secuenciales (solo si hiciera falta BD, probablemente no).

## Decisiones de arquitectura que el plan DEBE resolver (con trade-offs, no una sola opción)
1. Modelo de navegación: ¿un client-component SPA con estado de tab interno (como el viejo)
   VS. rutas reales con un layout móvil compartido (deep-link, back nativo, SSR)?
   Recomienda una y justifica.
2. Mecanismo de gating móvil/desktop: CSS puro (render ambos, ocultar por media query) VS.
   hook `useIsMobile` (riesgo de hydration mismatch SSR) VS. detección server-side por
   user-agent. Analiza SSR/hydration y flash.
3. Dónde se engancha: `(dashboard)/page.tsx`, el layout del grupo, o un layout nuevo.
4. Reutilización de datos: ¿fetch propio en el cliente (como el viejo) VS. compartir loaders
   con las páginas desktop existentes? Evitar duplicar queries y descuadres (recuerda:
   agregados sobre facturas filtran borradores/anuladas).
5. Mapeo de las 5 tabs a secciones reales existentes y qué se rediseña nativo vs. qué
   reusa páginas responsive actuales.

## Formato de salida del plan
1. Resumen de la decisión de arquitectura (las 5 de arriba resueltas, 1-2 líneas c/u).
2. Fases → PRs independientes y mergeables. Empieza SIEMPRE por PR1 = fundación
   (gating + shell + tabbar + Home nativo con datos reales), luego una tab nativa por PR.
   Para cada PR: objetivo, archivos a crear/editar (rutas absolutas), riesgos, y criterio
   de "hecho" (incluida QA claro/oscuro + artifact).
3. Lista de archivos huérfanos a reutilizar/reescribir/borrar.
4. Riesgos transversales (hydration, safe-area iOS, teclado/inputs 16px anti-zoom iOS,
   tabbar tapando contenido, accesibilidad/focus, performance de fetch en cliente).
5. Preguntas abiertas para Manuel antes de arrancar PR1.

Explora el repo con grep/read para fundamentar cada afirmación; marca lo que no puedas
verificar como suposición explícita. Sé quirúrgico: nada de features no pedidas.
```
