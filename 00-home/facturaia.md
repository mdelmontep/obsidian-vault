---
title: facturaia
date: 2026-05-10
tags: [cliente, facturaia, hub]
---

# FacturaIA — Hub maestro

App SaaS de facturación con IA (OCR, agente WhatsApp, voz, recomendador). Multi-tenant. **Este archivo es el ÚNICO punto de entrada al proyecto.** Todo lo nuevo (idea, pendiente, smoke test, decisión, doc) entra aquí o se enlaza desde aquí.

## Cómo usar este hub

- **Al empezar sesión FacturaIA**: leer este archivo entero. Es la foto del proyecto.
- **Durante**: añadir cualquier cosa nueva en su sección. No esperar al final.
- **Al cerrar sesión**: `/obsidian-1` propondrá actualizar las secciones tocadas + mover lo cerrado a `## Histórico`.
- **Reglas**: 1-2 líneas por entrada. Si necesita más, link a subfile en `knowledge/projects/agentesia/facturaia-*.md`.

---

## Estado actual

- **Producción**: facturaia.agentesia.world (Dokploy viejo, activo) + **tufacturaia.com** (Dokploy nuevo `185.47.13.170`, SSL pendiente Cloudflare DNS-only) · spec [[facturaia-migracion-tufacturaia-com]]
- **Stack**: Next 16 + Supabase (proyecto `lahqlyaxvobqjgdiftag`) + n8n + OpenAI Vision + Anthropic Claude
- **Plan comercial**: Starter / Pro / Enterprise + add-ons (Conciliación 19€, Anti-fraude 9€, +21 con badge Próximamente)
- **Orgs activas en prod**: AgentesiaLab (Enterprise), tecnocloud (Enterprise), Borja Galván (Enterprise), AgenteIA PRUEBA (Starter)
- **Última deploy mayor**: 2026-05-08 (PR #47 audit log + idempotency)
- **Tests Vitest**: 175+ pasando (HMAC, cursor, idempotency, SERIE_BY_TIPO, IVA, rate-limit)

---

## NOW (trabajo activo)

- **🔴 BUG — Convertir presupuesto a factura por WhatsApp no funciona** — detectado 2026-05-12. El flujo end-to-end por voz/chat (audio "convierte el presupuesto NUM a factura" → bot confirma con botones → usuario confirma → conversión real) está roto. Histórico relevante: hubo 2 fixes previos (resumen totales 0€ por iterar `data.lineas` que el agente no devuelve para `convertir_presupuesto` → solucionado con lookup HTTP en `Parsear y Calcular Totales`; y matching difuso/typos Whisper → solucionado en system prompt con lista candidatos numerados + memoria conversacional, commits `5cf48a3` + `6d41b9b` + `4e98d76` del 2026-05-10). Verificar: (a) qué falla exactamente ahora — ¿el bot detecta la intención?, ¿muestra los botones?, ¿la confirmación llega al endpoint backend?, ¿el endpoint convierte?, (b) revisar execution logs n8n del workflow `zYcHHa8jWXB6dY5i` (últimos fallos), (c) verificar persistencia del prompt en n8n con grep marker, (d) probar `/api/voice/convert-presupuesto` con curl + Bearer fia_live + ver respuesta, (e) confirmar que el feature `generador_voz` sigue activo en la org de prueba. **Bloqueante para Bloque 1 (Borja necesita esto OK antes de soltar el bloque a clientes)**
- ~~**🔴 P0 inmediato — rotar OpenAI key expuesta en repo**~~ ✅ **HECHO 2026-05-12** — verificado que prod n8n ya usaba `$env.OPENAI_API_KEY` (hardening previo 2026-05-06, doc `docs/security/ocr-n8n-hardening-applied.md`). Key vieja revocada en OpenAI, nueva añadida en env Dokploy n8n + restart, OCR smoke-test funcional. Eliminados snapshots stale: `n8n/workflows/whatsapp-receptor-v2.json`, `whatsapp-receptor-v1-backup.json`, `whatsapp-receptor.json` (contenían literal pre-hardening). Repo grep limpio. **Pendiente**: commit del repo limpio + decisión sobre `git filter-repo` (key ya revocada, riesgo bajo)
- **Migración a `tufacturaia.com` + Dokploy nuevo** — F1+F2+F3 completos (2026-05-13). App verde en `185.47.13.170`, `/api/health` OK. **Bloqueado**: SSL Let's Encrypt falla por Cloudflare DNS proxiado → Dani debe poner DNS-only. **Pendiente**: n8n-prod proyecto (compose en `ops/docker-compose-n8n.yml`), versión exacta n8n del viejo, migration 074 aplicar en Supabase prod, crons configurar en Dokploy nuevo. Spec: [[facturaia-migracion-tufacturaia-com]]
- **Bloque 1 — generar-view form manual** (commit `820684b`, 2026-05-07) — corregido `SERIE_POR_TIPO` (proforma F, abono eliminado), `tipo_documento` seteado en INSERTs, rama proforma cae en presupuestos. Abono manual desde generar-view eliminado por incumplir RD 1619/2012. Nuevo flujo: botón "Anular y emitir abono" en detalle de factura emitida con selector R1-R5 (`POST /api/facturas/[id]/anular`). `GET /api/render-pdf?tipo=&id=` (cierra 404 "Ver PDF" en presupuestos). `/api/email/send` acepta `presupuesto_id` (`sendPresupuestoByEmail` lib nueva)
- **Cumplimiento fiscal: referencia en abonos** — PDF de abono debe mostrar nº y fecha de la factura original que rectifica. Campo `factura_origen_id` ya en BD pero templates no lo muestran. Bloque separado del commit anterior
- **Tests proformas + abonos rectificativos** — Vitest pendientes
- **Mobile responsive resto** — PR #5 cubre críticos. Pendiente: formularios <480px, search topbar polish, admin pages
- **Archivar sub-workflows voz antiguos en n8n** — Voice Process / Confirm / Correct (arquitectura v1) ya no se usan desde receptor v2. Activos pueden confundir
- **agency-portal PRs abiertos**: #54 quotes actions, #55 actor passthrough, #56 unificación facturas. Esperando review Borja. Tras merge #54: regen `types.gen.ts`, quitar 3 `as never`, migration `quotes.converted_facturaia_factura_id` + populate

## Smoke tests pendientes

- **🟢 Deploy 2026-05-12 (módulo Cobros completo) — commit `b48d9cb` ya pusheado y desplegado**:
  1. ✅ Cron `cobros-reminders` en Dokploy con shell=bash + Command sin wrap manual + comillas DOBLES `-H "x-service-key: $FACTURAIA_SERVICE_KEY"` — Run Now devuelve HTTP 200 + JSON con `summary` (verificado 2026-05-12 23:20: orgs_scanned=1, orgs_skipped_quiet_hours=1 → comportamiento correcto, ventana 21:00-08:00 default)
  2. **PENDIENTE — Meta**: solicitar plantilla utility `cobros_recordatorio_v1` en Meta Business Manager con variables `cliente_nombre, numero, importe_eur, fecha_vencimiento, dias_vencida, link_pago, firma`. Aprobación humana Meta 24-72h. Luego registrar en `/admin/config?tab=cobros-pricing` con form de plantilla Meta
  3. **PENDIENTE — envs Dokploy**: añadir `META_WHATSAPP_PHONE_NUMBER_ID` (del número WABA +34 919 93 26 18) + `META_WHATSAPP_ACCESS_TOKEN` (long-lived, 60d o System User Token)
  4. **PENDIENTE — n8n env**: confirmar que workflow `zYcHHa8jWXB6dY5i` tiene env `FACTURAIA_SERVICE_KEY` (debe coincidir con backend) para que el branch STOP del receptor v2 pueda hacer POST a `/api/internal/cobros-stop`
  5. **End-to-end real con cliente test** (cuando 1-4 OK): UPDATE `clientes` para validar telefono propio de prueba → poner `cobros.hora_envio` a la hora actual → forzar Run Now → recibir WhatsApp en móvil propio con plantilla aprobada → responder STOP → verificar opt-out en BD + notif al dueño
  6. **UI verifica**:
     - `/agentes` → Agente de cobros → tab Configuración: form 6 keys con preview en vivo, sin section cards pesadas, footer balanceado (helper text + botón)
     - `/emitidas?view=aging`: switcher Tabla/Aging, KPI strip + 5 buckets + tabla agrupada con icono teléfono verde/rojo (sin pulse) tooltip nativo
     - Click "Enviar ahora" → Modal con selector canal WhatsApp/Email (email Próximamente disabled)
     - Drawer campana: chips filter single-select + menú ⋯ por notif con Snooze (1h/esta noche/mañana/lunes/semana) + Descartar + footer "Preferencias y horas silenciosas"
     - `/settings?tab=notificaciones`: sección "Mis preferencias" arriba con quiet hours personales + días semana + canales + digest opt-in (disabled hasta Resend)
     - `/admin/system?tab=cobros`: KPIs cross-org + top orgs + Pausar con frase tipeada `PAUSAR COBROS <ORG>`
     - `/admin/config?tab=cobros-pricing`: tabla editable plan_quotas + form Meta template
  7. **Hydration**: confirmar `/settings?tab=notificaciones` no muestra error de hydration mismatch (anterior bug arreglado con `useSearchParams` + Suspense)
- **🔴 Deploy 2026-05-11 (reorganización admin)** — tras push + Deploy Dokploy:
  1. **Sidebar admin** en 3 secciones (NEGOCIO / PRODUCTO IA / SISTEMA). "Sugerencias IA" aparece como "Recomendador". "Tareas programadas", "Alertas", "Storage" desaparecen del nivel raíz (ahora en "Salud")
  2. **`/admin/system`** abre con 4 tabs (Tareas programadas · Almacenamiento · Alertas · Webhooks). `?tab=` actualiza URL al cambiar. Cada tab carga su panel
  3. **Redirects**: `/admin/storage`, `/admin/alerts`, `/admin/system/crons` redirigen a `/admin/system?tab=...`. No 404
  4. **`/admin/config`** abre con 5 tabs (Entorno · Email · Fiscal · Mantenimiento · WhatsApp). Tab Entorno muestra envs ✓/✗ por categoría + commit/uptime/Node/Next
  5. **Tab Email** muestra "No configurado" (warning rojo) hasta que `SMTP_HOST` esté seteada en Dokploy
  6. **Tab Fiscal** lista cola Verifactu + tasa éxito 30d + certificados (caducados/7d/30d). NO hace ping AEAT
  7. **Tab Mantenimiento** locked por defecto. Click "Desbloquear" → modal contraseña → unlock. Editar banner: texto + severidad + caducidad → Guardar
  8. **Banner global**: tras guardar banner activo, aparece banda arriba en `/dashboard` (y todas las rutas). Refresh persiste. Click X dismissa per-session
  9. **Kill switch**: en modal de confirmación, sin escribir "ACTIVAR MANTENIMIENTO" el botón está disabled. Tras escribir + activar → indicador rojo en `/admin/system` header + sección con datos quién/cuándo/expira
  10. **Kill switch ON, usuario no-superadmin** intenta crear factura → 503 "Sistema en modo mantenimiento". Mismo superadmin sigue pudiendo. Lectura siempre OK
  11. **Kill switch ON, superadmin** entra a `/admin/config` y `/api/admin/config/maintenance` siguen accesibles (recovery path) → desactivar OK
  12. **Features** `/admin/features`: cada row muestra chip "N planes" antes de Core/switch. Click expande mini-lista con plan-nombre · plan-id
  13. **Audit log** `admin_audit_log` tiene row tras toggle banner / activar / desactivar kill switch. Campos: `actor_user_id`, `action`, `old_value`, `new_value`
- **🔴 IMPORTANTE — Deploy 2026-05-11 (módulos IA + observabilidad crons)** — tras redeploy con los últimos commits (`5255547` + `d4b7566` + `d43f80d` + `6442182`):
  1. **Cron `cashflow-alerts`** — Run Now en Dokploy → debe responder ✅ (era ❌ por endpoint 404 antes del push). Verificar row `status=success` en tabla `cron_runs` y en `/admin/system/crons` semáforo verde
  2. **Cron `storage-quota-check`** — Run Now → era ❌ con `invalid warn_mb` por env vacía. Tras fix `parseMb` (commit `5255547`) debe pasar a ✅. Verificar en `/admin/system/crons`
  3. **Panel `/admin/system/crons`** en producción — los 6 crons listados con datos, semáforo correcto por cada uno (verde si corrió OK en su ventana, ámbar si excede 80% del intervalo, rojo si falló o lleva más del max). VerifACTU como gris/sin datos hasta que se active
  4. **Tooltip de info** en cada card — hover sobre icono "i" muestra popover OPACO (no transparente) con título + descripción + bloque azul "Ejemplo real". Verificar contraste en dark mode y light mode
  5. **Modal de detalle del cron** — click en card abre modal con bloque "Ejemplo real" antes de "¿Qué pasa si falla?" + tabla de últimas 10 ejecuciones
  6. **OCR `auto_categorizar` trigger BD** — desactivar toggle en `/settings/modulos` para una org con OCR; subir factura recibida; verificar que `facturas.categoria` queda NULL aunque el LLM/n8n haya enviado categoría
  7. **Conciliación `auto_marcar_cobradas` trigger BD** — con factura recibida en `sin_aprobar`/`pendiente` y movimiento bancario coincidente (mismo importe ±tolerancia, ±ventana_días), verificar transición automática a `estado='pagada'` + row en `module_events` tipo `factura_pagada_auto`
  8. **Copiloto gate `orgHasFeature('copiloto')`** — con org Starter sin add-on activo: botón "Preguntar a IA" del topbar debe OCULTARSE; intentar abrir vía `window.dispatchEvent('open-ai-assistant')` desde consola NO debe abrir el chat; `POST /api/ai-assistant` debe devolver 403. Activar override `org_features` para esa org y verificar que vuelve a funcionar
  9. **Copiloto `idioma` + `guardar_historial`** — cambiar idioma a `en` en `/settings/modulos`, mandar pregunta, verificar respuesta en inglés. Con `guardar_historial=true`, verificar rows en `copiloto_conversaciones` (user + assistant del mismo `thread_id`). Con `guardar_historial=false`, no debe persistir nada
  10. **Cashflow `umbral_alerta_caja`** — configurar umbral alto (ej 50000€), forzar Run Now del cron `cashflow-alerts`, verificar notif `caja_baja` en campanita de org de control + row en `module_events`
  11. **ModuloConfig defaults** — abrir modal de cualquier módulo con `org_module_config` vacío para esa org → toggles default-true (`auto_categorizar`, `auto_marcar_cobradas`, `incluir_recurrentes`, `guardar_historial`) deben mostrarse como ✅ "Activado" (NO "Desactivado" como antes del fix)
  12. **Error handling save module config** — desconectar red, intentar guardar config → toast rojo de error (NO falso "✓ Guardado")
  13. **Notif `cron_failed_<name>`** — provocar fallo intencional en un cron (ej desconfigurar URL en Dokploy temporalmente) → verificar notif en campanita de la org de control + entrada roja en panel `/admin/system/crons`
- **Deploy 2026-05-07 (post)**:
  1. Anular factura emitida → ver abono ligado en banner rojo del modal + tab "Abonos" con count correcto
  2. Crear presupuesto/proforma desde `/generar` (serie P/F + Ver PDF sin 404)
  3. Probar 3er botón "Emitir como pendiente" (Verifactu sí, email no, estado=`pendiente`)
  4. Dashboard KPIs no inflados con borradores
  5. Menú 3 puntitos sin Editar/Eliminar en factura emitida, sin Anular en abono
- **Bloque 1 manual post-deploy** (`820684b`):
  1. Crear factura/presupuesto/proforma desde `/generar` y verificar serie A/P/F + `tipo_documento` correcto en BD
  2. Anular factura emitida con motivo R1-R5 → abono serie B con líneas en negativo + factura origen anulada + remisión AEAT si VeriFACTU
  3. "Ver PDF" en presupuestos sin 404
  4. Enviar presupuesto/proforma por email con PDF adjunto
- **VeriFACTU cron — verificar frecuencia** — confirmar en Dokploy que cron de `/api/verifactu/process` corre cada 1min (no cada hora). Si fuera 1h, incumple normativa AEAT (remisión no puede ser diferida). Solo config, sin código
- **PR #47 prod** — verificar entries en `audit_log` tras marcar cobrada / reenviar email / anular / DELETE vía API v1
- **agency-portal PR #56 post-merge** — badge fiscal en row, redirect 301 `/agency/facturaia/*`, botones según estado/origen, modal motivo R1-R5 obligatorio, doble-click sin duplicar (Idempotency-Key)

## WIP (sesiones en curso, branches sin mergear)

_(añadir aquí ramas activas con propósito y bloqueador si lo hay)_

## Progreso en vivo

Log cronológico de cada cosa que se trabaja. **Antes de empezar** algo nuevo, Claude busca aquí (+ NOW + Histórico) para detectar conflictos, solapes o trabajo previo. **Al avanzar/cerrar** algo, Claude añade entrada.

Formato: `YYYY-MM-DD HH:MM · estado · qué · ref (commit/PR/file)`. Estados: `[empezado]` / `[en progreso]` / `[bloqueado: razón]` / `[hecho]` / `[descartado: razón]`.

Reglas para el motor de conflictos:
- Idea nueva → grep en este log + NOW + LATER + Histórico ANTES de añadir. Si match → avisar "ya existe / ya se hizo / ya está en progreso por X" y proponer fusionar.
- Si dos cosas tocan el mismo archivo/feature → flagear solape y preguntar prioridad.
- Si lleva >7 días `[en progreso]` sin update → marcar `[stale]` en poda quincenal.
- Cuando una entrada llegue a `[hecho]` y sea hito relevante → mover a `## Histórico de hitos` con fecha + 1 línea.

<!-- nuevas entradas debajo, lo más reciente arriba -->
- 2026-05-13 · `[bloqueado: Cloudflare DNS-only pendiente Dani]` · **F3 — servidor nuevo tufacturaia.com operativo** — `185.47.13.170` Dokploy, proyecto `tufacturaia-prod`, servicio `facturaia-app` Docker Compose desde repo `AgentesIA-MAdrid/facturaia` branch `main`. App verde, `/api/health` → `{status:"ok", supabase.ok:true, latency_ms:110}`. SSL bloqueado por Cloudflare proxiado (nube naranja → cert ACME falla con 204). Dominio añadido en Dokploy con Let's Encrypt, esperando DNS-only de Dani.
- 2026-05-13 · `[hecho]` · **F1+F2 — refactor main + compose Redis + rate-limit Redis + n8n compose** — commits `7aabe38` (healthcheck, cron locks migration 074, CRON_BASE_URL, /api/health, middleware isServiceRoute) + `b7a8fbc` (rate-limit.ts async con ioredis + fallback in-memory, docker-compose Redis service, healthcheck curl, log rotation) + `bcb5743` (fix healthcheck wget→curl, depends_on no-blocking, ops/docker-compose-n8n.yml con healthcheck+pruning+memoria). Lint/typecheck/build limpios.

- 2026-05-12 · `[hecho]` · **P0 secundaria detectada y parchada — OCR Factura workflow tenía la misma key revocada hardcoded** — descubierto al hacer backup de los 7 workflows n8n (Fase 0.3): el workflow `zf2la2N2YBXKQNKk` (FacturaIA - OCR Factura) usaba la OpenAI key revocada esta mañana en literal hardcoded en el nodo "OpenAI Vision OCR". Tras la rotación de la mañana, **OCR vía `/ingesta` (drag&drop UI) y email polling estaban ROTOS silentes** (401 OpenAI) — pero el smoke test inicial pasó por WhatsApp/receptor v2 que tiene OCR inline propio con env var, así que no se detectó. Fix: script `ops/n8n-patches/apply-ocr-factura-env-key.py` idempotente. Cambia Authorization header de `Bearer sk-proj-...` literal a `Bearer {{$env.OPENAI_API_KEY}}` (expresión n8n). Aplicado vía PUT API n8n, verificado con grep marker post-PUT (cero literales sk-*). Backup pre-patch en `~/.facturaia-migration-secrets/2026-05-12-pre-flip/` (fuera del repo, chmod 600). **Pendiente smoke test usuario**: subir factura por `/ingesta` y verificar datos extraídos
- 2026-05-12 · `[hecho]` · **Fase 0.3 backups workflows n8n** — 6 de 7 workflows FacturaIA backupeados en `ops/migration/snapshot-2026-05-12-pre-flip/n8n-workflows/` (sin secretos). El 7º (`zf2la2N2YBXKQNKk` con literal sk-*) movido a `~/.facturaia-migration-secrets/` fuera del repo. CSVs de tablas BD saltados por redundancia con Supabase PITR
- 2026-05-12 · `[hecho]` · **Fase 0.5 auditoría URLs BD prod limpia** — 7 queries SQL ejecutadas en Supabase contra `module_metadata`, `system_config`, `webhook_endpoints`, `voice_prompt_versions`, `voice_chat_bindings`, `notifications`, `organizations.settings`. **Todas devuelven 0 rows**. Cero URLs hardcoded a `facturaia.agentesia.world` o `facturaia.com` en BD prod. No hay UPDATEs SQL a aplicar pre-flip. Fase 0.5 cerrada sin acción
- 2026-05-12 · `[hecho]` · **Fase 0.8 pre-flight checks** — lint + typecheck + tests Vitest + build los 4 verdes en `main`. Repo estable y listo para refactor de Fase 1
- 2026-05-12 · `[hecho]` · **Resend custom domain operativo + Supabase Custom SMTP cableado** — `tufacturaia.com` y `auth.tufacturaia.com` verificados en Resend EU (Frankfurt). **Plan Pro 20€/mes activado** (necesario para 2+ dominios; cubre 50.000 emails/mes). DNS añadido en IONOS: DKIM `resend._domainkey` + MX `send` (feedback-smtp.eu-west-1.amazonses.com prio 10) + SPF `send` tanto en root como auth subdomain. 2 smoke tests OK: desde `noreply@tufacturaia.com` (ID `fa41f746-382d-49d3-aafe-b1ba71966418`) y desde `noreply@auth.tufacturaia.com` (ID `a9bc870c-4814-42ba-9623-555183fce985`). 2 API keys creadas con scope restringido: `facturaia-app-transactional` (root domain) y `facturaia-supabase-auth` (auth subdomain). Supabase Auth → Custom SMTP cableado a `smtp.resend.com:465` con key auth. Magic link test funcional (llega desde `noreply@auth.tufacturaia.com` con DKIM válido). Block 0.7 de Fase 0 cerrado
- 2026-05-12 · `[bug-detectado]` · **Convertir presupuesto a factura por WhatsApp roto** — usuario reporta flujo end-to-end no funciona. Histórico: 2 fixes previos 2026-05-10 (totales 0€ + matching difuso typos Whisper). Diagnóstico pendiente: revisar execution logs n8n `zYcHHa8jWXB6dY5i`, grep marker prompt, curl directo a `/api/voice/convert-presupuesto`. Bloqueante Bloque 1
- 2026-05-12 · `[hecho]` · **Caos engineer audit + fixes finales módulo Cobros** — commit `671b890` pusheado y desplegado. Agente con mindset "humano adversarial intentando romper" encontró 13 issues, 8 reales aplicados. **🔴 2 críticos**: (1) regex STOP n8n era case-sensitive sin tildes → "stop"/"baja"/"NO MÁS" no matcheaban → RGPD breach silente. Patch script actualizado con clases `[Ss][Tt]...` + tilde `[ÁA]` + idempotent re-apply (detecta regex viejo y actualiza in-place). Aplicado al workflow productivo `zYcHHa8jWXB6dY5i` con marker re-verificado. (2) Doble envío real por `network_error` post-Meta-delivery — `failed` no bloqueaba UNIQUE → retry cron a los 15min → cliente recibía 2x. Fix migration 073: trigger BEFORE INSERT rechaza retry mismo (factura, nivel) durante 6h tras failed lanzando 23505 → orchestrator lo trata como `skipped:duplicate`. **🟠 4 altos**: (3) Admin stats panel mentía sobre pausadas tras migration 071 cambió shape boolean→objeto — helper `isPaused` con doble shape support; (4) Lost update concurrente pause-org (dos admins simultáneos perdían pausa) — migration 072 con RPCs `cobros_pause_org_set/clear` atómicas usando jsonb_set + operador `-`; (5) DELETE validate-phone dejaba telefono_e164 stale → re-validación usaba número viejo del cliente equivocado — DELETE limpia ambos campos, POST siempre recanonicaliza desde `telefono`; (6) Aging endpoint sin límite temporal en recordatorios — crecía linealmente, fix `.gte(attempted_at, 90d ago)`. **🟡 2 medios**: (7) Race opt-out vs send mid-flight — re-check `isClientOptedOut` justo antes del fetch Meta + marca como opted_out si llega tarde; (8) Bucket aging día 0 (vto=hoy) — alineado con cron `vto<CURRENT_DATE`: ahora `diasVencida <= 0` va a "por_vencer". **Falsos positivos descartados**: dedupe_key sin org_id (verificado manualmente: notify_upsert sí usa UNIQUE(org_id, dedupe_key)), regex escapeValue bytes 0x00-0x1F invisibles (correctos), quiet hours start==end (no security). 2 migrations nuevas aplicadas (072+073). 256 tests + typecheck + lint + build limpios.
- 2026-05-12 · `[hecho]` · **Módulo Agente de cobros completo end-to-end** — commit `b48d9cb` pusheado y desplegado en prod. Backend: 6 migrations 065-070 (cobros_recordatorios append-only con UNIQUE idempotency, trigger cancel-on-terminal, SQL function `cobros_pending_for_org` SECURITY INVOKER triple-check, notification_preferences + quiet hours org/user con tabla y dos funciones SQL, clientes_opt_out RGPD append-only + telefono_e164 + telefono_validado_at + CHECK config validation, cobros_envios_billing + cobros_plan_quotas editable desde admin con seed Starter=0/Pro=500/Enterprise=2000). Lib TS: 9 plantillas hardcoded (3 tonos × 3 niveles, RD 1619/2012 auditable) con render single-pass anti-recursión, E.164 canonicalizer con default ES, Meta Graph wrapper (template/text mode con fallback) + send-email TODO Resend gated, quota check con membership inside, opt-out check con DEFAULT-deny en error, orquestador con race condition handling (re-leer status tras INSERT, ON CONFLICT 23505 manejado como `skipped:duplicate`). Endpoints: cron `/api/internal/cobros-reminders` con withCronTracking + ventana hora_envio ±30min + quiet hours operativas + batch cap 500/run, manual `/api/cobros/send-now` con rate limit 5/min + 30/día + role check + cross-tenant guard + 404 (no 403) para no revelar existencia, webhook `/api/internal/cobros-stop` n8n-friendly + sin enumerar count cross-org, opt-out manual RGPD, preferences GET/PUT, snooze con IDOR guard, phone validation. Admin: `/api/admin/cobros/{stats,pause-org,quotas}` todos con audit log + frase tipeada "PAUSAR COBROS <ORG>" + auto-expira 7d. Workflow n8n receptor v2 parcheado con branch IF "Es STOP?" + HTTP "Notificar STOP a FacturaIA" + "Confirmar STOP al Cliente" — marker `cobros_stop_marker_v1` verificado post-PUT. UI: tab Configuración con preview en vivo (overrideTab para 'cobros' en ModuloDetalleModal) — steppers limpios "día/días", segmented control tono (suave/profesional/firme), Aging view en `/emitidas?view=aging` con KPI strip + 5 buckets segmented + tabla agrupada por cliente con details/summary + cards mobile, icono teléfono estático rojo/verde sin pulse con tooltip nativo, Modal "Enviar ahora" rediseñado con resumen factura + canal selector WhatsApp/Email (email Próximamente Resend, disabled) + tono + preview burbuja + Enviar. Drawer notif: chips filter single-select por categoría con contadores + menú ⋯ por notif con Snooze (1h/esta noche/mañana/lunes/semana) + Descartar + footer link `/settings?tab=notificaciones` + useSyncExternalStore singleton para tick estable sin loops infinitos. Settings: nueva sección "Mis preferencias" con quiet hours personales + días semana toggleable + canales con switches iOS + digest opt-in placeholder. Admin `/admin/system?tab=cobros` con stats cross-org + top 10 orgs + acciones pausar con frase tipeada. Admin `/admin/config?tab=cobros-pricing` con tabla editable plan_quotas + addon_quotas + Meta template config (name/language/body_variable_keys). Auditoría: 6 agentes paralelos (2 rondas planning UX/design × 1 backend auditor) → 1 P0 + 3 P1 + 2 P2 aplicados + falsos positivos descartados con razón. 40 tests Vitest nuevos (256 total). Migrations aplicadas a prod desde local con psql. **Conexiones verificadas end-to-end**: catalog keys ↔ validate_cobros_config SQL ↔ orchestrator ↔ UI; admin pause-org → system_config.cobros_org_paused → cobros_check_quota → cron salta; admin quotas → cobros_plan_quotas → cobros_check_quota lee tabla; workflow n8n STOP → /api/internal/cobros-stop → clientes_opt_out → orchestrator skip; phone validation UI → endpoint → BD; isServiceRoute middleware cubre /api/internal/*. **Patrones aprendidos**: useSyncExternalStore con `getSnapshot` debe devolver valor cacheado (no `Date.now()` directo) o loop infinito; Dokploy cron requiere shell `bash` + Command sin `bash -c` wrap + comillas DOBLES alrededor del header `-H "x-service-key: $VAR"`; SettingsView con `useState(getter)` + `if (typeof window === 'undefined')` causa hydration mismatch → usar `useSearchParams` + Suspense wrapper. **Mockup data seedeado** en AgentesiaLab (3 facturas con vto pasado para buckets aging, 2 clientes telefono_validado_at, 1 cobros_recordatorio sent, 3 module_events, 3 notifs variadas)
- 2026-05-12 · `[hecho]` · **P0 OpenAI key rotada** — verificado vía API n8n que prod ya usaba env var (`$env.OPENAI_API_KEY` en nodo "Disparar OCR" del workflow `zYcHHa8jWXB6dY5i`, hardening 2026-05-06). Key vieja revocada, nueva en env Dokploy n8n + restart, OCR smoke OK. Borrados 3 snapshots stale del repo: `whatsapp-receptor-v2.json`, `whatsapp-receptor-v1-backup.json`, `whatsapp-receptor.json`. Backups recientes en `ops/n8n-backups/` ya estaban limpios. Repo grep cero hits secrets. Desbloquea Fase 1 migración tufacturaia.com
- 2026-05-11 · `[empezado]` · **Plan migración tufacturaia.com + Dokploy nuevo** — 3 agentes paralelos auditaron infra/integraciones/seguridad-escalabilidad. 1 agente crítico segundo pase descubrió 17 gaps no obvios. P0 detectado: OpenAI key literal en `whatsapp-receptor-v2.json` (repo público). Plan 9 fases en [[facturaia-migracion-tufacturaia-com]] cubre: rotación P0, refactor en main pre-migración (fallbacks hardcoded, CRON_BASE_URL, cron locks distribuidos, healthcheck real, rate-limit Redis), diseño compose (n8n separado, Redis, pdf-renderer en red interna, GitHub auto-deploy), provisión Dokploy aislada, staging E2E + caos, flip aditivo con 13 pasos ordenados (incluye UPDATE SQL en BD para URLs hardcoded, CORS Storage, Meta/Retell/Google dashboards, desactivar schedules viejos), redirect 301 mes 1-3, apagado viejo mes 3+, hardening continuo. **Pendiente OK Manuel** en 4 decisiones de arquitectura
- 2026-05-11 · `[empezado]` · **Integraciones bancarias — análisis y spec** — confirmado estado actual: tabla `movimientos_bancarios` (043) + triggers bidireccionales 061 + módulo Conciliación con config schema. Gap = cero ingesta (tabla vacía en prod). Spec [[facturaia-open-banking-psd2]] reescrita con 3 opciones (Norma 43 / GoCardless BAD PSD2 / pasarelas cobro) + roadmap 6 fases + riesgos compliance/cifrado consent. Decisiones cerradas: empezar por N43 (coste 0, 80% valor), GoCardless BAD como primer agregador (no Tink/Plaid), pasarelas cobro como módulo aparte. Añadidos a NEXT: Norma 43 import + trigger simétrico emitidas→cobrada. LATER expandido: PSD2 + pasarelas
- 2026-05-11 · `[hecho]` · **Reorganización admin — sidebar 3 secciones + `/admin/system` tabs + `/admin/config` tabs + banner global + kill switch read-only** — 4 agentes paralelos (backend/frontend/security/product) debatieron plan, sintetizado y aplicado. Migración 064 `admin_audit_log` (RLS service-only) + reuso `system_config` con keys `maintenance_banner` y `read_only_mode`. Endpoints nuevos: `/api/admin/system/webhooks`, `/api/admin/config/{env-check,email,fiscal,maintenance}`, `/api/system/banner` (público). Kill switch en `with-api-auth.ts` y `handler.ts` v1 con bypass por rol superadmin + prefijos `/api/admin/system/*` y `/api/admin/config/*` (recovery path). Banner global en root layout, poll 60s + on-focus, dismiss per-session. UI: tabs componente accesible (`src/components/admin/ui/tabs.tsx`), 6 paneles config + 1 webhooks panel, redirects en next.config (`/admin/storage` → `/admin/system?tab=storage` y similar). Cross-link Features ↔ Planes con chip "N planes". 5 bugs detectados en autorevisión (columnas BD: `status_code` vs `http_status`, `vence_at` vs `expires_at`, `verifactu_enviada_at` vs `verifactu_fecha_envio`, `plans.id` es código no `plans.codigo`, regex range escapada mal). React 19 purity: `Date.now()` durante render → derivar booleano server-side. Lint/typecheck/build OK. Migración aplicada en prod. **Pendiente push + deploy + smoke tests**. **Diferidos por debate**: email_log Fase A (recomendado SÍ próxima sesión), AEAT health derivado de últimas N facturas (SÍ ~5min), comparador planes visual (NO, valor bajo), feature flags globales (NO, YAGNI)
- 2026-05-11 · `[hecho]` · **Observabilidad de crons + panel admin** — tabla `cron_runs` (063), `withCronTracking` wrapper en 6 crons, panel `/admin/system/crons` con semáforo + tooltips + ejemplos reales por cron. Notif `cron_failed_<name>` a campanita de org de control si falla. Registry con descripción human-friendly. Commits `9892e4c` + `1b14779` + `d4b7566` + `d43f80d`
- 2026-05-11 · `[hecho]` · **Bug destapado y arreglado** — `storage-quota-check` fallaba semanal en silencio por env `STORAGE_QUOTA_WARN_MB=""` → `Number("")=0` ≤ 0 → throw. Fix con helper `parseMb` (fallback robusto null/empty/non-numeric). Destapado al primer run de `cron_runs`. Commit `5255547`
- 2026-05-11 · `[hecho]` · **Módulos IA mejorados — OCR + Conciliación via triggers BD** — migrations 060/061: `respect_ocr_auto_categorizar` (BEFORE INSERT/UPDATE facturas) + `auto_mark_pagada_on_bank_match` (AFTER INSERT/UPDATE facturas + AFTER INSERT movimientos_bancarios). Triggers cubren todos los callers (n8n, ingesta-view, API v1, voice). Catálogo: `auto_categorizar` + `auto_marcar_cobradas` `implemented: true`. Commit `33d5c7c`
- 2026-05-11 · `[hecho]` · **Cashflow IA opts + cron Opción B** — `buildCashflowData` acepta `{horizonteDias, incluirRecurrentes}`, cableado en cashflow-view/dashboard-view/impersonate. Nuevo cron `/api/internal/cashflow-alerts` (Dokploy `30 7 * * *`, chunks 10 + Promise.all, dedupe 24h, gate orgHasFeature). Commit `164dd9a`
- 2026-05-11 · `[hecho]` · **Copiloto — gate + idioma + persistencia historial** — gate `orgHasFeature('copiloto')` en `/api/ai-assistant` (cierra fuga billing preexistente), Topbar oculta botón sin feature, `AIAssistantHost` gatekeep evento `open-ai-assistant`. System prompt en `{idioma}`. Tabla `copiloto_conversaciones` (062, RLS por user_id) + thread_id desde cliente. Commit `19ee00f`
- 2026-05-11 · `[hecho]` · **ModuloConfig UI fixes** — toggles respetan `f.default` cuando config vacío (afectaba auto_categorizar, auto_marcar_cobradas, incluir_recurrentes, guardar_historial — se mostraban "Desactivado" la primera vez). Error handling con toasts en `save()`. Commit `3fefc3a`
- 2026-05-11 · `[hecho]` · **6 agentes paralelos auditaron cambios** (2 rondas × 3 expertise: security/backend/frontend) — 1 P0 + 3 P1 + 2 P2 reales aplicados, ~50% falsos positivos descartados con razón documentada
- 2026-05-10 · `[empezado]` · **Sistema comunicaciones email — Resend** — Spec consolidada tras review de 5 agentes paralelos (codebase, security, architecture, UX product, UI consistency). 5 PRs secuenciales reemplazan plan original 60d. Reutiliza `outbox_events` + `notifications` + `ai_module_suggestions` (NO duplica). Auth via Supabase + Custom SMTP Resend en dominio separado `auth.facturaia.agentesia.world`. Spec completa: [[facturaia-comunicaciones-emails]]. **Pendiente: Manuel hace setup Resend (2 dominios + Cloudflare DNS + Supabase SMTP + Dokploy env) antes de PR 1**
- 2026-05-10 · `[hecho]` · Hub maestro FacturaIA creado con NOW/Smoke/WIP/NEXT/LATER/Ideas/Decisiones/Stack/Manuales/Specs/Workflows/Histórico · commit `922ccea` vault
- 2026-05-10 · `[hecho]` · Sección Progreso en vivo añadida al hub para tracking de conflictos · commit pendiente vault
- 2026-05-10 · `[hecho]` · Hub poblado desde Slack canvas Panel FacturaIA — Bloque 1 generar-view, smoke tests Bloque 1, mobile responsive, sub-workflows voz a archivar, sección Seguridad (3 prio + 3 hardening), 9 features IA en NEXT, 8 features producto en LATER, suite E2E Playwright al histórico · commit pendiente vault
- 2026-05-10 · `[hecho]` · Manuales actualizados con UX real del módulo voz — manual-usuario sección "Convertir presupuesto" reescrita con 4 escenarios (1 match / candidatos numerados / fallback típos Whisper / ya facturado) + manual-admin sección 23.12 con root cause + fix técnico. Commit `4e98d76`
- 2026-05-10 · `[hecho]` · **Fix UX matching presupuestos** (E2E real reveló): resumen 0€ por iterar `data.lineas` que el agente no devuelve para `convertir_presupuesto` → branch en `Parsear y Calcular Totales` con lookup HTTP a Supabase. Y system prompt mejorado: matching permisivo (acentos/diminutivos/typos Whisper), lista candidatos numerados en >1 match, fallback "últimos 5 abiertos" en 0 matches, memoria conversacional para que el usuario responda "1"/"2". Commits `5cf48a3` + `6d41b9b`. Backups en ops/n8n-backups/
- 2026-05-10 · `[hecho]` · **F1+F2 voz + híbrido + workflow patched + verificación exhaustiva** — 12 commits: endpoints find/convert + UI variables/avanzado + métricas drill-down + admin /admin/voice + binding chat_id↔org_id + pg_cron purge + endpoint internal voice-system-prompt + endpoint voice-chat-bindings + workflow patched (consultar_presupuestos toolCode + branch convert post-confirm) + 5 bugs hardening (PGRST203, feature_gate, iva_pct min/max, invalid_json 400, ocr-audit FK 404). 101 tests E2E reales contra Supabase prod, 60/60 unit, lint/typecheck/build OK. **Pendiente push + deploy + activar generador_voz por org + phone en profiles antes de E2E con Meta**

---

## NEXT (próximas 2 semanas)

- ~~⭐ WhatsApp convertir presupuesto a factura por intención~~ ✅ **HECHO 2026-05-10** (commits + workflow patched, falta push/deploy + E2E real con Meta)
- ~~⭐ Admin módulo Voz/WhatsApp~~ ✅ **HECHO 2026-05-10** (`/admin/voice` con tabla overrides + métricas drill-down + sistema híbrido prompt variables/avanzado)
- **Sistema comunicaciones email (Resend)** — 5 PRs secuenciales: mailer core + auth via Supabase SMTP, outbox unificado + 8 plantillas, notifications multi-canal, módulo + UI cliente, admin UI + custom domain + 3 IA. Spec: [[facturaia-comunicaciones-emails]]. Bloqueado por setup Resend manual (cuenta + 2 dominios + DNS + Supabase SMTP + Dokploy env). ~3 semanas total
- **Stripe en activación add-ons** — hoy CTA "+XX€/mes" redirige a `/settings?tab=plan` sin cobro. Conectar checkout para que toggle = compra. Conciliación 19€ y Anti-fraude 9€ ya seedeados
- ~~**Cobros backend**~~ ✅ **HECHO 2026-05-12** (commit `b48d9cb`, endpoint cron operativo en prod, falta plantilla Meta aprobada + envs META_WHATSAPP_* para envíos reales)
- **Manuales actualizar Bloque 1** — `manual-usuario.md` y `manual-admin.md` describen flujo viejo: 2 botones generar (no 3), no mencionan anular ni tab Abonos ni nuevos pills/badges
- **Abono ligado a factura real** — nueva tool n8n `consultar_facturas_recientes` para que el agente confirme "¿te refieres a F2026-0042 a Tecnocloud por 121€?" antes de generar abono. Liga vía `factura_origen_id`. ~1 día
- **Post-confirm "añadir al catálogo"** — tras crear documento, si hubo productos marcados con ✨ (no estaban en catálogo), enviar mensaje extra con botones "Sí, añadir / No". Endpoint nuevo `/api/voice/learn-product`. ~1 día
- **Cobrador inteligente** — job nocturno detecta facturas vencidas y envía WhatsApp personalizado al cliente del emisor sin intervención. Reutiliza agente WhatsApp existente. Config por org: días de gracia, tono, canales. ~1-2 días. **Impacto alto** — mayor dolor de autónomos/PYMEs
- **Alertas anomalías facturas recibidas** — al ingestar factura de proveedor conocido, comparar importe contra histórico. Si desviación >X% → "Esta factura de Vodafone es 40% más alta que la media". Coste: query histórico en pipeline OCR. ~medio día
- **OCR conversacional bidireccional** — cuando OCR no encuentra campo crítico (NIF, total, fecha), agente pregunta por WhatsApp en vez de dejar fila incompleta. Reutiliza agente conversacional. ~1 día
- **Auto-categorización de gastos** — clasificar facturas recibidas leyendo histórico del proveedor: "facturas de Vodafone siempre van a Telefonía". Pedir confirmación solo cuando hay duda. ~1-2 días
- **Centralizar OCR en un solo workflow n8n** — hoy hay 2 paths: receptor v2 (inline OCR para WhatsApp) y zf2 OCR Factura (HTTP webhook para `/ingesta` upload + email polling). Refactor: que `/api/upload` y `process-attachments` llamen a un único endpoint o consoliden la lógica OCR en un sub-workflow compartido. Reduce deuda + futuras rotaciones de key se hacen en 1 sitio. ~medio día. Apuntado tras incidente 2026-05-12 (key revocada rompió zf2 silente mientras receptor v2 seguía OK)
- **Per-org email domains (Resend Fase 2)** — cada org verifica su propio dominio en Resend para que emails salgan desde `@<su-dominio.com>` con DKIM real del cliente (no `via FacturaIA`). Stack: tabla `org_email_domains` (RLS por org) + 4 endpoints API + UI `/settings/emails` con form + DNS records copiables + cron daily re-verificar pending + lógica envío con fallback a `facturaia.com`. ~4-5 días puros. Feature del plan Pro/Enterprise (justifica add-on). Diferido hasta que un cliente lo pida explícitamente — aditivo, no rompe nada migrando después. Spec base: [[facturaia-comunicaciones-emails]]
- **Diagnóstico inteligente rechazos AEAT** — hoy errores AEAT llegan como código técnico. Mejorar para que IA explique en lenguaje llano qué falló y cómo corregir, en el modal de la factura. Reutiliza `ai-validate.ts`. ~horas
- **Predicción de cashflow** — con historial de facturas + patrones de cobro por cliente (quién paga 30d, quién 90d), proyectar cashflow del próximo mes con desglose confirmado vs en riesgo. Datos ya en BD. ~2-3 días
- **Import Norma 43 / CSV bancario para conciliación** — UI en `/settings/conciliacion` con drag&drop, parser AEB-43 (formato fijo posicional), preview de mapping, INSERT batch a `movimientos_bancarios` con `fuente='n43'`, dedupe por hash `(fecha, importe, descripcion, referencia)`, resumen post-import con count de facturas auto-marcadas pagadas (lo hace solo el trigger 061). Paso 1 del roadmap de integraciones bancarias. Reutiliza tabla y triggers ya en prod, sin coste recurrente. ~1-2 días. Spec: [[facturaia-open-banking-psd2]]
- **Trigger simétrico emitidas → cobrada** — copia de migration 061 con `tipo='emitida'`, signo positivo de importe, set `fecha_cobro` (campo ya en migration 034). Cierra el otro lado de la conciliación. ~horas. Spec: [[facturaia-open-banking-psd2]]
- **Versionado de defaults módulos** — cambiar default global no debe sorprender a orgs sin override (snapshot del valor previo o aviso visible)
- **Log de cambios de config por org** — audit trail granular para reconstruir "quién cambió qué config de qué org cuándo"

## LATER (backlog)

- **Backends módulos pendientes** — Fiscal (modelos AEAT 303/111/115/347), Firma eIDAS, Cashflow IA forecast. ~21 opciones config con badge Próximamente
- **Conexión bancaria automática PSD2 (GoCardless BAD)** — paso 4 del roadmap, tras Norma 43 + trigger emitidas. Tabla `bank_consents` cifrada, endpoints connect/callback/sync, cron 4-6h, dedupe por `provider_transaction_id`, notif `bank_consent_expiring` 7d antes. Empezar con sandbox + 1 banco real (BBVA o Santander). 1-2 semanas. Reutiliza `movimientos_bancarios` y triggers 061 tal cual. Spec: [[facturaia-open-banking-psd2]]
- **Pasarelas de cobro (Stripe Invoice + Redsys)** — módulo aparte, no conciliación. Webhook `invoice.paid` → match por `metadata.factura_id` → estado cobrada sin pasar por extracto. Cablear cuando Stripe checkout para add-ons esté en NEXT. Spec: [[facturaia-open-banking-psd2]]
- **Asistente IA multi-canal** — copiloto WhatsApp para consultas (vencidas, resúmenes, cobrador, predicción cashflow, auto-categorización, alertas, presupuestos por contexto, informe fiscal). Spec: [[facturaia-bloque-4-agent-query-spec]]
- **Google OAuth email por org** — cada org envía desde su email vía Gmail API
- **Canales Ingesta + Plan/Facturación** (spec 2026-04-24) — rediseño canales sin toggles, página planes reales con método pago e historial
- **Conciliación bancaria IA** (spec 2026-04-21) — 5 tablas, pipeline Claude 2 fases, UI aprobación por lotes
- **Cleanup mockup AgentesiaLab** — plan SQL elaborado. Org `ea201784-...`
- **Multi-WhatsApp números por org** — Tecnocloud necesita su phone_number_id Meta. Spec: [[facturaia-arquitectura-multi-whatsapp-numbers]]
- **Exportación contable** — formato compatible con gestorías (A3, Sage, etc.)
- **App iOS sin Swift** — Expo Go / React Native, mínima para consultar facturas recibidas/emitidas/bandeja IA. Gestión compleja → desktop. Valorar dificultad vs nativa Swift
- **Control de stock**
- **Enlace contable** para programas de contabilidad
- **Entrada y salida de caja**
- **Liquidaciones de facturas recibidas**
- **Facturación recurrente con SEPA**
- **Dashboard financiero avanzado** con predicciones cashflow basadas en patrones históricos

---

## Ideas crudas / inbox

_(volcado sin filtrar — pasan a NEXT/LATER si maduran, o se descartan en poda quincenal)_

- **Email_log Fase A** (recomendado próxima sesión, ~30min) — tabla `email_log` con insert en `send-factura`/`send-presupuesto`/`notify-quota`. Endpoint `/api/admin/config/email` devuelve último envío + counts 24h/7d. Sin webhook Resend de bounces todavía (Fase B siguiente). Hoy panel Email muestra "No configurado" + "Sin tracking en v1" — bloquea visibilidad cuando se configure SMTP
- **AEAT health derivado de últimas N facturas** (~5min) — cambiar `/api/admin/config/fiscal` para que el semáforo del panel se calcule desde las últimas 5-10 facturas enviadas (todas fallaron = rojo, alguna falla = ámbar). Sin ping a AEAT (lento + bloqueable). Más reactivo que tasa absoluta 30d
- **Exportar matriz planes a CSV** (~15min) — botón en `/admin/plans` que devuelve CSV plan↔feature para mandar a Borja o preparar pricing page. Alternativa al comparador visual (descartado por baja utilidad)
- _(añadir ideas aquí según surjan)_

## Decisiones cerradas (referencia)

- **2026-05-12 · Supabase Cloud se mantiene durante migración tufacturaia.com** — debatido self-host Supabase. Argumento user: "mejor ahora que con 300 usuarios reales". Contra-argumento: estamos en medio (4 orgs reales + agency-portal integrado), self-host añade 7 servicios a operar (Postgres + GoTrue + PostgREST + Storage + Realtime + Studio + Kong), coste real ~30€/mes VPS + backup ~5€/mes ≈ Supabase Pro (~25€/mes) sin contar tiempo, y triplicaría el riesgo de la migración actual. Re-evaluable en 6-12 meses con plan dedicado. Acción opcional: montar Supabase self-host en sandbox aparte un fin de semana para probarlo sin tocar prod, decidir con datos reales

## Decisiones pendientes (producto)

- **Cliente live vs congelado** — hoy snapshot fiscal al crear factura (datos cliente embebidos). Si editas cliente, PDFs viejos conservan datos antiguos (legalmente correcto, confunde UX). ¿Botón "Re-emitir con datos actuales" o congelado siempre? → cuando se decida, ADR en `decisions/`
- **Feature flags experimentales globales** — debatido 2026-05-11, descartado por YAGNI (`org_features` por org ya cubre piloto/experimentos). Si en el futuro aparece caso real de "flag global para TODAS las orgs", usar `system_config` key-value sin UI dedicada hasta tener 3+ flags. NO construir abstracción especulativa

## Bloqueos / esperando a terceros

- **[IMPORTANTE] Declaración Responsable AEAT como fabricante de SIF** — AgentesIA debe presentar este trámite administrativo para que FacturaIA opere legalmente en producción con VERI*FACTU. SIF = Sistema Informático de Facturación (RD 1007/2023). Sin esto el sistema no está homologado. Confirmar con Dani+Gonzalo si ya está o iniciar trámite
- **Dani**: DNS `tufacturaia.com` → poner A record en **DNS only** (nube gris) en Cloudflare para que Let's Encrypt emita el cert SSL. Sin esto la app no tiene HTTPS válido.
- **Dani + Gonzalo**: subir certificado P12 por org en Ajustes → VERIFACTU. Sin él no se envían facturas a AEAT y aparece error en dashboard
- **Borja**: review/merge agency-portal PR #54, #55, #56

## Seguridad

🟡 **Hardening diferido**:
- Logs estructurados en endpoints (correlation IDs)
- CSP headers más estrictos
- Métricas de uso de API IA (consumo OpenAI/Anthropic por org)

---

## Stack técnico

- **Frontend**: Next 16 (App Router), Tailwind, primitives Button/Card/Input/Modal en `components/ui/`
- **Backend**: Next API routes + Supabase (Postgres, RLS obligatoria por tabla)
- **OCR**: OpenAI Vision (`gpt-4o-mini`), fallback Anthropic Claude Vision
- **Voz**: n8n workflows + Retell (números WhatsApp por tenant)
- **Pagos**: Stripe (checkout pendiente cablear a add-ons)
- **Fiscal**: Verifactu (QR en PDFs, AEAT integrado)
- **Auth/RLS**: superadmin impersona vía `?org_id=` query param, no cookie
- **Tests**: Vitest (175+ unit/integration) + Playwright E2E (`tests/e2e/`: setup, smoke, explorer). Pre-release: `npm run e2e:explorer` y revisar `report.json`

## Reglas de proyecto (resumen)

Ver `facturaia/CLAUDE.md` (en repo) para versión completa.
- `lint` + `typecheck` + `build` limpios pre-commit
- Toda tabla nueva = `ENABLE ROW LEVEL SECURITY` + políticas en la misma migración
- Migration `ADD COLUMN NOT NULL` = `ADD nullable → UPDATE backfill → SET NOT NULL` en transacción
- Endpoint nuevo = auth + rate limit + validación input siempre
- Cambios Zod API público = `openapi.json` en mismo commit (clientes openapi-typescript no leen `refine`)
- UI con badge "implementado" = grep que el backend lee el valor (anti regresión silenciosa)

---

## Manuales y docs

| Doc | Link | Estado |
|---|---|---|
| Manual usuario | [GitHub](https://github.com/AgentesIA-MAdrid/facturaia/blob/main/docs/manuals/manual-usuario.md) | Bloque 1 desactualizado (3 botones, abonos, pills) |
| Manual admin | [GitHub](https://github.com/AgentesIA-MAdrid/facturaia/blob/main/docs/manuals/manual-admin.md) | Bloque 1 desactualizado |
| Módulos producto | [docs/MODULOS-PRODUCTO.md](https://github.com/AgentesIA-MAdrid/facturaia/blob/main/docs/MODULOS-PRODUCTO.md) | Vivo |
| CLAUDE.md proyecto | `facturaia/CLAUDE.md` | Vivo |

## Specs detalladas (subfiles)

- [[facturaia-comunicaciones-emails]] — sistema emails Resend + auth Supabase, 5 PRs, reutiliza outbox/notifications/ai_module_suggestions
- [[facturaia-integracion-api-v1-portal]] — webhooks HMAC, outbox, Stripe-style sync con agency-portal
- [[facturaia-test-tanda-2-3]] — tests de tanda 2 y 3
- [[facturaia-arquitectura-multi-whatsapp-numbers]] — multi-tenant WhatsApp por org
- [[facturaia-bloque-4-agent-query-spec]] — copiloto IA multi-canal
- [[facturaia-open-banking-psd2]] — conexión bancaria PSD2
- [[facturaia-prompt-auditoria-dashboard]] — prompt reutilizable: auditoría dashboard (exactitud + mejoras + arquitectura + benchmarking Holded/Quaderno con foco IA)

## Workflows n8n (backups en `knowledge/projects/agentesia/n8n-backups/facturaia/`)

| Workflow | ID | Función |
|---|---|---|
| OCR Factura | `zf2la2N2YBXKQNKk` | Vision → estructurado |
| WhatsApp Receptor v2 | `zYcHHa8jWXB6dY5i` | Ingesta + intención |
| WhatsApp Verify | `LlBeZfa2P6mg13wc` | Verificación Meta |
| Voice Process | `KVk45rJARQk0EKaF` | Procesar audio |
| Voice Confirm | `5Q3pmag3XnIQOkQV` | Confirmación voz |
| Voice Correct | `Q1WB42g8GtyX3qnp` | Corrección voz |
| Email Polling | `dqvzeyeifTcNv50u` | Ingesta email |

---

## Links rápidos

- [GitHub repo](https://github.com/AgentesIA-MAdrid/facturaia)
- [App producción](https://facturaia.agentesia.world)
- [Dokploy](https://dokploy.agentesia.world)
- [Slack canvas Panel FacturaIA](https://agentesialab.slack.com/docs/T0ARXF0V31S/F0AV38CHYSJ) (`F0AV38CHYSJ`)
- [Canal Slack](https://agentesialab.slack.com/archives/pro-facturaia) (#pro-facturaia)
- WhatsApp público: `+34 919 93 26 18`

## Credenciales (refs en memoria, NO secrets aquí)

- Supabase FacturaIA → memoria `supabase-facturaia.md`
- Anthropic API key → memoria `anthropic-api-key.md`
- OpenAI API key → memoria `openai-api-key.md`
- WhatsApp config → memoria `whatsapp-facturaia.md`
- Gemini (backup) → memoria `gemini-api-key.md`

---

## Histórico de hitos

- **2026-05-12** Módulo Agente de cobros end-to-end + caos engineer audit (commits `b48d9cb` + `ad5d8a4` + `671b890`) — backend 8 migrations (065-073) + 9 libs TS + 11 endpoints + workflow n8n parcheado dos veces (init STOP detection + regex case-insensitive con tildes), UI 4 componentes Cobros + drawer notif rediseñado con chips/snooze + settings preferencias personales + 2 admin panels + Aging view en /emitidas. Tres auditorías independientes (6 agentes planning paralelos + 1 backend static + 1 caos engineer adversarial) → 8 fixes reales aplicados con ~50% falsos positivos descartados con razón. 256 tests. Migrations aplicadas prod. Mockup data seedeado. Endpoint cron operativo en Dokploy `*/15 * * * *`. **Pendiente externo**: aprobar plantilla Meta `cobros_recordatorio_v1` (24-72h Meta review) + envs `META_WHATSAPP_PHONE_NUMBER_ID` + `META_WHATSAPP_ACCESS_TOKEN` en Dokploy → entonces envíos reales. **Patrones aprendidos** (10 nuevos para CLAUDE.md): (a) useSyncExternalStore getSnapshot devolver valor cacheado, NO `Date.now()` directo → "Maximum update depth"; (b) Dokploy cron Command sin wrap + comillas DOBLES alrededor de `-H "x-service-key: $VAR"` (simples NO expanden); (c) SettingsView con useState getter + window check → hydration mismatch → useSearchParams + Suspense; (d) 9 plantillas hardcoded RD 1619/2012 auditable git, cuotas+template Meta SÍ editables admin; (e) Lost update concurrente JSONB → usar jsonb_set/operator `-` SQL atomic en RPCs, no read-modify-write TS; (f) Auditoría con DOS perspectivas: static analyzer + adversarial pen-test descubren cosas distintas; (g) Falsos positivos típicos auditor: regex con bytes invisibles que parecen `[ --]` pero son control chars, dedupe_key con kind+date sin entender que el helper usa (org_id, dedupe_key) UNIQUE; (h) DELETE de validation flag debe limpiar TODOS los campos derivados (no solo el flag), o re-validación usa valores stale; (i) Aging/dashboard queries deben tener límite temporal explícito en JOIN a tablas append-only (recordatorios, audit, etc.) o crecen linealmente con histórico; (j) Race opt-out vs send mid-flight: defensa segunda haciendo re-check ANTES del fetch externo, no solo en INSERT inicial; (k) Network error post-delivery Meta es CRÍTICO: necesita cool-down BD para evitar retry → doble envío real; (l) n8n IF regex node es case-sensitive por defecto — usar clases [Ss][Tt]... explícitas + cubrir tildes con [ÁA]
- **2026-05-11** Reorganización admin (sidebar + Salud + Config + mantenimiento) — 4 agentes paralelos planificaron (backend/frontend/security/product), síntesis aplicada en 1 sesión. Migración 064 `admin_audit_log` + reuso `system_config` para `maintenance_banner` y `read_only_mode`. 7 endpoints nuevos (5 admin + 1 público banner + features extendido). 14 componentes UI nuevos (tabs accesible + paneles config/system + banner global). Kill switch en `with-api-auth.ts` + `handler.ts` v1 con bypass superadmin + recovery path. Redirects en next.config para zero-breakage (URLs viejas siguen sirviendo). Cross-link Features ↔ Planes. 5 bugs columnas BD pillados en autorevisión antes de runtime. Lint/typecheck/build OK. Migración aplicada en prod (`psql $SUPABASE_DB_URL -f`). **Patrones aprendidos**: (a) 4-agente paralelo con expertise dispares produce planes convergentes; (b) importar páginas Next.js existentes como panel-components inside tabs view = zero breakage refactor pattern; (c) reutilizar tabla key-value existente (system_config) en lugar de crear singleton para configs relacionadas; (d) admin destructive actions requieren re-auth + typed phrase + auto-expire + bypass recovery path; (e) grep schemas BD antes de escribir endpoints — 5 mismatches detectados; (f) `Date.now()` durante render bloquea react-hooks/purity en React 19 strict; (g) Next 15 redirects vs imports = capas independientes (URL redirect no rompe import). **Diferidos**: email_log Fase A (recomendado SÍ próxima), AEAT health derivado (SÍ ~5min), comparador planes y feature flags globales (NO)
- **2026-05-11** Sesión grande módulos IA + observabilidad — (1) Módulos IA mejorados: OCR `auto_categorizar` + Conciliación `auto_marcar_cobradas` via triggers BD (migrations 060/061 cubren todos los callers n8n/manual/API v1/voice); Cashflow IA `{horizonteDias, incluirRecurrentes, umbral_alerta_caja}` con cron `/api/internal/cashflow-alerts` Opción B (chunks 10 + dedupe 24h + gate orgHasFeature); Copiloto `idioma` + `guardar_historial` con tabla `copiloto_conversaciones` (062) + gate `orgHasFeature('copiloto')` cerrando fuga billing preexistente + Topbar oculta botón + `AIAssistantHost` gatekeep evento global; ModuloConfig fix defaults `value !== undefined ? value : default` + error handling. (2) Observabilidad crons: tabla `cron_runs` (063), `withCronTracking` wrapper aplicado a 6 crons (webhook-dispatcher, check-vencimientos, cashflow-alerts, storage-quota-check, run-module-suggestions, verifactu-process — éste con auth custom `SUPABASE_SERVICE_ROLE_KEY`), panel `/admin/system/crons` con semáforo + tooltips con ejemplos reales + notif `cron_failed_<name>` a campanita. (3) Bug destapado: storage-quota-check fallaba semanal por env vacía → fix `parseMb`. (4) Auditoría: 6 agentes paralelos (2 rondas × 3 expertise) → 1 P0 + 3 P1 + 2 P2 aplicados, ~50% falsos positivos descartados con razón. Commits: `33d5c7c` + `164dd9a` + `19ee00f` + `3fefc3a` + `9892e4c` + `1b14779` + `5255547` + `d4b7566` + `d43f80d` + `6442182` (CLAUDE.md vault). 4 migrations aplicadas en prod. ADR-001 documenta decisión cron observability. **Patrones aprendidos** 6 learnings nuevos + 1 update + 9 reglas CLAUDE.md global + sección Vault Obsidian en CLAUDE.md proyecto
- **2026-05-10** Primera prueba E2E real WhatsApp del módulo voz — Borja envió audio "convierte el presupuesto a factura" → bot detectó intención correctamente y mostró botones, pero descubiertos 2 bugs UX en producción: (1) resumen con totales 0€ por iterar `data.lineas` que el agente no devuelve para `convertir_presupuesto` (fix con lookup HTTP a Supabase REST en `Parsear y Calcular Totales`); (2) matching estricto con dictado por voz fallaba ("manvel"≠"Manuel") y bot pedía "número exacto" en bucle (fix con system prompt: matching permisivo + 4 casos: 1 match / >1 candidatos numerados / 0 matches con últimos 5 abiertos / memoria conversacional para responder "1"/"2"). Commits `5cf48a3` + `6d41b9b` + `4e98d76` (manuales). Backups en ops/n8n-backups/. **Patrones aprendidos** documentados como 3 learnings nuevos: lista candidatos numerados + memoria conversacional vs error genérico (LLM ambiguity), parchear downstream o lookup recurso real al extender contrato JSON-out, verificar persistencia tras PUT con grep marker único (idempotency check defectuoso reportó OK sin aplicar). Pendiente: que Borja reintente la prueba con bot ya parcheado en producción
- **2026-05-10** Módulo Voz F1+F2 completo — convertir presupuesto por intención + admin completo. 12 commits a main: endpoints `/api/voice/find-presupuesto` + `convert-presupuesto` + `/api/internal/{voice-system-prompt,voice-chat-bindings}` + `/api/modules/generador_voz/{prompt,history,restore,preview,playground}` + `/admin/voice` (tabla overrides). 6 migraciones (053 voice_invocations, 054 voice_idempotency PK compuesta, 055 voice_chat_bindings, 056 voice_prompt_versions con RLS por org, 057 grants/purge, 058 pg_cron 03:00 UTC). Sistema híbrido del prompt: 12 variables tipadas + modo Avanzado override libre, template canónico HEADER/FOOTER inviolables. UI tab Configuración custom + tab Avanzado banner rojo + Playground con tokens/coste/historial + WAI-ARIA tabs completo. 5 bugs hardening detectados E2E: PGRST203 RPC overload (todas las conversiones rotas en prod), feature_gate ausente en find/convert, iva_pct sin .min(0).max(100), invalid_json devolvía 422 (debe 400), ocr-audit FK violation devolvía 500. Workflow `zYcHHa8jWXB6dY5i` patcheado vía API n8n: 64→67 nodos, +consultar_presupuestos toolCode + Es Conversion? IF + Convertir Presupuesto HTTP post-confirm. Backup en `ops/n8n-backups/`. **101 tests E2E reales contra Supabase prod (0 fail), 60/60 unit, lint/typecheck/build OK**. Pendiente push + deploy + activar generador_voz en orgs + phone en profiles antes de E2E real con Meta WhatsApp
- **2026-05-08** Suite E2E Playwright (`tests/e2e/`) — 3 proyectos: setup (login → storageState), smoke (4 paths críticos) y explorer (bot recorre app, rellena forms, clica tabs/filas/modales, captura console errors + HTTP 4xx/5xx + crashes). Output a `tests/e2e/report.json`. Comandos: `npm run e2e:smoke|e2e:explorer|e2e:report`. 2 bugs UI detectados y fixeados (commit `394a7ff`): (a) `/emitidas` y `/recibidas` 404 silenciosos por falta de guard `logo_url='not_found'` en `facturas-view.tsx:842,1082` (estaba en otros 4 sitios — bug por inconsistencia entre componentes); (b) `/ingesta` con 0 canales apuntaba a `/admin/connectors` (404), redirigida a `/settings?tab=integraciones`. CI verde tras fix `vitest.config.ts` (excluir `tests/e2e/**`). Re-run explorer post-deploy: 0 issues vs 8 antes. **Patrón aprendido**: cuando un guard `algo === 'sentinel_string'` se replica entre componentes, verificar TODOS los puntos de uso con grep
- **2026-05-08** PR #47 mergeado — audit log en marcar-cobrada/reenviar-email/anular/DELETE + idempotency en DELETE
- **2026-05-07** Sesión grande — 31 commits a main: 175 tests, withApiAuth en 19 endpoints, UI primitives, 14 modales role=dialog, FacturaMeta badges, tabs Facturas/Abonos, fix bug fiscal informes IVA, fix EstadoPill MAP, 3er botón "Emitir como pendiente", menú condicional por estado, CI integration job, RLS migration_037, .env.example expandido, migrations 047/048/049, deploy verde, 5 learnings + 5 reglas CLAUDE.md
- **2026-05-07** Voz WhatsApp en producción — 10 puntos verificados (e2e orgs, OCR receptor v2, presupuestos, textos WA, 403 toggles, modal series, duplicados BD, response limpio)
- **2026-05-07** Presupuestos/Proformas/Abonos completos — emisión funcional desde form manual + voz
- **2026-05-07** Secrets rotados — `fia_live_…` API key + `whsec_fia_…` webhook secret
- **2026-05-06** Sistema módulos premium completo — catálogo + add-ons + recomendador IA con 2 evaluators reales + activity feed + métricas + 137 tests Vitest
- **2026-05-06** Cron Dokploy recomendador IA configurado y validado (1 sugerencia generada para AgentesiaLab)
- **2026-05-02** Integración API v1 ↔ agency-portal — webhooks HMAC, outbox, Stripe-style sync, 7 PRs apilados
- **2026-04-28** Presupuestos/proformas/abonos voz + form manual; modal series builder; validación formato; invitaciones equipo; fix workflow voz abono; cleanup mockup AgentesiaLab
- **2026-04-27** VeriFACTU integración completa (QR en PDFs, AEAT)
- **2026-04-26** Billing banner + feature-locked rediseñados; datos fiscales completos clientes/proveedores; simplificación workflow voz WhatsApp
- **2026-04-25** Plantillas factura PDF pixel-perfect; system_config + admin config; security hardening; admin limits/storage fix; generador facturas voz desplegado; rediseño formulario nueva factura + email
- **2026-04-21** WhatsApp ingesta multi-tenant + Admin Panel + Feature Flags
