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

## Estado (03-ago, noche)

- **F0: 9 issues cerrados de 17; el 013 y el 012 construidos y desplegados.** Gate con **21 comprobaciones
  y 916 tests**, `db:replay`, **smoke de 16 contra el servidor desplegado** y las **18 migraciones aplicadas
  y verificadas preguntándole el ACL efectivo a la base**.
- ✅ **El panel de plataforma (013)**: censo, ficha, suspender/reactivar, `is_test`, personas, el alta como
  pantalla y los planes con excepciones. La frontera la impone el **compilador** —el cliente del panel no
  puede nombrar una tabla de dominio— y llegar a los datos exige pasar por la puerta que ya escribió la fila
  de `access_log`. Ver [[acotar-por-tipo-que-tablas-puede-tocar-una-zona-del-codigo]] y
  [[una-accion-de-servidor-de-next-es-un-endpoint-publico]], que fue el agujero menos evidente: el guard del
  layout protege lo que se pinta, no lo que se puede llamar.
- ✅ **La capa de derechos (012)** enchufada a los DOS canales con `G-S5`, que es lo que impide el fallo de
  TuFacturaIA —gate en el wrapper web, API pública saltándoselo, 13 de 90 rutas—. Motivo y caducidad de una
  excepción son `not null` en la BASE, no en un formulario.
- ⚠️ **`smoke:admin` está escrito (14 comprobaciones) y NUNCA ejecutado**: necesita la clave de servicio. El
  013 está construido y probado en unidad, **no verificado**. Es lo primero al retomar.
- ⚠️ **Regresión mía desplegada y corregida el mismo día**: el límite por IP contaba todas las peticiones y
  dejaba inalcanzable el de 600/min por clave. Ver
  [[un-limite-por-ip-que-cuenta-todas-las-peticiones-anula-el-limite-por-credencial]].
- **`npm run pendientes`** dice qué falta con una comprobación que se ejecuta, así que **se corrige solo**.
  **`npm run evals`** monta el harness de A16 y falla a propósito: el conjunto está vacío.
- ✅ **YA SE PUEDE ENTRAR.** Era el agujero de fondo: `ADR-002` delegó el alta en «la plataforma», que **no
  está construida**, así que con la API en producción y 705 tests en verde no había forma de que entrara
  nadie. Ahora hay alta manual (`scripts/alta-organizacion.mjs`, idempotente y verificada dos veces contra
  la base) y login por enlace de un solo uso. La primera pantalla enseña la organización **leída por el
  usuario con RLS filtrando**: primera vez que la base decide lo que ve una persona.
  Ver [[un-plan-que-delega-en-un-sistema-que-no-existe-deja-el-producto-sin-puerta]].
- ✅ **`truncate` tiraba el append-only en las doce tablas, y `db:replay` era ciego** (migración `014`).
  Ver [[truncate-salta-rls-y-sobrevive-al-revoke-de-update-y-delete]] ·
  [[el-replay-que-arranca-mas-limpio-que-produccion-es-ciego]].
- ✅ **El límite de tasa estuvo dos días construido y sin enchufar**, con todo en verde. Issue 008 cerrado,
  con gate estático. Ver [[una-proteccion-construida-y-no-enchufada-no-la-caza-ningun-test]].
- ✅ **Las 18 migraciones aplicadas y verificadas EN PRODUCCIÓN**, preguntándole a la base y no fiándose del
  script. ✅ `autoDeploy` funciona desde hoy (era el intermedio TLS del panel, no Dokploy). ✅ Leído Dolibarr:
  siete huecos en el modelo, cuatro tablas nuevas en F1.
- **Issue `015` (aprovisionamiento desde la plataforma) POSTERGADO**: dos tercios son código que lee lo que
  manda otro sistema, y sin un payload real el parser se inventa (I4).

## Bloqueos

- 🔴 **`SUPABASE_SERVICE_ROLE_KEY` en `.env.local`** — desbloquea `smoke:admin` y con él la verificación del
  013 entero. Está en el panel de Supabase, no en 1Password. Los scripts leen `.env.local` solos.
- 🟠 **`NEXT_PUBLIC_SUPABASE_ANON_KEY` en el panel de Dokploy** — sin ella el login responde
  `no_configurado` en el despliegue. Es **pública por diseño** (viaja al navegador). Un minuto, y el
  contenedor necesita redespliegue. La API v1 no se ve afectada, y eso es deliberado.
- 🟠 **Rotar la clave de la API de Dokploy**, que quedó en el historial de una conversación.
- 🟠 Sesión de diseño (índigo exacto, densidad, 4 pantallas) → bloquea el **009**. Manuel eligió que le
  prepare el material y elegir en 20 minutos.
- 🟠 **`ADR-004` está tomado provisionalmente**: confirmar que el acceso sin contraseña vale para sus
  clientes, y cuánto dura la sesión.
- 🟠 **P22 · los topes de la API ya activos en producción**: 600/min por clave y 1.200/min por organización.
  Confirmados provisionalmente; subir un tope no rompe a nadie, bajarlo sí.
- 🟠 **P24 y P25**: dónde está la raya entre «censo» y «datos de un cliente» (qué deja fila en `access_log`),
  y si el cliente puede ver quién de AgentesIA entró en sus datos. Las dos tomadas provisionalmente.
- 🟠 **P23 · el índigo** está tomado provisionalmente con contraste medido; los tokens ya están dentro con su
  gate `sync:shared` vivo. Falta el tono definitivo y los componentes.
- 🟠 Tres decisiones de `PREGUNTAS-PARA-MANUEL.md` §5.ter: obligatoriedad de `expected_close_date`, dueño
  del consentimiento y jerarquía de empresas. (Las dos de §5.bis siguen provisionales y ya aterrizadas.)
- 🟠 **La app sigue en HTTP**. Decidido el camino: **subdominio de un dominio propio en IONOS** con wildcard
  al VPS, en vez de esperar a `tucrmia.com`. Mientras siga en HTTP **no entran datos reales**, y las claves
  emitidas hasta entonces hay que rotarlas.
- 🟠 Registrar `tucrmia.com`, App Review y Access Verification de Meta → bloquean F2, no antes.

## Decisiones

- `ADR-001` — sin número de WhatsApp compartido: capacidades W0 (sandbox por org) y W2 (canal dedicado).
- `ADR-002` — es un módulo activable de una plataforma: alta, login y cobro dejan de ser nuestros.
- `ADR-003` — el CRM **no cobra**. Cierra P21, que ya no bloquea F1.
- `ADR-004` — **identidad propia por enlace de un solo uso** mientras no exista la plataforma. Sin
  contraseñas, que era el espíritu del `ADR-002`. Cuando la plataforma exista, la federación se añade **al
  lado** y este camino se queda como acceso de soporte. *Provisional.*

## Learnings de este proyecto

[[test-de-equivalencia-entre-artefactos-generados-es-tautologia-sobre-la-definicion]] ·
[[el-entorno-de-un-test-que-evalua-sql-emitido-no-se-escribe-a-mano]] ·
[[replay-de-migraciones-contra-un-postgres-desechable-en-docker]] ·
[[rls-multi-org-active-vs-membership]] ·
[[pooler-supabase-inalcanzable-aplicar-migracion-por-management-api]] ·
[[pipe-a-tail-enmascara-el-exit-code-del-comando]] ·
[[traefik-me-no-emite-certificado-por-cupo-compartido-agotado]] ·
[[dig-ns-vacio-no-significa-que-el-dominio-este-libre]] ·
[[truncate-salta-rls-y-sobrevive-al-revoke-de-update-y-delete]] ·
[[el-replay-que-arranca-mas-limpio-que-produccion-es-ciego]] ·
[[una-proteccion-construida-y-no-enchufada-no-la-caza-ningun-test]] ·
[[request-url-detras-de-un-proxy-trae-el-host-interno-del-contenedor]] ·
[[membresia-invitada-con-politicas-que-exigen-activa-entra-y-no-ve-nada]] ·
[[enlace-de-acceso-canjeado-en-el-servidor-con-hashed-token]] ·
[[un-plan-que-delega-en-un-sistema-que-no-existe-deja-el-producto-sin-puerta]]

## Trampas conocidas

- El **pooler de Supabase no va desde la red habitual**: migraciones por Management API **registrando la
  versión a mano**.
- `application.one` de Dokploy **devuelve los secretos en claro**; usar `dokploy-safe.sh`.
- Mientras la URL sea HTTP, **sin datos reales de clientes**.
- El alta manual exige `CRM_BASE_URL` **sin defecto**: con uno, se emite un enlace a `localhost` para un
  cliente, o contra producción desde una prueba local.
