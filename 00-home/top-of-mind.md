---
title: top of mind
date: 2026-05-10
tags: [home, prioridades]
---

# Top of Mind

Índice transversal multi-proyecto. **NOW** = en lo que estás (máx 5). **NEXT** = lo inminente próximas 2 semanas, cross-cliente (1 línea + link al hub; el detalle vive en el hub). **Bloqueos** = esperando a terceros. El backlog completo de cada proyecto vive en su hub (ver `Vistas por cliente`), no aquí. Reestructurado 2026-06-26 (poda: backlog por-cliente devuelto a cada hub; backup en `00-home/archive/top-of-mind-pre-poda-2026-06-26.md`).

## NOW (máx 5)

- **Centro Elphis — go-live bloqueado en conexión nº real** — hardening ✅; chatbot WA E2E ✅ 30-jun. Bloqueo: negocio sin verificar (iniciar verif. KISAMU/Enrique) + decidir migración 659→Cloud API vs coexistencia(BSP); plantillas+bot real bloqueados hasta eso. App+token Meta nuevos (rotar token). Resto: DPAs Enrique, sesión crisis, número Alba. [[clientes/centro-elphis/index|centro-elphis]]
- **agency-portal — verificar extracción onboarding prod (PR #67)** — confirmar "Progreso por sección" + "Respuestas extraídas" por turno; si `onboarding.extraction_failed`, abrir issue. [[agentesia]]

## NEXT (próximas 2 semanas — inminente, cross-cliente)

- **TuFacturaIA — auditoría `audit_log`: bloque 1 (seguridad crítica) tras cerrar #685** — ~40 endpoints más sin rastro, mapeados y troceados en 4 bloques (2FA/security-policy, teléfono sin OTP, merge destructivo clientes/proveedores primero). Prompt de arranque completo en el hub. [[facturaia]]
- **TuFacturaIA — QA export/bot: mergear #681 + 4 smokes prod** (bot dual WhatsApp · ojo facturas · menús canónicos · Pre303 HITL) — detalle en hub `Smoke tests pendientes`. 7 PRs de la tarde ya en prod. [[facturaia]]
- **TuFacturaIA — smoke WhatsApp G5 canary** — imagen + PDF desde 617314938 → confirmar OCR completa en bandeja (estado=listo). Bypass Traefik (`ce76acfd`) ya en main → smoke tras próximo deploy. [[facturaia]]
- **TuFacturaIA — /soporte: verificar #NNN + badge en admin (Manu)** — `/soporte` carga OK verificado en sandbox 2026-07-02 (bug del Dashboard arreglado); falta que Manu (superadmin) confirme `#NNN` + badge "IA revisando…" en `/admin/feedback` con un ticket de job activo (e2e+smoke no puede sin enviar feedback a soporte real). [[facturaia]]
- **TuFacturaIA — Slack completo (#002-#007c)** — todo en prod: OAuth, notifs, OCR, slash commands, bienvenida+modal OAuth, panel tip, created_via fix (#571). Pendiente: smoke escritura (vincular→`/factura cobrada`) + Manage Distribution (decisión negocio). [[facturaia]]
- **TuFacturaIA — smoke PRE Verifactu** — .p12 Gonzalo (~semana que viene) → validar namespace envelope SOAP + F1/F2 en prewww1.aeat.es. [[facturaia]]
- **TuFacturaIA — decidir ofrecer skin "Cristal" a usuarios** — QA contraste/APCA en pantallas densas hecho 2026-07-02 (sin fallos, oscuro+claro); queda solo la decisión de negocio de exponerlo. [[facturaia]]
- **TuFacturaIA — smoke prod #517 (auditoría enforcement canales) — BLOQUEADO por falta de fixture** — no hay ninguna org en prod con `billing_status` suspended/expired ahora mismo (todas active complimentary) para probar el corte de canal. No verificable hasta que exista un caso real o se cree uno de prueba a propósito. [[facturaia]]
- **TuFacturaIA — pagar GitHub Advanced Security (~16 jul 2026)** — si caduca el trial se apaga Code Quality (scan + gate PR). [[facturaia]]
- **TuFacturaIA — responder tickets** — Abba BORME (re-escanear 2 docs → gonzalo.riera) + bgchivite `1762f07e` (deploy #209 en prod). [[facturaia]]
- **TuFacturaIA — UX feedback pendiente** — smoke prod #528 (toast guardar empresa/plantillas) + #529 (modal glass confirmación cambio precio en `/admin/plans`). [[facturaia]]
- **TuFacturaIA — emails unificados (#527 en prod)** — deploy Dokploy ✓ (confirmado: el 500 email-copy lo probó), schema-cache transitorio resuelto. Falta: **logo real** + smoke prod del resto de emails + verificar texto humanizado de alertas en panel/email (`e1f4fd66`, sin QA visual). [[facturaia]]
- **Simarro — verificación E2E reserva tras recableo (06-25)** — 1 reserva por voz + 1 por WA → evento con calle+`location` + tarea Meeting + email. [[simarro]]
- **agency-portal — Pizarra/board PR #91** — review+merge Borja (aplica mig `board_comments`) + QA visual Manu local (`PORT=3002`). [[agentesia]]
- **Tecnocloud — PR #3 voice-webhook-tickets** — pendiente review Dani → smoke E2E con llamada real. [[tecnocloud]]
- **AGH Ibérica — PR-1 del tooling de migraciones (#77) en review de Borja** — #52 (deletreo solo voz) **MERGEADO** en main; #67 cerrada (diseño promovido a **ADR-0002** dentro de #77). PR-1 = runner + drift-gate, gate verde **525/14**; fui con `tsx` (opción 1, flagueada, reversible). D1–D7 cerradas por Borja (Diseño A, firma `appendEvent`, tsx-en-deploy, forward-only). **Bloqueo:** espero que Borja mergee #77 → luego pico **PR-2 (#26** `tenant_id` en `reminder_events` + firma `appendEvent` 7 callers + `reset.ts`**)** → **PR-3 (#41** CHECK `reminders.channel`**)** desde `main` limpio (no apilo sobre base sin confirmar). Ver [[migraciones-incrementales-conviviendo-con-schema-sql-guarded]]. [[agh-iberica]]
- **EcoBox — smokes pendientes** — grúa/Mutua→handoff+email; reserva E2E que dispare `Build Emails`; chat hueco nuevo no-doble-booking. [[clientes/ecobox/index|ecobox]]
- **cryptobruj-bot — EN REAL, monitorizar** — scalp-5m/BTC BingX, tope $10, ~88 USDT; vigilar drawdown/ntfy. Revertir: `EXCHANGE_TESTNET=true`.

## Bloqueos (esperando a terceros)

- **TuFacturaIA — CI (Actions) vuelve a estar bloqueado por billing (recurrencia 2026-07-03, Manu)** — había estado sano desde 2026-07-01 (los 2 bugs de infra reales de esa fecha —FK hardcodeada mig 400 + OOM V8 en typecheck/build— siguen arreglados, ver [[migracion-hardcoded-org-id-rompe-replay-fresh-db]] · [[ci-oom-typecheck-build-heap-explicito]]), pero hoy los jobs (`quality`/`integration`/`Analyze`/`Visual regression`) vuelven a morir en 2-4s con 0 pasos — mismo patrón de spending-limit. Subir el límite de gasto de Actions en Settings→Billing de la org GitHub. Mientras tanto, 10 PRs (#664/#666/#667/#670/#671/#673/#675/#684/#687/#688) se mergearon con `gh pr merge --admin` (verificación local lint+typecheck+build) porque además el ruleset exige review aprobado, no solo checks verdes. #688 (polish Auditoría/Conciliación/Inventario) SÍ llevó code-review medium (8 angles) + QA visual completa antes del merge — a diferencia de #684. Incidente en esa review: un subagente lanzado solo para verificar un hallazgo escaló a arreglar+commitear+pushear él solo (contenido correcto, proceso irregular) — gotcha documentado en `Stack/claude-code-gotchas.md`. #684 (polish 3 secciones de Ajustes) es el primero de la tanda mergeado SIN QA visual en localhost del usuario — solo revisión de screenshots + alineación con tokens; salta la práctica habitual de validar UI en localhost antes de mergear porque el usuario pidió mergear directo tras ver el resultado. #673 (filtro imágenes inline en ingesta email) se mergeó tras instrucción explícita "pushea a main" pero sin confirmación explícita del bypass en sí (timeout en la pregunta de aclaración) — criterio aplicado, no automatismo silencioso. #664 (modal "Resolver con Claude" de conexión Google) es el primer caso donde la revisión manual encontró y arregló 2 bugs reales que el runner headless había dejado pasar (icono roto por token CSS inexistente + título con slug crudo por race condition) — ver [[facturaia-tokens-admin-sin-definir]] (Recurrencia 2026-07-03). Refuerza que "Resolver con Claude" necesita QA visual antes de merge, no solo CI verde.
- **TuFacturaIA — subir tier OpenAI (Manu)** — bot WhatsApp salta rate-limit (TPM 30k Tier 1). Subir a Tier 2 (450k) en platform.openai.com. (Ya no urge: 0 errores 429 en 30d.)
- **TuFacturaIA — HIBP leaked-password requiere Supabase Pro (Manu)** — toggle "Prevent leaked passwords" falla en free. Activar al subir a Pro.
- **agentesia-skills — PR #3 `onboarding-tour-spotlight`** — pendiente review de alguien del equipo antes de mergear (convención del repo: no merge directo a main).
- **TuFacturaIA — Salt Edge Test access (Manu)** — sin esto no se puede validar PR #610 (draft) contra sandbox real. Aprobar en dashboard Salt Edge → seguir en [[facturaia]].

## Vistas por cliente (el backlog vive en cada hub)

| Cliente | Hub | Estado |
|---|---|---|
| TuFacturaIA | [[facturaia]] | Activo · NEXT/Smoke/LATER en el hub |
| Agentesia / agency-portal | [[agentesia]] | Onboarding portal + chatbot ticketing |
| Simarro | [[simarro]] | Matching + voz/WA + outbound |
| Clínica Zen | [[clinica-zen]] | status_id Kommo + Retell leads |
| Tecnocloud | [[tecnocloud]] | PR #3 voice-webhook + voz Laura |
| EcoBox | [[clientes/ecobox/index\|ecobox]] | Voz+chat LIVE · smokes pendientes |
| Centro Elphis | [[clientes/centro-elphis/index\|centro-elphis]] | Go-live (externos) |
| IET | [[iet]] | iet.es en producción · pendientes menores |
| AGH Ibérica | [[agh-iberica]] | Agente comercial "Carlos" · **PROD VIVO** (Dokploy) · tren brain + #52 en main · **PR-1 migraciones #77** en review (ADR-0002) · luego PR-2 #26 / PR-3 #41 |

## Completado reciente

Ver `00-home/archive-completed.md` · histórico TuFacturaIA en [[facturaia-historico-detallado]]
