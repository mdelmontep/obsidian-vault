# Handoff — máquina de contenido TuFacturaIA: panel en pestañas, publicar en Instagram, campañas Google Ads

Escrito el 2026-08-14 (noche) al cierre de la sesión que completó la máquina de marketing. La sesión nueva arranca con `/grill-with-docs` sobre los tres bloques de abajo. Repo: `~/Projects/facturaia` (worktree propio desde `origin/main`; hay OTRA sesión paralela con WIP sin commitear en `src/lib/billing/` y `src/app/(admin)/admin/orgs/` — no pisar).

## Estado del que se parte (verificado hoy, no asumido)

- **Spec #1643 fases 1-4 COMPLETAS.** Explorador de tendencias (#1748→PR #1775, mig 691), salud del runner (#1771→PR #1777), métricas+analista (#1654/#1655→PR #1780, mig 692). Todo mergeado y en prod.
- **Instagram conectada y verificada**: cuenta `@tufacturaia` (IG User ID `17841438173452357`), página FB `TuFacturaia` (`1194843583723159`), token largo cifrado en `system_config` (clave `marketing_metricas_instagram`), run manual del cron `marketing-metricas` en `success` con `instagram.conectada: true`. El token del alta **ya incluye `instagram_content_publish`** (relevante para el bloque 2). Caduca ~10-oct; credenciales en el ítem 1Password «Meta Graph API · Instagram métricas Facturaia» (vault FacturAIA) — nunca imprimirlas.
- **Google Ads NO conectada** (ni hay campañas). La conexión actual solo LEERÍA métricas; el wizard existe.
- **Ticket #1787 (vía rápida, independiente de este handoff)**: hooks en 4 modos + retención en guionista, `postura` en ideación, copy real del wizard. No lo dupliques; si ya está mergeado, mejor.
- Crons: `marketing-runner-salud` (*/15) y `marketing-metricas` (04:10 Madrid) como schedules de Dokploy sobre el compose `tufacturaia-app`, comando `sh /app/ops/cron/sign-call.sh /api/internal/<slug> POST`.

## Los tres bloques a grillar (en este orden)

### 1. Pestañas en `/admin/marketing/contenido` (solo frontend)

La página es hoy una columna de ~10 tarjetas y el propio Manuel no encontró la de Métricas. Propuesta de partida (a validar en el grill): `Segmented` de la casa con **Piezas** (cola+preview+métricas por pieza) · **Cerebro** (brief, mix/pilares, tendencias, analista, reglas de estilo) · **Producción** (vídeo, imagen, topes) · **Conexiones y salud** (métricas-conexiones, log de runs). Página: `src/app/(admin)/admin/marketing/contenido/page.tsx` (+`_parts/page/*`). Inviolables frontend en `CLAUDE.md` del repo (Segmented obligatorio, nada de tabs a mano).

### 2. Publicar en Instagram desde la pieza (cierra el bucle de métricas)

El gesto manual más frágil hoy es pegar `publicacion_ref` a mano. Con `instagram_content_publish` ya concedido se puede: botón «Publicar en Instagram» en pieza aprobada → asset del bucket `marketing-assets` a URL pública → contenedor Graph API (IMAGE/CAROUSEL/REELS) → publish → guardar permalink en `publicacion_ref` automáticamente. Decisión ya tomada por Manuel implícita en la propuesta aceptada: **botón explícito, nunca auto-publicar al aprobar** (confirmar en el grill de todos modos).

Preguntas para el grill: estado intermedio `publicando` y qué pasa si falla a medias (el container se crea y el publish falla) · URL firmada con caducidad larga vs bucket público (Meta descarga async) · límite de 100 publicaciones/día de la API · quiet hours/ventana de publicación · ¿reels necesitan share_to_feed? · dónde vive el permiso (superadmin con `marketing_write`? — ojo: `superadmin_permissions` está VACÍA hoy, decisión pendiente en el hub).

### 3. Campañas de Google Ads EN PAUSA desde el panel

Recomendación ya dada a Manuel (aceptada en principio, confirmar): crear campaña+grupo+keywords+RSA por API **siempre en PAUSED** y con tope de presupuesto diario obligatorio; activar es un clic suyo en Google Ads. El agente `copy_ads` ya produce titulares/descripciones; cliente OAuth+GAQL existe en `src/lib/marketing/metricas/google-ads.ts`. **Bloqueo externo**: developer token con acceso Basic (aprobación de Google, días/semanas) — muro solo-humano, usar `/wizard` cuando toque. Sin cuenta de Ads activa aún.

## Restricciones de la casa que aplican a los tres

- ADR-012: el runner NUNCA lleva credenciales de BD ni tokens de Meta/Google; publicar/crear campañas son acciones de la APP (endpoints admin), no del runner.
- Espejos TS↔SQL con tests anti-deriva; cualquier estado nuevo de `marketing_pieces` exige TS+SQL en el mismo PR (los nueve espejos, ver CLAUDE.md fila del equipo de contenido).
- Contrato runner: `docs/architecture/marketing-runner-contract.md`. Contexto de dominio: `CONTEXT.md` §equipo de contenido. Decisiones previas: `docs/decisions/ADR-012-*.md`.
- Migraciones: número provisional + `mig:renumerar` antes del merge; pooler de prod estuvo caído HOY entero (workaround: SQL editor + verificación por catálogo, ver `Stack/incidents.md` del vault).
- Progreso en Slack `C0AU00N25FC` al arrancar y cerrar cada ticket (regla del equipo de contenido).
- Copy visible: `docs/architecture/copy-humano.md`. Todo campo nuevo del panel se autoexplica.

## Suggested skills

1. `/grill-with-docs` — la sesión empieza aquí; deja ADRs (auto-publicación, pausado-por-defecto, reparto de pestañas) y actualiza `CONTEXT.md`.
2. `/research` en background durante el grill — fuentes primarias de: Instagram Content Publishing API (contenedores IMAGE/CAROUSEL/REELS, requisitos de URL, rate limit 100/día, `publishing_limit`) y Google Ads API mutate (CampaignBudget/Campaign/AdGroup/AdGroupAd/criteria, REST, versión vigente).
3. `/to-spec` → `/to-tickets` → `/implement` por ticket con `/clear` entre cada uno (tracker: GitHub Issues `AgentesIA-MAdrid/facturaia`).
4. `/wizard` — solo cuando llegue el muro del developer token de Google Ads.

## Aparcado (no entra en esta sesión)

- Analista cualitativo (P1): esperar 2-3 semanas de métricas reales; anotado en el hub del vault.
- Conectar Google Ads (métricas): sin campañas no hay nada que medir.
- `gen:types` de `database.types.ts` contra prod: pendiente de que el pooler vuelva (las entradas a mano son equivalentes).
