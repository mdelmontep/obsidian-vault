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

## Ha vuelto a pasar (5)

Estas no son advertencias teóricas: su learning documenta que el fallo **reincidió** después de
estar escrito. Si una de estas se puede comprobar con un comando, su sitio es un hook, no esta lista.

- **Un guard en código que predice una restricción de la BD acaba mirando otro universo** — si la unicidad la impone un índice y el chequeo previo la reescribe con otro scope, divergen y el `INSERT` revienta: la consulta del guard debe ser la **expresión literal del índice**. Ver [[guard-en-codigo-que-predice-un-indice-unico-de-sql-diverge]]
- **Un comentario que dice "esto es deliberado" solo cubre el caso que su autor tenía delante** — si la justificación es más específica que el `if` que la protege, falta el `if`. Ver [[comentario-que-declara-una-formula-deliberada-solo-cubre-su-mitad]]
- **Un staging deja de ser fuente de verdad tras el commit, y editarlo sigue "guardando"** — el buffer (JSONB de OCR, borrador, import) se copia al registro al aprobar; después el staging persiste con éxito y el registro no cambia. Tras el commit: mostrar el valor DEL REGISTRO y rechazar en voz alta. Ver [[staging-deja-de-ser-fuente-de-verdad-tras-el-commit-y-editarlo-no-cambia-nada]] · [[editor-inline-que-compara-contra-el-valor-mostrado-encalla-al-reescribir-lo-mismo]]
- **Un backfill que no cierra el origen vuelve a morder con la siguiente fila** — si el alta necesita hijas para funcionar, se siembran TODAS en el trigger de alta, no a medias entre trigger y onboarding. Ver [[seed-partido-entre-trigger-y-onboarding-deja-filas-a-medias]]
- **Si algo se puede reintentar, el callback del intento VIEJO cerrará lo que ya se reabrió** — actúa sobre un estado que no es el que él dejó; la guarda de idempotencia no cubre la de vigencia ("¿sigo siendo el intento actual?"). Ver [[callback-de-un-intento-viejo-cierra-lo-que-ya-se-reabrio]]

## El resto (54)

- **Un checker que no puede ponerse rojo no es un checker** — un crawler que escribe informe y sale 0, un guard que nunca has visto fallar, un lint que se enganchó mal: ocupan el hueco de la cobertura sin darla. Verlo en rojo a propósito, y comprobar que además se ejecuta. Ver [[crawler-que-escribe-informe-y-sale-cero-es-recolector-no-test]]
- **Con dos formas de cerrar algo, ramifica por el mecanismo, no por un campo que suele correlacionar** — si escribes donde el productor de la lista no lee, no cierras: es un `setState` con toast. La prueba es recargar. Ver [[dos-mecanismos-de-cierre-y-la-ui-ofrece-el-que-no-aplica]]
- **Sanear el valor y olvidar la clave** — el NOMBRE del parámetro también es entrada del usuario, y un campo que nadie ve como "texto libre" acaba siendo mejor canal de inyección que el que sí lo es: solo se valla lo que parece peligroso. Ver [[sanear-el-valor-y-olvidar-la-clave-el-nombre-del-parametro-tambien-es-entrada]]
- **Migrar a un primitivo compartido puede quitar accesibilidad que venía gratis** — roving tabindex sin selección deja el grupo entero fuera del tabulador; los `<button>` a mano se tabulaban solos. Mira los hermanos de la carpeta antes de tocar el primitivo. Ver [[roving-tabindex-sin-seleccion-deja-el-grupo-fuera-del-tabulador]]
- **Mide el reparto de fallos antes de arreglar el que te cuentan** — "murió por timeout, mejora el prompt": los timeouts eran 6 de 34 fallos; el resto, config y watchdog. Y con decenas de jobs no distingues prompt v1 de v2, así que "más criterios de calidad" es infalsable. Ver [[mide-el-reparto-de-fallos-antes-de-arreglar-el-que-te-cuentan]]
- **Una orden imposible en su entorno no hace que el agente diga "no puedo"** — explora hasta que lo matan (captura de pantalla sin navegador, build que revienta por OOM). Y la misma instrucción repetida en dos capas de prompt acaba divergiendo: cada una en un solo sitio. Ver [[orden-imposible-en-su-entorno-el-agente-explora-hasta-que-lo-matan]]
- **Documentar un hueco no es cerrarlo, y el silencio no es salud** — si el fallo es silencioso (un cron que nunca corrió, un EOL que pasó), la única defensa es código que grite: un "auditar de vez en cuando" en la documentación falla justo cuando hace falta. Ver [[estar-en-el-catalogo-de-crons-no-es-estar-programado]]
- **Un fix no está verificado hasta crear una entidad NUEVA tras el deploy** — leer los datos que arregló el backfill no prueba nada del código; el compositor no es el punto de persistencia y la suite verde no cubre el camino que tocas. Ver [[cambiar-la-semantica-de-una-columna-el-compositor-no-es-el-punto-de-persistencia]]
- **Una PR encadenada se mergea en su BASE, no en main** — si no borras la rama base al mergear la primera; «MERGED» no significa «en main», verifícalo con grep sobre `origin/main`. Ver [[pr-encadenada-se-mergea-en-su-base-si-no-borras-la-rama]]
- **Cada fix de agente medido contra el modelo real destapa el siguiente hueco** — el ruido busca cualquier `kind`; y si un turno sigue rojo tras el fix, sospecha del assert antes que del código. Ver [[cada-fix-de-agente-medido-contra-el-modelo-real-destapa-el-siguiente-hueco]]
- **Un check de coherencia no puede afirmar un desajuste si no pudo preguntar** — clave ausente/401/429 es "no verificado" (UNA alerta media), no N desajustes altos; la alerta falsa induce a recrear datos que están bien. Delator: fallan TODAS las filas con el MISMO motivo. Ver [[fallo-de-credencial-no-es-dato-ausente-en-un-check-de-coherencia]]
- **Una clave read-only NO se verifica escribiendo** — el `POST` de prueba que esperaba un 403 devolvió 200 y creó objetos reales en una cuenta live. Lo comprobable leyendo es la CUENTA (`GET /v1/account`), no la ausencia de permiso de escritura. Ver [[no-verificar-una-clave-read-only-escribiendo-con-ella]]
- **`--force-with-lease` sin `fetch` no protege nada** — compara contra tu `origin/<rama>` LOCAL, así que un checkout desactualizado autoriza rebobinar `main` 40+ commits. Lease con SHA explícito, y verifica la recuperación por ÁRBOL, no por log. Ver [[force-with-lease-sin-fetch-no-protege-nada]]
- **Un locator que resuelve a 0 elementos es un test roto, no evidencia** — en un `if (isVisible)` es falso verde; tras un `test.skip(count === 0)`, verde PERMANENTE. Afirmar por rol/nombre accesible, nunca por clase de CSS Module. Ver [[locator-de-test-atado-a-la-implementacion-caduca-y-da-falso-verde]]
- **IDs de entorno cableados en un spec miden una org que no existe** — `count` a 0 y `update` que no toca filas, en silencio. Resolver del entorno y fallar con mensaje claro. Ver [[spec-con-ids-de-entorno-cableados-mide-una-org-inexistente]]
- **`gh pr merge` desde un worktree falla DESPUÉS de mergear en remoto** — el error (`'main' is already used by worktree`) lo da el checkout local posterior, no el merge; comprobar con `gh pr view N --json state` antes de reintentar. Ver [[gh-pr-merge-desde-worktree-falla-despues-de-haber-mergeado]]
- **El stash es compartido entre worktrees** — una sesión paralela puede recuperar tu stash y dejarte sin fix; cero `stash` en repos con worktrees. Ver [[stash-es-compartido-entre-worktrees-y-rompe-sesiones-paralelas]]
- **Subagente que reporta «hecho, verde» sin que exista el código** — `git show --stat` + `grep` del símbolo + rojo-primero repetido por ti. Ver [[subagente-reporta-hecho-codigo-que-no-existe-o-no-compila]]
- **Un override de BD que sustituye al schema del código vuelve INESCRIBIBLES las claves que omite** — pasa al endurecer el contrato de escritura; separar schema de render (override) del de escritura (unión). Caso real: 8 cuentas del asiento contable congeladas en prod. Ver [[override-de-bd-que-sustituye-al-schema-del-codigo-congela-claves]].
- **Gate de auto-aplicación: "n≥50 y acierto ≥95%" NO sostiene el 95%** — Wilson con n=50 da [0,851 , 0,984]; una org al 90% real abre el gate el 11% de las veces. Decide por cota inferior, sweep semanal + cooldown, y cobertura como condición aparte (el silencio no es aceptación). Ver [[gate-de-automatizacion-n50-al-95-no-sostiene-el-95-usa-cota-wilson]].
- **Relajar un filtro duro que además era techo implícito de un score abre una ruta de auto que nadie diseñó** — calcula el máximo alcanzable SIN esa señal antes de tocarlo; separa `umbral_sugerencia` de `elegible_auto` y codifica el invariante, no la constante. Ver [[relajar-filtro-duro-que-era-techo-implicito-abre-automatizacion-no-disenada]].
- **En un worktree `.git` es FICHERO, no directorio** — detectar la raíz con `existsSync('.git')` + `basename(dir)` devuelve la RAMA como nombre de proyecto (rompió el panel de horas). Parsear el `gitdir:`. Ver [[git-worktree-dotgit-es-fichero-basename-devuelve-la-rama]].
- **Un guard que recalcula la fórmula que asegura no verifica nada**: pasa en verde con el cuerpo viejo. Inspecciona `prosrc`/`pg_get_expr` (contiene lo nuevo Y **no** el patrón viejo) + filas reales. Ver [[guard-de-migracion-que-recalcula-la-formula-no-verifica-nada]]
- **Universo de datos en dos sitios divergge** — el detector de cambios debe leer el universo de la misma fuente que lo guardó. Ver [[universo-de-datos-reimplementado-en-dos-sitios-divergge]]
- **FK RESTRICT ≠ regla de negocio** — no distingue estados; la política va en la operación. Ver [[fk-restrict-no-sirve-como-regla-de-negocio-no-distingue-estados]]
- **"Contenedor recreado, logs limpios" no verifica un cambio de env** — verifica que arrancó. La prueba es una llamada que devuelva el EFECTO (p. ej. el endpoint devuelve bajo qué identidad entra la clave). Ver [[verificar-deploy-de-env-por-comportamiento-no-por-contenedor-recreado]]
- **Flota de workers parada = solo se ve en la simultaneidad** — la salud por racha de cada worker nunca llega a rojo; avisa el reaper al liberar ≥N locks, con N sacado de la distribución histórica. Ver [[parada-de-flota-solo-se-ve-en-la-simultaneidad]]
- **Un guard nuevo se mide contra los datos que YA existen** — cuenta cuántas filas lo violan antes de desplegarlo (8 de 498 en prod, y por un campo mal leído por el OCR): si el mensaje no da salida es un callejón, y duplicar la regla como `min` del control del cliente bloquea sin poder explicar. Ver [[un-guard-nuevo-se-mide-contra-los-datos-que-ya-existen]]
- **El universo comparable de un diff es lo que se PERSISTE** — no lo que el motor carga para calcular; confundirlo reintroduce el falso positivo por el otro lado. Ver [[el-universo-comparable-es-lo-que-se-persiste-no-lo-que-se-carga]]
- **Mockear `withApiAuth` esconde el 400 que ve el usuario** — un POST sin body necesita `bodyOptional`; añade un test sobre las opts con que se registra la ruta. Ver [[mockear-el-wrapper-de-auth-esconde-el-400-que-ve-el-usuario]]
- **Si un barrido omite una fuente por coste, no puede resolver sus alertas** — ausente-porque-no-se-mira ≠ recuperada. Ver [[lo-que-un-barrido-omite-no-puede-darse-por-recuperado]]
- **Un camino crítico sin smoke se pudre meses aunque haya miles de tests al lado** — 7.541 unitarios y ninguno arrancaba Chromium: dos fallos de 2 meses en el que genera TODAS las facturas. Si produce el artefacto que ve el cliente y ningún test lo produce de verdad, no está cubierto. Ver [[camino-critico-sin-smoke-se-pudre-meses]]
- **Cambio de motor de render: A/B con el mismo código, no "el build pasa"** — dos imágenes, payload del repo + variante multipágina, comparar páginas → texto extraído → píxeles. Ver [[validar-cambio-de-motor-de-render-con-ab-de-misma-imagen]]
- **Un helper de auth que dice "el caller ya validó X" es una fuga esperando** — el gate va DENTRO. Al unificar dos implementaciones divergentes, la más restrictiva suele ser la correcta: compara semántica antes de borrar la "copia". Ver [[helper-de-auth-que-asume-validacion-del-caller]]
- **Divergencia conocida = test VERDE que la afirma, no rojo permanente** — un rojo se normaliza en dos días y rompe el gate de todos. Ver [[characterization-test-diverge-en-vez-de-rojo-permanente]]
- **Clic por coordenadas tras un salto de layout no cae en el botón** — no pasa nada, sin error ni petición: idéntico a un botón roto. En smokes, clicar por referencia de elemento, y ante un "no hace nada" descartar primero que el clic cayera fuera. Ver [[clic-por-coordenadas-tras-salto-de-layout-no-cae-en-el-boton]]
- **Un test nuevo no vale hasta que le rompes el código a propósito y falla** — dos minutos de mutación distinguen "pasa" de "vigila algo". Caza el test que se salta solo y el que mide el artefacto vecino. Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]]
- **Worktree en `/private/tmp` sin commitear = código perdido, pero el transcript no** — el `.jsonl` de la sesión guarda el resultado completo de cada subagente: se reconstruye la SPEC y se reimplementa. Ver [[transcript-jsonl-sobrevive-al-worktree-borrado]]
- **El coste de compilar el módulo se le cobra al PRIMER test y lo saca de su timeout** — 2,8 s en aislado, >10 s con la suite entera; sale como flaky con mensajes de aserción, no de timeout. Precalentar en un `beforeAll` con timeout propio, no subir `testTimeout`. Ver [[el-coste-de-compilar-el-modulo-se-cobra-al-primer-test]]
- **Marcar "enviado" antes de enviar = mensaje perdido para siempre** — el dedup escribe la clave, el envío falla después y el siguiente barrido salta. Marcar tras el OK. Ver [[marcar-enviado-antes-de-enviar-pierde-el-mensaje-sin-reintento]]
- **Recordatorio "X horas antes" sin ventana horaria escribe de madrugada** — resta el offset a la hora de apertura: si no lo mandarías tú a mano, está roto. Ver [[recordatorio-relativo-sin-ventana-horaria-escribe-de-madrugada]]
- **`250 queued` no es entrega** — sonda a una dirección INEXISTENTE de Gmail: si sale de verdad rebota en segundos; sin rebote y sin entrega, el hosting no está sacando el correo. Ver [[smtp-acepta-con-250-queued-y-no-entrega-fuera]]
- **Exit 0 + árbol limpio ≠ "no había trabajo"** — un proceso que agota cuota se hace pasar por "sin cambios". Clasificar por texto de stdout, no por exit code. Ver [[proceso-que-agota-la-cuota-puede-salir-con-exit-0-y-parecer-sin-cambios]]
- **Credencial de test que "no va": mira proyecto Y membresías** — el `iss` del JWT delata el proyecto; un usuario sin org es login válido y app inservible. Ver [[credencial-de-test-guardada-puede-apuntar-a-otro-proyecto-y-a-un-usuario-sin-membresias]]
- **Detectar una dependencia sondeando el BINARIO elige el camino roto** — `docker --version` responde con Docker parado; sondea el subcomando real y degrada con aviso, no abortes. Ver [[sondear-la-capacidad-real-no-la-presencia-del-binario]]
- **«Cierra #N» no cierra el issue: GitHub solo entiende las keywords en inglés** — la PR se mergea y el issue queda abierto, señal de "libre" para otra sesión. Ver [[keywords-de-cierre-de-github-solo-funcionan-en-ingles]]
- **Un gate con cientos de skips por entorno sale ✓ VERDE sin haber probado nada** — el puerto ocupado por otro proyecto es la causa más frecuente; desglosa los skips por fichero antes de decir verde. Ver [[e2e-smoke-skip-honesto]]
- **Tests rojos con los tiempos clavados en 5000 ms = contención, no código** — córrelos aislados antes de diagnosticar nada. Ver [[tests-que-caen-por-contencion-de-cpu-verificalos-aislados-antes-de-diagnosticar]]
- **Un `pgrep -f` sobre una cadena que acabas de escribir se encuentra a sí mismo** — el bucle no sale y das por vivo un proceso terminado. Ver [[el-bucle-que-espera-con-pgrep-se-encuentra-a-si-mismo]]
- **Un fake cuya FORMA de retorno satisface la aserción verifica el fake, no el código** — y `toMatchObject` para afirmar AUSENCIA de una clave siempre pasa. Ver [[mock-funcion-compartida-en-test-endpoint-falso-verde-composicion]]
- **Cambiar el destinatario de un envío arrastra su gate de verificación** — decide por CANAL (email sí, WhatsApp solo si ese número está validado), no por persona. Ver [[redirigir-un-envio-sin-mover-su-gate-de-verificacion]]
- **Un nodo huérfano puede estarlo a propósito** — el efecto puede producirlo otro sistema (bot del pipeline, trigger, cron). Mira su contador de uso en el otro lado ANTES de conectarlo: reconectar duplica el mensaje al cliente. Ver [[nodo-huerfano-puede-estar-desconectado-porque-otro-mecanismo-ya-lo-cubre]]
- **Si la auditoría es la única copia que quedará del dato, no puede ir en fire-and-forget** — al escribir un endpoint destructivo, pregunta qué queda del dato después: si la respuesta es "la fila de auditoría", esa fila es parte de la transacción (antes del borrado y bloqueante). Ver [[auditoria-que-es-la-unica-copia-del-dato-no-puede-ir-en-fire-and-forget]]
- **Un campo que MUESTRA un formato y GUARDA otro descarta la edición en silencio** — formatter de solo-lectura sobre un input libre + `return` mudo de validación = pérdida de datos que parece guardado. El control lo decide el tipo del dato (fecha → DatePicker compartido), y ninguna rama de guardado sale sin avisar. Ver [[campo-que-muestra-un-formato-y-guarda-otro-descarta-la-edicion-en-silencio]]
- **Año de dos dígitos en un documento: `DD-MM-YY` o `YY-MM-DD` es indecidible para el modelo** — y si lo persiste al revés, el dato se va a otro ejercicio sin que salte nada. Desambiguar en código por convención local + sanity check contra la fecha de alta. Ver [[ocr-lee-dd-mm-yy-como-yy-mm-dd-y-manda-la-factura-a-otro-ejercicio]]
- **Un worker con `autoDeploy` y `watchPaths` vacío pierde su trabajo en cada push ajeno** — y sin handler de SIGTERM la culpa cae en quien no la tiene ("sin latido" del agente, no "te lo cargó tu deploy"). Cruza el último latido con `deployments[].createdAt`. Ver [[autodeploy-sin-watchpaths-mata-el-trabajo-en-vuelo-del-worker]]
