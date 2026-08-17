---
title: hot cache
date: 2026-07-29
tags: [stack, index]
---

# Hot Cache

- **Al retirar una columna o su escritor, grep de quién la LEE** — el `DROP` no avisa de la función que la usa (cuerpo en cadena = sin `pg_depend`, revienta con `42703` en runtime), y un guard sobre una columna que ya nadie rellena compila y tiene tests verdes sin proteger nada. Ver [[funcion-sql-con-cuerpo-en-cadena-no-registra-dependencia-de-columna]]
- **«¿Existe X?» se busca por la LLAMADA, no por el módulo** — la carpeta esperada contesta otra pregunta. Ver [[buscar-una-capacidad-por-su-llamada-no-por-el-modulo-donde-crees-que-vive]]
- **Un guard que mide un sustituto bloquea sin que nadie pruebe el hecho** — si aborta ANTES de intentar la operación, el error nunca aparece (once días parados). Comprueba el RESULTADO al final, no el permiso al principio. Ver [[un-guard-que-mide-un-sustituto-bloquea-sin-que-nadie-pruebe-el-hecho]]
- **Acotar una API por scopes no la acota** — rutas distintas comparten scope: allowlist de endpoints en el wrapper, así una ruta nueva nace fuera. Ver [[acotar-una-api-por-scopes-no-la-acota-usa-allowlist-de-endpoints]]
- **El sujeto de un smoke debe pasar los gates ANTERIORES** — un 402 de billing tapa el 403 que medías. Ver [[el-gate-de-billing-va-antes-que-el-de-plan-y-tapa-lo-que-querias-medir]]
- **`gh pr merge --delete-branch` con worktrees mergea pero NO borra** — sale con error tras mergear; comprueba `ls-remote`, no el exit code. Ver [[gh-pr-merge-delete-branch-no-borra-la-rama-si-falla-su-checkout-local]]
- **Un barrido devuelve cero sin decir que no midió** — `git grep -E` sin `\s`, zsh sin word-splitting, `:t` modificador. Control en las dos direcciones. Ver [[el-instrumento-devuelve-cero-sin-decir-que-no-ha-medido]]
- **Un agente muerto deja un motor desacoplado vivo** — sube por `ppid`; `TaskStop` no vale. Ver [[un-agente-muerto-puede-dejar-un-motor-desacoplado-vivo]]
- **Aseverar el `import` no asevera la llamada** — `toContain("import { X")` sigue verde si otra función ocupa el sitio de `X`; asevera el USO. Ver [[aseverar-sobre-el-import-no-asevera-sobre-la-llamada]]
- **Probar la aritmética no prueba el cableado** — 5 tests de la función pura en verde con el DTO pasándole un `0`; cubre también quién le pasa los argumentos. Ver [[probar-la-aritmetica-no-prueba-el-cableado-que-la-invoca]]
- **Rojo de la suite + máquina saturada ≠ regresión** — 3 corridas, 3 conjuntos de rojos sin solape; pasan aislados. Mira la duración antes que el nombre (123 s vs 11.780 s). No solapes gates. Ver [[la-suite-completa-bajo-paralelismo-no-distingue-regresion-de-saturacion]]

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
>
> ⚠️ Pero un hook **envejece por partes**: 3 de 4 reglas de `git-guard` compartían un defecto que solo
> se arregló en una, y la peor fallaba ABIERTA. Ver [[un-guard-envejece-por-partes-arregla-una-regla-y-sus-hermanas-siguen-rotas]] · y que **decida por EJECUCIÓN, no por mención** — el que bloquea un `git commit` por NOMBRAR el comando caro se aprende a rodear: [[un-guard-que-decide-por-mencion-bloquea-lo-que-solo-nombra-el-comando-caro]].

**Tope: 60.** Es el número real de hoy, no un deseo: antes convivían "~45" y "tope duro de 25" en esta
misma cabecera mientras el fichero tenía 73, y un tope que se incumple 2,4x no ordena nada. La forma de
bajarlo es la de arriba (convertir en hook), no volver a podar por fecha — eso ya falló dos veces
(40→15 el 13-jul, 146→129 el 25-jul, y **de vuelta a 159 en dos días**).

Transversales de fondo en [[index]] §Transversales y [[patterns-cross-proyecto]].

## Ha vuelto a pasar (24)

Estas no son advertencias teóricas: su learning documenta que el fallo **reincidió** después de
estar escrito. Si una de estas se puede comprobar con un comando, su sitio es un hook, no esta lista.

- **Un backfill se guarda por el INVARIANTE, no por el síntoma** — «a toda fila sin X, ponle X» habría duplicado 106 de 115 filas; la condición que lo hace neutro deja 9. Ver [[backfill-guardado-por-invariante-en-vez-de-por-sintoma]]
- **Citar el delimitador dentro de su propia región la cierra ahí mismo** — `$$` en un comentario de `do $$`, acento grave en plantilla, `*/` en JSDoc; el error sale LEJOS. Nadie lo ve porque `allowJs:false` deja los `.mjs` fuera de `tsc` y un fichero que nadie ejecuta no lo analiza nada. Ver [[citar-el-delimitador-dentro-de-su-propia-region-la-cierra-ahi-mismo]]
- **Un gate que cruza dos listas es ciego a lo que no está en ninguna** — cruzar A contra B no ve lo que falta en las dos; hace falta una tercera fuente, normalmente el disco. Ver [[un-gate-que-cruza-dos-listas-es-ciego-a-lo-que-no-esta-en-ninguna]]
- **Un «no se puede» heredado caduca** — pregunta POR QUÉ, no SI: el booleano envejece, el hecho no. Ver [[un-no-se-puede-heredado-caduca-como-cualquier-otra-frase]]
- **`cmd > fichero` vacía el fichero antes de arrancar `cmd`** — un generador que falla borra su propia fuente de verdad, sin propagar el exit code. Ver [[redirigir-con-mayor-que-destruye-el-fichero-antes-de-arrancar-el-comando]]
- **El gate escrito justo tras el arreglo mide cero casos** — demuestra el rojo contra el árbol ANTERIOR. Ver [[el-gate-escrito-justo-despues-del-arreglo-mide-cero-casos]]
- **Un gate sobre el RESULTADO no valida la transformacion** — si reescalas dos campos a la vez (uno /f, otro xf), el producto es invariante **por construccion para cualquier f**: el gate que compara el resultado antes y despues pasa en verde con f=10. Ataca el PARAMETRO, no el resultado. Test para saber si tu gate es gate: ¿con que valor fallaria? Si no encuentras ninguno, no es un gate. Ver [[un-gate-sobre-el-resultado-no-valida-la-transformacion]]
- **Redondea antes de decidir la frontera, no despues** — si no, salen «5 h 60 min» y «60 s». Y pruebalo con un BARRIDO: con casos elegidos (59 y 60) la banda de en medio pasa. Ver [[decidir-una-frontera-con-el-valor-crudo-produce-imposibles]]
- **Un trigger que PISA en vez de calcular te resincroniza los datos al migrar** — `SET hijo = NEW.padre` propaga el valor del padre, no tu conversion, y de paso corrige toda desincronia previa: 188 precios movidos. Ver [[un-trigger-que-pisa-en-vez-de-calcular-resincroniza-al-migrar]]
- **La precision de una columna la marca su valor MAXIMO, no el tipico** — `SELECT max(col)` antes de elegir la escala. Y la fila basura que documentas y decides ignorar **sigue participando en los calculos**. Ver [[una-fila-basura-amplifica-el-error-de-redondeo-de-toda-la-tabla]]
- **Un precio unitario de 1,00 marca una cantidad que en realidad son euros** — truco universal de los ERP para colar un importe por la columna de cantidad; sin excluirlas, cualquier `SUM(cant*precio)/SUM(cant)` mezcla dos unidades. Agrupa por precio y ordena por volumen: la fila contaminada canta sola. Ver [[precio-unitario-1-00-marca-una-cantidad-que-son-euros]]
- **Antes de decir «ese dato no está», barre el catálogo de columnas** — `sys.columns` / `information_schema.columns` por el nombre del CONCEPTO sobre todas las tablas cuesta un segundo y convierte «no lo encontramos» en «no existe». Con el cliente eso deja de ser duda nuestra y pasa a ser un número que solo puede dar él. Ver [[barrer-el-catalogo-de-columnas-convierte-no-lo-encuentro-en-no-existe]]
- **Un campo migrado puede estar en la unidad de origen y no fallar nunca** — si el otro factor vino en la MISMA unidad equivocada se compensan, y no hay síntoma hasta que tocas una pieza creyéndote el nombre del campo (+49 %). Detección barata: busca la fila que se autodescribe y comprueba que vale lo que dice. Ver [[dos-piezas-en-la-misma-unidad-equivocada-dan-el-resultado-correcto]]
- **La `confianza` que declara un LLM no separa aciertos de fallos** — medido: 44 % dentro del ±10 %, con errores de −85 % y +3.757 % a confianza 0,80-0,90. Como umbral de auto-aceptación no filtra, solo lo aparenta: busca ground truth ANTES de elegir el umbral. Ver [[la-confianza-autodeclarada-de-un-llm-no-predice-su-acierto]]
- **Verdes que no miden lo que parece** — un 0 se lee como dato y suele ser «no medido»; el verde de un doble no distingue enchufado de olvidado. Ver [[campo-numerico-opcional-omitido-suma-cero-y-parece-dato]] · [[asercion-e2e-que-mide-datos-en-vez-de-montaje-es-verde-o-rojo-por-azar]] · [[agregar-sobre-todas-las-orgs-mezcla-datos-sembrados-con-datos-de-cliente]]
- **Tocar un prompt: la posición manda y n=10 no basta** — la regla dentro de su viñeta se aplica, en una nota posterior no; un literal JSON en un READ sangra al WRITE; comparar variantes exige **n≥25 entrelazado**. Ver [[un-prompt-es-una-superficie-con-localidad-no-un-documento]] · [[una-suite-de-evals-cuesta-llamadas-por-prompt-mide-el-cache-antes-de-proponerlo]]
- **Una ejecución en verde no prueba que el efecto ocurriera** — `success` = "no explotó"; mide que el nodo de efecto CORRIÓ (268 verdes y 0 envíos; 10-ago, 73 y 3). Y el `else` de un `switch` sobre un valor que rellena un LLM tiene que AVISAR: cada enum alucinado es un aviso perdido, en verde. Ver [[ejecucion-en-verde-no-prueba-el-efecto]] · [[el-else-de-un-clasificador-que-rellena-un-llm-debe-avisar-no-callar]]
- **Un job de fondo: pasada en el BOOT, no solo `setInterval`** — con autodeploy el timer nunca cumple un ciclo (4 días sin barrer); y su `last_error` en la BD no vale si nadie lo consulta. Ver [[un-timer-mas-largo-que-la-cadencia-de-despliegue-no-corre-nunca]] · [[persistir-el-error-no-basta-si-ninguna-superficie-lo-lee]]
- **Rama nueva desde main local sin fetch** — `worktree add ... main` nace vieja y pisa lo ya mergeado; usar `origin/main`. Al integrarla: fichero reescrito >2 veces → merge, no rebase; y sus rojos se clasifican (copy → actualizar esperado, regla del repo → arreglar código). Ver [[rama-nueva-desde-un-main-local-sin-fetch-revierte-trabajo-ajeno]] · [[rama-que-reescribe-el-mismo-fichero-varias-veces-se-integra-con-merge]] · [[los-tests-rojos-que-hereda-un-merge-se-clasifican-uno-a-uno]]
- **Al partir una pila en PRs, el fix va con el commit que lo causa** — si no, mergear el primero publica el fallo; con datos personales el hueco entre merges ES la exposición. Al MERGEARLA, squashear el padre deja a la hija `CONFLICTING` **o `MERGEABLE` reaplicando su diff**: `rebase --onto origin/main <padre>`. Ver [[al-partir-una-pila-en-prs-el-fix-tiene-que-viajar-con-lo-que-lo-causa]] · [[delete-branch-al-mergear-cierra-la-pr-apilada-no-la-reapunta]]
- **`create or replace` con otra firma crea una sobrecarga y `db push` dice `Finished`** — el fix se despliega muerto. Verifica `pg_proc`: UNA fila. Ver [[postgres-rpc-firma-identica-create-replace]]
- **Un comentario que afirma una invariante es una deuda de test** — grepea la afirmación contra el código antes de fiarte; si nadie la comprueba, no es cierta. Ver [[un-comentario-que-afirma-una-invariante-es-una-deuda-de-test]]
- **Un gate solo puede fallar HACIENDO RUIDO** — un camino que no encuentra nada y sale con 0 es un adorno: fail-closed, y avisar por `stderr` sin pesar en el exit code no es avisar. El gate que corres aparte NO es el del hook. Ver [[gate-en-segundo-plano-no-incluye-los-trinquetes-del-pre-commit]] · [[una-limpieza-multitabla-en-una-sola-query-es-todo-o-nada]] · [[un-script-gate-con-guard-de-entrypoint-degrada-a-no-op-silencioso]] · [[gate-con-ruta-relativa-no-corre-desde-subdirectorio-y-sale-verde]] · [[una-suite-en-verde-no-prueba-el-camino-real]] · [[git-toma-destino-e-identidad-del-entorno-no-del-cwd]]
- **Herramienta nueva sin barrer sus call-sites escritos NO se adopta** — el agente ejecuta lo ESCRITO (permisos, runbooks, memories), no lo del PATH. Ver [[un-wrapper-nuevo-no-se-adopta-si-no-barres-los-call-sites-escritos]]

- **Un verde esperado «vacío» no mide nada si el estado ya era vacío** — RLS sobre tabla vacía da `[]` con y sin RLS. Ver [[verificar-rls-en-tabla-vacia-no-discrimina]]

- **Un candado nuevo en `main` caza las PRs abiertas escritas ANTES que él** — solo lo ve el gate de la combinación. Ver [[un-candado-nuevo-en-main-caza-las-prs-abiertas-escritas-antes]]

## El resto (35)


- **Antes de decir «esto no se puede medir», enumera la taxonomía cerrada** — suele estar ya partido, y su comentario dice qué se decidió NO medir. Y decide señal (excepción → numerador) vs dimensión por evento (tasa → denominador). Ver [[una-senal-cuenta-excepciones-una-tasa-necesita-denominador]]
- **"Quién usa X ahora" en columna escalar (`used_by`) pierde con 2+ actores a la vez** — el último que reporta pisa al anterior sin error visible. Modelar como fila-por-actor, PK `(recurso, actor)`. Ver [[atribucion-quien-usa-x-ahora-columna-escalar-pierde-bajo-concurrencia]]
- **Protección construida y no enchufada: ningún test la caza** — el doble de la prueba ES el relleno. Señal: módulo con tests y cero consumidores. Ver [[una-proteccion-construida-y-no-enchufada-no-la-caza-ningun-test]]
- **Un entorno de pruebas más limpio que producción es ciego** — y su verde se cita como prueba. Ver [[el-replay-que-arranca-mas-limpio-que-produccion-es-ciego]]
- **Cambiar una ruta de estados vara en silencio las filas que ya cruzaron por la vieja** — nadie vuelve a mirarlas y no dan error; backfill por invariante en el MISMO PR, y con `UPDATE` directo, no con la RPC de dominio (arrastra sus efectos de negocio). Ver [[cambiar-la-ruta-de-una-maquina-de-estados-deja-varadas-las-filas-que-ya-pasaron]] y [[reparar-datos-con-la-rpc-de-dominio-arrastra-sus-efectos-de-negocio]]
- **«Determinista» en un comentario sobre un `sort` por timestamp es una alarma** — un `insert` en batch da a las N filas el mismo `created_at` y el orden pasa a ser el físico. Ver [[insertar-en-batch-da-el-mismo-created-at-y-ordenar-por-fecha-deja-de-desempatar]]

- **Un fix no está verificado hasta crear una entidad NUEVA tras el deploy** — leer los datos que arregló el backfill no prueba nada del código; el compositor no es el punto de persistencia y la suite verde no cubre el camino que tocas. Ver [[cambiar-la-semantica-de-una-columna-el-compositor-no-es-el-punto-de-persistencia]]
- **Un check de coherencia no puede afirmar un desajuste si no pudo preguntar** — 401/429 es "no verificado" (UNA alerta media), no N desajustes altos: la falsa induce a recrear datos sanos. Delator: fallan TODAS con el MISMO motivo. Ver [[fallo-de-credencial-no-es-dato-ausente-en-un-check-de-coherencia]]
- **Una clave read-only NO se verifica escribiendo** — el `POST` de prueba que esperaba un 403 devolvió 200 y creó objetos reales en una cuenta live. Lo comprobable leyendo es la CUENTA (`GET /v1/account`), no la ausencia de permiso de escritura. Ver [[no-verificar-una-clave-read-only-escribiendo-con-ella]]
- **`FETCH_HEAD` miente en cuanto haces un segundo `fetch`** — lo repunta, y lo que compruebes después mide otro árbol: falso negativo con `file:line` detrás. Usar `origin/<rama>`. Ver [[un-segundo-git-fetch-pisa-fetch-head-y-auditas-el-arbol-equivocado]]
- **`--force-with-lease` sin `fetch` no protege nada** — compara contra tu `origin/<rama>` LOCAL, así que un checkout desactualizado autoriza rebobinar `main` 40+ commits. Lease con SHA explícito, y verifica la recuperación por ÁRBOL, no por log. Ver [[force-with-lease-sin-fetch-no-protege-nada]]
- **Un locator que resuelve a 0 elementos es un test roto, no evidencia** — en un `if (isVisible)` es falso verde; tras un `test.skip(count === 0)`, verde PERMANENTE. Afirmar por rol/nombre accesible, nunca por clase de CSS Module. Ver [[locator-de-test-atado-a-la-implementacion-caduca-y-da-falso-verde]] Y un aserto por subcadena sobre `2>&1` lo cumple el mensaje de ERROR: asertar sobre estructura parseada. Ver [[un-aserto-por-subcadena-sobre-stdout-mas-stderr-lo-cumple-el-error]]
- **`npm ci` va DESPUÉS del rebase, y en cada proyecto del gate** — `node_modules` caduco: el gate muere en typecheck sin nombrar la causa. Ver [[rebasar-un-worktree-deja-node-modules-caduco-y-el-gate-no-lo-distingue]]
- **«No hardcodear el modo» lo vuelve inverificable desde el repo** — si el modo vive sólo en el panel, el checklist da verde leyendo una plantilla y lo irreversible se ejecuta bien. Léelo del sistema vivo. Ver [[no-hardcodear-el-modo-lo-hace-inverificable-desde-el-repo]]
- **Un camino crítico sin smoke se pudre meses aunque haya miles de tests al lado** — 7.541 unitarios y ninguno arrancaba Chromium: dos fallos de 2 meses en el que genera TODAS las facturas. Si produce el artefacto que ve el cliente y ningún test lo produce de verdad, no está cubierto. Ver [[camino-critico-sin-smoke-se-pudre-meses]]
- **Un test no vale hasta que le rompes el código y falla** — y miente en las dos direcciones: sin víctima, sospecha del **arnés** o del **estímulo** antes que del candado (un parche que dispara por OTRO motivo se lee igual que un gate que funciona). La lista de mutaciones sale del `git diff`, no del issue. Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] · [[un-arnes-de-mutacion-sobre-vitest-no-ve-los-candados-de-tipos]] · [[una-mutacion-que-produce-codigo-valido-no-demuestra-ningun-rojo]] · [[al-provocar-una-carrera-con-page-route-retrasa-la-entrega-no-el-envio]]
- **Frontera: verifica que existe ANTES de escribir, y que la sonda SABE FALLAR** — 12 «fugas cross-org» falsas por lo primero; otras 4 por una sonda que daba 200 con un id inexistente. Ver [[test-que-escribe-para-probar-una-frontera-verifica-antes-que-existe]] · [[un-control-negativo-que-no-discrimina-invalida-el-test-entero]]
- **Exit 0 + árbol limpio ≠ "no había trabajo"** — un proceso que agota cuota se hace pasar por "sin cambios". Clasificar por texto de stdout, no por exit code. Ver [[proceso-que-agota-la-cuota-puede-salir-con-exit-0-y-parecer-sin-cambios]]
- **El `$?` que lees puede ser el del `echo`, y el rojo puede no ser tuyo** — `gate > log; echo "exit=$?"`; basura local en `.gitignore` pero no en `.dockerignore`; un artefacto de build que falta. Ver [[el-exit-code-que-lees-no-es-el-del-comando-que-te-importa]] · [[dockerignore-no-es-gitignore-y-la-basura-local-pone-el-gate-rojo]]
- **Antes de «N candados», mide cuántos PUEDEN fallar** — de 141 aserciones, 137 eran incapaces de fallar. Cierra la clase en el INSTRUMENTO y asevera el bicondicional, no la igualdad. Ver [[mide-cuantos-pueden-fallar-antes-de-elegir-entre-n-candados-y-un-tripwire]] · [[aseverar-la-igualdad-congela-un-accidente-asevera-el-bicondicional]] · [[un-fichero-nuevo-es-un-solo-hunk-y-el-barrido-de-mutacion-no-lo-cubre]]
- **Un gate con cientos de skips por entorno sale ✓ VERDE sin haber probado nada** — el puerto ocupado por otro proyecto es la causa más frecuente; desglosa los skips por fichero antes de decir verde. Ver [[e2e-smoke-skip-honesto]]
- **Rojos que no son del código: dos causas, y se confunden** — tiempos clavados en el tope = contención (aísla; si reincide al crecer la suite, sube el tope). **Exit 143 + RSS bajo + cero jetsam = te han matado**: otra sesión con `pkill -f` y cambiar de puerto no protege. Ver [[tests-que-caen-por-contencion-de-cpu-verificalos-aislados-antes-de-diagnosticar]] · [[otra-sesion-con-pkill-mata-tu-servidor-y-parece-un-bug-del-producto]]
- **Un fake cuya FORMA de retorno satisface la aserción verifica el fake, no el código** — y `toMatchObject` para afirmar AUSENCIA de una clave siempre pasa. Ver [[mock-funcion-compartida-en-test-endpoint-falso-verde-composicion]]
- **Un `Workflow` muerto a mitad no pierde nada: está en `journal.jsonl`** — vuelca los resultados al repo ANTES de arreglar; reanuda con `resumeFromRunId` y los agentes idénticos salen de caché, así que subir un tope y reanudar es barato. Ver [[workflow-cortado-a-mitad-los-resultados-viven-en-journal-jsonl]]
- **Un helper de traza con `if (!orgId) return` deja sin auditar justo lo global** — mide la DISTRIBUCIÓN de acciones registradas, no que la tabla tenga filas. Ver [[helper-de-auditoria-con-early-return-deja-sin-traza-lo-global]]
- **Specs de una rama contra el binario de otra: el marcador sale y no vale** — clasifica un rojo construyendo `origin/main` en el MISMO worktree. Ver [[tanda-e2e-con-specs-de-una-rama-y-binario-de-otra-no-mide-nada]]

- **Ese «bloqueante» de arriba no bloquea si el helper se traga los fallos** — supabase-js no lanza en un insert fallido, devuelve `{ error }`: envolverlo en `try/catch` es código muerto. Ver [[supabase-js-no-lanza-en-insert-asi-que-el-try-catch-del-caller-es-codigo-muerto]]
- **Tu red de tests puede estar ciega al gesto real** — jsdom y `fill()` de Playwright no teclean. Ver [[jsdom-no-reproduce-el-reset-de-seleccion-al-cambiar-input-type]] · [[playwright-fill-escribe-value-y-deja-obsoleto-el-estado-del-componente]]
- **Un arreglo se verifica recorriendo el caso real** — el apaño del usuario atascado dispara el guard nuevo. Ver [[el-parche-del-usuario-atascado-dispara-el-guard-del-arreglo]] · [[una-pista-detras-de-un-gate-que-el-caso-afectado-no-cumple-no-existe]]
- **El esquema se aplica ANTES de mergear su código, y el hueco de migración caduca** — si no, prod llama a lo que no existe. Ver [[aplicar-migraciones-a-prod-antes-del-merge-caduca-la-reserva-de-numero]]
- **Convertir una columna en DERIVADA arma el pasado** — las filas que ya tenían el valor a mano no tienen evento y el primer recálculo las pone a cero (1.312 facturas). Censo, backfill, y verificar volviendo a derivar. Ver [[convertir-columna-en-derivada-exige-backfill-del-historico]]
- **Clave única compuesta `(org_id, business_key)` desde el diseño elimina el guard de upsert cross-tenant** — decide la composición del índice ANTES de escribir el upsert, no después. Ver [[clave-compuesta-por-tenant-elimina-el-guard-de-upsert-cross-tenant]]
- **Un gate que enumera con `git ls-files` no ve un fichero nuevo sin `git add` antes** — un fichero recién escrito y sin añadir al índice es invisible para el gate que lo debía vigilar. Ver [[gate-por-git-ls-files-no-ve-un-fichero-nuevo-sin-git-add]] · [[hot-archivo-2026-08-01]]
- **Fail-closed sobre INICIAR lo peligroso, nunca sobre SUPERVISAR lo que ya está en vuelo** — abortar el arranque mata también el plano de control y deja sin vigilancia lo que sigue abierto; la guarda va en el cuello de la acción, no en el arranque. Ver [[una-guarda-que-mata-el-proceso-deja-huerfano-lo-que-ya-esta-en-vuelo]]
- **Antes de mergear una validación que bloquea, cuenta en prod a quién bloquea** — y cuántos de esos YA usan el flujo. Esa segunda cifra es la que cambia la decisión. Ver [[antes-de-mergear-una-validacion-que-bloquea-cuenta-a-quien-bloquea]]
- **Antes de preguntarle un DATO al cliente, míralo en su sistema origen** — 3 veces en un día íbamos a pedir lo que ya teníamos en su backup. Las preguntas legítimas son de decisión. Ver [[antes-de-preguntar-al-cliente-mira-si-el-dato-esta-en-el-sistema-origen]]
- **Un guard cuya aguja cubre UNA forma sintáctica se esquiva refactorizando** — sacar el objeto de `style={{…}}` a una variable lo hacía invisible sin quitarlo del DOM. Al tocar algo que un trinquete debería contar, comprueba que el número se mueve; si no se mueve, el guard es el bug. Ver [[un-guard-cuya-aguja-cubre-una-sola-forma-sintactica-se-esquiva-refactorizando]]
