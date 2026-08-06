---
title: TuCRMIA
updated: 2026-08-06 (021 CERRADO — UI + dos bugs reales encontrados navegando + auditoría de composición)
tags: [hub, tucrmia, crm]
---

# TuCRMIA — hub

CRM conversacional de AgentesIA. **Módulo activable de una plataforma**, con app y base propias.
Repo `AgentesIA-MAdrid/tucrmia` · local `~/Projects/agentesia-crm`.

**El contexto vive en el repo, no aquí.** Este hub es solo el índice desde el vault:
- `CLAUDE.md` — reglas y contexto que no se deduce del código. Se lee primero.
- `docs/plan/ESTADO.md` — progreso. **Fuente de verdad.**
- `docs/plan/PROMPT-CONTINUACION.md` — cómo retomarlo en otra sesión.

## Estado (06-ago)

- **F0: 11/17. F1 con CUATRO issues de dominio cerrados (018/019/020/021).** Gate **1386 tests**,
  veinticinco migraciones. Desplegado: `9eb31cb7`.
- ✅ **021 CERRADO — campos personalizados (E1.4)**: sobre el motor ya construido (validación por
  delta, escritura canónica, gate G-D10), esta sesión construyó lo que faltaba para que fuera
  verificable en el navegador: pantalla `/ajustes/campos` (definiciones por tipo de entidad,
  opciones para select/multiselect con `key`/`data_type`/`code` inmutables tras el alta — D9,
  nunca se borra una opción —, y para leads una matriz pipeline×etapa que fija required/hidden) y
  botón "Campos" en la ficha de lead/contacto/empresa (oculto si la org no tiene ninguna
  definición), reusando `CampoPersonalizadoInput` ya existente. Construido con dos agentes en
  paralelo sobre ficheros disjuntos (pantalla de ajustes vs. fichas), núcleo de escritura y
  verificación por el hilo principal.
  **Dos bugs reales, encontrados verificando en el navegador contra `tucrmia-prod` con una
  organización de prueba real, no leyendo código**: `listarOpcionesDeCampos()` no filtraba
  `archived_at is null` (a diferencia de su hermana de un solo campo) — una opción archivada
  seguía ofreciéndose como elegible en la pantalla y en los modales; la escritura nunca estuvo en
  riesgo (`validateCustomFields()` ya la excluye por su cuenta), pero la UI mentía sobre qué estaba
  archivado. Y el modal de la ficha mandaba siempre el snapshot COMPLETO de valores al guardar, no
  el delta: `validateCustomFields()` revalida cualquier clave PRESENTE en el payload, así que
  reabrir la ficha de un lead con un valor bajo una opción ya archivada y pulsar "Guardar" sin
  tocar nada lo rechazaba — y de paso bloqueaba también cualquier otro campo del mismo formulario.
  Arreglado calculando el delta real contra los valores con los que se abrió el modal, con test de
  regresión en las tres features. Ver
  [[modal-que-reenvia-snapshot-completo-revalida-de-balde-valores-sin-tocar]].
  También encontrado antes de la UI: `OpcionDeCampo`/`listarOpciones()` no exponían `color`/`sort`
  reales (solo las mutaciones los aceptaban) — expuestos en el núcleo antes de delegar la pantalla.
- ✅ **Auditoría de composición del 6-ago, sobre los 80 ficheros del 021**: 19 hallazgos, los 19
  refutados, **17 sobreviven**. Cinco mecánicos arreglados en la misma sesión — el más
  transferible: **G-S4-ALIAS (ESLint) solo miraba el OBJETO de una llamada a método
  (`secreto.trim()`), nunca el nombre del MÉTODO** — `fila.obtenerTokenHash() === entrada`, con
  `fila` sin raíz sospechosa, pasaba limpio. Ver
  [[regla-eslint-de-secreto-en-llamada-a-metodo-debe-mirar-tambien-el-nombre-del-metodo]]. Los
  otros cuatro: estado vacío de `/leads` sin CTA, dos tablas sin wrapper accesible
  (`role="region" tabIndex={0}`), las siete subrutas de `/admin` sin `loading.tsx`, un comentario
  de `pii.ts` que afirmaba una cobertura RGPD que el array real no tenía.
  **Uno verificado con evidencia real y descartado, no en disputa ya**: si `DbDeCenso` puede
  llamar cualquier RPC de dominio sin GRANT — probado contra `tucrmia-prod` con la propia
  `service_role` key llamando `write_lead_custom_fields`: `42501 permission denied`. Hueco de
  tipos (TypeScript deja escribir lo que Postgres ya rechaza), no vía de escritura real.
  **Doce sin tocar, documentados en `PREGUNTAS-PARA-MANUEL.md` #27**: tres gates de seguridad
  (`admin-check.mjs`, `ratelimit-check.mjs`/`s5-check.mjs`) resuelven la procedencia por texto en
  todo el fichero, no por ámbito — misma familia que ya costó cara con G-RL-ENCHUFADO, exige AST y
  tests adversariales nuevos, no parche de una noche; dos latentes sin caso real
  (`s6-check.mjs`/`tokens-check.mjs`); uno de producto (kanban de leads sin alternativa de teclado
  a drag&drop).
- ✅ **Artifact huérfano, TERCERA vez, mismo patrón que `da457fcf…` en su día**: `f2541d7c…` no
  figuraba en `Artifact({action:'list'})` de esta cuenta, y republicar sobre esa URL fallaba con
  «could not verify the target page is not a review page» — pero mintar una publicación NUEVA sin
  `url` funcionó a la primera, confirmando que el servicio estaba arriba: era la URL, no el
  servicio (a diferencia de la rotura anterior del 5-ago, que sí era el servicio caído). Nueva URL
  `3204ff62…`, referencias actualizadas en `ESTADO.md`/`PROMPT-CONTINUACION.md`. **Lección
  aplicable a otros proyectos**: ante «could not verify...», probar SIEMPRE primero una
  publicación sin `url` antes de asumir servicio caído — si esa funciona, es la URL vieja la
  huérfana. Ver [[artifact-solo-lo-republica-la-cuenta-que-lo-publico]].
- ✅ **El estudio de harness que el 05-ago quedó encargado, hecho**: describe tautológico de
  `crm_can` eliminado, `scripts/sql/replay-asserts.sql` deja de ser territorio ciego de
  `auditoria:alcance`, gate nuevo **G-REPLAY-VIVO**, y `.githooks/pre-push` exige `db:replay` en
  verde al tocar esquema/acceso (fail-closed). Ver
  [[bloque-generado-para-gate-byte-a-byte-nunca-se-transcribe-de-memoria]].
- ✅ **021, motor (sesión previa a esta)**: migración 024 (esquema: cinco tablas + índice derivado
  `custom_field_index`, G2) y 025 (`write_lead/contact/company_custom_fields()`, `security
  invoker`, D6 resuelto con función Postgres). `validateCustomFields()` + `writeCustomFields()` +
  gate G-D10 + `custom-field-operators.ts` + integración en `moveLeadToStage()`. Ver también
  [[verifactu-rpc-atomico-cierra-race-transacciones-rest-separadas]] (variante security invoker).
  La UI que le faltaba a esto y los dos bugs que salieron al construirla están arriba, en el
  cierre del 021.
- ✅ **020 CERRADO — contactos y empresas (E1.3)**: migración 023 (`countries`/`contact_roles`
  globales, `contacts`/`companies` con `phone_e164` normalizado, `company_contacts`/`lead_contacts`
  con `is_primary` único parcial), aislamiento del teléfono entre organizaciones **por clave
  compuesta `(org_id, phone_e164)`** en vez de un guard de upsert — ver
  [[clave-compuesta-por-tenant-elimina-el-guard-de-upsert-cross-tenant]]. **Encontrado y arreglado
  navegando, no leyendo código**: la edición inline del teléfono borraba email/NIF/dirección en
  cada envío parcial (F12 del catálogo, palabra por palabra). Verificado en el navegador contra
  `tucrmia-prod` con organización real de punta a punta.
- ✅ **Los dos backlogs viejos de auditorías (9 hallazgos de alcance del 4-ago, 49+33 sin refutar
  del 3-ago) y G-COLUMNAS-REALES, cerrados** por su proceso propio: los 9 con decisión documentada
  (2 quedan como `PREGUNTAS-PARA-MANUEL.md` 23/24, producto), los 49+33 declarados
  IRRECUPERABLES (la lista de candidatos nunca se persistió, solo el recuento — "reanudar" habría
  sido auditar desde cero) con la cifra que faltaba para decidir si vale la pena: **141 ficheros de
  aquellos dos audits siguen byte a byte idénticos hoy**, sin que ninguna auditoría de alcance
  posterior los haya vuelto a mirar (`PREGUNTAS-PARA-MANUEL.md` 25, tu decisión de coste). Y un
  hallazgo nuevo y crítico de la sesión: el test que dice comprobar `crm_can()` contra fugas
  cross-org es tautológico —compara dos constantes del propio test, nunca evalúa el SQL real—
  porque el evaluador JS del repo no sabe interpretar el guard de membresía todavía
  (`PREGUNTAS-PARA-MANUEL.md` 26, también tuya).
  Ver [[bloque-generado-para-gate-byte-a-byte-nunca-se-transcribe-de-memoria]] (lección de la
  migración 023, al empalmar el bloque `crm_can()` generado).
- ⚠️ **Tablero caído por segunda vez el 5-ago, sin resolver** — el servicio de Artifacts devolvía
  "could not verify..." incluso al publicar sin URL previa (no es problema de propiedad, es el
  servicio). `ESTADO.md`/`tablero.html` están al día en el repo (`77db909f`); falta reintentar
  `Artifact publish` cuando el servicio vuelva. Ver
  [[artifact-solo-lo-republica-la-cuenta-que-lo-publico]].
- ✅ **Dos auditorías de composición del 5-ago (sesión anterior), sobre el árbol del 019 y sobre
  «Hallazgos abiertos» del 4-ago**: cerraron G-S5, G-S4 (ESLint de una pasada), G-ADMIN-SQL,
  G-ROUTE-WRAPPER, G-ADMIN-ACCION, G-S6 y G-ACCESS-DRIFT (comparar por tabla contra la salida real
  del generador, no solo entre migraciones con marcador). Ver
  [[un-detector-que-enumera-sintaxis-se-queda-corto-comprueba-la-identidad]] ·
  [[typescript-import-type-y-declaracion-local-mismo-nombre-si-conflictan]].
- ✅ **Coordinación de equipo por Slack, desde el 5-ago**: canal `#crm-agentesia`, canvas de
  referencia. Reclamar issue antes de empezar, avisar con el resultado al terminar/bloquear — regla
  en `CLAUDE.md`. Ver [[slack-create-canvas-no-se-liga-a-un-canal-ni-hay-tool-de-pin]].
- ✅ **019 CERRADO — leads y kanban (E1.2)**: migración `022` (`position numeric(20,10)` X30,
  `status`, `amount`, `custom_fields`...), `moveLeadToStage()` (D6/D8), kanban con arrastre HTML5
  nativo (sin librería nueva) y rollback visual (F3) probado con un test de componente. **X30
  medido de verdad**: `npm run smoke:x30` siembra 1.000 leads en producción y confirma que
  arrastrar la última a la primera posición escribe una sola fila (`updated_at` intacto en las
  999 restantes), rojo demostrado forzando el rebalanceo siempre. Verificado en el navegador con
  una organización real — encontró que `crearLead` no fijaba `owner_id`, bloqueado en silencio por
  RLS con la visibilidad por defecto. Ver
  [[rls-insert-con-visibilidad-own-por-defecto-exige-owner-id-del-que-escribe]].
- ✅ **`ADR-005` cerrado**: un usuario no puede estar activo/invitado en dos organizaciones a la
  vez — índice único parcial en `org_members` (migración 021), no `unique` a secas (una baja se
  conserva como historial). Cierra la puerta a un flujo de multi-organización por usuario que
  nunca se llegó a construir.
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
- ⚠️ **Backlogs viejos de auditorías del 3-ago, sin tocar y probablemente IRRECUPERABLES**: 49
  hallazgos sin refutar de una tanda y 33 de otra (mal etiquetada "4-ago" en la prosa de
  `ESTADO.md`, pero es del 3-ago por commit). Comprobado el 5-ago: la lista real de candidatos no
  se persistió en ningún fichero, solo el recuento — "refutarlos" hoy sería auditar desde cero,
  no reanudar. Distinto de los 9 de la auditoría del 4-ago (esos sí tienen decisión de ALCANCE
  pendiente, no de refutación, y están en `ESTADO.md` → «Ahora mismo»).

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
- `ADR-005` — **un usuario, una organización activa a la vez**: índice único parcial en `org_members`
  (`where status <> 'disabled'`, no `unique` a secas — una baja se conserva como historial). Cierra
  `issues/011` sobre "cambio de organización activa": con esta decisión, no hace falta esa pantalla.

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
[[workflow-tool-args-array-llega-como-string-json-pasa-csv-plano]] ·
[[rls-insert-con-visibilidad-own-por-defecto-exige-owner-id-del-que-escribe]] ·
[[artifact-solo-lo-republica-la-cuenta-que-lo-publico]] ·
[[typescript-import-type-y-declaracion-local-mismo-nombre-si-conflictan]] ·
[[slack-create-canvas-no-se-liga-a-un-canal-ni-hay-tool-de-pin]] ·
[[clave-compuesta-por-tenant-elimina-el-guard-de-upsert-cross-tenant]] ·
[[bloque-generado-para-gate-byte-a-byte-nunca-se-transcribe-de-memoria]] ·
[[verifactu-rpc-atomico-cierra-race-transacciones-rest-separadas]] (variante security invoker) ·
[[gate-por-git-ls-files-no-ve-un-fichero-nuevo-sin-git-add]]

## Trampas conocidas

- El **pooler de Supabase no va desde la red habitual**: migraciones por Management API **registrando la
  versión a mano**.
- `application.one` de Dokploy **devuelve los secretos en claro**; usar `dokploy-safe.sh`.
- Mientras la URL sea HTTP, **sin datos reales de clientes**.
- El alta manual exige `CRM_BASE_URL` **sin defecto**: con uno, se emite un enlace a `localhost` para un
  cliente, o contra producción desde una prueba local.
