---
title: TuFacturaIA — vista móvil, segunda ola (glass + push + offline + gestos)
date: 2026-07-15
source: claude-code-session
tags: [facturaia, frontend, mobile, pwa, spec]
---

# Vista móvil TuFacturaIA — segunda ola

**Estado (2026-07-16): SEGUNDA OLA COMPLETA EN PROD.** Primera ola (PR0-PR6) + segunda ola (8 PRs: #907/#910/#911/#916/#917/#921 + #928/#929/#930) mergeadas. Único pendiente: calibración de blur (bloqueada, esperando fotos de Manu) y confirmación de deploy VAPID. Spec original (prompt de ejecución) queda abajo como referencia histórica. [[facturaia]]

## Progreso (2026-07-15 — 5 PRs MERGEADOS a main, deploy auto en Dokploy)

- **#907 PR-A** glass chrome móvil + menú "Más" flotante (radio 28) + **fondo con halos brand** para dar cuerpo al glass (2 feedbacks de Manuel aplicados). QA completa claro/oscuro + artifact.
- **#910 PR-B** PWA: service worker offline (navegación network-first→offline.html, datos API nunca cacheados, escrituras no interceptadas) + migración `462_push_subscriptions` + endpoint `/api/push/subscribe` + `PwaManager`. **Envío push = follow-up (bloqueado por VAPID de Manuel).** Fix en QA: middleware redirigía `/sw.js`+`/offline.html` a /login (307) → añadidos al matcher.
- **#911 PR-D** botón "Recordar cobro" 1 toque en el home (reusa `/api/cobros/send-now`). **Parte 2 (detalle móvil con barra de acciones) pendiente** (inviolables acciones-por-estado).
- **#916 PR-F** badges menú "Más" (`useSidebarCounts`) + reset de overlays al cruzar breakpoint + fix real de focus-trap Shift+Tab (más-menu/create-sheet/notifications-drawer).
- **#917 PR-E** escaneo multipágina (combina imágenes en 1 PDF client-side con pdf-lib → reusa `/api/upload`, sin cambios de backend) + aviso de calidad (varianza Laplaciano). **Manual de usuario pendiente** + calibrar umbral blur.

**Diferido a sesión aparte:** PR-C (gestos swipe+undo, pull-to-refresh, scroll infinito — toca `useFacturasData`/`usePaginationParams` compartido + mutaciones) y auditoría de rendimiento (LCP móvil throttled).

**Merge (2026-07-15):** los 5 + fix #921 (renumerada `462_push_subscriptions`→**463**, chocaba con `462_holded` de #908). Merges limpios (hunks disjuntos), deploy auto.

**Los 5 puntos — CERRADOS 2026-07-16 (sesión /loop con agentes paralelos):**
1. ✅ **Migración 463 a prod** — aplicada, RLS+4 políticas verificadas por psql directo.
2. ✅ **VAPID + push server-side** (PR #929) — Manu puso las claves en Dokploy. `sendPushForNotification` (`src/lib/push/send.ts`) enganchado a `notify()` solo warning|critical, gateado en VAPID, respeta `shouldDeliver`+quiet hours, poda 404/410. Gap real cerrado en el mismo PR: `/api/push/subscribe` no activaba `channel_push` → nadie habría recibido nada. **Pendiente**: confirmar `compose.deploy` (rebuild) para que `NEXT_PUBLIC_VAPID_PUBLIC_KEY` se hornee en el bundle cliente + smoke de envío real en iOS instalado.
3. ⚠️ **Manual de usuario** (PR #928) mergeado. **Blur calibration BLOQUEADA** — sin fotos reales en el repo; esperando 2-3 de Manu (nítida+borrosa) para tocar `BLUR_VARIANCE_THRESHOLD` en `image-quality.ts`.
4. ✅ **Smokes prod con Artifact** — recorrido completo iPhone 14 claro/oscuro contra FacturaIA Sandbox. Descartado un falso positivo (skeleton de Facturas por contención de CPU multi-sesión, no bug — ver [[cpu-contencion-multisesion-falso-positivo-ui-atascada]]). Hallazgo preexistente fuera de alcance: [[theme-en-localstorage-sin-cookie-espejo-causa-hydration-mismatch]].
5. ✅ **PR-C** (#930) gestos — swipe+undo (2 patrones: commit-inmediato+revert-endpoint en facturas, pending-commit 5s en ingesta), pull-to-refresh, scroll infinito bifurcado sin tocar desktop. Revisado línea por línea antes de mergear. **Auditoría de rendimiento**: Lighthouse+throttling contra build de producción — LCP 5.1s/FCP 3.7s/CLS 0/TBT 10ms/score 0.72 (medido sobre `/login` por bloqueo de auth en servidor standalone); sin margen claro, no se tocó código.

Gotcha de QA de esta sesión: [[agent-browser-set-device-antes-de-open-para-ssr-mobile]].

Gotcha CSS de la sesión: [[turbopack-lightningcss-dropea-backdrop-filter-sin-prefijo]]. Failure modes de merge/worktree: [[claude-code-agentes-worktree-failure-modes]] (G recrear worktree corrupto, H stash compartido).

## Hallazgo que motiva la fase 1 (glass)
El chrome móvil de la primera ola es SÓLIDO, no glass: `.csheet`/`.mmenu`/`.ming`/`.mfac__card` = 0 reglas de `backdrop-filter`, mientras la app tiene sistema glass real (`.glass-sheen` globals.css ~37, patrón `notifications-drawer`). La fase 1 unifica a glass; cada pieza nueva nace glass.

## Prompt (pegar en la siguiente sesión, Opus)

```
Continúa la vista móvil nativa de TuFacturaIA. PR0-PR6 YA ESTÁN EN PROD (home nativo,
shell+PWA, sheet "+", tab Facturas, tab Documentos, menú "Más"). Ahora toca la SEGUNDA
OLA: glassmorphism consistente + notificaciones push + offline PWA + gestos táctiles +
home accionable + escaneo multi-página + pulido. HACERLO TODO, sin atajos, profesional,
funcional, con la estética GLASSMORPHISM como inviolable visual.

## Inviolable nº1: GLASSMORPHISM CONSISTENTE (leer y respetar)
La app tiene un sistema glass real en globals.css: `.glass-sheen` (línea ~37), `.glass`,
`.glass-strong`, `.glass-panel` (backdrop-filter + destello), y el patrón de referencia
es `notifications-drawer` (usa `glass-sheen`). PERO los componentes móviles que ya
construimos son SUPERFICIES SÓLIDAS (`--bg-elev`), NO glass: `.csheet` (sheet +),
`.mmenu` (menú Más), `.ming` (ingesta), `.mfac__card` (facturas) → 0 reglas de
backdrop-filter. La PRIMERA fase migra todo eso a glass real, y CADA pieza nueva NACE
glass. Respeta los fallbacks ya existentes (reduced-transparency / Android, globals.css
~14438) y los tokens (nunca hardcodear color). QA SIEMPRE con el skin glass activo,
claro Y oscuro. Si una superficie no se ve glass (blur + translucidez + sheen), no está
terminada.

## Fuentes de verdad (léelas primero)
- docs/architecture/gotchas.md (§Storage, §OCR, §Notificaciones, §Auth, §Crons)
- docs/architecture/ARCHITECTURE.md + dependency-map.md
- El sistema glass en src/app/globals.css (`.glass-sheen`/`.glass`/fallbacks ~14438) y
  notifications-drawer.tsx como patrón glass de referencia.
- Componentes móviles actuales: src/components/layout/mobile/{create-sheet,more-menu,
  mobile-tabbar,mobile-header}.tsx, src/components/facturas/mobile-facturas-list.tsx,
  src/components/ingesta/mobile-ingesta.tsx, src/components/dashboard/mobile-home.tsx.
- Notificaciones existentes (use-notifications, notify()) para enganchar el push.
- Endpoint de recordatorio de cobro existente (para la acción rápida del home).

## Alcance — PRs (independientes salvo dependencia marcada)
- **PR-A · Coherencia glass del chrome móvil (BASE, primero).** Migrar csheet, mmenu,
  ming, mfac cards, y revisar las tarjetas del home a glass real (backdrop-filter +
  glass-sheen + fallbacks). Solo CSS/classNames, cero cambio funcional. Fija el lenguaje
  visual para todo lo demás. QA glass claro/oscuro + artifact antes/después.
- **PR-B · Service Worker + Offline + Push** (plataforma; VAPID = dependencia de Manuel).
  · SW profesional (estrategia tipo fintech): precache del app-shell (cache-first),
    runtime network-first para datos con fallback a caché SOLO con marca visible de
    antigüedad ("datos de hace X"), página offline, NUNCA mostrar cifras financieras
    obsoletas sin ese aviso; acciones de escritura NO offline salvo cola/background-sync
    explícita.
  · Push: migración tabla `push_subscriptions` (RLS + políticas misma migración, NNN
    secuencial), endpoint de suscripción con withApiAuth, disparo web-push desde el
    server enganchado a las notificaciones que YA existen (vencidas, cobros, fiscal),
    UI de permiso no intrusiva. VAPID keys las genera Manuel (ver Dependencias).
- **PR-C · Gestos y navegación táctil.** Swipe en tarjetas (factura→marcar cobrada;
  documento ingesta→aprobar/descartar) con undo; pull-to-refresh; scroll infinito /
  "cargar más" sustituyendo la PaginationBar de escritorio en Facturas y Documentos.
  Respetar prefers-reduced-motion.
- **PR-D · Home accionable + detalle móvil.** Botón "Recordar cobro" de 1 toque en cada
  vencimiento del home (reusa el endpoint de recordatorio); rediseño del detalle de
  factura en móvil con barra de acciones fija inferior (cobrar/anular/enviar) al alcance
  del pulgar, en vez del modal de escritorio reutilizado.
- **PR-E · Escaneo multi-página + calidad de imagen.** Varias fotos → un solo documento;
  aviso de calidad ("foto borrosa / recorta") antes de gastar cuota OCR. PDFs vía
  fileUrl(); subida como ingesta-view (POST /api/upload).
- **PR-F · Badges menú "Más" + pulido.** Badges de conteo en los tiles (reusa
  use-sidebar-counts, p.ej. "Documentos · N por revisar"); reset de estado sheet/menú al
  cruzar el breakpoint; focus-trap que capture Shift+Tab desde el contenedor (afecta a
  todos los drawers, arreglar en el patrón).
- **Auditoría transversal · rendimiento.** Medir LCP/bundle del home móvil en 4G
  emulada + device modesto (no solo emulador rápido); reportar y, si hay margen claro,
  optimizar (dynamic imports, peso de imágenes). NO microoptimizar a ciegas.

Dependencias de orden: PR-A primero (base visual). Tras merge de PR-A, PR-C/D/E/F
paralelizables. PR-B independiente (toca SW/backend/DB), puede ir en paralelo.

## Setup
Worktree LIMPIO desde origin/main por PR (symlinka node_modules + .env.local + .env.test
del repo raíz). PR-C/D/E/F/B en ramas propias desde origin/main, PR directo a main. Máx
2-3 worktrees a la vez; todos tocan la sección móvil de globals.css → conflictos menores
esperables, merge rápido y resolver rama por rama (globals.css lo edita SOLO el main loop
o un único agente por vez).

## Protocolo multi-agente (idéntico al de PR0-PR6)
- Delegación por modelo: Explore→haiku (mapeos: sistema glass, endpoints notif/recordatorio,
  use-facturas-data). Piezas UI acotadas (glass migration, gestos, cards, badges, detalle)
  →facturaia-frontend (sonnet). Endpoint push/suscripción→facturaia-backend (sonnet).
  Migración tabla push→facturaia-db (sonnet). Auditoría post-PR + revisor del diff + audit
  cross-PR de composición→general-purpose (fable). Integración, Service Worker (delicado),
  globals.css, wiring del shell y decisiones = main loop (Opus), NO delegar.
- Diff post-agente revisado por el main; nunca dos agentes sobre el mismo archivo; filtra
  auditores (~50% falsos positivos), verifica con Read antes de actuar.
- Paralelismo: lanzar en un solo mensaje los subagentes independientes. Audit cross-PR de
  COMPOSICIÓN (fable) tras la última ola.

## Inviolables (repo)
- GLASS obligatorio (arriba). Tokens Filson/Switzer/JetBrains + paleta --brand/--brand-2/
  --danger; iconos <Icon> (NUNCA emojis); feature gating useFeatures (nunca RPC);
  EstadoPill cubre cada estado. Type-safety E2E, 0 any, Zod v4 encadenado.
- Tabla nueva = ENABLE RLS + políticas en la MISMA migración (NNN secuencial, nunca
  timestamp); SECURITY DEFINER nueva → REVOKE EXECUTE FROM PUBLIC, anon.
- Endpoint /api/* con sesión → withApiAuth (NO /api/v1 ni /api/admin); ruta service nueva
  → isServiceRoute + reiniciar dev.
- No romper desktop: bifurcación por useIsMobile; el componente desktop sigue siendo dueño
  de datos/filtros/modales (las vistas móviles son presentacionales).
- SW: nada de cifras financieras obsoletas sin marca; escritura offline solo con cola
  explícita. Registrar el SW sin romper el manifest ni las rutas públicas.
- Inline styles solo runtime (CSS var --pct), respetar el trinquete; si sube baseline,
  documentar y `npm run ratchet:update`.

## Gates por PR (innegociables)
npm run lint && npm run typecheck && npm run build + npm run deps:circular limpios · QA
localhost GLASS claro+oscuro en iPhone (agent-browser: set device "iPhone 16 Pro" SIN set
viewport; close --all para reiniciar, NUNCA pkill; snapshot además de screenshot; verificar
ancho real con sips -g pixelWidth) · artifact antes/después por pantalla · PR con
gh pr create; el loop NUNCA mergea (PR abierto = "listo"; merge de Manuel tras su QA, o
--admin tras gates verdes por la política de Actions bloqueado). Cero warnings; no silenciar
lint salvo inevitable + comentario.

## Dependencias de Manuel (bloquean solo el push, no el resto)
- Generar VAPID: `npx web-push generate-vapid-keys` → poner VAPID_PUBLIC_KEY,
  VAPID_PRIVATE_KEY, VAPID_SUBJECT (mailto:) en envs de Dokploy (container recreado, no
  restart) + NEXT_PUBLIC_VAPID_PUBLIC_KEY para el cliente. Dar los comandos exactos.
- Smoke push en iOS: requiere la PWA instalada (iOS solo permite push en standalone, 16.4+).

## Cierre
Artifact resumen con enlaces a los PRs, capturas glass antes/después por pantalla
(claro+oscuro), medición de rendimiento y desviaciones. Al terminar, /obsidian-1. No te
desvíes del plan sin opciones numeradas.
```

## Notas
- **iOS push** solo en PWA instalada (standalone) e iOS 16.4+ — recogido en el smoke, no es limitación nuestra.
- **Rendimiento** va como auditoría (medir antes de optimizar), no como PR de features a ciegas.
- Learning aplicable de la primera ola: [[grid-1fr-no-encoge-con-contenido-nowrap-usar-minmax-0-1fr]].
