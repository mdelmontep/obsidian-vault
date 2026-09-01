---
title: hot cache
date: 2026-07-29
tags: [stack, index]
---

# Hot Cache

- **Un alcance calculado contra la rama base se vacía al mergear** — y el gate pasa a auditar lo que haya suelto en el árbol, sin avisar. Ver [[un-alcance-calculado-contra-la-rama-base-se-vacia-al-mergear]]
- **Una sonda con el nombre inventado da un ✗ indistinguible de un fallo real** — los tres ✗ de la verificación eran los tres nombres que no salieron de leer el `create function`. Deriva la lista de la fuente. Ver [[una-sonda-cuyo-nombre-no-salio-de-la-fuente-da-un-fallo-que-parece-del-sistema]]
- **El porcentaje de swap no discrimina thrashing; los `Swapouts` sí** — al 89 % con 0 swapouts/s el swap está asentado y se puede conducir un navegador. Para una ola de 3-4, el criterio del 50 % sigue mandando. Ver [[el-porcentaje-de-swap-no-discrimina-thrashing-los-swapouts-si]]
- **«✔ verificado contra el repo» encuentra la migración que CREÓ la columna, no la que la borró** — un nombre de esquema se verifica en la ÚLTIMA migración que lo toca. Ver [[verificado-contra-el-repo-no-ve-la-columna-que-un-adr-mando-borrar]]
- **Un subagente cita el mecanismo, nunca el guard que lo cierra** — lee tú el `if` de 30 líneas antes, o diseñas contra un riesgo inexistente. Ver [[un-subagente-cita-el-mecanismo-no-el-guard-que-lo-cierra]]
- **Un guard que discrimina por el NOMBRE de la etiqueta no vigila lo que dice** — en JSX ese nombre es una variable: hace falta un segundo guard que lo reserve. Ver [[un-guard-que-lee-el-nombre-de-la-etiqueta-miente-si-el-nombre-es-un-alias]]
- **Cero `fetch()` no es cero uso** — mídelo en producción antes de llamar huérfano a un endpoint. Ver [[ausencia-de-consumidor-no-es-ausencia-de-funcion]]
- **Un fix dentro de una media query, sobre un selector que ahí no existe** — compila, pasa el gate y no cambia nada: contar `querySelectorAll` A ESE ancho antes de escribirlo. Ver [[un-fix-en-una-media-query-sobre-un-selector-que-no-existe-ahi-es-codigo-muerto]]
- **Una piel/tema se mide por ALCANCE, no por tokens redefinidos** — cuántas cajas pintadas cambian al encenderla (2-16 % aquí, por los valores a mano). Ver [[una-piel-de-tokens-solo-alcanza-lo-que-no-esta-escrito-a-mano]]
- **El parche de un agente en worktree revierte lo que no commiteaste** — nace del último commit: se fusiona el hunk, no se copia el fichero. Ver [[el-parche-de-un-agente-en-worktree-borra-lo-que-no-estaba-commiteado]]
- **Las frases entrecomilladas de un prompt son un guion** — el modelo las recita literales (32,6 % → 18,2 % de turnos). Ver [[las-frases-entrecomilladas-de-un-prompt-son-un-guion-que-el-modelo-recita]]
- **Lee 2-3 transcripciones de casos que PASAN** — las métricas solo cubren lo que ya sospechabas; el defecto que enfada al usuario vive en el verde. Ver [[la-transcripcion-de-un-test-que-pasa-es-donde-esta-el-defecto-que-nadie-mide]]
- **Un cero solo discrimina si el evento PUDO ocurrir** — y una ventana anclada al arranque caduca con cada merge (autodeploy recrea el contenedor, incluso en un merge solo-docs ajeno): ancla al EVENTO. Ver [[una-ventana-de-observacion-anclada-al-arranque-caduca-con-cada-merge]]
- **Un check rojo que muere en 3 s sin pasos es la plataforma** — mira si `main` también falla antes de depurar la rama. Ver [[un-check-que-muere-en-segundos-sin-ejecutar-pasos-es-la-plataforma]]
- **La vía que nadie recorre se pudre sin ruido** — webhook a cero tapado por el cron: la proporción entre las dos fuentes es señal de salud. Ver [[una-verificacion-que-nadie-ejerce-puede-llevar-meses-rota]]
- **Sesión de app Supabase sin password ni Node** — `generate_link` → `curl -w '%{redirect_url}'` → cookie `base64-`+b64url a mano; el action_link no inicia sesión en apps code-flow. Ver [[cookie-de-supabase-ssr-a-mano-para-smokes-sin-node]]
- **La frescura del evento solo decide revivir, nunca limpiar el error** — con crons que reprocesan timestamps fijos, condicionar la limpieza a "evento nuevo" deja el error pintado días. Ver [[la-frescura-del-evento-solo-decide-revivir-nunca-limpiar-el-error]]
- **El orden del `||` decide el copy, no quién lo revisó** — `detail || error || 'frase'` tapa el texto del cliente con el error interno. Ver [[el-detail-tecnico-se-pinta-antes-que-la-frase-humana-y-la-tapa]]
- **Un push que falla pasa por éxito** — se verifica por SHA (`ls-remote` == `rev-parse`), nunca por exit code. Van dos veces. Ver [[push-que-falla-por-red-imprime-everything-up-to-date-al-final]]
- **Una pestaña instrumentada da por inerte una app sana** — antes de declarar caída, reprodúcelo en un navegador limpio. Ver [[pestana-instrumentada-da-inerte-lo-que-esta-sano]]
- **Un fallo transitorio que ESCRIBES se lee luego como veredicto** — enum con el porqué + barrido que lo deshiele, y el catálogo del tercero se PREGUNTA (no se declara). Ver [[un-fallo-transitorio-guardado-en-una-columna-se-lee-como-veredicto]]
- **«SIN VÍCTIMA» tiene tres lecturas, no dos** — hueco de test, mutante equivalente, o **guard equivocado**: preguntar qué entrada distinguiría las dos versiones antes de escribir el test que falta. Ver [[un-mutante-sin-victima-tambien-puede-ser-un-guard-equivocado]]
- **Un trinquete que mide por FICHERO absuelve al que ya importa el helper** — anclar en la OCURRENCIA, no en el import. Ver [[un-trinquete-por-fichero-absuelve-al-que-ya-importa-el-helper]]
- **El coste de Claude Code está en el tamaño de sesión, no en el CLAUDE.md** — 77 % es cache-read y el 91 % se gasta por encima de 200k. Y un `paths:` de rules dispara con `Read`, **no con Bash**. Ver [[donde-se-va-el-coste-de-claude-code-no-es-el-claude-md]]
- **Un hook que resuelve git en el cwd de la SESIÓN juzga otro checkout** — y renunciar (`exit 0` al ver un `cd`) lo deja decorativo justo donde importa. Ver [[hook-que-resuelve-git-en-el-cwd-de-la-sesion-juzga-el-repo-equivocado]]
- **Todo bot de voz o chat debe identificarse como IA en la primera interacción** (art. 50 del AI Act, vigente desde el 2-ago-2026) — y el aviso va en el flujo, no en el prompt: si depende del modelo, el incumplimiento es silencioso. Ver [[una-obligacion-legal-no-puede-colgar-del-prompt-del-llm]]
- **Un control que afirmas a un cliente necesita REGISTRO con fecha** — una afirmación de control no la caza ningún test, solo una auditoría. Ver [[un-control-que-un-documento-cliente-facing-afirma-necesita-registro]]

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

## Ha vuelto a pasar (34)
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




- **Un artefacto que vive en un panel se compara carácter por carácter** — «v1 · 21 ago» → «v2 · 27 ago» no mueve el tamaño: 2 de 5 pesaban igual servidas de otra versión. Ver [[comparar-por-tamano-no-ve-un-artefacto-servido-desde-otra-version]]

- **Un gate que descubre lo que audita pasa en verde si su lista sale vacía** — suelo explícito y fallar CERRADO. [[un-gate-derivado-del-repo-necesita-guarda-contra-su-propia-ceguera]]
- **La fuente única no impide que reescriban el cálculo a mano** — el guard va sobre el PATRÓN, no sobre los sitios. [[una-funcion-correcta-no-impide-que-la-reescriban-a-mano]]
- **El arnés se mide a sí mismo** — un gate que construye la orden en vez de ejecutarla, un mock que declara una cadena que el código ya no usa, un check que nadie invoca, un default que nadie corrió, y el más fino: uno que mide que algo cambió pero no **dónde**. [[el-arnes-se-mide-a-si-mismo]]
- **Verificar la conclusión, no la evidencia** — el estado de un secreto externo lo dice el proveedor, no un `SELECT`. [[verificar-la-conclusion-no-solo-la-evidencia]]
- **El proxy de Next trunca a 10 MB en silencio y rompe firmas HMAC** — 401 intermitente solo en payloads grandes; excluir la ruta del matcher (la auth es del handler) + preflight antes de gastar. Ver [[proxy-de-next-trunca-el-body-a-10mb-y-rompe-firmas-hmac]]
- **Un gate que exige el artefacto a la fase que lo produce es un deadlock** — y el mock del contrato en el test del productor lo esconde. Ver [[gate-que-exige-el-artefacto-a-la-fase-que-lo-produce-es-deadlock]]
- **El control de una medida es del mismo tipo que lo medido** — borrador contra publicada dio una caída falsa en 6 variantes. [[un-borrador-y-la-version-publicada-no-son-comparables-el-control-es-otro-borrador]]

## Archivado

Lo que no reincide vive fuera, con su wikilink intacto y recuperable navegando:
[[hot-archivo-2026-08-30]] (14) · [[hot-archivo-2026-08-18]] (37) · [[hot-archivo-2026-08-01]]

- **`it.each` sobre un `.filter()` vacío no registra ningún test** — vitest no se queja; el bloque desaparece del recuento. Ver [[it-each-sobre-filter-vacio-no-registra-ningun-test]]
- **Republicar un artifact exige haberlo leído EN ESA sesión** — y `updated` del listado es la fecha del registro, no la del contenido. Medir el `diff` antes de pagar la lectura. Ver [[republicar-un-artifact-exige-haberlo-leido-en-esa-sesion]]
- **Una respuesta que llega justo al tope no es un resultado, es el tope** — si `len(resultado) == límite`, trátalo como truncado: casi borro una rama con un PR abierto. Ver [[el-limite-silencioso-una-respuesta-que-llega-al-tope-parece-completa]]
- **Un recuento sobre el estado final no ve la ventana de exposición** — para *nunca debe estar expuesto* la evidencia es `git log -S`, no `grep` del árbol de hoy. Ver [[un-recuento-sobre-el-estado-final-no-ve-la-ventana-de-exposicion]]
