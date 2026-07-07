---
title: AGH Ibérica — auditoría Tier 3 pendiente de ejecutar (prompt final embebido)
date: 2026-07-07
tags: [inbox, agh, auditoria]
---

Prompt escrito y pulido esta sesión (NO ejecutado). Tier de "red de seguridad + repetibilidad +
endurecimiento enterprise". **Cinco pistas ordenadas por peso** — HITL (G) y Observabilidad (H) son
las dos de mayor prioridad porque hacen que TODO lo demás sea seguro y auditable de forma repetible:

- **G — HITL correctness** (máxima): barrido EXHAUSTIVO "todo write executor + toda tool con efecto
  pasa por propose→confirm; ningún path ejecuta sin confirm". NO re-audit de Tier 1 — busca HUECOS
  DE COBERTURA nuevos, no re-lista el #217 ya arreglado. Es lo que ningún tier ha hecho completo.
- **H — Observabilidad & evals como sistema** (máxima): ¿el SCHEMA de la traza captura lo necesario
  para el error-analysis semanal (categorizar fallos, outcome de cada write, latencias, clarify-loops)?
  Sin esto ninguna otra auditoría es repetible.
- **I — Aislamiento multi-tenant (capa datos) + secretos/config** (alta): cada query scoped por
  tenant/owner (BOLA by-id #47), RLS, cifrado tokens M365, fail-closed config (#54).
- **J — Persistencia & integridad** (media): FKs/CASCADE/CHECK vs esquema real, migraciones, parse-
  don't-validate, transacciones multi-tabla.
- **K — Lifecycle & recursos** (media-baja): cierre pool/queue/worker en SIGTERM, fugas (síntoma
  #275), estructuras in-memory sin cota.

Harness Workflow 2-fases (5 finders paralelos + verify×3 lentes, ~50% FP), verificando contra el
**esquema real** de la BD (`pg_constraint`/`pg_policies`/`\d+`), `--maxWorkers=2`. Dedup vs cosechas
Tier 1 (#252-256) y Tier 2 (#260-268,#275). Slack: dar el texto para pegar, no enviar. Merge = Borja.

---

## Prompt Tier 3 completo (verbatim — copiar y ejecutar)

```
Ejecuta una AUDITORÍA ADVERSARIAL TIER 3 del agente comercial "Carlos" (repo agh-iberica,
cwd actual). Es el tier de "red de seguridad + repetibilidad + endurecimiento enterprise". Cinco
pistas ORDENADAS POR PESO — G (HITL) y H (observabilidad) son las dos de mayor prioridad porque
hacen que TODO lo demás sea seguro y auditable de forma repetible; si un finder tiene que recortar,
recorta de K antes que de G/H. Read-only → issues, sin fixes en la sesión (docs/agents/audit-process.md).

SETUP OBLIGATORIO (no negociable, aprendido de Tier 1 y Tier 2):
1. Corre TODO contra origin/main, NO contra la rama del cwd: `git fetch && git worktree add
   ../agh-audit-t3 origin/main` y audita ahí. Al terminar, `git worktree remove --force`.
2. Antes de filar cada hallazgo, dedup a conciencia: `gh issue list --state all --search "<keyword>"`
   y `git log --oneline`. Crúzalo TODO contra las cosechas Tier 1 (#252–#256) y Tier 2 (#260–#268,
   #275) + ~90 issues; comenta el issue existente si es faceta nueva de uno abierto. Regla dura del
   repo: cero duplicados. OJO: Tier 1 ya auditó HITL (sacó #217) — la Pista G NO re-lista lo suyo;
   busca HUECOS DE COBERTURA nuevos (paths sin gate), no re-reporta bugs ya arreglados.
3. Levanta pg (pgvector:pg16, 5433, user/pass, agh_dev) y redis (6380). Para I/J, INSPECCIONA EL
   ESQUEMA REAL (crea BD fresca, migra) — `\d+ <tabla>`, `SELECT conname,contype FROM pg_constraint`,
   `SELECT * FROM pg_policies` (RLS), `information_schema.columns`. Verifica, no teorices.
4. Suites con `--maxWorkers=2` (evita OOM y el flake de teardown #275).

HARNESS: Workflow de 2 fases (opt-in multi-agente). Fase 1 = 5 auditores en paralelo (Pistas G–K)
con salida estructurada. Fase 2 = por cada hallazgo, 3 verificadores adversariales con lentes
distintas (¿reproduce en main / en el esquema real? · ¿guard/constraint/test/RLS/gate existente lo
cubre? · ¿impacto real para AGH?); sobrevive si ≥2 de 3 no lo refutan. Asume ~50% de falsos
positivos; descártalos antes de reportar. Pásales a finders y a la lente de cobertura el digest de
issues ya trackeados para dedup en origen.

PISTA G — HITL CORRECTNESS (máxima prioridad · la red de seguridad de todo lo demás): barrido
EXHAUSTIVO, no muestral. Enumera TODOS los write executors (src/brain/writes/*: create-client,
create-contact, update-client, email-send, meeting, tasks-reminders, crm-write-executors) y el
registro del HitlBrain (src/brain/hitl-brain.ts, write-executor.ts, write-executor-registry) + toda
tool/servicio con EFECTO DE LADO (m365 mail-tool/calendar-tool → Graph POST; reminders; outbound;
provisioning/reset; stores). Para cada uno prueba la invariante: NADA con efecto externo o de
escritura se ejecuta sin un turno "confirm" explícito del humano. Busca el agujero: ¿algún
execute() alcanzable desde un turno que NO sea confirm (prepare que ya escribe, un read-tool que
muta, un prerequisite inyectado —#237/#155— que crea sin pasar por HITL, un batch donde un write
se ejecuta aunque otro se cancele)? ¿"correct"/"cancel" tienen semántica correcta (correct
re-ejecuta prepare #40; cancel limpia; un fallo de write limpia el pending #217 y no re-ejecuta)?
¿El pending es idempotente ante reintento/redelivery/reconexión (que no ejecute dos veces)? ¿La
propuesta caduca (#70) y un pending stale no ejecuta un write viejo fuera de contexto? El OWASP
LLM06 (excessive agency) es el marco: el gate humano es el único freno.

PISTA H — OBSERVABILIDAD & EVALS COMO SISTEMA (máxima prioridad · sin esto NINGUNA auditoría es
repetible): la pregunta no es "¿hay trazas?" sino "¿la traza captura lo NECESARIO para el
error-analysis semanal (cadencia #2 del audit-process)?". Revisa src/observability/langfuse-tracer.ts,
tracing.ts, gateway/inbound-pipeline.ts (donde se emiten los turnos). ¿El SCHEMA de traza permite
CATEGORIZAR fallos sin el texto del usuario?: reason de error (turn_error/unknown_identity/…),
outcome de CADA write (kind + status proposed/confirmed/executed/failed + last_error), latencia por
turno y por tool, clarify-loops (turnos que repiten pregunta), tool failures (401/403/timeout),
canal, tenant. ¿TODO fallo deja traza estructurada o hay paths que solo hacen console.error efímero
(nadie se entera en prod — busca los `console.error` sin traza asociada)? ¿La traza es una por turno
y estable (#148) o hay huérfanas? ¿El flag de contenido (#173) hace lo que dice y RGPD se respeta
(userId hasheado, sin texto/teléfono/externalId en trazas ni logs)? ¿Las EVALS opt-in (*.opt.test)
cubren los fallos reales reportados por los smokes/testers, o hay categorías de fallo sin caso oro?
¿Hay health/readiness y métricas mínimas, o el error-analysis se queda a ciegas? Hallazgo tipo: "el
error X no es distinguible del Y en la traza → el análisis semanal no puede contarlos".

PISTA I — AISLAMIENTO MULTI-TENANT (capa de datos) & SECRETOS/CONFIG (alta · crux enterprise, pura
novedad): por cada postgres store (postgres-{client,opportunity,consultant,contact,meeting,note,
task,reminder,conversation,onboarding,provisioning}-store, processed-message, whitelist,
recipient-resolver, m365/token-store) verifica que CADA query filtra por tenant_id Y owner/user
donde toca — NO solo el happy path: ¿las ops by-id (get/update/delete) llevan el backstop de owner
(#47) o un id filtrado lee/escribe cruzando tenant/usuario (OWASP API1 BOLA)?, ¿los resolvers
(store-{client,entity,consultant,internal-contact}) resuelven entidades de otro tenant?, ¿el recall
pgvector (meeting-recall-read-tool, note-store search) está scoped por tenant+user o trae notas de
otro comercial?, ¿RLS en Postgres o TODO depende de acertar el WHERE (una query sin filtro = fuga)?
Secretos: cifrado de tokens M365 en reposo (m365/crypto.ts, postgres-token-store) — de dónde sale la
clave, ¿en env?, ¿rota?; ¿secretos hardcoded/defaults inseguros?; oauth-state/pkce (entropía,
expiración, replay); fail-closed de config prod (#54); RGPD residencia del dato (el prompt al LLM
cruza el perímetro — escalones de arquitectura-rag-enterprise).

PISTA J — PERSISTENCIA & INTEGRIDAD DE DATOS (media): schema.sql vs realidad en BD: ¿toda tabla
tenant-scoped referencia tenants ON DELETE CASCADE (regla del repo)?, ¿FKs o relaciones solo por
convención (huérfanos)?, ¿CHECK para enums de estado (funnel stage, reminder #41, availability) o
texto libre?, ¿NOT NULL/UNIQUE donde toca (wamid, jobId, un onboarding por usuario)? Migraciones
(migrator, boot-migrate, drift, check-drift): idempotencia, forward sobre BD vieja vs HEAD (crash-loop
ADR-0002), drift no detectado. Parse-don't-validate en bordes (regla inviolable): JSONB pending y
filas de BD se PARSEAN o se castean a ciegas (`as`, JSON.parse sin validar)? Transacciones: writes
multi-tabla atómicos (meeting+nota #253 abierto — busca OTROS: contact+client, opportunity+candidate,
provisioning) o escritura parcial. Anti-patrón "integración crítica en JSONB pierde observabilidad".

PISTA K — LIFECYCLE & RECURSOS (media-baja): apagado (shutdown.ts, server.ts): ¿se cierran
pool/queue/worker en SIGTERM o quedan colgados?, fugas de conexión (síntoma #275), ¿estructuras
in-memory sin cota (in-memory-conversation-store, in-memory-processed-message-store sin prune vivo,
timers del scheduler, turnVoice/inFlight de retell, oauth-state) → fuga de memoria en proceso
long-running?, paginación del reconciler (#26), backpressure de BullMQ, ¿qué pasa si una dependencia
(BD/redis/gateway) está caída al arrancar (fail-closed vs zombie)?

SALIDA por hallazgo: severidad · tipo (a bug/b riesgo/c mejora) · pista · evidencia archivo:línea con
fragmento (para I/J, el resultado de la consulta a la BD real que lo confirma) · caso de fallo
(condición→esperado→real) · por qué el guard/constraint/RLS/gate/test existente NO lo cubre · impacto
para AGH (multinacional: agencia sin confirmar=acción no querida, error-analysis ciego, fuga entre
tenants, RGPD) · fix sugerido (no implementar; si toca schema.sql → migración versionada, no editar
el HEAD). Al final: resumen por pista + nº descartados. Fila issues (needs-triage, sin asignar) solo
de lo que sobrevive Y no esté ya trackeado. Flagea lo crítico en Slack #cli-agh-iberica ANTES de
filar y el resultado después — DA EL TEXTO PARA PEGAR, no envíes tú a Slack. Registro = los issues +
una línea en docs/PROJECT-STATUS.md (o su docs-PR). Merge lo autoriza Borja.

Fuentes: Anthropic — Demystifying evals (https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents),
OWASP LLM Top 10 2025 (LLM06 excessive agency para HITL; https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf)
y OWASP API Security Top 10 (API1 BOLA para aislamiento by-id, API8 config), Postgres RLS, y "parse,
don't validate" en los bordes.
```
