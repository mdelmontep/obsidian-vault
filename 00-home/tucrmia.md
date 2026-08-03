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

## Estado (03-ago, madrugada)

- **F0: 9 issues cerrados de 17; el panel VERIFICADO contra un servidor y la pantalla de salud
  construida.** Gate **22/973**, smoke de **16 contra el despliegue** y otro de **25 del panel**,
  18 migraciones aplicadas y verificadas contra el ACL efectivo. Desplegado: `80c4f59f`.
- ✅ **El panel (013), verificado de verdad: 25 de 25** contra `next start` y la base real. Y el
  bloqueo que lo tenía parado **no existía**: la Management API sirve las claves del proyecto con
  el PAT que ya estaba en 1Password. Ver
  [[las-claves-de-un-proyecto-supabase-se-piden-con-el-token-de-cuenta]].
- ⚠️ El smoke encontró **dos fallos en sí mismo**: sembraba `auth.users` con SQL, produciendo
  cuentas que salen en el censo y **no pueden entrar** sin un solo error
  ([[insertar-en-auth-users-a-mano-crea-cuentas-que-no-pueden-entrar]]), y una comprobación
  colgaba del `default` de una columna.
- ✅ **Pantalla de salud del sistema (014)**: build, crons con los cinco estados, el límite de tasa
  tal como está compuesto, y **lo que todavía no mira** como bloque de primera clase. Tres de los
  cinco bloques no tienen tabla y se declaran con un candado que obliga a borrarlos el día que
  exista.
- 🔴 **NADIE DISPARA NINGÚN CRON**, y lo destapó construir esa pantalla. Las tres purgas no las
  llama nadie, así que **`api_request_log` crece sin tope**. La pantalla lo dice en la cara desde
  hoy; el arreglo espera OK (P23).
- ✅ **Auditoría adversarial de composición**: 64 hallazgos, 13 supervivientes. **Seis gates decían
  proteger y protegían menos**, incluidos un `revoke` COMENTADO que satisfacía a G-S1 y acciones de
  superadmin sin permiso que se escapaban por la forma de exportarlas. Ver
  [[un-trinquete-que-cuenta-por-regex-tambien-cuenta-los-comentarios]] ·
  [[un-detector-que-enumera-sintaxis-se-queda-corto-comprueba-la-identidad]].
- ⚠️ **Quedan 49 hallazgos SIN REFUTAR**, dichos como «ni confirmados ni descartados». No darlos
  por buenos ni por descartados sin pasarlos por refutación.
- ✅ **Dos fallos silenciosos de meses**: el panel entero sin su tipografía —tres tokens que no
  existen, [[un-var-de-css-que-no-existe-no-falla-se-queda-con-lo-heredado]]— y la lista de
  pendientes mintiendo sobre el despliegue por mirar el entorno local. Gate nuevo **G-TOKENS**.
- ✅ **La auditoría dejó de dispararse por calendario**: `npm run auditoria:alcance` decide por lo
  que ha cambiado y sabe decir que no hace falta. Falta correr la lente `interfaz`, que nunca ha
  corrido.
- ✅ **La capa de derechos (012)** enchufada a los DOS canales con `G-S5`. ✅ **YA SE PUEDE ENTRAR**
  (alta manual + login por enlace de un solo uso). ✅ `truncate` tiraba el append-only en las doce
  tablas (migración `014`). ✅ El límite de tasa estuvo dos días construido y sin enchufar.
  ✅ `autoDeploy` funciona. ✅ Leído Dolibarr: siete huecos, cuatro tablas nuevas en F1.
- **Issue `015` POSTERGADO** y **`016` (correo) también**: los dos por I4, sin payload real el
  parser se lo inventa.

## Bloqueos

- 🔴 **P23 · nadie dispara los crons** — las tres purgas no se ejecutan y `api_request_log` crece sin
  tope. Recomendado: `pg_cron` para las purgas (son SQL puro, la base se llama a sí misma) y el
  mecanismo de TuFacturaIA para los diez crons de §14. **Falta tu OK a programar un borrado
  periódico en producción.**
- 🟠 **P24 · el proveedor de correo del 016** — propuesto Resend, que TuFacturaIA ya tiene rodado
  con su receptor de entregas. Sin clave no se manda un correo, y sin payload real el receptor
  choca con I4 igual que el 015.
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
[[un-plan-que-delega-en-un-sistema-que-no-existe-deja-el-producto-sin-puerta]] ·
[[un-var-de-css-que-no-existe-no-falla-se-queda-con-lo-heredado]] ·
[[insertar-en-auth-users-a-mano-crea-cuentas-que-no-pueden-entrar]] ·
[[un-detector-que-enumera-sintaxis-se-queda-corto-comprueba-la-identidad]] ·
[[las-claves-de-un-proyecto-supabase-se-piden-con-el-token-de-cuenta]] ·
[[un-trinquete-que-cuenta-por-regex-tambien-cuenta-los-comentarios]]

## Trampas conocidas

- El **pooler de Supabase no va desde la red habitual**: migraciones por Management API **registrando la
  versión a mano**.
- `application.one` de Dokploy **devuelve los secretos en claro**; usar `dokploy-safe.sh`.
- Mientras la URL sea HTTP, **sin datos reales de clientes**.
- El alta manual exige `CRM_BASE_URL` **sin defecto**: con uno, se emite un enlace a `localhost` para un
  cliente, o contra producción desde una prueba local.
