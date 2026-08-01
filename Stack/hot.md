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

## Ha vuelto a pasar (6)
- **Una etiqueta nacida de un caso concreto sobrevive a su contexto** — y acaba midiendo otra cosa; los tests unitarios no lo ven por construcción. Ver [[una-etiqueta-nacida-de-un-caso-concreto-sobrevive-a-su-contexto]]

Estas no son advertencias teóricas: su learning documenta que el fallo **reincidió** después de
estar escrito. Si una de estas se puede comprobar con un comando, su sitio es un hook, no esta lista.

- **Rama nueva desde main local sin fetch** — `worktree add ... main` nace vieja y pisa lo ya mergeado; usar `origin/main`. Ver [[rama-nueva-desde-un-main-local-sin-fetch-revierte-trabajo-ajeno]]
- **`create or replace` con otra firma crea una sobrecarga y `db push` dice `Finished`** — el fix se despliega muerto. Verifica `pg_proc`: UNA fila. Ver [[postgres-rpc-firma-identica-create-replace]]
- **Un comentario que afirma una invariante es una deuda de test** — grepea la afirmación contra el código antes de fiarte; si nadie la comprueba, no es cierta. Ver [[un-comentario-que-afirma-una-invariante-es-una-deuda-de-test]]

## El resto (61)


- **Una aserción de ausencia está verde gratis si el fixture no puede producir la presencia** — al lado de cada «no pasa X», una aserción de que **el camino se recorrió**; y verificar rompiendo el guard. Ver [[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]]

- **Un checker vale por CÓMO se pone rojo** — el que no puede fallar no verifica nada: provoca el fallo antes de confiar en el verde. Ver [[un-checker-vale-por-como-se-pone-rojo]]
- **Un fix no está verificado hasta crear una entidad NUEVA tras el deploy** — leer los datos que arregló el backfill no prueba nada del código; el compositor no es el punto de persistencia y la suite verde no cubre el camino que tocas. Ver [[cambiar-la-semantica-de-una-columna-el-compositor-no-es-el-punto-de-persistencia]]
- **Un check de coherencia no puede afirmar un desajuste si no pudo preguntar** — clave ausente/401/429 es "no verificado" (UNA alerta media), no N desajustes altos; la alerta falsa induce a recrear datos que están bien. Delator: fallan TODAS las filas con el MISMO motivo. Ver [[fallo-de-credencial-no-es-dato-ausente-en-un-check-de-coherencia]]
- **Una clave read-only NO se verifica escribiendo** — el `POST` de prueba que esperaba un 403 devolvió 200 y creó objetos reales en una cuenta live. Lo comprobable leyendo es la CUENTA (`GET /v1/account`), no la ausencia de permiso de escritura. Ver [[no-verificar-una-clave-read-only-escribiendo-con-ella]]
- **`--force-with-lease` sin `fetch` no protege nada** — compara contra tu `origin/<rama>` LOCAL, así que un checkout desactualizado autoriza rebobinar `main` 40+ commits. Lease con SHA explícito, y verifica la recuperación por ÁRBOL, no por log. Ver [[force-with-lease-sin-fetch-no-protege-nada]]
- **Un locator que resuelve a 0 elementos es un test roto, no evidencia** — en un `if (isVisible)` es falso verde; tras un `test.skip(count === 0)`, verde PERMANENTE. Afirmar por rol/nombre accesible, nunca por clase de CSS Module. Ver [[locator-de-test-atado-a-la-implementacion-caduca-y-da-falso-verde]]
- **`gh pr merge` desde un worktree falla DESPUÉS de mergear en remoto** — el error (`'main' is already used by worktree`) lo da el checkout local posterior, no el merge; comprobar con `gh pr view N --json state` antes de reintentar. Ver [[gh-pr-merge-desde-worktree-falla-despues-de-haber-mergeado]]
- **El stash es compartido entre worktrees** — una sesión paralela puede recuperar tu stash y dejarte sin fix; cero `stash` en repos con worktrees. Ver [[stash-es-compartido-entre-worktrees-y-rompe-sesiones-paralelas]]
- **En un worktree `.git` es FICHERO, no directorio** — detectar la raíz con `existsSync('.git')` + `basename(dir)` devuelve la RAMA como nombre de proyecto (rompió el panel de horas). Parsear el `gitdir:`. Ver [[git-worktree-dotgit-es-fichero-basename-devuelve-la-rama]].
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
- **Tu red de tests puede estar ciega al gesto real** — jsdom no resetea la selección al cambiar `input.type` (dígitos invertidos en el navegador, verde en jsdom) y `fill()` de Playwright escribe `.value` sin teclear. Ver [[jsdom-no-reproduce-el-reset-de-seleccion-al-cambiar-input-type]] · [[playwright-fill-escribe-value-y-deja-obsoleto-el-estado-del-componente]]
- **"Ya comprobé que el hueco de migración está libre" caduca** — se asigna justo antes del merge; si aplicaste a prod antes, repara el ledger. Ver [[aplicar-migraciones-a-prod-antes-del-merge-caduca-la-reserva-de-numero]]

> **Las otras 50 no se han borrado**: siguen igual de vigentes, pero el tope de este fichero es 25 y
> todo lo que esté aquí se paga en cada sesión sin disparador. Viven en
> [[hot-archivo-2026-08-01]] y sus learnings se recuperan igual por wikilink y por grep.
