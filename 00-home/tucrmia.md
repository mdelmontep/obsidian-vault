---
title: TuCRMIA
updated: 2026-08-15 iteraciones 21-23 (auditoría de composición entera: 96 hallazgos, 32 en pie, drenados a issues 106-117 · `meta` 147 · 096 cerrado: la PII del outbox sobrevivía al derecho al olvido · siguiente: 106 o 104)
tags: [hub, tucrmia, crm]
---

# TuCRMIA — hub

CRM conversacional de AgentesIA. **Módulo activable de una plataforma**, con app y base propias.
Repo `AgentesIA-MAdrid/tucrmia` · local `~/Projects/agentesia-crm`.

**El contexto vive en el repo, no aquí.** Este hub es solo el índice desde el vault:
- `CLAUDE.md` — reglas y contexto que no se deduce del código. Se lee primero.
- `docs/plan/ESTADO.md` — progreso. **Fuente de verdad.**
- `docs/plan/PROMPT-CONTINUACION.md` — cómo retomarlo en otra sesión.

## Estado (15-ago, iteraciones 21-23) — la auditoría que se debía, y el registro mintiendo sobre la parada

**Desplegado y al día en `7d4c4a9f`.** Gate **63 pasos / 376 ficheros / 5.073 pruebas**. `db:replay`
verde sobre **72** migraciones aplicadas. `meta` 113 → **147**.

**La auditoría de composición que la iteración 19 dejó a deber se hizo entera**: 10 lentes, 85 ficheros,
77 agentes, **96 hallazgos · 33 refutados · 32 en pie**, y con `lentesCaidas: []` / `sinVeredicto: []` /
`sintesisCaida: false`. Esas tres marcas se escribieron precisamente porque la del 19 murió entera y el
guion devolvió «no encontraron nada»: hoy son lo que certifica que el cero es un cero de «se miró».
**Drenados el mismo día a `issues/106`–`117`.** `meta` sube 34 porque los 32 pasan a contarse como deuda
abierta y las 12 fichas entran en la cola — deuda que ya estaba, sin contar.

**Dos críticos, ninguno explotado hoy**: `clienteDeServicio()` entrega el `SupabaseClient` **entero**
—`.auth.admin`, `.storage`, `.schema`— a los ~20 módulos de `core/`, cuando `core/admin` ya cerró esa
superficie con `Pick` + candado en ejecución (`ADR-015`); escrito en un endpoint público emitiría sesión
de cualquiera sin fila en `access_log`. Y el derrame de literal **con cero claves propias** vuelve a
apagar los tres gates de la puerta v1 — el arreglo del 15-ago por la mañana cubría sólo la variante de
una clave. → [[un-gate-que-exige-n-claves-se-apaga-trayendo-el-resto-con-spread]]

**`096` cerrado, y es el de más daño del mes**: el derecho de supresión **no alcanzaba el sobre del
outbox**, donde el correo, el teléfono, el E.164, el NIF y la dirección viajan copiados verbatim.
Migración `087` en producción. Rojo demostrado antes con el dato impreso. Y ampliar la función **borró
en silencio** la supresión de los mensajes, porque partí de la migración donde nace en vez de la última:
lo cazó una aserción que EJECUTA. → [[create-or-replace-copiar-de-version-vigente]]

**`100` cerrado**: cinco gates que vigilaban menos de lo que su cabecera prometía. En cada uno la
evidencia es que **el gate viejo salía verde sobre el mismo fichero real** — el embed de PostgREST, el
alias del `update`, «definido» tratado como global en CSS, y dos funciones que tocan disco sin un solo
test. → [[un-guard-sobre-sql-tiene-que-conocer-el-embed-y-el-alias-de-postgrest]] ·
[[un-fail-closed-cuenta-la-fuente-que-puede-fallar-no-el-agregado]]

⚠️ **Y cinco hallazgos apuntaban a este proyecto hablando de sí mismo, los cinco ciertos.** El peor: la
iteración 22 cerró declarando `meta` **111** con el comando imprimiendo **113** — medí antes de
commitear. → [[la-metrica-de-estado-se-mide-despues-de-commitear]]. Los otros: el tablero decía 16
épicas sobre 15 y se republicó cinco veces sin recontar; `db:replay` anclado a un commit anterior a la
087; `LOOP-CIERRE` declaraba 9 señales sobre 10; y su paso 9 enumeraba 6 smokes de 11.

⚠️ **Un error de método, anotado porque es el patrón que este repo persigue**: empujé sobre un gate en
rojo (`gate` → 1 → `commit --no-verify` → `push`, log leído después). Era el flake de `issues/104`, que
sube por delante de las fichas de arnés sin víctima.

**Siguiente**: `106` (la clave sin valla, crítica y hoy sin coste) o `104`. Cola en **19**.

## Estado (15-ago, iteraciones 15-16) — mensajería, y la auditoría con 32 confirmados

Condensado. `049` cerró el núcleo de mensajería entero (seis tablas, dos funciones `security definer` y
el canal `sandbox` que las escribe, para no dejar la quinta pieza construida y desenchufada), verificado
con `smoke:mensajeria` 20/20 contra producción y **no** en navegador, porque el issue no traía pantalla.
Tres gates nuevos: G-SANDBOX-SIN-RED, G-MSG-DUENO y G-SINTAXIS
([[citar-el-delimitador-dentro-de-su-propia-region-la-cierra-ahi-mismo]]). La auditoría de la 16 dio 97
hallazgos con 32 confirmados; su corrida murió a mitad y lo primero fue **persistir desde el journal**
([[workflow-cortado-a-mitad-los-resultados-viven-en-journal-jsonl]]). De ahí salieron el derrame que
apagaba tres gates y el `onBlur` que borraba el NIF de una empresa en producción
([[el-hermano-tiene-el-mismo-bug-y-su-fixture-nace-nula-asi-que-nadie-lo-ve]]). Detalle día a día en
`docs/plan/ESTADO.md` del repo.

## Estado (14-ago, cierre) — F1 sin issues cogibles; la siguiente unidad es la mensajería

**Desplegado y al día en `c642cfa2`.** Gate **58 pasos / 363 ficheros / 4.882 pruebas**. `meta`
**113**, cola en **3** — y de las tres, `049` (núcleo de mensajería, E2.1) es la única que puede
coger un agente: `015` está bloqueado por fuera y `082` es de Manuel.

**`090` cerrado, y la lección no es la línea del arreglo.** La importación no escribía ni una ficha
en producción por no pasar `ownerId` —el estado por defecto de toda organización nueva— y lo
anunciaba en caja verde. Lo que cerró el issue fueron las **cuatro capas que lo tapaban** y una
aserción contra Postgres real, que es el único sitio donde puede volver a romperse sin que nada
avise: ni el gate estático lee políticas ni el doble las evalúa.
Ver [[una-ruta-de-escritura-secundaria-falla-solo-bajo-rls-y-solo-en-el-caso-por-defecto]].

**Cuatro instrumentos daban por bueno lo que no habían mirado, y los cuatro en verde.** El catálogo
de enums con dos dueños pintando el equivocado (`091` → `enum-huerfano:check`); un valor CSS
inválido que el navegador tiraba entero (`092` → G-CSS-VALIDO,
[[un-valor-css-invalido-tira-la-declaracion-entera-y-stylelint-lo-caza]]); la señal de recorridos
contando verde lo que nunca preguntó si pasó (`ADR-013`,
[[un-registro-de-ultima-corrida-cuenta-verde-lo-que-nunca-pregunto-si-paso]]); y un smoke que dejó
mil leads en producción diciendo que limpió — **segunda vez del mismo fallo**, así que gate y no
parche (`093`, [[una-limpieza-multitabla-en-una-sola-query-es-todo-o-nada]]).

**Al escribir esos gates salieron las dos trampas del árbol de sintaxis** —el falso verde de la
clave citada en una referencia de TIPO, y el falso rojo de castigar que extraigas un ayudante—:
[[dos-trampas-al-escribir-un-gate-por-arbol-de-sintaxis]].

**Recorridos**: siete corridos contra producción y verdes. Quedan **cinco caducados**, y conviene
saber por qué antes de alarmarse: cuatro sólo porque el commit tocó una rama de traducción de
errores que no ejercen —territorio generoso a propósito—, y el quinto,
`ajustes-y-baja-de-organizacion`, lleva **dos corridas seguidas** sin poder ejercer su segunda
mitad por falta de una cuenta de superadmin de plataforma: a la tercera le toca cuarentena
declarada, no sumar uno cada noche.

**Antes, ese mismo día**: la `083` aplicada (68 versiones), con la parte B de la 068 pasando de cero
a dieciséis aserciones — su primera versión estaba rota de una forma que ningún gate estático ve
(`returns table` con `email text` sobre `citext`) y la cazó `db:replay`:
[[pg-returns-table-no-lleva-tipos-ni-nulabilidad-y-eso-explota-al-ejecutar]]. Más el quinto
«construido y sin llamante» enchufado, una corrección de tipos que compilaba sin proteger nada
([[una-correccion-de-tipos-sobre-un-parser-que-recibe-unknown-es-inerte]]), y los recorridos `089`
y `080` verdes comprobando **contando filas** y no leyendo el chip
([[verificar-un-filtro-traducido-es-contar-filas-no-leer-el-chip]]).

**Para arrancar otra sesión multiagente**: `docs/plan/ARRANQUE-MULTIAGENTE.md` en el repo. No copia
cifras a propósito — las deriva de `ESTADO.md`, `npm run meta` y los `Status:`.

## Estado (11-ago) — los 124 hallazgos juzgados, y la API v1 con puerta de entrada

**De 124 hallazgos sin juzgar a 1 abierto, en cuatro iteraciones del bucle.** 120 escépticos en
tres tandas, dos por hallazgo con ángulos distintos: **76 en pie por unanimidad, 23 divididos, 25
refutados**. Falsos positivos reales del 20 %, no el 50 % que suponíamos — y la prueba de que
medía el árbol de hoy es que los cuatro que los commits del día anterior ya habían arreglado
salieron refutados solos. Queda `#13`: la impersonación que ninguna superficie usa.

**La API v1 tenía 27 rutas y ninguna forma de pedir una llave** (`issues/077`): `issueApiKey` la
llamaban sólo los dos scripts de smoke. Séptima aparición de «escrito no es enchufado» y la más
cara — lo desenchufado era la entrada de una épica entera. Ya está en `/ajustes/api`: la
credencial se enseña **una vez** porque la base sólo guarda el hash, el derecho vive en la ACCIÓN
y no en el layout, y la pantalla **avisa cuando el alcance elegido no alcanza ninguna fila** (una
clave válida que devuelve listas vacías con 200 se lee igual que «no hay nada»).

**Cinco gates nuevos en cuatro noches**, todos de fallos ya ocurridos: `ratchet:tamano`
(G-TAMANO) y `tipos:check` (G-TIPOS-CERRADOS) —los dos llevaban tiempo escritos en el plan **sin
existir en el disco**, el patrón P8—, `deps-v1:check` (G-DEPS-ENCHUFADOS), más G-CAT R5 y
G-CRON-DESPROGRAMADO. Y una lección de método:
[[un-gate-de-enchufado-no-se-copia-entre-huecos-que-se-rellenan-distinto]].

**Lo que encontró EJECUTAR y no leer, tres veces seguidas**: `smoke:x30` llevaba semanas sin
arrancar (su resolutor no conocía el alias `@/`, moría en el `import`); la frontera entre zonas se
saltaba con una ruta relativa mientras el alias sí se bloqueaba; y 🔴 **el smoke de la v1 llevaba
desde la migración 066 dejando en producción todo lo que sembraba** →
[[una-limpieza-multitabla-en-una-sola-query-es-todo-o-nada]]. El recorrido en navegador aportó lo
suyo: [[rejilla-de-casillas-con-el-distintivo-en-un-span-hermano-deja-n-controles-con-el-mismo-nombre]].

**Decisiones del bucle sin Manuel**: `ADR-007` (un trabajo periódico sin nada que hacer se
desprograma — escribía 96 filas `failed` al día) y `ADR-008` (cuándo puede subir la línea base de
un trinquete, con lo que NO autoriza escrito).

🔴 **Tuyo**: borrar las **7 organizaciones de prueba** que quedaron en producción — `npm run copia`
primero y deja de ser irreversible (`issues/082`) —, el ticket del `grant` de Storage, el *Email
Log Search* de Workspace y el secreto viejo de Google.

## Estado (10-ago, tarde) — F1 de verdad, desplegado, y la auditoría que no llegó a juzgar

**Seis épicas de F1 en un día, doce agentes en paralelo sobre ficheros disjuntos**: formulario web
con consentimiento versionado (`E1.21`), doble factor y sesiones (`E1.23`), exportación y retención
(`E1.24`), catálogo de 37 métricas (`E1.25`), contrato v1 operable (`E1.26`), infraestructura de
integraciones (`E1.22`). Más `013`, `048`, `053`, `056`, `058`, `066`, `067`. **11 migraciones
aplicadas**, gate de 52 pasos y 4.205 pruebas, desplegado y verificado.

**Manuel tiene cuenta de superadmin y está dentro.** Producción limpia: de 15 organizaciones a 2.

**Dónde aparecieron los fallos, que es la lección**: los doce agentes cerraron en verde y luego
`db:replay` hizo falta cuatro veces, `gen:types` destapó 22 errores y la suite cazó tres pantallas
sin enlace. Ver [[una-suite-en-verde-no-prueba-el-camino-real]].

**Auditoría de composición: 124 hallazgos y MURIÓ SIN REFUTAR** (límite de sesión). Devolvió
`sobreviven: 0`, que no significa limpio — ver [[un-workflow-que-muere-a-mitad-devuelve-cero-y-cero-no-es-limpio]].
*(Juzgados y cerrados el 11-ago: ver el bloque de arriba.)*

**Decisiones de Manuel**: correo desde `info@agentesia.madrid`, **`tucrmia.com` NO se compra** —lo
que convierte el plantado de cookie de `sslip.io` en exposición aceptada y deja a `ADR-006` sin su
precondición—, y Resend como proveedor cuando toque, derogando el SMTP genérico de P21.

**Sin cerrar entonces**: el rastro de accesos sin llamante *(cerrado el 11-ago)*, la descarga de
exportación esperando el `grant` de Storage, y el correo que entra en Google y no sale.

## Estado (10-ago, madrugada) — el arnés cerrado, y F1 sin tocar

**Lo que hay que saber para retomar**: `npm run meta` es la condición de parada del bucle
(`docs/plan/LOOP-CIERRE.md`) — **121 rojas el 11-ago**. Sube cuando se descubre, y eso es correcto:
ver la ley 5 del contrato y [[claude-code-harness]].

- **El repositorio se vació y se restauró.** Un commit borró 1.082 ficheros de `origin/main`; el árbol de
  un portátil era la única copia. Causa raíz cerrada: [[git-toma-destino-e-identidad-del-entorno-no-del-cwd]].
- **Seis gates nuevos**, todos de fallos ya ocurridos: `epicas` (el tablero declaraba 59 épicas con 90 en
  el plan), `cola` (12 de 23 issues «abiertos» estaban hechos), `gates` (la tabla documentaba 26 de 46),
  `lentes`, `git-aislado`, y `zona` sin su punto ciego (tres recortes de ISO en verde, uno pintando la
  caducidad de un derecho un día antes).
- **Producto**: telemetría de uso (mig. **066 aplicada**) — el panel llamaba «inactiva» a una organización
  que entra a diario; `052` (una segunda ruta devolvía 200 donde debía 404); `063` (cuatro campos que se
  editaban sin dejar rastro del fallo).
- **Lo que más enseñó**: cinco de siete hallazgos los encontró EJECUTAR, no leer.
  [[una-suite-en-verde-no-prueba-el-camino-real]] · [[una-asercion-deja-de-medir-cuando-cambia-su-fuente]].
- **Deuda de rumbo, dicha en voz alta**: tres iteraciones seguidas de arnés y **ninguna épica de producto
  entera**. La siguiente va a F1.

## Estado (09-ago, tarde) — YA SE ENTRA AL CRM

Hasta hoy el producto **se podía montar y no se podía entrar**: única vía el enlace por correo, y sin SMTP
propio el remitente de Supabase sólo entrega a miembros del equipo del proyecto. Ahora tres vías, verificadas
**contra el despliegue** y no con dobles:

- **Contraseña** — mala → `credenciales`; **undécimo intento → `demasiados_intentos`** (el contador de
  Postgres persiste entre peticiones en el proceso desplegado).
- **Google** — cliente y proyecto propios (`crmia-505008`), llega a la pantalla de consentimiento; sin
  cabecera `Origin` la ruta falla cerrado. Declarado ANTES de encenderlo, así que el gate lo vigila.
- **Enlace** — SMTP propio autenticado (`235`). **Sin verificar que un correo LLEGUE**: falta cuenta con
  buzón real.

**Registro público CERRADO** (`signup_disabled`): estaba abierto con la clave anónima. Config de Auth
declarada en el repo y cruzada contra el despliegue (G-AUTH-DERIVA): 27 ajustes coincidiendo, **2 declarados
y bloqueados por plan** (HIBP exige Pro, hook antifuerza bruta exige Teams) — impresos en cada corrida, no
bajados de valor para poner el gate en verde. Ver
[[un-limite-delante-de-tu-accion-no-protege-si-la-operacion-es-publica]].

**La cookie de sesión no era `HttpOnly`** y llevaba dentro el token de refresco, con cuatro comentarios del
repo afirmando que sí lo era → [[una-afirmacion-repetida-no-es-una-verificacion]].

También: **meter a una segunda persona en una organización** (las 5 membresías de prod eran 5 propietarios,
así que la visibilidad por rol y equipo no la podía ejercer nadie), rastro de accesos, poner/cambiar
contraseña, embudo por defecto, accesibilidad del armazón. Migraciones 061/062/064 aplicadas; 065 escrita y
**declarada bloqueada** por plan.

**Tuyo**: registrar `tucrmia.com` (Meta/Google F2 + SPF/DKIM), crear el sitio de **Turnstile** (decidido:
gratis sin límite, invisible, no monetiza datos), y una cuenta con buzón real. Pendiente y no construido a
propósito: prefijo `__Host-` en la cookie, que mitiga `sslip.io` sin esperar al dominio →
[[sslip-io-y-nip-io-no-estan-en-la-public-suffix-list]].

## Estado (09-ago, cierre) — la capa agéntica, reescrita para cuando el usuario sea una máquina

Premisa del encargo: dentro de dos años el trabajo dentro del CRM no lo hará una persona haciendo
clic sino un agente en su nombre —el nuestro, y **el suyo**, contra la API—. Se editaron
`docs/plan/{27,05}` y §11/§15.3/§16 del maestro: **A140-A180 con 41 gates `G-AGT-*`**, clasificados
(20 estáticos · 17 de suite · 4 en CI) y registrados con su fase de nacimiento.

- 🔴 **El hallazgo caro: «95 % sobre 50 decisiones» no se podía demostrar, y estaba en cinco
  documentos.** 50 aciertos de 50 dan cota inferior de Wilson del 92,9 %; leído como demostrado la
  puerta no abría nunca, leído como porcentaje son 48/50 con tasa real posible del 87 %. Redefinido
  sin cambiar el nombre: **95 es la confianza, 90 la cota**. Y **el learning ya existía desde el
  25-jul** y no lo aplicó nadie porque no tenía un enlace entrante desde ningún hub →
  [[gate-de-automatizacion-n50-al-95-no-sostiene-el-95-usa-cota-wilson]].
- ✅ **No existía puerta de CIERRE de la autonomía.** Con «nada de interruptor» prohibido —con razón—,
  lo único capaz de cerrar era lo prohibido. Añadida, **asimétrica a propósito** (abrir exige
  demostrar, cerrar exige sospechar; un fallo grave cierra con N=1) más caducidad por falta de
  evidencia fresca. Y la unidad pasa a **(organización × clase de decisión)** →
  [[la-unidad-de-acumulacion-decide-si-una-puerta-de-calidad-es-alcanzable]].
- ✅ **La caja negra del turno, y es lo primero de todo**: `prompt_versions` (identidad calculada del
  contenido, como `BUILD_COMMIT`), `ai_turn_snapshots` (contexto congelado) y `ai_feedback_events`
  (veredicto **derivado del acto que el usuario ya iba a hacer**, sin pulgares). Misma familia que
  `persistReferral()` y el consentimiento: lo que no se persiste en el momento no se recupera nunca.
  Épica **E2.24, antes de E2.15** → [[una-aceptacion-no-es-senal-hasta-que-envejece-sin-ser-contradicha]].
- ✅ **La trampa del bucle, con corte mecánico**: troncal humano inmutable, tope del 60 % de casos
  cosechados, y **troncal a la baja con aceptación al alza congela la cosecha** →
  [[un-golden-set-que-se-nutre-de-produccion-necesita-troncal-inmutable]].
- ✅ **MCP remoto se queda en F4; lo que sube es su factura.** Lo caro es el authorization server
  (I17). Lo que llega tarde es el **contrato**: precondición sobre `row_version` (nunca `updated_at`),
  idempotencia en todo verbo, límites en cabecera, errores con el scope que faltaba,
  `GET /v1/events?since=` sobre `activity_events` heredando visibilidad por fila, y **credencial que
  propone y no ejecuta**. Épica **E1.26**, y son rompedores en cuanto haya un integrador: la v1 ya
  sirve siete recursos.
- ✅ **Lista cerrada de lo que NUNCA se agentiza** (15 entradas con motivo), incluidos el desenlace del
  lead —porque es la variable que puntúa al agente— y **los mandos del propio sistema** (A180).
- ✅ **P13 deja de bloquear**: el techo en € necesita libro de tarifas con vigencia y tarifa congelada
  en la fila, que es la pieza que E2.6 ya construye para WhatsApp. Corregido en `ESTADO.md`,
  `PREGUNTAS-PARA-MANUEL` §13 y el tablero, que llevaban desde el principio diciendo lo contrario.
- ⚠️ **Nada de esto está construido**: es plan. Y hay **otra sesión en el mismo repo** (copias de
  seguridad) que dejó el índice de git cargado; no se commiteó nada.

## Copias de seguridad (09-ago) — de no existir a probadas de punta a punta

- ✅ **La base de producción NO tenía copia de ninguna clase.** Supabase en plan **free**, que no las
  incluye, mientras `ESTADO.md` decía «Pro sin PITR». Ahora: `npm run copia` (cifrada X25519+AES-GCM
  **sólo con la clave pública**: el proceso que copia no puede leerla), `copia:drill` (Postgres 17
  desechable, 59 migraciones, reinyecta y **compara recuentos**) y `copia:estado`. Diaria en `launchd`,
  `G-SEC-RESTORE` en `pre-push`, y los rojos demostrados uno a uno.
- ✅ **Sale de la máquina**: se sube cifrada a Wasabi `eu-west-2` (bucket del Dokploy, prefijo
  `crm-supabase/`), y lo que lo demuestra es que **se bajó de allí y se restauró** — 1.607 filas + 8
  usuarios. → [[una-limpieza-multitabla-en-una-sola-query-es-todo-o-nada]] ·
[[un-gate-de-enchufado-no-se-copia-entre-huecos-que-se-rellenan-distinto]] ·
[[rejilla-de-casillas-con-el-distintivo-en-un-span-hermano-deja-n-controles-con-el-mismo-nombre]] ·
[[firma-sigv4-consulta-sin-codificar-devuelve-cero-con-200]] ·
  [[buckets-con-puntos-obligan-a-path-style-por-el-wildcard-tls]]
- ✅ **La clave privada vive sólo en 1Password** (`op://Agentesia/krtkmll2u5zlzgflpkwdhanxka/credencial`,
  **por ID: el guión largo del título invalida la referencia**). Probado tras borrar el fichero local.
- 🔴 **Tuyo**: adjuntar la política IAM al bucket propio `crm-supabase.agentesia.madrid` (opcional, hoy no
  hay hueco: las copias salen igual) · los **4 endpoints de FacturaIA** (#33) · **Pro NO se paga hasta el
  primer cliente real** (#32, decidido con las cifras: 18 MB de 500, 7 usuarios de 50.000).
- ⚠️ **Incidente de la sesión paralela**: el repo apareció en `core.bare=true` por pruebas de hooks de git
  sobre el árbol real; restaurado, nada perdido, nada llegó al remoto. →
  [[probar-hooks-de-git-en-el-repo-real-lo-deja-en-core-bare]]

## Estado (09-ago, noche) — el plan revisado contra Kommo, y lo que no existía

- ✅ **Ocho lentes en paralelo sobre el PLAN** (no sobre el código), contrastadas con la superficie
  funcional viva de Kommo de agosto 2026: salieron **8 secciones nuevas** en `docs/plan/23-30`
  (~3.000 líneas), **24 épicas** repartidas por fase y ~130 invariantes con gate. El plan maestro las
  cita desde cabecera y el `CLAUDE.md` del repo las enruta por disparador.
- ✅ **Cinco áreas que el plan no nombraba en ninguna fase**: difusiones —que la carta fundacional
  promete y ninguna épica construía—, captación web, atribución de anuncios, reservas y consentimiento.
  `channels.kind` ya admitía `webform` desde el primer diseño **sin épica que lo construyera**.
- ✅ **Tres movimientos de calendario con motivo escrito**: reservas de «sin fecha» a **F2** (la demanda
  ya factura: los clientes de la casa son negocios de cita), voz Retell a épica de **F3** (lo único que
  Kommo no puede copiar), correo por **IMAP/SMTP en F3** y OAuth a F4 →
  [[gmail-restricted-scopes-exigen-evaluacion-de-seguridad-si-almacenas]].
- ✅ **La frontera con TuFacturaIA, diseñada leyendo el repo hermano y no su documentación**: dueño por
  columna, alta sin GET previo (su `POST /v1/clientes` ya es find-or-create por NIF), proyección de
  documentos en tabla propia, y su firma en base64url que **no se puede reutilizar** con la de salida.
- 🔴 **Tuyo, y es lo caro: la base de producción NO tiene copia de seguridad.** Organización Supabase en
  plan **free**, comprobado contra la Management API. El `ESTADO.md` decía «Pro sin PITR» sobre una
  cuenta free. Pregunta #32 → [[el-plan-gratuito-del-proveedor-se-manifiesta-como-fallos-dispersos]].
- 🔴 **Tuyo: los 4 endpoints que faltan en `facturaia`** (pregunta #33). Sin el primero, activar el
  paquete lleva dentro una intervención manual nuestra por cada cliente, para siempre.
- ⚠️ **Lo urgente de verdad es de orden, no de esfuerzo**: `persistReferral()` va DENTRO de la ingesta
  de E2.2 → [[el-referral-de-click-to-whatsapp-solo-existe-en-la-ingesta]].
- 📌 **Divergencia muda por resolver**: §13 pide `@dnd-kit` y el árbol usa arrastre nativo. NO es fallo
  de accesibilidad —el `<Select>` por tarjeta es la alternativa que WCAG 2.5.7 exige, y está puesta a
  propósito— pero el plan pide una cosa y el código hace otra sin decisión escrita.

## Estado (07-ago, noche) — cuatro tracks, la paleta y el cierre de la crítica

- ✅ **La cola de webhooks YA SE VACÍA** (issue 044, migración `049`). Era la **tercera** vez del
  mismo patrón —el limitador con la puerta abierta, las ocho purgas sin barrido— y esta vez el
  silencio era literal. `pg_cron` + `pg_net` despiertan una ruta de la aplicación; la credencial no
  es un secreto compartido sino la fila de `cron_runs`, que vale una vez. **Verificado sembrando una
  entrega pendiente y viéndola salir**: con la cola vacía el verde no distingue un worker que
  funciona de uno que nadie llama.
- ✅ **Al producto se llega desde sí mismo**: `querySelectorAll('a')` daba CERO en `/leads`. Barra
  lateral, superior y barra inferior en móvil, con las pantallas en un route group `(app)`.
- ✅ **El tablero se usa con teclado y con el dedo**: la tarjeta pasa a enlace real, la etapa se
  cambia desde la propia tarjeta (el arrastre HTML5 no dispara en táctil), `aria-live` + Deshacer, y
  `/leads/[id]` con panel lateral. 404 tanto si no existe como si RLS no lo deja ver.
- ✅ **PALETA DECIDIDA por Manuel: el azul del LOGOTIPO** (`#83b9ff`), sacado del PDF de marca —la
  familia entera vive en el tono 255,3°. Lo que lo hace usable es que lleva **tinta oscura encima**
  (la contraforma del propio logo): con blanco da 2,03:1, con `#292a30` da 7,05:1. Comparte tono con
  TuFacturaIA, así que ya NO se distinguen por el color sino por cómo lo usan — corregido en
  `03-DESIGN-CONTEXT` en vez de maquillado. Y con ella: `--danger-strong` para el botón de peligro
  (3,61 → 5,29) y la rampa `--stage-*` del embudo, consumida de verdad.
- ✅ **Crítica de diseño cerrada**: un solo formateador de dinero (había tres), una sola altura de
  control (había cuatro — los tokens existían desde el issue 009 y **no los leía nadie**), la barra
  de filtros deja de gastar un tercio del móvil en decir «ninguno», /tareas deja de desbordar 37px, y
  el rebote sale del token donde se heredaba a todo. Gates nuevos: **G-FORMATO**, **G-MARCA-TINTA**,
  trinquete `ratchet:ui` (3 primitivos sin llamante, con motivo escrito, que no suban).
- ⚠️ **Lo que NO está verificado, y conviene saberlo**: los 37px de /tareas no los midió nadie en la
  pantalla real; la paleta en kanban y listados no la ha visto nadie (necesitan sesión); del worker
  se probó una entrega que FALLA, no una que llega bien.
- ⚠️ **Tres tracks de agentes se perdieron enteros** al retirar los worktrees con `--force` antes de
  commitear en ellos; rehechos a mano desde los informes. Ver
  [[claude-code-agentes-worktree-failure-modes]] (failure mode M).
- ⚠️ **El verde de la suite dependía de la carga del portátil** hasta este cierre. Ver
  [[tests-que-caen-por-contencion-de-cpu-verificalos-aislados-antes-de-diagnosticar]].

## Estado (07-ago) — la jornada más larga del proyecto

- **F1 con NUEVE issues de dominio cerrados.** Gate **2.488 tests**, **49 migraciones** aplicadas.
  Desplegado y verificado en `https://tucrmia.185.99.186.76.sslip.io`, `smoke:v1` 57/57 y
  `smoke:admin` 32/32 contra el despliegue.
- ✅ **HTTPS, tras cuatro días bloqueado por una deducción de más.** El cupo agotado era el de
  `traefik.me`; de ahí se concluyó «hace falta dominio propio» y era falso — otra app del MISMO host
  llevaba desde junio con certificado real sobre `sslip.io`. Puerta en claro borrada. Ver
  [[traefik-me-no-emite-certificado-por-cupo-compartido-agotado]] y
  [[un-no-se-puede-heredado-caduca-como-cualquier-otra-frase]].
- ✅ **Las tres variables de Dokploy, puestas por SSH.** El `env` está cifrado en su base, así que la
  receta de leer-fusionar-escribir no era ejecutable; se sustituyó por huellas SHA-256. Ver
  [[dokploy-guarda-el-env-cifrado-la-receta-de-leer-fusionar-escribir-no-vale]].
- ✅ **Entraron**: candado del módulo en la base (`050`), barrido de retención con `pg_cron` (`052`),
  contador de tasa duradero (`044`), hora en la zona de la organización, vínculos heredando la
  visibilidad de su ficha (`042`), reparto de `outbox_events` (`045`), ciclo de vida del módulo
  (`047`), búsqueda y timeline por la API v1 (`048`).
- ✅ **Sesión de `impeccable` (16/40)**: el producto se pintaba con la FUENTE DEL SISTEMA sobre blanco
  de navegador — `body` no consumía los tokens y las tres familias nombradas no las cargaba nadie.
  Arreglado, con gate G-FUENTES. Ver [[el-gate-escrito-justo-despues-del-arreglo-mide-cero-casos]].
- 🔴 **PENDIENTE Y NUEVO: la cola del outbox se llena y no la vacía nadie** (issue 044). El reparto
  crea las entregas y nada invoca `procesarPendientes`. Es el mismo fallo un escalón más abajo.
- ✅ **3 CVE graves en dependencias, y el punto ciego que los dejó entrar.** Los encontró Borja con
  `npm` a mano: `postcss@8.4.31` y `sharp@0.34.5`, las dos pinneadas por `next@16.2.11`. Cerrados con
  `overrides` sin subir Next (16.2.12 seguía en 8.4.31), verificado con `npm ci` en árbol vacío —
  `npm ls` mentía porque el lockfile iba desfasado. **Lo grave era el hueco**: `npm audit` no estaba
  en ninguno de los 34 gates y `audit-ratchet.mjs` estaba especificado en el plan **y nunca escrito**,
  porque «patrón ya reusado 3×» describía a TuFacturaIA. Ver
  [[un-plan-que-hereda-patrones-de-un-repo-hermano-da-por-existente-lo-que-solo-existe-alli]] ·
  [[npm-overrides-necesario-cuando-dependencia-fija-optionaldependency-vieja]].
- ✅ **Y con ellos, CI por primera vez.** Hasta hoy los 34 gates solo corrían en el portátil de quien
  commitea — un hook se salta, y un clon sin `npm install` no tiene ni `core.hooksPath`. Entran
  `gate.yml` (push/PR) y `seguridad-dependencias.yml` (G-AUDIT **diario**, porque un CVE se publica
  solo), **G-BASE-FIJADA** (digest multiarch, validado desplegando en el amd64 de Dokploy),
  **G-BASE-FRESCURA** (30 días) y `--ignore-scripts`. Y el aviso por Slack pasa de norma escrita a
  hook. Ver [[al-fijar-imagen-base-por-digest-usar-el-del-indice-multiarquitectura]] ·
  [[el-install-script-que-declara-el-registro-npm-puede-no-estar-en-el-tarball-real]].
- 🔴 **Tuyo**: **habilitar la facturación de GitHub Actions** (org en plan free con 24 repos privados;
  los workflows disparan pero GitHub no los ejecuta, y cada push deja dos aspas rojas que NO son
  código roto), el `grant` de Storage (pasos en `PREGUNTAS-PARA-MANUEL.md` §29), rotar las claves
  emitidas mientras estuvo en HTTP y la de Dokploy, y **elegir paleta** (pediste verla antes).
- ⚠️ **Dos sesiones en el mismo checkout, ya cuatro veces.** Un commit ajeno se llevó un fichero mío
  dentro; y el 7-ago por la tarde una sesión paralela **borró mis `overrides` sin commitear** y
  después **empujó mis commits a `origin/main`** dentro de su propio push. Ninguna hizo daño, las
  cuatro dicen lo mismo: un worktree por sesión.
  Ver [[commit-por-ruta-no-te-aisla-de-otra-sesion-con-el-indice-cargado]].

## Estado (06-ago)

- **F0: 11/17. F1 con CUATRO issues de dominio cerrados (018/019/020/021).** Gate **1386 tests**,
  veinticinco migraciones. Desplegado: `9eb31cb7`.
- ✅ **021 · campos personalizados (E1.4)** — pantalla `/ajustes/campos` + botón «Campos» en las tres
  fichas, sobre el motor ya existente. Dos bugs reales cazados NAVEGANDO, no leyendo: opción archivada
  que seguía elegible, y el modal mandando el snapshot completo en vez del delta (revalidaba de balde y
  bloqueaba el formulario entero). Detalle en el `status-log` del repo.
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

[[firma-sigv4-consulta-sin-codificar-devuelve-cero-con-200]] ·
[[buckets-con-puntos-obligan-a-path-style-por-el-wildcard-tls]] ·
[[probar-hooks-de-git-en-el-repo-real-lo-deja-en-core-bare]] ·
[[una-afirmacion-repetida-no-es-una-verificacion]] ·
[[un-limite-delante-de-tu-accion-no-protege-si-la-operacion-es-publica]] ·
[[sslip-io-y-nip-io-no-estan-en-la-public-suffix-list]] ·
[[formaction-con-server-action-secuestra-el-name-del-boton]] ·
[[el-plan-gratuito-del-proveedor-se-manifiesta-como-fallos-dispersos]] ·
[[el-referral-de-click-to-whatsapp-solo-existe-en-la-ingesta]] ·
[[gmail-restricted-scopes-exigen-evaluacion-de-seguridad-si-almacenas]] ·
[[agentes-paralelos-de-diseno-colisionan-en-la-numeracion-de-invariantes]] ·
[[un-hallazgo-que-solo-vive-en-el-resumen-no-existe]] ·
[[un-plan-que-hereda-patrones-de-un-repo-hermano-da-por-existente-lo-que-solo-existe-alli]] ·
[[al-fijar-imagen-base-por-digest-usar-el-del-indice-multiarquitectura]] ·
[[el-install-script-que-declara-el-registro-npm-puede-no-estar-en-el-tarball-real]] ·
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
