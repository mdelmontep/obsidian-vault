---
title: TuCRMIA
updated: 2026-08-05 (madrugada, cierre)
tags: [hub, tucrmia, crm]
---

# TuCRMIA — hub

CRM conversacional de AgentesIA. **Módulo activable de una plataforma**, con app y base propias.
Repo `AgentesIA-MAdrid/tucrmia` · local `~/Projects/agentesia-crm`.

**El contexto vive en el repo, no aquí.** Este hub es solo el índice desde el vault:
- `CLAUDE.md` — reglas y contexto que no se deduce del código. Se lee primero.
- `docs/plan/ESTADO.md` — progreso. **Fuente de verdad.**
- `docs/plan/PROMPT-CONTINUACION.md` — cómo retomarlo en otra sesión.

## Estado (04/05-ago, cierre de sesión)

- **F0: 11 issues cerrados de 17. F1 arrancado: primer issue de dominio real cerrado (018,
  pipelines y etapas).** Gate **22 comprobaciones, 1250 tests**, veinte migraciones aplicadas y
  registradas. Desplegado y comprobado: `76461cc6`.
- ✅ **017 CERRADO — outbox y webhooks salientes**: los cuatro endpoints que faltaban, firma HMAC,
  secreto cifrado en reposo, 9 comprobaciones nuevas en `smoke:v1` contra la base real.
- 🔴 **Incidente cerrado: el despliegue automático llevaba 17 commits fallando en silencio** —
  `package-lock.json` pinnaba un paquete npm (`flat-cache@6.1.24`) retirado del registro;
  invisible en local porque el build de aquí nunca vuelve a bajarlo. Ver [[incidents]] y
  [[lockfile-pinna-paquete-npm-retirado-del-registro-build-limpio-lo-revela]].
- ✅ **018 CERRADO — pipelines y etapas (E1.1)**: migración `020`, CRUD con TDD, pantalla de
  configuración, verificado en el navegador contra `tucrmia-prod` con una organización real.
- ✅ **Auditoría de composición del 4-ago (noche), registrada en `auditorias.json`**: 7 lentes
  sobre los 216 ficheros cambiados desde el 3-ago, **15 hallazgos y los 15 sobreviven** a dos
  escépticos independientes cada uno — ninguno refutado. Seis cerrados en la misma sesión: G-D11
  (identificador de tabla entrecomillado), G-S4 (secreto por corchetes), G-TOKENS (substring sin
  límite de palabra), un test tautológico del catálogo, la portada de `/admin` con el 012/014
  dados por pendientes, y tres mutaciones de pipelines sin `.select()` tras el `update` — mismo
  patrón D8 de TuFacturaIA, primera vez que reincide en este proyecto. Ver
  [[update-que-afecta-cero-filas-no-devuelve-error-en-postgrest]] y
  [[un-detector-que-enumera-sintaxis-se-queda-corto-comprueba-la-identidad]] (las tres del gate).
  **Quedan 9** que piden decisión de alcance, no arreglo mecánico — el mayor: el worker de
  entrega de webhooks del 017 no lo invoca nada del producto todavía.
- ✅ **009 portado** (sesión previa): los 45 componentes puros de `components/ui/`. **No cierra**:
  sigue bloqueado por la sesión de diseño con `impeccable`.
- ✅ **013 · impersonación**: la decisión construida y probada. Banner y `G-IMP` esperan a F1.
- **016 (correo) sigue postergado**, sin llamante real. **Proveedor decidido: SMTP genérico**
  (`nodemailer`, como TuFacturaIA), no Resend.
- ⚠️ **Backlog de la auditoría del 3-ago sigue abierto aparte**: 6 hallazgos confirmados sin
  cerrar y 33 sin refutar de esa tanda anterior, en `ESTADO.md` → «Hallazgos abiertos». No se ha
  tocado esta sesión — es distinto del backlog de 9 de la auditoría nueva de arriba.

### Hitos anteriores, condensados

- ✅ **012 CERRADO** (3-ago): planes verificados contra servidor, `smoke:admin` 31/31.
- ✅ **El sistema visual no se aplicaba desde el commit 1** (3-ago): los 86 tokens colgaban de
  `:root[data-theme]` sin que nadie escribiera el atributo. Ver
  [[un-token-definido-bajo-un-selector-que-nadie-produce-no-existe]].
- ✅ **Auditoría del 4-ago: 55 hallazgos, 22 refutados y sobreviven** (tope subido de 15 a 22:
  faltaba cobertura, no effort).

- ✅ **013 · panel de plataforma** verificado contra `next start` y la base real. El bloqueo que lo
  tenía parado no existía: la Management API sirve las claves con el PAT que ya estaba en 1Password
  ([[las-claves-de-un-proyecto-supabase-se-piden-con-el-token-de-cuenta]]). Su smoke encontró dos
  fallos en sí mismo, el peor sembrar `auth.users` con SQL
  ([[insertar-en-auth-users-a-mano-crea-cuentas-que-no-pueden-entrar]]).
- ✅ **014 · pantalla de salud**, y lo que destapó construirla: 🔴 **nadie dispara ningún cron**, así
  que las tres purgas no corren y `api_request_log` crece sin tope (P23). Los tres bloques sin tabla
  se declaran con candado en vez de pintarse vacíos.
- ✅ **Auditoría del 3-ago**: 64 hallazgos, **seis gates decían proteger y protegían menos**
  ([[un-trinquete-que-cuenta-por-regex-tambien-cuenta-los-comentarios]] ·
  [[un-detector-que-enumera-sintaxis-se-queda-corto-comprueba-la-identidad]]). Y el panel entero sin
  su tipografía por tres tokens que no existen → gate **G-TOKENS**
  ([[un-var-de-css-que-no-existe-no-falla-se-queda-con-lo-heredado]]).
- ✅ **La auditoría decide su alcance por lo que cambió**, no por calendario, y una lente nueva entra
  aunque su territorio no se haya tocado — que es lo que trajo el hallazgo del sistema visual.
- ✅ **Ya se puede entrar** (alta manual + enlace de un solo uso). ✅ `truncate` tiraba el append-only
  en las doce tablas (migración `014`). ✅ El límite de tasa estuvo dos días construido y sin
  enchufar. ✅ `autoDeploy` funciona. ✅ Leído Dolibarr: siete huecos, cuatro tablas nuevas en F1.
- **`015` POSTERGADO** y **`016` (correo) también**: los dos por I4, sin payload real el parser se
  lo inventa.

## Bloqueos

- 🔴 **P23 · nadie dispara los crons** — las tres purgas no se ejecutan y `api_request_log` crece sin
  tope. Recomendado: `pg_cron` para las purgas (son SQL puro, la base se llama a sí misma) y el
  mecanismo de TuFacturaIA para los diez crons de §14. **Falta tu OK a programar un borrado
  periódico en producción.**
- ✅ **P24 SUPERADA (4-ago): el correo del 016 va por SMTP genérico (`nodemailer`), no Resend.**
  El bloqueo de la clave de solo-envío de Resend ya no aplica — se decidió no usar un proveedor con
  webhooks de entrega. Coste aceptado: el criterio de rebote del 016 sólo caza el rechazo SMTP
  síncrono, nunca el diferido. El 016 sigue postergado igual, pero por falta de llamante real, no
  por esto.
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
- 🟠 **Onboarding Dani y Borja (04-ago)**: GitHub OK (`tecnocloudes`→write, `notcapi`→admin ya
  estaba) y claves de `tucrmia-prod` compartidas en 1Password (vault `TUCRMIA`, no en
  `Compartida Agentesia`). Trabajan los tres contra el único proyecto —sin datos reales de
  cliente todavía, así que el coste de compartirlo es bajo; revisar antes de F2/HTTPS. Falta:
  invitar a Borja al dashboard de Supabase (Dani ya está), confirmar que ambos son miembros del
  vault `TUCRMIA`, y que cada uno genere su propio `SUPABASE_ACCESS_TOKEN` en su vault personal
  —nunca en el compartido, ver
  [[guardar-token-personal-en-vault-compartido-de-equipo-comparte-tu-identidad]].

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
[[un-trinquete-que-cuenta-por-regex-tambien-cuenta-los-comentarios]] ·
[[un-token-definido-bajo-un-selector-que-nadie-produce-no-existe]] ·
[[no-restricted-imports-compara-el-texto-cierra-por-importnames]] ·
[[el-recuento-de-un-gate-sale-de-la-funcion-rota-y-miente-igual]] ·
[[guardar-token-personal-en-vault-compartido-de-equipo-comparte-tu-identidad]] ·
[[op-item-move-destination-vault-no-vault-private-resuelve-al-vault-real]] ·
[[guard-de-secretos-por-nombre-de-clave-bloquea-palabras-espanolas-que-contienen-la-inglesa]] ·
[[supabase-js-select-con-embeds-necesita-string-literal-no-concatenado]] ·
[[lockfile-pinna-paquete-npm-retirado-del-registro-build-limpio-lo-revela]] ·
[[exactoptionalpropertytypes-con-css-module-string-o-undefined-exige-coalescer]] ·
[[update-que-afecta-cero-filas-no-devuelve-error-en-postgrest]] ·
[[workflow-tool-args-array-llega-como-string-json-pasa-csv-plano]]

## Trampas conocidas

- El **pooler de Supabase no va desde la red habitual**: migraciones por Management API **registrando la
  versión a mano**.
- `application.one` de Dokploy **devuelve los secretos en claro**; usar `dokploy-safe.sh`.
- Mientras la URL sea HTTP, **sin datos reales de clientes**.
- El alta manual exige `CRM_BASE_URL` **sin defecto**: con uno, se emite un enlace a `localhost` para un
  cliente, o contra producción desde una prueba local.
