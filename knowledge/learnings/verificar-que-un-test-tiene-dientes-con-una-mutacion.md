---
title: un test nuevo no vale hasta que le rompes el código a propósito y falla
date: 2026-07-28
updated: 2026-08-10
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
tamaño** (`expect(n).toBeGreaterThan(500)`) como primer caso.

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
la vez**: ahí sí cae, y eso es lo que se documenta.

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
