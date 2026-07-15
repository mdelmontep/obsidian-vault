---
title: TuFacturaIA — vista móvil, segunda ola (glass + push + offline + gestos)
date: 2026-07-15
source: claude-code-session
tags: [facturaia, frontend, mobile, pwa, spec]
---

# Vista móvil TuFacturaIA — segunda ola

**Estado (2026-07-15):** primera ola (PR0-PR6: home nativo, shell+PWA, sheet "+", tab Facturas, tab Documentos, menú "Más") EN PROD. Esta spec es el prompt de ejecución de la SEGUNDA ola, listo para lanzar en otra sesión de Claude Code (Opus, multi-agente). Decisiones cerradas con Manuel: **push = infra completa, VAPID las genera Manuel**; **offline = estrategia profesional tipo fintech** (shell precacheado, datos network-first con marca de antigüedad, nunca cifras obsoletas sin aviso). [[facturaia]]

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
