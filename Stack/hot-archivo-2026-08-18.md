---
title: hot cache — archivo 2026-08-18
date: 2026-08-18
source: claude-code-session
tags: [stack, index, archivo]
---

# Hot cache — lo movido el 2026-08-18

`Stack/hot.md` declara un tope de **25 entradas** y tenía **79**. Se mueve la
sección «El resto» (37 entradas): **ninguna está mal ni caducada** — son método transversal, y por eso
conservan su `[[wikilink]]`, que es lo que las hace recuperables navegando. Se mueven porque el hot se lee
al arrancar **sin disparador**, así que cada entrada se paga en sesiones a las que no viene al caso.

⚠️ Y un dato del propio fichero, porque es el patrón que este vault ficha una y otra vez: sus dos
encabezados **declaraban 25 y 35** cuando tenía **28 y 37**. Un contador escrito a mano deja de
contar en cuanto alguien añade sin actualizarlo — de ahí que la poda arregle también los números.

Ver [[hot]] · [[hot-archivo-2026-08-01]]

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
- **Reserva/dedup idempotente en n8n** — Redis INCR+TTL como lock (no hay SET NX) + bookingKey releído antes de crear. Ver [[lock-e-idempotencia-en-n8n-con-redis-incr-sin-set-nx]]

- **Un verde esperado «vacío» no mide nada si el estado ya era vacío** — RLS sobre tabla vacía da `[]` con y sin RLS. Ver [[verificar-rls-en-tabla-vacia-no-discrimina]]
- **Un candado nuevo en `main` caza las PRs abiertas escritas ANTES que él** — solo lo ve el gate de la combinación. Ver [[un-candado-nuevo-en-main-caza-las-prs-abiertas-escritas-antes]]
- **Importar un helper desde otro `.test.ts` re-ejecuta sus casos** — el delta de la rama miente y los gates cuadran igual. [[importar-de-un-fichero-de-test-re-ejecuta-sus-casos]]
