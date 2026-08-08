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

## Ha vuelto a pasar (8)

Estas no son advertencias teóricas: su learning documenta que el fallo **reincidió** después de
estar escrito. Si una de estas se puede comprobar con un comando, su sitio es un hook, no esta lista.

- **Un «no se puede» heredado caduca** — pregunta POR QUÉ, no SI: el booleano envejece, el hecho no. Ver [[un-no-se-puede-heredado-caduca-como-cualquier-otra-frase]]
- **`cmd > fichero` vacía el fichero antes de arrancar `cmd`** — un generador que falla borra su propia fuente de verdad, sin propagar el exit code. Ver [[redirigir-con-mayor-que-destruye-el-fichero-antes-de-arrancar-el-comando]]
- **El gate escrito justo tras el arreglo mide cero casos** — demuestra el rojo contra el árbol ANTERIOR. Ver [[el-gate-escrito-justo-despues-del-arreglo-mide-cero-casos]]
- **`git commit -- <ruta>` no te aísla** si otra sesión tiene el índice cargado en el mismo checkout. Ver [[commit-por-ruta-no-te-aisla-de-otra-sesion-con-el-indice-cargado]]
- **Un gate sobre el RESULTADO no valida la transformacion** — si reescalas dos campos a la vez (uno /f, otro xf), el producto es invariante **por construccion para cualquier f**: el gate que compara el resultado antes y despues pasa en verde con f=10. Ataca el PARAMETRO, no el resultado. Test para saber si tu gate es gate: ¿con que valor fallaria? Si no encuentras ninguno, no es un gate. Ver [[un-gate-sobre-el-resultado-no-valida-la-transformacion]]
- **El coste de un fan-out de agentes es CONTEXTO, no razonamiento** — 94 % en cache read/write, 6 % en output. La palanca no es bajar effort: es inyectarles lo que ya sabes en vez de que lo redescubran. Ver [[el-coste-de-un-fanout-de-agentes-es-contexto-no-razonamiento]]
- **Redondea antes de decidir la frontera, no despues** — si no, salen «5 h 60 min» y «60 s». Y pruebalo con un BARRIDO: con casos elegidos (59 y 60) la banda de en medio pasa. Ver [[decidir-una-frontera-con-el-valor-crudo-produce-imposibles]]
- **Un trigger que PISA en vez de calcular te resincroniza los datos al migrar** — `SET hijo = NEW.padre` propaga el valor del padre, no tu conversion, y de paso corrige toda desincronia previa: 188 precios movidos. Ver [[un-trigger-que-pisa-en-vez-de-calcular-resincroniza-al-migrar]]
- **La precision de una columna la marca su valor MAXIMO, no el tipico** — `SELECT max(col)` antes de elegir la escala. Y la fila basura que documentas y decides ignorar **sigue participando en los calculos**. Ver [[una-fila-basura-amplifica-el-error-de-redondeo-de-toda-la-tabla]]
- **Un precio unitario de 1,00 marca una cantidad que en realidad son euros** — el truco universal de los ERP para meter un importe (subcontrata) por una columna de cantidad. En los partes de WAPI eran **38 líneas con 53.111 «horas»** contra 451 con 25.361 reales; sin excluirlas, cualquier `SUM(cant*precio)/SUM(cant)` mezcla dos unidades. Agrupa por precio y ordena por volumen: la fila contaminada canta sola. Ver [[precio-unitario-1-00-marca-una-cantidad-que-son-euros]]
- **Antes de decir «ese dato no está», barre el catálogo de columnas** — `sys.columns` / `information_schema.columns` por el nombre del CONCEPTO sobre todas las tablas cuesta un segundo y convierte «no lo encontramos» en «no existe». Con el cliente eso deja de ser duda nuestra y pasa a ser un número que solo puede dar él. Ver [[barrer-el-catalogo-de-columnas-convierte-no-lo-encuentro-en-no-existe]]
- **Un campo migrado puede estar en la unidad de origen y no fallar nunca** — si el otro factor vino en la MISMA unidad equivocada, se compensan y el resultado sale bien. No hay síntoma hasta que tocas una pieza creyéndote el nombre del campo (poner un coste en €/hora real en un campo que estaba en unidades del ERP: +49 %). Detección barata: busca la fila que se autodescribe y comprueba que vale lo que dice (`TIEMPO 1 HORA` valía 1,4920). Ver [[dos-piezas-en-la-misma-unidad-equivocada-dan-el-resultado-correcto]]
- **La `confianza` que declara un LLM no separa aciertos de fallos** — medido contra ground truth: 44 % dentro del ±10 %, y errores de −85 % y +3.757 % con confianza 0,80-0,90. Como umbral de auto-aceptación no filtra nada, solo lo aparenta. Busca un ground truth aunque sea parcial ANTES de elegir el umbral; sin él no hay auto-aceptación posible. Ver [[la-confianza-autodeclarada-de-un-llm-no-predice-su-acierto]]
- **Verdes que no miden lo que parece** — un 0 se lee como dato (campo opcional que nadie escribe), y un agregado multi-tenant mide el seed (59.220 líneas sandbox contra 9 reales). Excluir `is_test` antes de concluir. Ver [[campo-numerico-opcional-omitido-suma-cero-y-parece-dato]] · [[agregar-sobre-todas-las-orgs-mezcla-datos-sembrados-con-datos-de-cliente]]
- **Tocar un prompt: la posición manda y n=10 no basta** — la regla dentro de su viñeta se aplica, en una nota posterior no; un literal JSON en un READ sangra al WRITE; comparar variantes exige **n≥25 entrelazado**. Ver [[un-prompt-es-una-superficie-con-localidad-no-un-documento]] · [[una-suite-de-evals-cuesta-llamadas-por-prompt-mide-el-cache-antes-de-proponerlo]]
- **Una ejecución en verde no prueba que el efecto ocurriera** — `success` = "no explotó"; mide que el nodo de efecto CORRIÓ (268 verdes y cero envíos). Ver [[ejecucion-en-verde-no-prueba-el-efecto]]
- **Un job de fondo: pasada en el BOOT, no solo `setInterval`** — con autodeploy el timer nunca cumple un ciclo (4 días sin barrer); y su `last_error` en la BD no vale si nadie lo consulta. Ver [[un-timer-mas-largo-que-la-cadencia-de-despliegue-no-corre-nunca]] · [[persistir-el-error-no-basta-si-ninguna-superficie-lo-lee]]
- **Rama nueva desde main local sin fetch** — `worktree add ... main` nace vieja y pisa lo ya mergeado; usar `origin/main`. Al integrarla: fichero reescrito >2 veces → merge, no rebase; y sus rojos se clasifican (copy → actualizar esperado, regla del repo → arreglar código). Ver [[rama-nueva-desde-un-main-local-sin-fetch-revierte-trabajo-ajeno]] · [[rama-que-reescribe-el-mismo-fichero-varias-veces-se-integra-con-merge]] · [[los-tests-rojos-que-hereda-un-merge-se-clasifican-uno-a-uno]]
- **Al partir una pila en PRs, el fix va con el commit que lo causa** — si no, mergear el primero publica el fallo; con datos personales el hueco entre merges ES la exposición. Ver [[al-partir-una-pila-en-prs-el-fix-tiene-que-viajar-con-lo-que-lo-causa]]
- **`create or replace` con otra firma crea una sobrecarga y `db push` dice `Finished`** — el fix se despliega muerto. Verifica `pg_proc`: UNA fila. Ver [[postgres-rpc-firma-identica-create-replace]]
- **Un comentario que afirma una invariante es una deuda de test** — grepea la afirmación contra el código antes de fiarte; si nadie la comprueba, no es cierta. Ver [[un-comentario-que-afirma-una-invariante-es-una-deuda-de-test]]
- **Un gate solo puede fallar HACIENDO RUIDO** — si hay un camino donde no mide y sale con 0, será el de producción. Al matar un CI, migrar sus gates uno a uno. Ver [[un-script-gate-con-guard-de-entrypoint-degrada-a-no-op-silencioso]] · [[una-metrica-por-regex-sin-test-del-parser-cuenta-ruido-y-se-vuelve-ignorable]]
- **Herramienta nueva sin barrer sus call-sites escritos NO se adopta** — el agente ejecuta lo ESCRITO (permisos, runbooks, memories), no lo del PATH. Ver [[un-wrapper-nuevo-no-se-adopta-si-no-barres-los-call-sites-escritos]]
- **Ni reforzando el prompt se garantiza que el LLM llame a una tool crítica** — content y tool_call son mutuamente excluyentes en una misma respuesta; si la tool tiene efecto externo obligatorio (email, CRM), pre-check determinista antes del LLM, no más prompt. Ver [[tool-description-generica-no-fuerza-ejecucion-de-tool-critica]]

## El resto (38)


- **Antes de decir «esto no se puede medir», enumera la taxonomía cerrada** — suele estar ya partido, y su comentario dice qué se decidió NO medir. Y decide señal (excepción → numerador) vs dimensión por evento (tasa → denominador). Ver [[una-senal-cuenta-excepciones-una-tasa-necesita-denominador]]
- **"Quién usa X ahora" en columna escalar (`used_by`) pierde con 2+ actores a la vez** — el último que reporta pisa al anterior sin error visible. Modelar como fila-por-actor, PK `(recurso, actor)`. Ver [[atribucion-quien-usa-x-ahora-columna-escalar-pierde-bajo-concurrencia]]
- **Protección construida y no enchufada: ningún test la caza** — el doble de la prueba ES el relleno. Señal: módulo con tests y cero consumidores. Ver [[una-proteccion-construida-y-no-enchufada-no-la-caza-ningun-test]]
- **Un entorno de pruebas más limpio que producción es ciego** — y su verde se cita como prueba. Ver [[el-replay-que-arranca-mas-limpio-que-produccion-es-ciego]]

- **Preferencia por tenant restaurada de un `localStorage` global se filtra entre organizaciones** — el switch de empresa recarga y aplica la clave del tenant anterior. Sembrar en servidor. Encender una restauración muerta es cambio de comportamiento, no arreglo. Ver [[localstorage-global-en-app-multitenant-filtra-entre-organizaciones]]
- **`curl` en macOS valida una cadena TLS que GitHub y Node rechazan** — completa el intermedio por su cuenta y te engaña; cuenta posiciones con `openssl s_client`. Ver [[cadena-tls-incompleta-curl-en-macos-la-salva-y-engana]]
- **Un fix no está verificado hasta crear una entidad NUEVA tras el deploy** — leer los datos que arregló el backfill no prueba nada del código; el compositor no es el punto de persistencia y la suite verde no cubre el camino que tocas. Ver [[cambiar-la-semantica-de-una-columna-el-compositor-no-es-el-punto-de-persistencia]]
- **Un check de coherencia no puede afirmar un desajuste si no pudo preguntar** — 401/429 es "no verificado" (UNA alerta media), no N desajustes altos: la falsa induce a recrear datos sanos. Delator: fallan TODAS con el MISMO motivo. Ver [[fallo-de-credencial-no-es-dato-ausente-en-un-check-de-coherencia]]
- **Una clave read-only NO se verifica escribiendo** — el `POST` de prueba que esperaba un 403 devolvió 200 y creó objetos reales en una cuenta live. Lo comprobable leyendo es la CUENTA (`GET /v1/account`), no la ausencia de permiso de escritura. Ver [[no-verificar-una-clave-read-only-escribiendo-con-ella]]
- **`FETCH_HEAD` miente en cuanto haces un segundo `fetch`** — lo repunta, y lo que compruebes después mide otro árbol: falso negativo con `file:line` detrás. Usar `origin/<rama>`. Ver [[un-segundo-git-fetch-pisa-fetch-head-y-auditas-el-arbol-equivocado]]
- **`--force-with-lease` sin `fetch` no protege nada** — compara contra tu `origin/<rama>` LOCAL, así que un checkout desactualizado autoriza rebobinar `main` 40+ commits. Lease con SHA explícito, y verifica la recuperación por ÁRBOL, no por log. Ver [[force-with-lease-sin-fetch-no-protege-nada]]
- **Un locator que resuelve a 0 elementos es un test roto, no evidencia** — en un `if (isVisible)` es falso verde; tras un `test.skip(count === 0)`, verde PERMANENTE. Afirmar por rol/nombre accesible, nunca por clase de CSS Module. Ver [[locator-de-test-atado-a-la-implementacion-caduca-y-da-falso-verde]] Y un aserto por subcadena sobre `2>&1` lo cumple el mensaje de ERROR: asertar sobre estructura parseada. Ver [[un-aserto-por-subcadena-sobre-stdout-mas-stderr-lo-cumple-el-error]]
- **`npm ci` va DESPUÉS del rebase, y en cada proyecto del gate** — un worktree rebasado tiene `node_modules` presente pero CADUCO; el gate muere en el typecheck y dice «murió antes de arrancar», que es cierto y no nombra la causa (3 corridas perdidas en un tren de 7 merges; 2 más el 7-ago). Ya hay máquina en camino (AGH #1062) → **sale de aquí cuando entre**. Ver [[rebasar-un-worktree-deja-node-modules-caduco-y-el-gate-no-lo-distingue]]
- **"No hardcodear el modo" lo vuelve inverificable desde el repo** — `TRADING_MODE`/`DRY_RUN` viven solo en el panel y el checklist da verde leyendo una plantilla. Un modo mal puesto no rompe: ejecuta bien lo irreversible (32 h en `live`, −1.613 USDT). Léelo del sistema vivo. Ver [[no-hardcodear-el-modo-lo-hace-inverificable-desde-el-repo]]
- **Un camino crítico sin smoke se pudre meses aunque haya miles de tests al lado** — 7.541 unitarios y ninguno arrancaba Chromium: dos fallos de 2 meses en el que genera TODAS las facturas. Si produce el artefacto que ve el cliente y ningún test lo produce de verdad, no está cubierto. Ver [[camino-critico-sin-smoke-se-pudre-meses]]
- **Un test no vale hasta que le rompes el código y falla** — y si la mutación sale SIN víctima, sospecha del **arnés** antes que del candado: medido 3 de cada 4. Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]]. **Y mutar a mano solo cubre tu hipótesis: el diff es la lista objetiva** (una PR con 9 mutaciones se coló igual, todas sobre sus propios ejes) → [[barrer-el-diff-en-vez-de-mutar-a-mano]]
- **Exit 0 + árbol limpio ≠ "no había trabajo"** — un proceso que agota cuota se hace pasar por "sin cambios". Clasificar por texto de stdout, no por exit code. Ver [[proceso-que-agota-la-cuota-puede-salir-con-exit-0-y-parecer-sin-cambios]]
- **Un gate con cientos de skips por entorno sale ✓ VERDE sin haber probado nada** — el puerto ocupado por otro proyecto es la causa más frecuente; desglosa los skips por fichero antes de decir verde. Ver [[e2e-smoke-skip-honesto]]
- **Tests rojos con los tiempos clavados en 5000 ms = contención, no código** — córrelos aislados antes de diagnosticar nada; y si es reproducible al crecer la suite, el tope de fábrica está decidiendo el color del rojo: súbelo en un solo sitio. Ver [[tests-que-caen-por-contencion-de-cpu-verificalos-aislados-antes-de-diagnosticar]]
- **Un fake cuya FORMA de retorno satisface la aserción verifica el fake, no el código** — y `toMatchObject` para afirmar AUSENCIA de una clave siempre pasa. Ver [[mock-funcion-compartida-en-test-endpoint-falso-verde-composicion]]
- **Un helper de traza con `if (!orgId) return` deja sin auditar justo lo global** — mide la DISTRIBUCIÓN de acciones registradas, no que la tabla tenga filas. Ver [[helper-de-auditoria-con-early-return-deja-sin-traza-lo-global]]
- **Specs de una rama contra el binario de otra: el marcador sale y no vale** — clasifica un rojo construyendo `origin/main` en el MISMO worktree. Ver [[tanda-e2e-con-specs-de-una-rama-y-binario-de-otra-no-mide-nada]]

- **Ese «bloqueante» de arriba no bloquea si el helper se traga los fallos** — supabase-js no lanza en un insert fallido, devuelve `{ error }`: envolverlo en `try/catch` es código muerto. Ver [[supabase-js-no-lanza-en-insert-asi-que-el-try-catch-del-caller-es-codigo-muerto]]
- **Tu red de tests puede estar ciega al gesto real** — jsdom y `fill()` de Playwright no teclean. Ver [[jsdom-no-reproduce-el-reset-de-seleccion-al-cambiar-input-type]] · [[playwright-fill-escribe-value-y-deja-obsoleto-el-estado-del-componente]]
- **Un arreglo se verifica recorriendo el caso real** — el apaño del usuario atascado dispara el guard nuevo. Ver [[el-parche-del-usuario-atascado-dispara-el-guard-del-arreglo]] · [[una-pista-detras-de-un-gate-que-el-caso-afectado-no-cumple-no-existe]]
- **El esquema se aplica ANTES de mergear su código, y el hueco de migración caduca** — si no, prod llama a lo que no existe. Ver [[aplicar-migraciones-a-prod-antes-del-merge-caduca-la-reserva-de-numero]]
- **Convertir una columna en DERIVADA arma el pasado** — las filas que ya tenían el valor a mano no tienen evento y el primer recálculo las pone a cero (1.312 facturas). Censo, backfill, y verificar volviendo a derivar. Ver [[convertir-columna-en-derivada-exige-backfill-del-historico]]
- **Clave única compuesta `(org_id, business_key)` desde el diseño elimina el guard de upsert cross-tenant** — decide la composición del índice ANTES de escribir el upsert, no después. Ver [[clave-compuesta-por-tenant-elimina-el-guard-de-upsert-cross-tenant]]
- **Dos escrituras a tablas distintas que deben ser atómicas exigen un RPC, nunca dos llamadas REST/supabase-js** — cada `.from(x).insert()` es su propia transacción. `SECURITY DEFINER` si escribe con privilegio de servicio, `INVOKER` si debe respetar la RLS de sesión igual que el cliente. Ver [[verifactu-rpc-atomico-cierra-race-transacciones-rest-separadas]]
- **Un gate que enumera con `git ls-files` no ve un fichero nuevo sin `git add` antes** — el "verde" de un gate recién escrito puede significar solo "no vio el árbol", no "el árbol está limpio". `git add` primero, gate después. Ver [[gate-por-git-ls-files-no-ve-un-fichero-nuevo-sin-git-add]]

> **Las otras 50 no se han borrado**: siguen vigentes en [[hot-archivo-2026-08-01]] y se recuperan por
> wikilink y por grep. (El tope vigente es el de la cabecera, no el "25" que decía aquí.)
>
> Los contadores de las dos secciones decían 7 y **63** con 7 y **36** reales: un número que nadie
> recalcula al añadir una entrada miente a la primera. Corregidos el 3-ago; si vuelven a divergir, el
> arreglo es contarlos con un comando, no a mano.
- **Fail-closed sobre INICIAR lo peligroso, nunca sobre SUPERVISAR lo que ya está en vuelo** — abortar el arranque mata también el plano de control y deja sin vigilancia lo que sigue abierto; la guarda va en el cuello de la acción, no en el arranque. Ver [[una-guarda-que-mata-el-proceso-deja-huerfano-lo-que-ya-esta-en-vuelo]]
- **Antes de mergear una validación que bloquea, cuenta en prod a quién bloquea** — y cuántos de esos YA usan el flujo. Esa segunda cifra es la que cambia la decisión. Ver [[antes-de-mergear-una-validacion-que-bloquea-cuenta-a-quien-bloquea]]
- **Antes de preguntarle un DATO al cliente, míralo en su sistema origen** — 3 veces en un día íbamos a pedir lo que ya teníamos en su backup. Las preguntas legítimas son de decisión. Ver [[antes-de-preguntar-al-cliente-mira-si-el-dato-esta-en-el-sistema-origen]]
- **Republicar un `Artifact`: pide el listado Y haz `WebFetch` antes** — la pertenencia al listado **no es estable** (cambia entre sesiones del mismo día, en los dos sentidos), y republicar sobre una URL listada falla igual con «this session hasn't viewed the latest version». Lo que desbloquea es el `WebFetch` previo, que además es lo único que enseña si la copia publicada va por detrás del fichero local. Seis URL huérfanas hasta aprenderlo (7-ago). Ver [[artifact-solo-lo-republica-la-cuenta-que-lo-publico]]
- **Descartar trabajo sin commitear ya es MÁQUINA, no advertencia** — `git-guard` bloquea `reset --hard` en todas sus formas, `checkout`/`restore` de rutas sucias (con y sin `--`) y `worktree remove` con cambios pendientes. Lo que sigue siendo tuyo: si aun así se pierde, el `.jsonl` de la sesión guarda el resultado completo de cada subagente y se reimplementa desde ahí; y no inventes el mecanismo de una anomalía sin reproducirla. Ver [[transcript-jsonl-sobrevive-al-worktree-borrado]] y [[dos-salidas-contradictorias-no-son-un-mecanismo-hasta-que-lo-reproduces]]
- **Un guard cuya aguja cubre UNA forma sintáctica se esquiva refactorizando** — sacar el objeto de `style={{…}}` a una variable lo hacía invisible sin quitarlo del DOM. Al tocar algo que un trinquete debería contar, comprueba que el número se mueve; si no se mueve, el guard es el bug. Ver [[un-guard-cuya-aguja-cubre-una-sola-forma-sintactica-se-esquiva-refactorizando]]
