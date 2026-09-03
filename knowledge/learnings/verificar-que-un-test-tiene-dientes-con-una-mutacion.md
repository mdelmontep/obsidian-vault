---
title: un test nuevo no vale hasta que le rompes el código a propósito y falla
date: 2026-07-28
updated: 2026-09-03
source: claude-code-session
tags: [testing, qa, metodo, verificacion]
---
Que un test pase no demuestra nada: puede saltarse, medir otra cosa o afirmar algo siempre cierto.
Rompe **a propósito** lo que dice vigilar y confirma el rojo. Dos minutos. Disciplina: mutar
**producción** (no el test), una por vez, revertir desde copia (nunca `git checkout --`), y dejar en
la PR qué mutación se usó y qué falló.

**La firma dominante — aserción negativa sin contraparte positiva** (AGH: 15 casos medidos, **9** así).
«No ejecuta», «cero acciones», «no contiene X» están verdes tanto si el código acierta **como si no
hace nada**. Un test llamado «re-propone» lo cumplía un brain que contestara «no te he entendido».
Arreglo: **añadir la mitad positiva** (que el outbound NOMBRE la propuesta, que el pending SIGA ahí).
Hermanas: fixture de tamaño 1 · fake **ya ordenado** (ordenar por `createdAt` == por `occurredAt` si
insertas en orden cronológico) · test **sin un solo `expect`** que cierra con un comentario · guard
cuyo escenario **no se puede construir** (mismo proveedor para escribir y leer = ciego por estructura).

**El arnés miente en las dos direcciones:**
- *Falso verde:* mutación **parcial**. Quité 1 de **4** menciones y el caso siguió 3/3. `grep -c` antes
  de romper y comprueba que llega a cero — si no, mediste tu `sed`.
- *Falso «sin víctima»*, y tiene **cuatro** causas; saltamos a la peor («no protege nada»): (1) la
  mutación no se aplicó (heredoc/comillas: el fichero nunca cambió); (2) el símbolo mutado **no está en
  el camino de ese test** (mutar `serialized-brain.ts` no tumba un test que construye `HitlBrain` a
  pelo); (3) es equivalente **solo con los datos de hoy** — tras arreglar un token, reintroducir un
  redondeo ya no tumba nada porque no queda dato en el filo, y eso se cierra con un **fixture en el
  filo**, no declarando equivalencia (ver [[un-candado-que-redondea-el-valor-que-compara-mueve-su-umbral]]);
  (4) el hueco real. Hay mutaciones **genuinamente equivalentes** (early-return por comparación consigo
  misma): ésas se **declaran por escrito**, no se cuentan como cubiertas.

Caza además el test que **se salta** sin que nadie lo note ([[e2e-smoke-skip-honesto]]) y el que mide
un artefacto vecino (el visor y el PDF son dos cosas: una perfecta y la otra rota dos meses).

**Y antes de creerte una mutación SIN víctima, sospecha del arnés: medido 3 de cada 4** (AGH, 7-ago).
Los tres modos: mutar **la aparición equivocada** del literal (el fichero cambia, pero no la línea que
importa) · apuntar a **un artefacto que esa ruta ni ejecuta** (mutar la migración cuando el bootstrap
aplica el schema) · lanzar el arnés **sin el entorno de la medición** (sin `DATABASE_URL`, contra otra
BD). La cuarta sí era del test, y era real: **no era re-ejecutable** — sembraba en la 1ª corrida lo
que la 2ª daba por hecho. Un test que solo mide la primera vez es un candado que se abre solo.

**Quinto modo, y no se arregla con más casos: la VARIANTE DETERMINISTA deja moldes ciegos.** Si el
código elige entre N redacciones hasheando el contenido (para que la medición sea reproducible), un
payload dado ejercita **siempre la misma**: mutar las otras no mata a nadie. Añadir casos solo tapa
las que se te ocurran hoy. Lo cierra una **invariante sobre el POOL** («ningún molde contiene "voy
a"»), que cubre además el molde que alguien añada mañana. AGH 7-ago: 2 de 4 moldes ciegos.

**Sexto modo — la aserción es un RANGO tan ancho que incluye el fallo.** No es la negativa sin
contraparte: aquí hay aserción positiva, pero admite el modo de fallo. FacturaIA 10-ago: el eje de
permisos exigía `status >= 400` para «un rol de solo lectura no puede escribir». Quité el
`requireWrite` de un endpoint y **siguió verde**, porque sin gate la validación del cuerpo devuelve
**422** — también 4xx. El test probaba «no es 2xx», no «está protegido». Se cierra exigiendo el
código CONCRETO de la defensa (401/403), y entonces un 400/422 dice lo que es: el permiso no se ha
probado. Regla: cuando el candado vigila una decisión, aserta **la señal de esa decisión**, no la
ausencia de éxito.

**Séptimo — universo vacío en un candado que se DERIVA del repo.** Un contrato que recorre
`git ls-files` con 129 casos pasa entero en verde si el comando falla: cero elementos, cero
asserciones ejecutadas, y el resumen dice «129 passed». Todo candado derivado necesita un **suelo de
tamaño** (`expect(n).toBeGreaterThan(500)`) como primer caso. Aplica igual a los gates escritos en
**shell**, y ahí no hay runner que avise: un verificador de restauraciones daba `OK` en 3 de 5
comprobaciones contra una base INEXISTENTE («0 tablas con el recuento exacto», «0 objetos con los
mismos permisos», y un `grep FALLO` sobre un fichero que solo contenía el error de `psql`). Esta
nota ya lo decía y el script se escribió igual (12-ago): el suelo se pone AL ESCRIBIRLO, y correr el
gate contra un destino muerto es el caso de control barato que lo destapa.

**Noveno — el proceso bajo prueba SIRVE el código viejo.** Distinto de «la mutación no se aplicó»:
el fichero cambia y el símbolo sí está en el camino, pero el servidor de larga vida no lo recarga.
FacturaIA 10-ago: Turbopack **no hot-reloada el proxy** (`proxy.ts` y lo que importa), así que mutar
el gate de `/admin` y correr el E2E midió el binario anterior → falso «sin víctima». Con cualquier
arnés que hable con un servidor/worker/contenedor vivo, **reinícialo dentro del comando de test**,
igual en el control que en el mutante.

**Décimo — no hay víctima porque hay DOS puertas.** Antes de declarar hueco, busca la guarda de
abajo: si el invariante está defendido en dos capas independientes, quitar una no cambia el
resultado y el mutante es equivalente **por defensa en profundidad**, que es la respuesta correcta y
conviene saberla antes de que alguien «simplifique» quitando una. Dos casos el mismo día
(FacturaIA 10-ago): el PDF de presupuesto (el handler filtra por org y el render vuelve a filtrar) y
`/admin` (proxy `isAdminRoute` + `AdminGuardedShell` en el layout). Se confirma mutando **las dos a
la vez**: ahí sí cae, y eso es lo que se documenta. **Y la puerta vecina puede ser TEMPORAL, no otra
capa de guardas** (AGH 13-ago, #1042): el `FOR UPDATE` de un subselect salía equivalente porque el
`INSERT … ON CONFLICT DO NOTHING` va SIEMPRE delante y **absorbe la espera**, así que cuando arranca el
`UPDATE` el otro ya confirmó y el snapshot es fresco. Lo grave fue lo de al lado: mi comentario ya
**afirmaba** que ese `FOR UPDATE` era el candado que sostenía el invariante. Al declarar un equivalente,
di también **qué es lo que sí lo sostiene** y qué cambio lo volvería imprescindible.

**Decimocuarto — la lista de mutaciones que te DAN tampoco es la lista objetiva.** Un issue bien escrito
sigue siendo una hipótesis: no deja de serlo por venir de otro ni por traer medición. AGH 13-ago, dos
veces. #1123 traía **dos** mutaciones medidas y nombradas —las dos caían con el arreglo— y sacar del
`git diff -U0` las líneas con conducta destapó **cuatro supervivientes más** que el issue no mencionaba.
Y #1042 dio **0 «sin víctima» pero 6 «ARNÉS ROTO»**: en un cambio de forma **coordinado** (el productor
devuelve otra cosa y el consumidor la consume), revertir un hunk deja el otro lado sin compilar — eso es
*no medido*, no *vigilado*, y obliga a mutar las conductas a mano. La lista sale del diff, también
cuando alguien ya te ha dado una. Corolario: si el arnés **no cubre la carpeta** (`scripts/`,
`dashboard/`), la única cobertura que existe es la que alguien se acuerde de hacer — 61 mutaciones a
mano en un día y **nueve huecos reales** salieron de ahí.

**Octavo, y este no es del test ni del arnés: el INFORME miente.** El reporter JSON de Playwright
recortó las anotaciones a los **14 primeros casos de 78** — y eran exactamente las primeras por orden
alfabético, con la forma creíble que tiene un dato verdadero. Cualquier cifra de cobertura sacada de
la salida de una herramienta ajena hay que contrastarla con un **marcador propio** (una línea por
caso a un fichero que escribes tú, tras un flag de entorno). Corolario del arnés, y ya con MÁQUINA detrás: «sin resumen de
tests reconocible» no es un resultado.

**Decimotercero — un «✓ VÍCTIMA» FALSO, la dirección peor** (AGH 12-ago). Todo lo de arriba vigila el
lado del «sin víctima», que te manda a investigar; un «víctima» falso **cierra el asunto** y nadie
vuelve. Tres seguidas salieron `✓ VÍCTIMA — exit=1 (sin resumen de tests reconocible)`: partí
`viejo|nuevo` por `|`, **un carácter que estaba dentro de los propios regex que mutaba**, el patrón se
aplicó truncado y el fichero ni compilaba. Tres candados dados por buenos sobre un mutante que nunca
corrió. Reglas: **un veredicto sin recuento de tests no es un veredicto, tenga la flecha que tenga**, y
el separador de una mutación nunca puede ser un carácter que el código pueda contener. Ya es candado
en `~/.claude/bin/mutate` (el cuarto): si el CONTROL trajo recuento y el mutante no, aborta con ARNÉS
ROTO — se compara contra el control para no perder los runners que nunca emiten recuento (pytest, go,
cargo), donde el exit code sigue siendo la única señal legítima. Suite en
`~/.claude/hooks/tests/mutate.test.sh`, con contrafáctico medido: sin el candado cae ese caso y solo
ése.


**Undécimo — la mutación cayó en un COMENTARIO, y por eso ya está mecanizado.** Variante peor del
modo «aparición equivocada del literal»: el fichero cambia, el `grep -c` baja, el resumen de tests
corre… y el mutante es idéntico al control porque lo mutado era prosa. FacturaIA 11-ago: cambié
`detect_lote_drift` en la línea 7 (cabecera del fichero) creyendo tocar la llamada de la 82, declaré
«el arnés del agente tiene un hueco», dije que no mergearía su PR y lo repetí **tres veces**. Lo
desmontó el propio agente corriendo *mi* mutación sobre el commit anterior al arreglo y sacando
víctima; la prueba estaba en mi propia salida de `grep`. Ahora `~/.claude/bin/mutate` **aborta** si
todas las apariciones de la aguja están en líneas de comentario (`//`, `#`, `*`, `--`, `<!--`), con
`--permitir-comentario` para el caso legítimo. Tercer candado del arnés, y los tres nacieron de un
falso «sin víctima» mío: árbol sucio · el comando no ejecutó tests · la aguja solo vive en comentarios.
Regla de conducta, más importante que el candado: **un «sin víctima» es una acusación contra el
código de otro y se verifica antes de publicarla**, no después de repetirla.

**Duodécimo — el caso de control pasó SIN LLEGAR al punto de decisión.** Hermano del «universo
vacío», pero dentro de un solo caso: el escenario «cadena sana» del worker de VeriFACTU estaba verde
porque el fake no devolvía `lineas_factura` y el worker se desviaba por «factura huérfana» mucho
antes de comprobar la cadena. Verde por no haber llegado. Se cierra afirmando **que el camino se
recorrió**: `expect(enviadas).toHaveLength(1)` en el caso sano, no solo el `toHaveLength(0)` de
avisos. Todo caso de control necesita una aserción de que ejecutó lo que dice controlar.

**Decimotercero — la mutación MUERE y aun así no está cubierta: importa QUIÉN la mata.** No es un
falso verde, es un falso **VÍCTIMA**. AGH 16-ago: bajar un umbral de aviso salía `✓ VÍCTIMA`… y lo
mataba un caso que escribía la frontera **a mano** (`aviso("caso", 2500, 5000)`) en vez de derivarla
de la política. Eso no la verificaba, la **duplicaba** — y habría dado un rojo diciendo «la frontera
está mal» a quien solo estuviera cambiando el umbral **a propósito**. Se cierra derivando la frontera
del propio umbral. Regla: ante un `✓ VÍCTIMA`, mira **cuál** caso se puso rojo y si asevera la
propiedad o **repite el cálculo**.

**Decimocuarto — la mutación SOBREVIVE porque ha DESACTIVADO el candado, no porque sea inocua.**
Pariente del «universo vacío», pero sin universo vacío: aquí la comparación se vuelve **tautológica**.
AGH 16-ago: invertir un cociente medido (`MAX/MIN` → `MIN/MAX`) dejó el factor en 0,148, la cota en
`Math.floor(0,44) = 0` y la aserción en `20 >= 0` — verde para siempre **sin tocar ni un dato
documentado**, los dos números seguían siendo correctos con su fuente y su fecha. Antes de declarar
equivalente un superviviente, comprueba si **anula la comparación**. Se cierra con anti-vacío sobre el
DATO antes de usarlo (aquí: `factor > 1`, porque un factor de contención menor que 1 diría que la
máquina cargada va más rápida que la que está en reposo — imposibilidad física, no política laxa).

**Decimoquinto — el arnés SE NEGÓ a mutar y tu propio filtro se comió el aviso.** No es «la mutación
no se aplicó» por comillas: `mutate` **exige que el patrón aparezca exactamente 1 vez** y aborta con
«el patrón aparece 2 veces (hace falta exactamente 1)» sin tocar el fichero. FacturaIA 17-ago: mutar
`function revertCell() {` en cuatro hooks; tres tenían dos definiciones por fichero → tres abortos. Y
como lancé el bucle con `| grep -E "control|VÍCTIMA"`, el aborto no casaba el filtro y quedaban solo
las líneas de control: leí la **ausencia de veredicto** como «SIN VÍCTIMA» y lo publiqué. La
conclusión de fondo era correcta por otra vía (ningún test montaba esa pantalla), pero la evidencia
que enseñé no existía. Dos reglas: **no filtres con `grep` la salida del arnés mientras interpretas
su veredicto** —son cuatro líneas, léelas crudas— y un patrón ambiguo se ancla con una línea única
del cuerpo, no con la firma de la función. Familia del [[decimotercero]] al revés: allí un `✓
VÍCTIMA` falso cerraba el asunto; aquí un «sin víctima» inventado abre una acusación que no sostiene
ninguna medición.

**Un «sin víctima» puede ser un test que mide, pero por otra rama** (18-ago-2026,
`series-formato-guard` de facturaia). Cegar el corte en `WHERE` del guard salía SIN VÍCTIMA
y el código estaba bien: al no reconocer la sentencia, el guard caía en su rama de «no
verificable», que también devuelve exit 0. El test miraba solo el código de salida, así que
no distinguía «está bien» de «no lo he entendido». Aserción que lo arregla: exigir además
que NO aparezca el aviso de no-verificable. Es decir, verde **por haber medido**, no por
haberse rendido.

Y el caso del comentario SQL necesitó **tres intentos** hasta discriminar: un comentario
antes de la sentencia no vale (el regex no llega), ni la sentencia comentada en varias
líneas (el `--` rompe el match igual); solo la comentada en UNA línea. Los dos primeros
habrían quedado como cobertura falsa, verdes para siempre.

**Decimosexto — el mutante corrió MENOS casos que el control, y «0 fallidos» se lee como sano.**
AGH 19-ago (#941 → #1396): `✗ SIN VÍCTIMA … 52 pasados, 0 fallidos` contra un control de **71**. Los 19
que faltaban eran un fichero `.pg` entero que **no se ejecutó** (base momentáneamente inalcanzable →
`ctx.skip()` en bloque). Repetido a mano: **18 de 19 en rojo** — el guard tenía víctima. Lo peligroso es
que aquí no chirría nada: ni un `0`, ni un crash, ni un exit raro; solo faltan casos, y el número que lo
delata está en la línea del control, 40 más arriba. El arnés de AGH ya tenía regla para esto y compara
contra **cero** (`0 pasados && 0 fallidos`), así que caza la corrida vacía ENTERA y es ciega a la
**parcial**. **Regla: el veredicto se compara contra el CONTROL, y no solo por color — también por
recuento.** Menos casos que el control ⇒ arnés roto, nunca «sin víctima». Y es sistemático, no casual:
los `.pg` se saltan en bloque cuando la base no responde, y un barrido lanza decenas de corridas contra
esa misma base, así que se dispara justo cuando más mutantes hay en vuelo.

**Decimoséptimo — la mutación muere, pero la matan los tests VIEJOS: no dice nada del candado
NUEVO.** Familia del decimotercero («importa quién la mata»), aplicada al caso más común de todos:
validar una aserción que **acabas de añadir**. FacturaIA 3-sep: tres mutaciones seguidas dieron
`✓ VÍCTIMA — 3 de 25`, y las tres eran inútiles, porque entre las tres víctimas estaban siempre los
dos casos que ya existían antes de mi cambio. Con esa evidencia la aserción nueva podía ser un
`expect(true)`. La cuarta se eligió para **perdonar** lo que ya tenía cobertura (el test dedicado
vivía en `alto_rel = 0,06`, así que la mutación disparaba desde `0,062`): cayó **1 de 25**, y era el
caso nuevo. Regla: para verificar un candado nuevo, la mutación no se elige por ser plausible sino
por **dejar en verde todo lo que ya estaba vigilado**; si no puedes construirla, es señal de que el
candado nuevo no añade poder discriminante y sobra. Y el veredicto útil no es «hubo víctima», es
**qué casos cayeron** — `mutate` da el recuento, los nombres hay que ir a buscarlos al log.
