---
title: migración facturaia → tufacturaia.com + dokploy nuevo
date: 2026-05-11
source: claude-code-session
tags: [facturaia, infra, migracion, dokploy, dns, traefik, spec]
---

# Migración TuFacturaIA → `tufacturaia.com` + Dokploy nuevo

Plan estructurado en 9 fases. Calidad > velocidad. Cero atajos. Cada fase con verificación + rollback documentado.

## Objetivos

1. Mover TuFacturaIA del dominio `facturaia.agentesia.world` a `tufacturaia.com` (marca propia).
2. Migrar a un **VPS nuevo dedicado** (`185.47.13.170`, Dokploy fresh).
3. **Migrar n8n también** a `n8n.tufacturaia.com` (en mismo Dokploy, proyecto separado).
4. **Configurar Resend con dominio propio** desde el inicio (`tufacturaia.com` transaccional + `auth.tufacturaia.com` Supabase Auth).
5. **Resolver 5 bugs estructurales de paso**:
   - Traefik reload manual tras cada redeploy (3 incidentes documentados en `Stack/docker-infra.md:48-59`).
   - Rate-limit in-memory (no escala multi-instancia).
   - Crons sin lock distribuido (race conditions con >1 réplica).
   - n8n SPOF (cae OCR, voz, email polling).
   - Puppeteer sin browser pool (browser nuevo por cada PDF).
6. Aprovechar para subir nivel: Redis añadido, healthcheck real, GitHub auto-deploy webhook, observabilidad mínima.

## Decisiones de arquitectura cerradas (2026-05-12)

| Decisión | Valor |
|---|---|
| Host físico nuevo | ✅ VPS dedicado `185.47.13.170`, Dokploy creado limpio 2026-05-12 |
| `api.tufacturaia.com` separado | ✅ Sí, desde día 1 |
| Migrar n8n | ✅ Sí, mismo Dokploy nuevo, proyecto separado `n8n-prod` |
| BD n8n | ✅ `pg_dump`/`pg_restore` + copiar `N8N_ENCRYPTION_KEY` para preservar credenciales |
| Resend custom domain | ✅ Desde el inicio (no diferir a hardening) |
| n8n.tufacturaia.com vs agentesia.world | ✅ Subdominio propio `n8n.tufacturaia.com` |

## Layout final en Dokploy nuevo

```
Dokploy en 185.47.13.170
├── Proyecto "facturaia-prod"
│   ├── facturaia-app    → Host: tufacturaia.com
│   ├── api-facturaia    → Host: api.tufacturaia.com (si separación física, sino router del mismo app)
│   ├── pdf-renderer     → interno, red facturaia-internal
│   └── redis            → interno, rate-limit + queue futuro
└── Proyecto "n8n-prod"
    ├── n8n              → Host: n8n.tufacturaia.com
    └── postgres-n8n     → interno, red n8n-internal
```

Networks: `dokploy-network` (external) compartida entre proyectos para Traefik. Cada proyecto tiene además su propia red interna aislada.

## P0 previo — bloqueante antes de empezar

**OpenAI API key literal en `n8n/workflows/whatsapp-receptor-v2.json`** (repo público GitHub):
- Key empieza por `sk-proj-G__taTj8N_kkUIdFO6...` (~165 chars).
- Acción: revocar → generar nueva → guardar solo en env n8n + memoria → PUT al workflow `zYcHHa8jWXB6dY5i` reemplazando literal por `{{$env.OPENAI_API_KEY}}` → grep marker post-PUT (HTTP 200 ≠ persistido) → borrar archivo del repo + commit.
- La key seguirá en historial git; opciones: `git filter-repo` (limpio) o asumir compromiso (estará revocada).

## Filosofía

- Cero downtime no es la prioridad. La prioridad es "bien hecho" — sin restos sucios, sin parches.
- Cada fase termina con verificación explícita; si no pasa, no se avanza.
- Reversible siempre: cada paso tiene rollback documentado.
- El contenedor viejo sigue vivo todo el tiempo hasta que el nuevo lleve **mínimo 7 días estable**.
- Cada cambio se documenta en hub + commit + canvas Slack.

---

## Fase 0 — Pre-flight (inventario + backups + auditorías BD)

### 0.1 Rotar OpenAI key (P0 arriba)

### 0.2 Inventario exhaustivo de envs
40 envs detectadas por audit:
- **Categoría a) URLs/dominios**: `NEXT_PUBLIC_APP_URL`, `NEXT_PUBLIC_SITE_URL`, `NEXT_PUBLIC_SUPABASE_URL`, `N8N_WEBHOOK_URL`, `PDF_RENDERER_URL`, `VERIFACTU_AEAT_URL`.
- **Categoría b) Secretos rotables**: `SUPABASE_SERVICE_ROLE_KEY`, `ANTHROPIC_API_KEY`, `WEBHOOK_SIGNING_KEY` (¡NO ROTABLE ojo, cifra secrets en BD!), `FACTURAIA_SERVICE_KEY`, `OPENAI_API_KEY`, `GOOGLE_CLIENT_ID/SECRET`, `RESEND_API_KEY`, `N8N_API_KEY`.
- **Categoría c) Secretos NO rotables** (cifran datos en BD): `CREDENTIAL_ENCRYPTION_KEY`, `VERIFACTU_ENCRYPTION_KEY`, `API_CURSOR_SECRET`, `WEBHOOK_SIGNING_KEY`. Copiar literales al nuevo, NUNCA regenerar.
- **Categoría d) Feature flags**: `LLM_PROVIDER`, `VOICE_CONVERT_ENABLED`.
- **Categoría e) Integraciones externas**: `SMTP_HOST/PORT/USER/PASS/FROM`, `STORAGE_QUOTA_*`, `SUPERADMIN_EMAILS`, `AGENTESIA_NIF`.

Snapshot a archivo cifrado local (no repo, no vault). Solo nombres en memoria del agente.

### 0.3 Backups previos
- 7 workflows n8n del hub → `ops/n8n-backups/2026-05-11-pre-migration/{workflow_id}.json`.
- CSV de tablas críticas: `module_metadata`, `org_module_config`, `system_config`, `admin_audit_log`, `api_keys`, `webhook_endpoints`, `voice_prompt_versions`, `voice_chat_bindings`.
- Supabase point-in-time-recovery snapshot verificado activo últimas 24h.

### 0.4 Snapshot funcional UI
Pantallazos: `/admin/system` (4 tabs), `/admin/features`, `/admin/config`, `/admin/voice`, `/admin/modules`, `/admin/crons`. Estos son la referencia post-flip: "lo de antes debe verse igual después".

### 0.5 Auditoría de URLs hardcoded en BD prod (descubierto por crítico — P1)
ANTES del flip, ejecutar contra Supabase prod y guardar resultados:
```sql
SELECT id, ia_prompt, descripcion_larga, acciones FROM module_metadata 
  WHERE acciones::text ILIKE '%agentesia.world%' 
     OR ia_prompt ILIKE '%agentesia.world%' 
     OR descripcion_larga ILIKE '%agentesia.world%';
SELECT key, value FROM system_config WHERE value::text ILIKE '%agentesia%';
SELECT id, url FROM webhook_endpoints WHERE url ILIKE '%agentesia.world%';
SELECT id, prompt FROM voice_prompt_versions WHERE prompt ILIKE '%agentesia.world%';
```
Cada hit es UPDATE SQL explícito a aplicar en Fase 5. Sin esto, esos datos quedan apuntando al viejo aunque el contenedor esté nuevo.

### 0.6 Auditoría URLs hardcoded en workflows n8n (descubierto por crítico — P0)
`grep -rE 'agentesia\.world|facturaia\.com' n8n/workflows/ ops/n8n-backups/`. Encontrado al menos:
- `whatsapp-receptor-v2.json:1237` → `https://facturaia.agentesia.world/api/voice/generate` literal.
- `email-polling.json:27` fallback dominio viejo.
- `voice-process/confirm/correct.json` fallback `facturaia.com` (dominio futuro pero aún no vivo).

Plan de parchado vía API n8n en Fase 3, con grep marker post-PUT.

### 0.7 Compra dominio + DNS
- `tufacturaia.com` registrado en Cloudflare.
- TTL 60s configurado en A records (rollback rápido).
- A records preparados pero **no publicados** hasta Fase 4.
- Subdominios pre-creados:
  - `tufacturaia.com` — app principal
  - `auth.tufacturaia.com` — Supabase Custom SMTP (futuro)
  - `n8n.tufacturaia.com` — n8n nuevo
  - `staging.tufacturaia.com` — entorno permanente staging
  - `api.tufacturaia.com` — decisión Fase 1.4 (sub vs misma raíz)

### 0.8 Pre-flight checks
- `grep -rE "sk-(proj|live|test)|AIza|whsec|fia_(live|test)|stripe_(sk|whsec)"` repo entero → cero hits.
- `npm run lint && npm run typecheck && npm run build && npm run test && npm run e2e:smoke` → 5 verdes.
- Sin commits locales sin push en `main`.

**Salida F0**: inventario completo + backups + cero secretos en repo + auditoría BD/workflows + DNS preparado.

---

## Fase 1 — Refactor en `main` (dominio viejo aún, ventana grande)

### 1.1 Eliminar fallbacks hardcoded
- `src/app/api/v1/openapi.json/route.ts:11` → throw si `NEXT_PUBLIC_APP_URL` falta.
- `src/app/api/team/members/route.ts:134` → eliminar fallback `?? 'https://facturaia.agentesia.world'`, throw 500.
- `src/components/settings/api-keys-section.tsx:278` → leer runtime, no literal.
- Comentarios curl en `/api/internal/*/route.ts` → cosmético, actualizar.

### 1.2 Crons internos: URL configurable
Env nueva `CRON_BASE_URL` (default `http://facturaia-app:3000` interno). Reemplazar literal `curl https://facturaia.agentesia.world/api/internal/...` por `curl $CRON_BASE_URL/api/internal/...`. Beneficio: crons no dependen de DNS público ni Traefik.

### 1.3 Lock distribuido en crons (P1 audit, bloqueante para coexistencia)
Migration `065_cron_locks.sql`:
```sql
ALTER TABLE cron_runs ADD COLUMN locked_at TIMESTAMPTZ;
CREATE UNIQUE INDEX uniq_cron_in_flight ON cron_runs (cron_name) WHERE finished_at IS NULL;
```
Modificar `withCronTracking`: `INSERT ON CONFLICT DO NOTHING` aborta si row in-flight existe. Test Vitest con dos ejecuciones concurrentes.

### 1.4 Decisión arquitectónica: `api.` subdominio separado (PENDIENTE OK MANUEL)
Opción A: `api.tufacturaia.com` desde día 1 — CORS/CSP/rate-limit independientes, métricas separadas.
Opción B: todo en raíz, separar después si crece.

### 1.5 Healthcheck real
`GET /api/health` que valide: Supabase reachable, último `cron_runs` < 10min, kill switch state. JSON `{status: 'ok'|'degraded'|'down', checks: {...}}`. Lo consumirá Traefik, Dokploy, uptime monitor.

### 1.6 Rate-limit Redis-backed (P1 audit)
Reemplazar `src/lib/rate-limit.ts` Map por `ioredis` + `INCR + EXPIRE`. Fallback in-memory con warning si `REDIS_URL` no set. Tests dobles.

### 1.7 Tests E2E
`tests/e2e/explorer/crawl.spec.ts:105` parametrizar same-origin filter via `E2E_BASE_URL` (hoy hardcoded `facturaia.agentesia.world`).

### 1.8 Deploy intermedio en contenedor VIEJO
Mergeado todo → deploy → verificar verde:
- Smoke E2E.
- `cron_runs` última semana sin regresiones.
- Webhook dispatcher OK.
- `/api/health` devuelve 200.

Si falla, NO migrar. Limpiar deuda primero.

**Salida F1**: código preparado, observabilidad mejor, cero hardcoded.

---

## Fase 2 — Diseño compose nuevo (sin aplicar)

### 2.1 Decisiones de arquitectura

| Tema | Decisión |
|---|---|
| n8n separado | **SÍ** — proyecto Dokploy propio. Resuelve bug Traefik. |
| Host físico | Confirmar contigo: ¿mismo VPS o nuevo? Si nuevo, n8n queda en `185.99.186.76` y TuFacturaIA va a host limpio. |
| Networking | `dokploy-network` (external) + `facturaia-internal` (bridge isolated). |
| Traefik labels | Router único `facturaia-app`, `traefik.docker.network=dokploy-network` explícito, `priority=10`. |
| Replicas | 1 inicialmente, compose listo para 2+. |
| PDF renderer | Servicio aparte (existe). Pool Puppeteer browsers (P3 audit). |
| Redis | Añadido. Rate-limit + futuro Bull queue. |
| Logs | stdout + driver `json-file` rotation `max-size=10m max-file=5`. |
| Backups n8n | Cron diario a R2/S3. |

### 2.2 Compose nuevo (estructura)
`facturaia-app` + `pdf-renderer` (red interna only) + `redis` + opcional `n8n-backup-cron`. Healthchecks con `start_period: 90s` (resuelve "Traefik enruta antes de estar listo"). Labels Traefik con healthcheck path `/api/health`.

### 2.3 GitHub webhook → Dokploy auto-deploy
Pendiente investigar en `Stack/docker-infra.md:59`. Si Dokploy auto-recarga Traefik en su deploy flow, eliminamos el paso manual "Reload".

### 2.4 NEXT_PUBLIC_* envs requieren rebuild, no restart
Documentar en runbook Fase 5. Cambios disparan `Deploy` no `Reload`.

**Salida F2**: compose escrito + revisado contigo + decisiones cerradas.

---

## Fase 3 — Provisión Dokploy nuevo

### 3.1 Crear proyecto "facturaia-prod"
Aplicar compose F2 + envs F0.2 + **labels Traefik aún desactivadas** (build sin exponer). Health interno verifica app levanta.

### 3.2 Crear proyecto "n8n-prod" separado
Compose mínimo con healthcheck + pruning + start_period 90s. Network propia + `dokploy-network`. WEBHOOK_URL apuntando a `n8n.tufacturaia.com` (sin publicar aún).

### 3.3 Decisión BD n8n: reusar la existente
Las credenciales cifradas con `N8N_ENCRYPTION_KEY` actual no se migran fácil. Reusar BD vía `pg_dump`/`pg_restore` preservando `n8n_encryption_key`. Confirmar antes.

### 3.4 Parchar workflows n8n
Antes de levantar n8n-prod, parchar las URLs hardcoded identificadas en F0.6 vía API n8n. Post-PUT, grep marker para verificar persistencia (HTTP 200 ≠ persistido — gotcha conocida CLAUDE.md).

### 3.5 Smoke aislamiento
Antes de publicar: `wget http://localhost:3000/api/health` desde terminal Dokploy → 200. Logs limpios 30 min.

**Salida F3**: entornos arrancados, verdes, aislados.

---

## Fase 4 — Staging público + validación E2E

### 4.1 Dominios staging
- DNS `staging.tufacturaia.com` → contenedor TuFacturaIA-nuevo.
- DNS `n8n-staging.tufacturaia.com` → n8n-nuevo.
- Traefik labels activas. Let's Encrypt emite certs.

### 4.2 Configuraciones para staging (sin tocar prod)
- Supabase: **añadir** (no reemplazar) `staging.tufacturaia.com/api/auth/callback` a Redirect URLs.
- Google Cloud: añadir `staging.tufacturaia.com/api/auth/google/callback`.
- Meta WhatsApp: NO tocar prod aún.

### 4.3 Smoke E2E real
- `E2E_BASE_URL=https://staging.tufacturaia.com npm run e2e:explorer` → cero issues.
- 101 tests E2E voz repuntados al staging → cero fail.
- Verificar:
  - Login Supabase OK.
  - Crear factura completa, ver PDF, Verifactu QR (sandbox AEAT).
  - Webhook saliente disparado.
  - Cron `webhook-dispatcher` corriendo, `cron_runs` actualizado.
  - Rate limit funcional (Redis incrementa).
  - Health endpoint OK.

### 4.4 Test de caos
- `docker restart facturaia-app` → vuelve solo + Traefik enruta sin reload manual.
- Restart n8n → healthcheck recupera.
- Kill Redis → app degrada a in-memory rate-limit con warning, no rompe.

**Salida F4**: staging validado E2E + caos, sin afectar prod viejo.

---

## Fase 5b — Flip atómico de n8n (paralelo o secuencial al flip app)

n8n no soporta dos instancias activas procesando los mismos webhooks (duplicaría mensajes WhatsApp / Retell). El flip debe ser atómico.

### Pre-requisitos
- n8n-prod arrancado en Dokploy nuevo (Fase 3).
- `N8N_ENCRYPTION_KEY` copiada literal del Dokploy viejo (sin esto, credenciales cifradas no descifran).
- `pg_dump` del Postgres n8n viejo → `pg_restore` en Postgres n8n nuevo.
- `n8n.tufacturaia.com` DNS publicado, Traefik enruta, Let's Encrypt OK.
- Workflows cargados en n8n-prod pero **DESACTIVADOS** (paused) hasta el flip.

### Validación previa al flip
1. Acceder al editor n8n nuevo → confirmar que se ven los 7 workflows + sus credenciales (no aparecen como "broken credential").
2. Ejecutar manualmente un workflow trivial (ej: `whatsapp-verify`) → confirma que Supabase/OpenAI credentials descifran y conectan.
3. Verificar `voice_chat_bindings` y `voice_prompt_versions` se leen OK desde n8n nuevo.

### Pasos del flip (5-15 min)
1. **Pausar workflows en n8n viejo** (Settings → Workflows → Deactivate all).
2. **Activar workflows en n8n nuevo** (Deactivate → Activate desde editor o API).
3. **Meta WhatsApp dashboard**: webhook URL `n8n.agentesia.world/webhook/...` → `n8n.tufacturaia.com/webhook/...`. Verificar webhook con mensaje prueba inmediatamente.
4. **Retell dashboard**: por cada agent_id en `voice_chat_bindings`, repuntar webhook URL al nuevo n8n.
5. **agency-portal email forwarding** (si aplica): repuntar destino.
6. **URLs internas en workflows**: env `FACTURAIA_APP_URL` en n8n-prod debe apuntar a `https://tufacturaia.com` (no al viejo). Verificar con `curl` desde dentro del contenedor.
7. **Smoke E2E real**: enviar WhatsApp test al número público + grabar llamada Retell test → confirmar ambos procesan en n8n-prod (revisar Executions).

### Rollback (<10 min si algo falla)
1. Reactivar workflows en n8n viejo.
2. Revertir Meta webhook al viejo URL.
3. Revertir Retell webhook al viejo URL.
4. Diagnóstico en n8n-prod sin presión.

### Coexistencia post-flip (2 semanas como red)
- n8n viejo permanece vivo con workflows pausados.
- Cualquier mensaje que llegue por error al viejo NO se procesa (workflows desactivados) → mejor que duplicar.
- Tras 2 semanas verde en el nuevo, apagar n8n viejo.

---

## Fase 5 — Flip de dominio (cuando staging lleva 48h verde)

Orden estricto:

1. **Auditoría URLs en BD aplicada**: UPDATE SQL con los resultados de F0.5.
2. **Actualizar Supabase Auth Dashboard**: Site URL → `tufacturaia.com` + añadir a Redirect URLs (no quitar viejo).
3. **CORS bucket Supabase Storage**: añadir `https://tufacturaia.com` a Allow-Origin en buckets `facturas`, `logos`, `certificates`.
4. **Banner usuarios 48h antes**: aviso de migración + sesiones requerirán re-login (cookie domain change).
5. **DNS Cloudflare publica `tufacturaia.com`** → IP nuevo. Let's Encrypt emite.
6. **Traefik labels multi-host**: añadir `tufacturaia.com` al router (coexistencia con staging hostname).
7. **Test fuera**: `curl https://tufacturaia.com/api/health` → 200 con datos correctos.
8. **Desactivar schedules Dokploy proyecto VIEJO** (bloqueante — sin esto, doble cron sobre misma BD).
9. **Meta WhatsApp dashboard**: webhook URL → `https://tufacturaia.com/api/whatsapp/...`. Verificar mensaje prueba inmediatamente.
10. **Retell dashboard**: cada `agent_id` en `voice_chat_bindings` → actualizar `webhook_url` al nuevo dominio.
11. **Google Cloud Console**: OAuth callback al nuevo dominio.
12. **Verificar `/api/v1/openapi.json`** devuelve `tufacturaia.com`.
13. **Avisar a clientes API v1** (agency-portal, integraciones) → regenerar SDKs.

### Comunicación
- Slack canvas Panel TuFacturaIA: entrada con fecha + URL nueva.
- Email a usuarios activos.
- PR en agency-portal: env `FACTURAIA_API_BASE`.

**Salida F5**: dominio nuevo = primario. Viejo coexiste, nada roto.

---

## Fase 6 — Coexistencia + redirect 301 (mes 1-3)

### 6.1 Configurar viejo como redirect-only
Contenedor viejo vivo, sin lógica activa. Traefik label redirect 301 `facturaia.agentesia.world/*` → `tufacturaia.com/*` preservando path+query.

### 6.2 Crons solo en nuevo
Schedules Dokploy proyecto viejo permanentemente off (paso F5.8 ya cubre).

### 6.3 Auditoría tráfico viejo
Logs Traefik 30 días. Cualquier IP/UA pegando al viejo → identificar (cliente, cron olvidado) y contactar.

### 6.4 Plan de rollback documentado
Runbook `ops/runbook-rollback-tufacturaia.md`:
- DNS rollback (TTL 60s, propagación 5-10 min).
- Reactivar schedules Dokploy viejo.
- Revertir Supabase Site URL al viejo.
- Comunicar a usuarios.

**Salida F6**: dominio viejo solo redirige, sin lógica.

---

## Fase 7 — Apagado viejo (mes 3+)

Cuando log viejo 2 semanas sin hits no-bot:
- Apagar contenedor viejo Dokploy.
- Eliminar redirect Traefik.
- DNS `facturaia.agentesia.world` → 404 explícito (no eliminar registros, mantener apuntando a fallback).
- Limpiar referencias residuales en código, manuales, vault, canvas.

---

## Fase 8 — Hardening post-migración (continuo)

No bloquea migración. Mes 1-6:
1. Resend custom domain `auth.tufacturaia.com` (spec [[facturaia-comunicaciones-emails]]).
2. Sentry / observabilidad real con correlation IDs.
3. pgbouncer si saturación conexiones (no preventivo).
4. Puppeteer browser pool en pdf-renderer.
5. n8n circuit breaker (cuando OCR/voz fallan, marcar error en BD + retry job).
6. Backups n8n automatizados a R2/S3.
7. Staging environment permanente en Dokploy.
8. Monitor uptime externo (UptimeRobot/BetterStack) → `/api/health` cada 60s, alerta Slack si caída >2min.

---

## Resumen métrico

- **9 fases**, **~6-10 semanas total** con margen amplio.
- **17 gaps no obvios** cubiertos por segundo pase crítico.
- **5 bugs estructurales resueltos** de paso (Traefik reload, rate-limit, cron locks, n8n SPOF, Puppeteer pool).
- **1 P0 inmediato** (OpenAI key) bloqueante.

## Decisiones pendientes con Manuel

1. Host nuevo en VPS distinto o mismo (F2.1)?
2. Subdominio `api.tufacturaia.com` desde día 1 o monolítico (F1.4)?
3. Reusar BD n8n via pg_dump (recomendado) o empezar limpio + re-conectar credenciales a mano (F3.3)?
4. Resend custom domain desde `auth.tufacturaia.com` ahora o en hardening F8?

## Referencias

- Audit infra: `/Users/manueldelmonte/facturaia/docker-compose.yml` (lineas 8, 15, 16 — dominios hardcoded a corregir vía env).
- Bug Traefik documentado: `Stack/docker-infra.md:48-59`.
- Stack proyectos activos: `Stack/docker-infra.md:140-147`.
- Spec emails Resend: [[facturaia-comunicaciones-emails]].
- Spec integraciones bancarias: [[facturaia-open-banking-psd2]].
