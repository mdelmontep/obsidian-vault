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

- **TuFacturaIA — 2 PRs de QA/compliance pendientes de revisión** — #639 (fix `/soporte` falso positivo + reload tras enviar presupuesto por email + doc de hueco real de descuento global) y #640 (verificación de 5 documentos legales PSD2/Centro Fiscal IA — CIF, ZDR OpenAI/Anthropic, subencargados — contra fuentes oficiales, no solo research). [[facturaia]]
- **TuFacturaIA — sección Documentos en admin (#642, mergeado 2026-07-02)** — legales PSD2/Fiscal (FNMT TSA, ZDR OpenAI/Anthropic, briefs abogado/seguro) visibles y descargables desde `/admin/documents`, con registro extensible para futuros docs. [[facturaia]]
- **TuFacturaIA — smoke WhatsApp G5 canary** — imagen + PDF desde 617314938 → confirmar OCR completa en bandeja (estado=listo). Bypass Traefik (`ce76acfd`) ya en main → smoke tras próximo deploy. [[facturaia]]
- **TuFacturaIA — /soporte: verificar #NNN + badge en admin (Manu)** — `/soporte` carga OK verificado en sandbox 2026-07-02 (bug del Dashboard arreglado); falta que Manu (superadmin) confirme `#NNN` + badge "IA revisando…" en `/admin/feedback` con un ticket de job activo (e2e+smoke no puede sin enviar feedback a soporte real). [[facturaia]]
- **TuFacturaIA — PR #641: detalle 130 mostraba nomenclatura del 303** — `CasillasTabla`/`ResultadoCard` no recibían `modelo` → "Casilla 71" + labels IVA en una declaración IRPF (cálculo OK, solo presentación). Fix pusheado; pendiente QA visual localhost del render 130 + merge. [[facturaia]]
- **TuFacturaIA — Slack completo (#002-#007c)** — todo en prod: OAuth, notifs, OCR, slash commands, bienvenida+modal OAuth, panel tip, created_via fix (#571). Pendiente: smoke escritura (vincular→`/factura cobrada`) + Manage Distribution (decisión negocio). [[facturaia]]
- **TuFacturaIA — smoke PRE Verifactu** — .p12 Gonzalo (~semana que viene) → validar namespace envelope SOAP + F1/F2 en prewww1.aeat.es. [[facturaia]]
- **TuFacturaIA — decidir ofrecer skin "Cristal" a usuarios** — QA contraste/APCA en pantallas densas hecho 2026-07-02 (sin fallos, oscuro+claro); queda solo la decisión de negocio de exponerlo. [[facturaia]]
- **TuFacturaIA — smoke prod #517 (auditoría enforcement canales)** — cuenta active sigue facturando/usando bot igual; cuenta suspendida recibe corte por canal voz/WA; verifactu cert solo admin. [[facturaia]]
- **TuFacturaIA — pagar GitHub Advanced Security (~16 jul 2026)** — si caduca el trial se apaga Code Quality (scan + gate PR). [[facturaia]]
- **TuFacturaIA — responder tickets** — Abba BORME (re-escanear 2 docs → gonzalo.riera) + bgchivite `1762f07e` (deploy #209 en prod). [[facturaia]]
- **TuFacturaIA — UX feedback pendiente** — smoke prod #528 (toast guardar empresa/plantillas) + #529 (modal glass confirmación cambio precio en `/admin/plans`). [[facturaia]]
- **TuFacturaIA — emails unificados (#527 en prod)** — deploy Dokploy ✓ (confirmado: el 500 email-copy lo probó), schema-cache transitorio resuelto. Falta: **logo real** + smoke prod del resto de emails + verificar texto humanizado de alertas en panel/email (`e1f4fd66`, sin QA visual). [[facturaia]]
- **Simarro — verificación E2E reserva tras recableo (06-25)** — 1 reserva por voz + 1 por WA → evento con calle+`location` + tarea Meeting + email. [[simarro]]
- **agency-portal — Pizarra/board PR #91** — review+merge Borja (aplica mig `board_comments`) + QA visual Manu local (`PORT=3002`). [[agentesia]]
- **Tecnocloud — PR #3 voice-webhook-tickets** — pendiente review Dani → smoke E2E con llamada real. [[tecnocloud]]
- **AGH Ibérica — tren cerrado (main `ee82131`); 3 trabajos desbloqueados, OK de Borja** — todas mis PRs (#8/#11/#14/#12) + #7/#10 mergeadas. Pendiente por hacer (PRs sueltas, cada una worktree+auditoría multi-agente+TDD, sin mergear): **(1) guardrails type-safety** — ESLint `no-explicit-any:error` + parsear JSONB `pending`/validar enums en `postgres-conversation-store.ts` (Borja: mételos tú; congelar antes de más código paralelo); **(2) resolver genérico nombre→id issue #32** — generaliza `ClientResolver` (Oportunidad/Consultor, absorbe Contacto de #10; NO romper firma pública); **(3) cabo #11** — cablear `task.create`/`reminder.schedule` como WriteExecutor en app.ts (vía libre). Prompt completo de los 3 preparado. **#13 (voz Retell) lo coge Borja** (Retell key + Dokploy ya montados). [[agh-iberica]]
- **EcoBox — smokes pendientes** — grúa/Mutua→handoff+email; reserva E2E que dispare `Build Emails`; chat hueco nuevo no-doble-booking. [[clientes/ecobox/index|ecobox]]
- **cryptobruj-bot — EN REAL, monitorizar** — scalp-5m/BTC BingX, tope $10, ~88 USDT; vigilar drawdown/ntfy. Revertir: `EXCHANGE_TESTNET=true`.

## Bloqueos (esperando a terceros)

- **TuFacturaIA — CI vuelve a correr (2026-07-01), billing ya no es el bloqueo activo** — jobs completan de nuevo (no mueren a 0 pasos). Lo que llevaba semanas roto detrás del billing eran **2 bugs de infra reales**: FK hardcodeada en mig 400 (abortaba el replay completo en BD fresca) + OOM de V8 en `typecheck`/`build` en runners grandes — ambos arreglados y mergeados (#634, #636), que además destaparon 6 regresiones de tests acumuladas sin CI. Si billing se re-bloquea, seguirá haciendo falta `gh pr merge --admin` (requiere OK explícito). Ver [[migracion-hardcoded-org-id-rompe-replay-fresh-db]] · [[ci-oom-typecheck-build-heap-explicito]].
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
| AGH Ibérica | [[agh-iberica]] | Agente comercial "Carlos" · **tren cerrado, todo en main (`ee82131`)** · pendiente: guardrails type-safety + resolver #32 + cabo #11; #13 voz (Borja) |

## Completado reciente

Ver `00-home/archive-completed.md` · histórico TuFacturaIA en [[facturaia-historico-detallado]]
