---
title: TuCRMIA
updated: 2026-08-03
tags: [hub, tucrmia, crm]
---

# TuCRMIA — hub

CRM conversacional de AgentesIA. **Módulo activable de una plataforma**, con app y base propias.
Repo `AgentesIA-MAdrid/tucrmia` · local `~/Projects/agentesia-crm`.

**El contexto vive en el repo, no aquí.** Este hub es solo el índice desde el vault:
- `CLAUDE.md` — reglas y contexto que no se deduce del código. Se lee primero.
- `docs/plan/ESTADO.md` — progreso. **Fuente de verdad.**
- `docs/plan/PROMPT-CONTINUACION.md` — cómo retomarlo en otra sesión.

## Estado (03-ago)

- **F0: 6 issues cerrados de 16.** El **006** completo salvo enchufar la idempotencia, y el **007** y el
  **008** construidos casi enteros. Gate con **17 comprobaciones y 673 tests**, `db:replay` contra un
  Postgres 17 real y un **smoke de 14 comprobaciones contra el servidor desplegado**.
- ✅ **Las trece migraciones aplicadas y verificadas EN PRODUCCIÓN**, preguntándole a la base y no fiándose
  del script: `service_role` inserta en `audit_log` y no puede `update` ni `delete`, `authenticated` no ve
  `cron_runs`, y el enum `audit_actor_type` trae los nueve actores del catálogo.
- ✅ **`autoDeploy` funciona desde hoy, y era un problema de TLS, no de Dokploy.** Al panel le faltaba el
  certificado intermedio: GitHub rechazaba el webhook con `x509` y `curl` en macOS lo salvaba, engañando.
  Cinco entregas muertas. Ver [[cadena-tls-incompleta-curl-en-macos-la-salva-y-engana]] y
  [[dokploy-guarda-en-su-bd-y-no-toca-el-disco]] — el arreglo estuvo **guardado e inerte** hasta la recarga.
- ✅ **El 405 y el 404 dejaron de salir de Next**, mudos y sin `X-Request-Id`. Ahora las tres cosas que
  responden bajo `/api/v1` comparten pipeline. Ver
  [[next-registra-handlers-exportados-por-desestructuracion]].
- ✅ **Leído Dolibarr por dentro** (411 tablas, 20 años en producción) para preguntarle qué le faltaba a
  nuestro modelo, no para copiarle nada: **siete huecos reales**, el peor que no había país en ningún sitio
  y `phone_e164` —la identidad del contacto y la clave de enrutado de WhatsApp— derivaba de una regla sin
  país. Cuatro tablas nuevas en F1. De ahí sale
  [[una-columna-deprecada-conserva-su-unique-y-sigue-rechazando-inserts]], con gate.
- Los tres agentes en paralelo **murieron mientras mutaban su implementación** y dejaron código roto en el
  disco: una mutación olvidada de nueve. Disciplina en [[claude-code-harness]].

## Bloqueos

- 🟠 **Rotar la clave de la API de Dokploy**, que quedó en el historial de una conversación.
- 🟠 Sesión de diseño (índigo exacto, densidad, 4 pantallas) → bloquea issues **009** y **011**.
- 🟠 **Cinco decisiones en `PREGUNTAS-PARA-MANUEL.md` §5.bis/§5.ter**: dirección postal y
  `contacts.tax_id` (**tomadas provisionalmente y ya aterrizadas en el plan** — cambiarlas cambia una
  migración de F1), obligatoriedad de `expected_close_date`, dueño del consentimiento, jerarquía de
  empresas.
- 🟠 **La app sigue en HTTP** (cupo de Let's Encrypt de `traefik.me` agotado; se arregla con dominio
  propio). Mientras siga así **no entran datos reales de clientes**, y las claves emitidas hasta entonces
  hay que rotarlas.
- 🟠 Registrar `tucrmia.com`, App Review y Access Verification de Meta → bloquean F2, no antes.

## Decisiones

- `ADR-001` — sin número de WhatsApp compartido: capacidades W0 (sandbox por org) y W2 (canal dedicado).
- `ADR-002` — es un módulo activable de una plataforma: alta, login y cobro dejan de ser nuestros.
- `ADR-003` — el CRM **no cobra**. Cierra P21, que ya no bloquea F1.

## Learnings de este proyecto

[[test-de-equivalencia-entre-artefactos-generados-es-tautologia-sobre-la-definicion]] ·
[[el-entorno-de-un-test-que-evalua-sql-emitido-no-se-escribe-a-mano]] ·
[[replay-de-migraciones-contra-un-postgres-desechable-en-docker]] ·
[[rls-multi-org-active-vs-membership]] ·
[[pooler-supabase-inalcanzable-aplicar-migracion-por-management-api]] ·
[[pipe-a-tail-enmascara-el-exit-code-del-comando]] ·
[[traefik-me-no-emite-certificado-por-cupo-compartido-agotado]] ·
[[dig-ns-vacio-no-significa-que-el-dominio-este-libre]]

## Trampas conocidas

- El **pooler de Supabase no va desde la red habitual**: migraciones por Management API **registrando la
  versión a mano**.
- `application.one` de Dokploy **devuelve los secretos en claro**; usar `dokploy-safe.sh`.
- Mientras la URL sea HTTP, **sin datos reales de clientes**.
