---
title: hot cache
date: 2026-07-29
tags: [stack, index]
---

# Hot Cache

- **El coste de Claude Code está en el tamaño de sesión, no en el CLAUDE.md** — 77 % es cache-read y el 91 % se gasta por encima de 200k. Y un `paths:` de rules dispara con `Read`, **no con Bash**. Ver [[donde-se-va-el-coste-de-claude-code-no-es-el-claude-md]]
- **StructuredOutput de Workflow cae con schemas anidados: reponer la dimensión como agente suelto con JSON-por-texto** — y un status `no-ejecutada` nunca cuenta como revisado. Ver [[workflow-structured-output-cae-con-schemas-anidados-relanzar-como-agente-suelto]]
- **Todo bot de voz o chat debe identificarse como IA en la primera interacción** (art. 50 del AI Act, vigente desde el 2-ago-2026) — y el aviso va en el flujo, no en el prompt: si depende del modelo, el incumplimiento es silencioso. Ver [[una-obligacion-legal-no-puede-colgar-del-prompt-del-llm]]
- **Un control que afirmas a un cliente necesita REGISTRO con fecha** — una afirmación de control no la caza ningún test, solo una auditoría. Ver [[un-control-que-un-documento-cliente-facing-afirma-necesita-registro]]
- **mig:renumerar fail-open en worktrees; propiedad de un número = catálogo, no registro** — [[aplicar-migraciones-a-prod-antes-del-merge-caduca-la-reserva-de-numero]]
- **Cuenta los motores que calculan el mismo número antes de arreglar uno** — una función SQL y su espejo TS divergen en silencio; el issue nombraba 1 de 2 mitades y 1 de 3 patas. Ver [[cuenta-los-motores-que-calculan-el-mismo-numero-antes-de-arreglar-uno]]
- **Al retirar una columna o su escritor, grep de quién la LEE** — el `DROP` no avisa de la función que la usa (cuerpo en cadena = sin `pg_depend`, revienta con `42703` en runtime), y un guard sobre una columna que ya nadie rellena compila y tiene tests verdes sin proteger nada. Ver [[funcion-sql-con-cuerpo-en-cadena-no-registra-dependencia-de-columna]]
- **«¿Existe X?» se busca por la LLAMADA, no por el módulo** — la carpeta esperada contesta otra pregunta. Ver [[buscar-una-capacidad-por-su-llamada-no-por-el-modulo-donde-crees-que-vive]]
- **Un guard que mide un sustituto bloquea sin que nadie pruebe el hecho** — si aborta ANTES de intentar la operación, el error nunca aparece (once días parados). Comprueba el RESULTADO al final, no el permiso al principio. Ver [[un-guard-que-mide-un-sustituto-bloquea-sin-que-nadie-pruebe-el-hecho]]
- **Acotar una API por scopes no la acota** — rutas distintas comparten scope: allowlist de endpoints en el wrapper, así una ruta nueva nace fuera. Ver [[acotar-una-api-por-scopes-no-la-acota-usa-allowlist-de-endpoints]]
- **El sujeto de un smoke debe pasar los gates ANTERIORES** — un 402 de billing tapa el 403 que medías. Ver [[el-gate-de-billing-va-antes-que-el-de-plan-y-tapa-lo-que-querias-medir]]
- **Borrar una rama es un paso APARTE, al final** — con `&&` al merge corre aunque el merge se aborte, y **cierra la PR sin poder reabrirla**; con worktrees, `--delete-branch` mergea pero NO borra. Ver [[el-borrado-de-rama-nunca-va-encadenado-al-merge]] · [[gh-pr-merge-delete-branch-no-borra-la-rama-si-falla-su-checkout-local]]
- **Un grep negativo por el nombre del origen es ciego a un renombrado en la frontera** — probaba que el identificador no está, no que el dato no llegue: cruzaba con otro nombre. Persíguelo desde el PRODUCTOR. Ver [[un-grep-negativo-por-el-nombre-del-origen-es-ciego-a-un-renombrado-en-la-frontera]]
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

## Ha vuelto a pasar (28)
- **Cierre de tanda = suite COMPLETA sobre `main`** — el gate por rama no ve los guards. Ver [[suite-filtrada-por-carpetas-del-pr-no-ve-los-guards-de-arquitectura]]

Estas no son advertencias teóricas: su learning documenta que el fallo **reincidió** después de
estar escrito. Si una de estas se puede comprobar con un comando, su sitio es un hook, no esta lista.

- **Arreglar un flake en UN fichero garantiza que vuelva por el hermano** — 7 de 9 nacieron sin el `pool.on("error")` copiado a mano; se cierra con un punto único que DISCRIMINE y un barrido que impida el noveno. Ver [[vitest-unhandledrejection-run-rojo-pese-a-0-fallos]]
- **Un backfill se guarda por el INVARIANTE, no por el síntoma** — «a toda fila sin X, ponle X» habría duplicado 106 de 115 filas; la condición que lo hace neutro deja 9. Ver [[backfill-guardado-por-invariante-en-vez-de-por-sintoma]]
- **Citar el delimitador dentro de su propia región la cierra ahí mismo** — `$$` en un comentario de `do $$`, acento grave en plantilla, `*/` en JSDoc; el error sale LEJOS. Nadie lo ve porque `allowJs:false` deja los `.mjs` fuera de `tsc` y un fichero que nadie ejecuta no lo analiza nada. Ver [[citar-el-delimitador-dentro-de-su-propia-region-la-cierra-ahi-mismo]]
- **Un gate que cruza dos listas es ciego a lo que no está en ninguna** — cruzar A contra B no ve lo que falta en las dos; hace falta una tercera fuente, normalmente el disco. Ver [[un-gate-que-cruza-dos-listas-es-ciego-a-lo-que-no-esta-en-ninguna]]
- **Un «no se puede» heredado caduca** — pregunta POR QUÉ, no SI: el booleano envejece, el hecho no. Ver [[un-no-se-puede-heredado-caduca-como-cualquier-otra-frase]]
- **`cmd > fichero` vacía el fichero antes de arrancar `cmd`** — un generador que falla borra su propia fuente de verdad, sin propagar el exit code. Ver [[redirigir-con-mayor-que-destruye-el-fichero-antes-de-arrancar-el-comando]]
- **El gate escrito justo tras el arreglo mide cero casos** — demuestra el rojo contra el árbol ANTERIOR. Ver [[el-gate-escrito-justo-despues-del-arreglo-mide-cero-casos]]
- **Un gate sobre el RESULTADO no valida la transformación** — dos campos reescalados a la vez dejan el producto invariante para cualquier `f`. Ataca el PARÁMETRO. Test: ¿con qué valor fallaría? Si no hay ninguno, no es un gate. Ver [[un-gate-sobre-el-resultado-no-valida-la-transformacion]]
- **Redondea antes de decidir la frontera, no despues** — si no, salen «5 h 60 min» y «60 s». Y pruebalo con un BARRIDO: con casos elegidos (59 y 60) la banda de en medio pasa. Ver [[decidir-una-frontera-con-el-valor-crudo-produce-imposibles]]
- **Un trigger que PISA en vez de calcular te resincroniza los datos al migrar** — `SET hijo = NEW.padre` propaga el valor del padre, no tu conversion, y de paso corrige toda desincronia previa: 188 precios movidos. Ver [[un-trigger-que-pisa-en-vez-de-calcular-resincroniza-al-migrar]]
- **La precision de una columna la marca su valor MAXIMO, no el tipico** — `SELECT max(col)` antes de elegir la escala. Y la fila basura que documentas y decides ignorar **sigue participando en los calculos**. Ver [[una-fila-basura-amplifica-el-error-de-redondeo-de-toda-la-tabla]]
- **Un precio unitario de 1,00 marca una cantidad que en realidad son euros** — truco universal de los ERP para colar un importe por la columna de cantidad; sin excluirlas, cualquier `SUM(cant*precio)/SUM(cant)` mezcla dos unidades. Agrupa por precio y ordena por volumen: la fila contaminada canta sola. Ver [[precio-unitario-1-00-marca-una-cantidad-que-son-euros]]
- **Antes de decir «ese dato no está», barre el catálogo de columnas** — `information_schema.columns` por el CONCEPTO sobre todas las tablas: convierte «no lo encuentro» en «no existe». Ver [[barrer-el-catalogo-de-columnas-convierte-no-lo-encuentro-en-no-existe]]
- **Un campo migrado puede estar en la unidad de origen y no fallar nunca** — si el otro factor vino en la MISMA unidad equivocada se compensan y no hay síntoma (+49 % al tocar una pieza). Detección: la fila que se autodescribe. Ver [[dos-piezas-en-la-misma-unidad-equivocada-dan-el-resultado-correcto]]
- **La `confianza` que declara un LLM no separa aciertos de fallos** — medido: 44 % dentro del ±10 %, con errores de −85 % y +3.757 % a confianza 0,80-0,90. Como umbral de auto-aceptación no filtra, solo lo aparenta: busca ground truth ANTES de elegir el umbral. Ver [[la-confianza-autodeclarada-de-un-llm-no-predice-su-acierto]]
- **Verdes que no miden lo que parece** — un 0 se lee como dato y suele ser «no medido»; el verde de un doble no distingue enchufado de olvidado. Ver [[campo-numerico-opcional-omitido-suma-cero-y-parece-dato]] · [[asercion-e2e-que-mide-datos-en-vez-de-montaje-es-verde-o-rojo-por-azar]] · [[agregar-sobre-todas-las-orgs-mezcla-datos-sembrados-con-datos-de-cliente]]
- **Tocar un prompt: la posición manda y n=10 no basta** — la regla va pegada al dato que prohíbe; comparar variantes exige n≥25 entrelazado. Ver [[un-prompt-es-una-superficie-con-localidad-no-un-documento]] · [[dato-en-bloque-de-contexto-se-lee-en-voz-alta-aunque-no-este-en-el-guion]] · [[una-suite-de-evals-cuesta-llamadas-por-prompt-mide-el-cache-antes-de-proponerlo]]
- **Una ejecución en verde no prueba que el efecto ocurriera** — `success` = «no explotó»: mide que el nodo de efecto CORRIÓ (268 verdes, 0 envíos). Y el `else` de un `switch` sobre un valor de LLM tiene que AVISAR. Ver [[ejecucion-en-verde-no-prueba-el-efecto]] · [[el-else-de-un-clasificador-que-rellena-un-llm-debe-avisar-no-callar]]
- **Un job de fondo: pasada en el BOOT, no solo `setInterval`** — con autodeploy el timer nunca cumple un ciclo (4 días sin barrer); y su `last_error` en la BD no vale si nadie lo consulta. Ver [[un-timer-mas-largo-que-la-cadencia-de-despliegue-no-corre-nunca]] · [[persistir-el-error-no-basta-si-ninguna-superficie-lo-lee]]
- **Rama nueva desde `main` local sin fetch** — nace vieja y pisa lo mergeado: usar `origin/main`. Fichero reescrito >2 veces → merge, no rebase; sus rojos se clasifican. Ver [[rama-nueva-desde-un-main-local-sin-fetch-revierte-trabajo-ajeno]] · [[rama-que-reescribe-el-mismo-fichero-varias-veces-se-integra-con-merge]] · [[los-tests-rojos-que-hereda-un-merge-se-clasifican-uno-a-uno]]
- **Al partir una pila en PRs, el fix va con el commit que lo causa** — mergear el primero publicaría el fallo; y squashear el padre pide `rebase --onto origin/main <padre>` en la hija. Ver [[al-partir-una-pila-en-prs-el-fix-tiene-que-viajar-con-lo-que-lo-causa]] · [[delete-branch-al-mergear-cierra-la-pr-apilada-no-la-reapunta]]
- **`create or replace` con otra firma crea una sobrecarga y `db push` dice `Finished`** — el fix se despliega muerto. Verifica `pg_proc`: UNA fila. Ver [[postgres-rpc-firma-identica-create-replace]]
- **Un comentario que afirma una invariante es una deuda de test** — grepea la afirmación contra el código antes de fiarte; si nadie la comprueba, no es cierta. Ver [[un-comentario-que-afirma-una-invariante-es-una-deuda-de-test]]
- **Un gate solo puede fallar HACIENDO RUIDO** — salir con 0 sin encontrar nada es un adorno: fail-closed, y avisar por `stderr` sin pesar en el exit no es avisar. El gate que corres aparte NO es el del hook. Ver [[gate-en-segundo-plano-no-incluye-los-trinquetes-del-pre-commit]] · [[una-limpieza-multitabla-en-una-sola-query-es-todo-o-nada]] · [[un-script-gate-con-guard-de-entrypoint-degrada-a-no-op-silencioso]]
- **Herramienta nueva sin barrer sus call-sites escritos NO se adopta** — el agente ejecuta lo ESCRITO (permisos, runbooks, memories), no lo del PATH. Ver [[un-wrapper-nuevo-no-se-adopta-si-no-barres-los-call-sites-escritos]]

- **Un verde esperado «vacío» no mide nada si el estado ya era vacío** — RLS sobre tabla vacía da `[]` con y sin RLS. Ver [[verificar-rls-en-tabla-vacia-no-discrimina]]

- **Un candado nuevo en `main` caza las PRs abiertas escritas ANTES que él** — solo lo ve el gate de la combinación. Ver [[un-candado-nuevo-en-main-caza-las-prs-abiertas-escritas-antes]]

- **Importar un helper desde otro `.test.ts` re-ejecuta sus casos en el importador** — el delta de la rama dice +11 aportando 6, y `tsc`/`eslint`/el resumen cuadran igual. Ver [[importar-de-un-fichero-de-test-re-ejecuta-sus-casos]]

## Archivado

Lo que no reincide vive fuera, con su wikilink intacto y recuperable navegando:
[[hot-archivo-2026-08-18]] (37) · [[hot-archivo-2026-08-01]]
- **Un gate que descubre lo que audita pasa en verde si su lista sale vacía** — suelo explícito (`toBeGreaterThanOrEqual`) y fallar CERRADO con lo que no sabe leer. Ver [[un-gate-derivado-del-repo-necesita-guarda-contra-su-propia-ceguera]]

- **El arnés se mide a sí mismo** — un gate que construye la orden en vez de ejecutarla, un mock que declara una cadena que el código ya no usa, un check que nadie invoca, un default que nadie corrió, y el más fino: uno que mide que algo cambió pero no **dónde**. [[el-arnes-se-mide-a-si-mismo]]
- **Verificar la conclusión, no la evidencia** — el estado de un secreto externo lo dice el proveedor, no un `SELECT`. [[verificar-la-conclusion-no-solo-la-evidencia]]
