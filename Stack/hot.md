---
title: hot cache
date: 2026-07-29
tags: [stack, index]
---

# Hot Cache

Este fichero se carga **cuando no hay disparador claro** (CLAUDE.md: "Default / dudo → `Stack/hot.md`").
O sea: es lo que se lee al arrancar sin saber todavía qué se va a tocar. Todo lo que esté aquí se paga
en contexto en esas sesiones, venga al caso o no.

**Qué entra:** SOLO **método y riesgo transversal** — lo que no sabes que tienes que buscar: trampas de
worktrees/subagentes/gate/verificación, y patrones de integridad que se repiten entre proyectos.
**Un gotcha de un stack concreto NO entra nunca**: su casa es `Stack/<tool>.md`, que ya se carga por
disparador cuando tocas ese fichero.

**Qué SALE (lo que faltaba, 29-jul):** una entrada sale de aquí cuando su riesgo pasa a estar
**bloqueado por una máquina** — hook de git, trinquete, test de conformidad, lint rule. Lo que un hook
impide no hace falta recordarlo en contexto: el hook lo dirá en el momento exacto. Aquí se queda solo
lo que **únicamente** existe como advertencia.

> Medido el 29-jul cruzando las 60 entradas contra los 14 gates reales (git-guard, pre-commit,
> pre-push, semáforo de CPU): **solo 1 estaba cubierta por un hook**. Ese es el hueco real de este
> fichero — no su tamaño. Cada entrada que reincide y sea comprobable por un comando debería
> convertirse en hook y salir de aquí. Ver [[claude-code-harness]].

**Tope: 60.** Es el número real de hoy, no un deseo: antes convivían "~45" y "tope duro de 25" en esta
misma cabecera mientras el fichero tenía 73, y un tope que se incumple 2,4x no ordena nada. La forma de
bajarlo es la de arriba (convertir en hook), no volver a podar por fecha — eso ya falló dos veces
(40→15 el 13-jul, 146→129 el 25-jul, y **de vuelta a 159 en dos días**).

Transversales de fondo en [[index]] §Transversales y [[patterns-cross-proyecto]].

## Ha vuelto a pasar (7)

Estas no son advertencias teóricas: su learning documenta que el fallo **reincidió** después de
estar escrito. Si una de estas se puede comprobar con un comando, su sitio es un hook, no esta lista.

- **Una ejecución en verde no prueba que el efecto ocurriera** — `success` = "no explotó"; mide que el nodo de efecto CORRIÓ (268 verdes y cero envíos). Ver [[ejecucion-en-verde-no-prueba-el-efecto]]
- **Rama nueva desde main local sin fetch** — `worktree add ... main` nace vieja y pisa lo ya mergeado; usar `origin/main`. Al integrarla: fichero reescrito >2 veces → merge, no rebase; y sus rojos se clasifican (copy → actualizar esperado, regla del repo → arreglar código). Ver [[rama-nueva-desde-un-main-local-sin-fetch-revierte-trabajo-ajeno]] · [[rama-que-reescribe-el-mismo-fichero-varias-veces-se-integra-con-merge]] · [[los-tests-rojos-que-hereda-un-merge-se-clasifican-uno-a-uno]]
- **Al partir una pila en PRs, el fix va con el commit que lo causa** — si no, mergear el primero publica el fallo; con datos personales el hueco entre merges ES la exposición. Ver [[al-partir-una-pila-en-prs-el-fix-tiene-que-viajar-con-lo-que-lo-causa]]
- **`create or replace` con otra firma crea una sobrecarga y `db push` dice `Finished`** — el fix se despliega muerto. Verifica `pg_proc`: UNA fila. Ver [[postgres-rpc-firma-identica-create-replace]]
- **Un comentario que afirma una invariante es una deuda de test** — grepea la afirmación contra el código antes de fiarte; si nadie la comprueba, no es cierta. Ver [[un-comentario-que-afirma-una-invariante-es-una-deuda-de-test]]
- **Un gate solo puede fallar HACIENDO RUIDO** — si hay un camino donde no mide y sale con 0, será el de producción. Al matar un CI, migrar sus gates uno a uno. Ver [[un-script-gate-con-guard-de-entrypoint-degrada-a-no-op-silencioso]] · [[una-metrica-por-regex-sin-test-del-parser-cuenta-ruido-y-se-vuelve-ignorable]]
- **Herramienta nueva sin barrer sus call-sites escritos NO se adopta** — el agente ejecuta lo ESCRITO (permisos, runbooks, memories), no lo del PATH. Ver [[un-wrapper-nuevo-no-se-adopta-si-no-barres-los-call-sites-escritos]]

## El resto (36)


- **Protección construida y no enchufada: ningún test la caza** — el doble de la prueba ES el relleno. Señal: módulo con tests y cero consumidores. Ver [[una-proteccion-construida-y-no-enchufada-no-la-caza-ningun-test]]
- **Un entorno de pruebas más limpio que producción es ciego** — y su verde se cita como prueba. Ver [[el-replay-que-arranca-mas-limpio-que-produccion-es-ciego]]

- **`:root{--x}` (0,1,0) pierde contra `:root[data-theme=…]` (0,2,0)** — el valor llega al DOM, se ve en el inspector y no pinta. Solo lo caza el valor COMPUTADO en un navegador: los unitarios validan la cadena y siguen verdes. Ver [[style-inyectado-con-root-pierde-contra-root-data-theme]]
- **Preferencia por tenant restaurada de un `localStorage` global se filtra entre organizaciones** — el switch de empresa recarga y aplica la clave del tenant anterior. Sembrar en servidor. Encender una restauración muerta es cambio de comportamiento, no arreglo. Ver [[localstorage-global-en-app-multitenant-filtra-entre-organizaciones]]
- **`curl` en macOS valida una cadena TLS que GitHub y Node rechazan** — completa el intermedio por su cuenta y te engaña; cuenta posiciones con `openssl s_client`. Ver [[cadena-tls-incompleta-curl-en-macos-la-salva-y-engana]]
- **Un fix no está verificado hasta crear una entidad NUEVA tras el deploy** — leer los datos que arregló el backfill no prueba nada del código; el compositor no es el punto de persistencia y la suite verde no cubre el camino que tocas. Ver [[cambiar-la-semantica-de-una-columna-el-compositor-no-es-el-punto-de-persistencia]]
- **Un check de coherencia no puede afirmar un desajuste si no pudo preguntar** — 401/429 es "no verificado" (UNA alerta media), no N desajustes altos: la falsa induce a recrear datos sanos. Delator: fallan TODAS con el MISMO motivo. Ver [[fallo-de-credencial-no-es-dato-ausente-en-un-check-de-coherencia]]
- **Una clave read-only NO se verifica escribiendo** — el `POST` de prueba que esperaba un 403 devolvió 200 y creó objetos reales en una cuenta live. Lo comprobable leyendo es la CUENTA (`GET /v1/account`), no la ausencia de permiso de escritura. Ver [[no-verificar-una-clave-read-only-escribiendo-con-ella]]
- **`FETCH_HEAD` miente en cuanto haces un segundo `fetch`** — lo repunta, y lo que compruebes después mide otro árbol: falso negativo con `file:line` detrás. Usar `origin/<rama>`. Ver [[un-segundo-git-fetch-pisa-fetch-head-y-auditas-el-arbol-equivocado]]
- **`--force-with-lease` sin `fetch` no protege nada** — compara contra tu `origin/<rama>` LOCAL, así que un checkout desactualizado autoriza rebobinar `main` 40+ commits. Lease con SHA explícito, y verifica la recuperación por ÁRBOL, no por log. Ver [[force-with-lease-sin-fetch-no-protege-nada]]
- **Un locator que resuelve a 0 elementos es un test roto, no evidencia** — en un `if (isVisible)` es falso verde; tras un `test.skip(count === 0)`, verde PERMANENTE. Afirmar por rol/nombre accesible, nunca por clase de CSS Module. Ver [[locator-de-test-atado-a-la-implementacion-caduca-y-da-falso-verde]]
- **El stash es compartido entre worktrees** — una sesión paralela puede recuperar tu stash y dejarte sin fix; cero `stash` en repos con worktrees. Ver [[stash-es-compartido-entre-worktrees-y-rompe-sesiones-paralelas]]
- **"No hardcodear el modo" lo vuelve inverificable desde el repo** — `TRADING_MODE`/`DRY_RUN` viven solo en el panel y el checklist da verde leyendo una plantilla. Un modo mal puesto no rompe: ejecuta bien lo irreversible (32 h en `live`, −1.613 USDT). Léelo del sistema vivo. Ver [[no-hardcodear-el-modo-lo-hace-inverificable-desde-el-repo]]
- **"Contenedor recreado, logs limpios" no verifica un cambio de env** — verifica que arrancó. La prueba es una llamada que devuelva el EFECTO (p. ej. el endpoint devuelve bajo qué identidad entra la clave). Ver [[verificar-deploy-de-env-por-comportamiento-no-por-contenedor-recreado]]
- **Un camino crítico sin smoke se pudre meses aunque haya miles de tests al lado** — 7.541 unitarios y ninguno arrancaba Chromium: dos fallos de 2 meses en el que genera TODAS las facturas. Si produce el artefacto que ve el cliente y ningún test lo produce de verdad, no está cubierto. Ver [[camino-critico-sin-smoke-se-pudre-meses]]
- **Un test nuevo no vale hasta que le rompes el código a propósito y falla** — dos minutos de mutación distinguen "pasa" de "vigila algo". Caza el test que se salta solo y el que mide el artefacto vecino. Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]]
- **Worktree en `/private/tmp` sin commitear = código perdido, pero el transcript no** — el `.jsonl` de la sesión guarda el resultado completo de cada subagente: se reconstruye la SPEC y se reimplementa. Ver [[transcript-jsonl-sobrevive-al-worktree-borrado]]
- **Exit 0 + árbol limpio ≠ "no había trabajo"** — un proceso que agota cuota se hace pasar por "sin cambios". Clasificar por texto de stdout, no por exit code. Ver [[proceso-que-agota-la-cuota-puede-salir-con-exit-0-y-parecer-sin-cambios]]
- **Un gate con cientos de skips por entorno sale ✓ VERDE sin haber probado nada** — el puerto ocupado por otro proyecto es la causa más frecuente; desglosa los skips por fichero antes de decir verde. Ver [[e2e-smoke-skip-honesto]]
- **Tests rojos con los tiempos clavados en 5000 ms = contención, no código** — córrelos aislados antes de diagnosticar nada. Ver [[tests-que-caen-por-contencion-de-cpu-verificalos-aislados-antes-de-diagnosticar]]
- **Un fake cuya FORMA de retorno satisface la aserción verifica el fake, no el código** — y `toMatchObject` para afirmar AUSENCIA de una clave siempre pasa. Ver [[mock-funcion-compartida-en-test-endpoint-falso-verde-composicion]]
- **Un helper de traza con `if (!orgId) return` deja sin auditar justo lo global** — mide la DISTRIBUCIÓN de acciones registradas, no que la tabla tenga filas. Ver [[helper-de-auditoria-con-early-return-deja-sin-traza-lo-global]]
- **Specs de una rama contra el binario de otra: el marcador sale y no vale** — clasifica un rojo construyendo `origin/main` en el MISMO worktree. Ver [[tanda-e2e-con-specs-de-una-rama-y-binario-de-otra-no-mide-nada]]

- **Ese «bloqueante» de arriba no bloquea si el helper se traga los fallos** — supabase-js no lanza en un insert fallido, devuelve `{ error }`: envolverlo en `try/catch` es código muerto. Ver [[supabase-js-no-lanza-en-insert-asi-que-el-try-catch-del-caller-es-codigo-muerto]]
- **Tu red de tests puede estar ciega al gesto real** — jsdom y `fill()` de Playwright no teclean. Ver [[jsdom-no-reproduce-el-reset-de-seleccion-al-cambiar-input-type]] · [[playwright-fill-escribe-value-y-deja-obsoleto-el-estado-del-componente]]
- **Un arreglo se verifica recorriendo el caso real** — el apaño del usuario atascado dispara el guard nuevo. Ver [[el-parche-del-usuario-atascado-dispara-el-guard-del-arreglo]] · [[una-pista-detras-de-un-gate-que-el-caso-afectado-no-cumple-no-existe]]
- **El esquema se aplica ANTES de mergear su código, y el hueco de migración caduca** — si no, prod llama a lo que no existe. Ver [[aplicar-migraciones-a-prod-antes-del-merge-caduca-la-reserva-de-numero]]

> **Las otras 50 no se han borrado**: siguen vigentes en [[hot-archivo-2026-08-01]] y se recuperan por
> wikilink y por grep. (El tope vigente es el de la cabecera, no el "25" que decía aquí.)
>
> Los contadores de las dos secciones decían 7 y **63** con 7 y **36** reales: un número que nadie
> recalcula al añadir una entrada miente a la primera. Corregidos el 3-ago; si vuelven a divergir, el
> arreglo es contarlos con un comando, no a mano.
- **Fail-closed sobre INICIAR lo peligroso, nunca sobre SUPERVISAR lo que ya está en vuelo** — abortar el arranque mata también el plano de control y deja sin vigilancia lo que sigue abierto; la guarda va en el cuello de la acción, no en el arranque. Ver [[una-guarda-que-mata-el-proceso-deja-huerfano-lo-que-ya-esta-en-vuelo]]
- **Antes de mergear una validación que bloquea, cuenta en prod a quién bloquea** — y cuántos de esos YA usan el flujo. Esa segunda cifra es la que cambia la decisión. Ver [[antes-de-mergear-una-validacion-que-bloquea-cuenta-a-quien-bloquea]]
- **PostgREST corta a 1000 y tus avisos de truncado no pueden dispararse** — el caso peor NO lleva `.limit()`; el `.in()` grande además revienta el DELETE con un 400. Ver [[postgrest-max-rows-trunca-silencioso-in-revienta-url]]
- **Antes de preguntarle un DATO al cliente, míralo en su sistema origen** — 3 veces en un día íbamos a pedir lo que ya teníamos en su backup. Las preguntas legítimas son de decisión. Ver [[antes-de-preguntar-al-cliente-mira-si-el-dato-esta-en-el-sistema-origen]]
- **Escribir la doc de exportación de un sistema lo audita entero** — «¿qué copio?» recorre todo; «¿qué arreglo?» no. Siete defectos en un barrido; PRs separados. Ver [[escribir-la-doc-de-exportacion-de-un-sistema-lo-audita-entero]]
- **Worktree que vaya a empujar: `npm ci` + `.env.local`, sin atajo** — Turbopack revienta con un `node_modules` enlazado fuera de la raíz. Ver [[turbopack-rechaza-symlink-node-modules-en-worktree]]
- **Navegación apilada = UN solo modal con la pila dentro** — dos que se desmontan en el mismo commit dejan el `<body>` sin scroll para siempre, sin error. Ver [[dos-modales-que-se-cierran-a-la-vez-dejan-el-body-sin-scroll]]
- **Tercera variante de la misma regla en un detector: para** — enumerar sintaxis se queda corto (S19); comprueba la identidad. Ver [[un-detector-que-enumera-sintaxis-se-queda-corto-comprueba-la-identidad]]
- **Un bloqueo ANOTADO no es un bloqueo comprobado** — mira si otra credencial que ya tienes sirve para pedir la que «falta». Se hereda y nadie lo recuestiona. Ver [[las-claves-de-un-proyecto-supabase-se-piden-con-el-token-de-cuenta]]
- **Baseline capturado de la página equivocada = verde para siempre** — si la ruta redirige, `--update-snapshots` guarda el destino. Asierta dónde aterrizaste antes de capturar. Ver [[baseline-de-screenshot-capturado-de-la-pagina-equivocada-es-verde-para-siempre]]
