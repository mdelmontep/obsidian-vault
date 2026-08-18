---
title: agh-iberica-historico
date: 2026-08-16
tags: [cliente, agh-iberica, historico]
---

# AGH Ibérica — histórico de estados

Estados anteriores del hub [[agh-iberica]], sacados del dashboard para que el arranque de sesión no
los pague. El detalle día a día vive en `docs/status-log/` del repo.

## 2026-08-17 (tarde)

🟢 **Seis PRs dentro, siete issues cerrados** (`4a83b42`), gate verde a la primera (`3670/239/5f`), combinación de las siete medida antes de mergear con suma exacta. 🩺 El flake `57P01` cerrado como CLASE, no por fichero. 🟢 **Langfuse recuperado sin Deploy** (`docker compose up -d clickhouse`): 1.064 trazas intactas, ventana real **10 días** — el diagnóstico previo y su corrección eran los dos falsos. 🔴 Tres premisas falsas del día eran propias (dos caminos de salida de un read donde hay uno; `git ls-files` donde el barrido usa `readdirSync`; censo 8/10 siendo 7/9).

## 2026-08-15 (noche) — `main` en `10faf60`

🟢 **Dentro la NOCHE del 15-ago: 13 PRs y 14 issues** (`ff1ce5d` → **`10faf60`**) — **siete mías y las CINCO de Dani y Borja**, más el arreglo del rojo y dos de cierre. Gate de las doce combinadas `agente 3429/239/5f · dashboard 1229/0/0f · base 219ee16` ✓. Prod `sha256:4ca23792… · 302 ficheros`.

🔑 **Lo reutilizable de la noche:**
- **Un candado nuevo en `main` caza las PRs abiertas escritas ANTES que él** — dejó `main` en rojo; ningún gate individual lo ve, solo el de la combinación → [[un-candado-nuevo-en-main-caza-las-prs-abiertas-escritas-antes]]
- Un candado **estructural** (cuenta marcadores en el fuente) **no cubre el cableado**; y un `SIN VÍCTIMA` puede ser **selección de tests estrecha**, no un hueco → [[el-hueco-esta-en-el-cableado-no-en-la-funcion-pura]]
- **Una escotilla que el mensaje de error anuncia y el parser no acepta** → [[una-escotilla-que-el-mensaje-de-error-anuncia-y-el-parser-no-acepta]]
- **100 bases `agh_*`** = 15 min sin `.pg` para todos tras un arranque sucio; y el Postgres de `5433` vive en **Colima tras un túnel SSH** → [[las-bases-efimeras-que-nadie-borra-hacen-eterno-el-arranque-sucio]]
- **5 de 6 premisas falsas, sesgo CORTO**: #1103 decía 3 sitios y eran 9 · #1211 nombraba un método **que no existe** · #1222 traía una aserción **tautológica**. Y **fechá la sesión como «16-ago» siendo 15**: viajó a `main`, al snapshot y a seis avisos sin que nada la comprobara (corregido en #1242, declarado en la nota).
- 🩺 **Dos rojos del REVISOR, no de las PRs**: el dashboard con `--root` desde la raíz rompe las rutas de los fixtures (11 × `404`; con `cwd=dashboard`, 17/17), y comparar rama-vs-main **en bloques** dio la dirección equivocada — entrelazando, `main` fallaba igual (carga 22).

🧾 **Issues nuevos de la noche (7):** #1226 · #1227 · #1228 · #1229 · #1230 · #1231 · #1232, todos con etiqueta. **#1204 re-medido: su cifra caducó AL DOBLE (9 → 18)** — y sus tres `_Aridad*` de `tone.ts` **no son basura, son un candado de tipos**.

## Historial detallado hasta el 14-ago

- **13/14-ago (Manu; 27 PRs en dos días)** — el 13 cinco y el 14 **veintidós**, todas de arnés y medición: golden de copia por canal, `verify:ui` que ABRE lo que hay que abrir, el coste de evals en un sitio, la línea `pg:`, el barrido cubriendo `dashboard/`, el **sello de imagen que verifica prod sin SSH**, el sello que dice la base real con pila, el candado del export fantasma, el punto ciego de las at-rules y la imagen sin `dashboard/` (−34,8 %). **Lo que sobrevive: 11 de 16 premisas falsas, y el sesgo NO es constante** — unas se quedan cortas, otras se pasan (una cifra mía, «cinco semanas», eran 8 días). Corolarios: *la lista objetiva sale del `git diff`, no de tu hipótesis*; *`Refs` y nunca `Closes` cuando entra media issue*; *el hueco está en el CABLEADO*, seis veces en la semana. → [[el-hueco-esta-en-el-cableado-no-en-la-funcion-pura]] · [[mide-cuantos-pueden-fallar-antes-de-elegir-entre-n-candados-y-un-tripwire]] · [[un-fichero-nuevo-es-un-solo-hunk-y-el-barrido-de-mutacion-no-lo-cubre]] · [[el-exit-code-que-lees-no-es-el-del-comando-que-te-importa]] · [[dockerignore-no-es-gitignore-y-la-basura-local-pone-el-gate-rojo]] · [[aseverar-la-igualdad-congela-un-accidente-asevera-el-bicondicional]] · [[closes-N-cierra-el-issue-entero-aunque-escribas-3-de-4-al-lado]]
- **7/10-ago (Manu + Borja; 17 PRs)** — **el gate verde no es la revisión** (dos PRs devueltas con el gate verde; su candado pasaba con la regla borrada) · nace `npm run mutate:diff` (#1049/#1051) · `agh_dev` **envenenada** y el remedio escrito pasaba de «envenenada» a «desfasada» imprimiendo éxito · **41 de 41 runs de Actions con 0 pasos**, o sea 10 PRs mergeadas con un CI que no ejecutó nada. → [[registrar-una-migracion-sin-ejecutarla-envenena-la-bd]] · [[un-comando-de-reparacion-corrido-desde-un-checkout-viejo-repara-a-la-version-vieja]] · [[el-rojo-de-ci-tiene-dos-causas-cuenta-los-pasos-ejecutados]]
- **3→6-ago (Manu; ~50 PRs en cuatro días)** — Fase 3 en código y cerrada, cortes del rediseño, el bypass del HITL (#945), el sweeper (#953), las 7 issues de voz y dos trenes mergeados de una en una con gate entre cada uno. El hilo de los cuatro días: **un candado que EXISTE no es un candado que MUERDE**, y **cuatro instrumentos mintieron en la dirección que deja mergear** (`n=10` habría dejado pasar una caída de 96 % → 48 %). Método que rindió y se quedó: revisar las PRs propias con agentes instruidos para **atacar** las afirmaciones. → [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] · [[el-gate-verde-no-sustituye-una-revision-adversarial-antes-de-mergear]] · [[un-prompt-es-una-superficie-con-localidad-no-un-documento]] · [[evidencia-fechada-por-reloj-muere-en-un-rebase]] · [[el-cierre-escrito-antes-de-acabar-la-sesion-caduca-en-su-propia-pr]] · [[recurso-de-test-con-nombre-constante-no-aisla-entre-procesos]]
- **1/2-ago** — #747 (el 32,8% de `clarify` no medía lo que creíamos: agregaba 4 conductas y excluía 5 caminos) · #712 (la raíz recogía `dashboard/test/**` → 38 ficheros corrían **dos veces** por gate) · #758 (el guard de grounding no vigilaba el lead: aprobaba **invertir una negación**) · #760 (SSH del host caído). Y la trampa que más costó: **los arneses dieron falsos por ENTORNO cinco veces en dos días** — endpoint que deriva entre horas, carga >50, `agh_dev` truncada por sesiones paralelas, rama sin rebasar (lo delata `dashboard 439` vs 472) y un control tautológico propio. → [[medir-un-cambio-contra-un-llm-entrelazado-no-en-bloques]] · [[el-control-que-deja-dentro-el-test-del-cambio-se-mide-a-si-mismo]] · [[cpu-contencion-multisesion-falso-positivo-ui-atascada]] · [[test-db-persistente-contaminada-entre-ramas-recrear-fresca]]

🗓️ **16-ago (madrugada) — 5 PRs y 5 issues** (`93d7fb2`→`c24d5c9`): `mutate:diff` acusó en falso («CERO MORDIDAS» midiendo **40 de 114**; con la muestra completa muerde 12) · premisa de #1228 FALSA y la protección era **incidental** · un agente muerto dejó un motor **desacoplado** mutando `src/` 1 h 56 min · 3 de 4 premisas falsas o cortas · 117 ramas locales → 4 con refs de archivo. Issues: #1245 · #1247 · #1248 · #1253.

🟢 **Dentro la mañana del 15-ago: 11 PRs y 12 issues** (`842a72a` → `a8dc258`). Reutilizable: 6 de 7 premisas falsas y todas cortas · noveno hueco en el **cableado** (cablear el arreglo bueno **no protege**; la clase se cierra en el **instrumento**) · las convenciones se descartan **con la cifra** · [[un-candado-que-vive-en-tsc-es-invisible-para-la-suite-y-para-la-mutacion]] · [[un-guard-que-detecta-por-contenido-caza-los-comentarios-que-lo-niegan]].

✅ **Las 4 decisiones de producto de esa mañana: TRES ya implementadas y dentro** (#1196 → #1233 · #1116 → #1235 · #1103 → #1234). Viva solo **#1092**, por su paso humano: mandar `hilos_pendientes_3` a un móvil REAL — que Meta apruebe el cuerpo **no** prueba que WhatsApp entregue. El *porqué* de cada una está en su issue.

🟢 **Dentro el 14-ago: 17 issues** en dos tandas. **Del 14-ago, condensado:** 11 de 16 premisas falsas y el sesgo NO es constante — *la cifra que nadie midió está mal en la dirección que le convenga al relato*, y **la recomendación de un issue es la premisa que menos se cuestiona**. Más: [[el-hueco-esta-en-el-cableado-no-en-la-funcion-pura]] · [[mide-cuantos-pueden-fallar-antes-de-elegir-entre-n-candados-y-un-tripwire]] · [[aseverar-la-igualdad-congela-un-accidente-asevera-el-bicondicional]] · [[un-fichero-nuevo-es-un-solo-hunk-y-el-barrido-de-mutacion-no-lo-cubre]] · [[dockerignore-no-es-gitignore-y-la-basura-local-pone-el-gate-rojo]] · [[el-exit-code-que-lees-no-es-el-del-comando-que-te-importa]].

🧰 ~~**En cola para Borja:** #1097 → #1098~~ — **MERGEADAS la noche del 15-ago**, y con ellas **#1144 · #1146 · #1161 quedan DESBLOQUEADAS**. La trampa se confirmó en vivo: **#1097 → #1098, apiladas** — ⚠️ al mergearlas, squashear el padre deja a la hija `CONFLICTING`, **o `MERGEABLE` reaplicando el diff del padre**: `gh pr edit --base` no arregla la historia, hace falta `git rebase --onto origin/main <rama-padre>` → [[delete-branch-al-mergear-cierra-la-pr-apilada-no-la-reapunta]]. Desbloquean **#1144 · #1146 · #1161** (las tres en `hitl-brain.ts`). Además **#1126** · **#1129**. ⚠️ **#1036/#1037 caen en `static.ts` con la #1140 de Dani: apilar, no paralelizar.**

---

### 17-ago (mediodía y madrugada) — condensado al cerrar la tarde

## Estado (2026-08-17) — `main` en `163ea09`; **TABLERO VACÍO**: cero PRs abiertas de nadie

🟢 **Mediodía: #1281 DECIDIDO y #1232 cerrado** (PR #1285 → `fbe54da`). **Ninguna de las tres opciones de #1281 era la buena**, y lo zanjaron dos comprobaciones que dos agentes read-only —con recomendaciones OPUESTAS— no podían hacer: `docker compose version` → **`docker: unknown command`** (recrear el contenedor **no desbloquea** nada: `check-drift.ts` invoca ese subcomando) y `DRIFT_MODE=local` → **`✅ sin drift` en 2,1 s**. 👉 **El local es el camino soportado** (ADR-0002 §6, con lo que lo invertiría). 🔴 **El hueco real era otro**: el drift vivía sólo en el `gate:full` OPCIONAL —la migración 0031 (#986) se mergeó sin él— y ahora el gate **FALLA** si el diff toca el SQL sin evidencia (huella, no reloj). 🧹 **#1232 tenía la premisa FALSA**: el gate **nunca creó bases**. **113 → 1**, y `--base-efimera` la retira sola. 🐳 El compose sin `name:` levantaba un **clúster vacío** desde cualquier worktree → [[docker-compose-deriva-el-proyecto-del-directorio-y-en-worktrees-eso-es-un-cluster-vacio]].

🔴 **#1284 — de Borja, y es de PROD:** el **ClickHouse de Langfuse no existe** en el host (ni parado) y **su volumen de DATOS tampoco**. **≥2 semanas de trazas perdidas**, y nadie se enteró porque **`/api/public/health` devuelve 200 con el backend caído**. La auditoría semanal (#979) y las mediciones de #1064/#535/#591 están **mudas** hasta el redespliegue. Causa **no atribuida**.

🗓️ **Madrugada del 17-ago, condensado** (6 PRs, 6 issues, `8863b57`→`feece17`): #1272 · #1265 · #1269 · #1259 · #1258 · #1256. Lo que sigue valiendo es **el método**: de ~11 mutaciones del revisor, **dos SIN VÍCTIMA y las dos huecos reales**, ambas sobre **la propiedad que el autor declara como su aportación en el cuerpo de la PR** — y `0 SIN VÍCTIMA` del barrido no cubre nada mientras el recuento de «sin medir» no sea 0. → [[al-revisar-muta-la-propiedad-que-la-pr-declara-como-su-aportacion]]. Issues que dejó: **#1273 · #1280 · #1282** (+ #1281, ya cerrado al mediodía).

### 17-ago (tarde) — narrativa completa del cierre

## Estado (2026-08-17, tarde) — `main` en `534858c`; abierta solo la #1302 de Borja

🟢 **SEIS PRs dentro y SIETE issues cerrados** (override de founder, avisado en Slack antes de tocar `main`, de una en una y sin `--delete-branch`): #1303/#1293 → #1287/#1280 → #1311/#980 → #1310/#1290 → #1294/#1260 → #1292/#1282+#1268. Último código: `4a83b42`. **Gate sobre `main` mergeado ✓ VERDE y a la PRIMERA** (`agente 3670/239/5f · dashboard 1271/0/0f`), y **prod verificada por contenido** (`sha256:8730cda2… · 308 ficheros`, calculado sobre el árbol y comparado con `/version`).

🔬 **Lo que más vale es el método, no los diffs: la COMBINACIÓN de las siete ramas se midió ANTES de mergear** (0 conflictos, `lint`+`tsc` ec=0, 7 candados transversales 289 passed) y **la suma cuadró exacta**: `3602 + 9+11+13+12+16+7 = 3670`. Es la comprobación que faltó el 15-ago cuando `main` quedó en rojo.

🩺 **El flake `57P01` no volvía: nunca se cerró la clase.** #275 lo arregló en UN fichero con un comentario al lado y siete hermanos nacieron expuestos. `64 passed · 4 errors · exit 1` → `76 passed · 0 errors · exit 0` (×2), carrera aislada `10/10 escapan antes · 0/10 después`, y el gate de `main` con el arreglo dentro sale limpio a la primera contra 3 de 4 corridas con flake ese día. → [[vitest-unhandledrejection-run-rojo-pese-a-0-fallos]]

🎯 **Root cause del `tests 0 passed`**: el parser de la línea del gate cogía la PRIMERA ocurrencia de `Tests`, que en una corrida con fallos es la cabecera `⎯⎯⎯ Failed Tests N ⎯⎯⎯` → **la línea miente en toda corrida con fallos**. Salió de un rojo ajeno que casi archivo como flake. → [[la-cabecera-de-error-del-runner-roba-la-primera-ocurrencia-al-parser]] · queda **#1291** (bloqueado hasta hoy por la PR que tocaba ese fichero, ya dentro).

🔴 **Tres premisas falsas del día eran MÍAS**: mi briefing a un agente afirmaba dos caminos de salida de un read y en voz hay **uno**; mi issue decía `git ls-files` donde el barrido usa `readdirSync`; y mi censo contaba 8 de 10 expuestos siendo **7 de 9**. Las tres las tumbaron los agentes porque el brief les pedía **medir cada premisa, incluidas las mías**. Ajenas: la central de **#1268** es falsa (max **1006 ms**, el 20 % del corte) y el ejemplo de **#980** también (el compacto lo emite `reminders`, no la agenda).

🟢 **Langfuse RECUPERADO sin Deploy** (era de Borja, #1284): `docker compose up -d clickhouse`, 20 s, los cinco sanos intactos. **El diagnóstico de la mañana era falso**: el volumen SÍ existía (**37 GB**) y las **1.064 trazas están intactas**. La ventana no eran «≥2 semanas» ni las «34 h» que dije yo, sino **10 días** medidos en la tabla. → [[Stack/docker-infra]] §«Un servicio AUSENTE» · [[Stack/incidents]]
⚠️ **Y lo que de verdad importa de eso no es la ventana**: **1.064 trazas en cinco semanas**, con días de 4 y 6 — Manu confirma que **no la usan mucho ahora**. Con ese caudal, «sin trazas» y «sin tráfico» son indistinguibles, así que cualquier medición de conducta real (auditoría #979, #1064, #535, #591) mide una muestra minúscula. La sonda que lo tapó diez días (`/health` da 200 con el almacén ausente) → **#1304**.

🩹 **Rojo ajeno filiado, y es una aserción verde por suerte desde #661**: `staffing.pg` asevera un ORDEN que su consulta no garantiza (los cuatro audits comparten `created_at` en la misma tx) → **#1309**, y con el gate creando su base de cero **saldrá más, no menos**. → [[order-by-created-at-empata-dentro-de-la-misma-transaccion]]

▶️ **Cola, ya desbloqueada por estos merges** (lo barato primero): **#1305** (una palabra: el subset de #247 es el CUARTO sitio que pide la costura de voz) · **#1291** · **#1306** (el backstop del borde solo vigila teléfonos; correo y fecha sin red en los dos canales — dos sesiones llegaron a él por separado) · **#1289** (`prepare` fuera de todo `try`: el embudo cubre los 6 throw sites por accidente) · **#1204** · **#1309** · **#1304**. `ready-for-human`: **#1288** (un prefijo derivado del RELOJ pasa los candados de #1260 **y** #999 a la vez) y **#1307** (la hora desnuda de la agenda).

## Estado (2026-08-17, noche) — archivado el 18-ago — `main` en `7c9bd36`; abierta solo la #1302 de Borja

🟢 **DOCE PRs dentro y DOCE issues cerrados** (#1309 · #1204 · #1291 · #1188 · #1308 · #1305 · #1306 · #1289 · #1262 · #1052 · #1300 · #1304; último código `94b99a3`). Gate sobre `main` **✓ verde a la primera y sin reintento** (`3748/239/5f · dashboard 1273/0/0f`), prod verificada por contenido (`sha256:d9b20f01… · 309 ficheros`), y la **combinación de las doce medida ANTES de mergear** con la suma exacta (3748).

🔴 **Lo más valioso: #1291 pedía un candado que NO puede existir**, y lo demostró el gate — la invariante que el issue pedía era el **diagnóstico** de `mutate-diff.ts`. → [[un-candado-que-el-issue-pide-puede-cegar-a-otro-consumidor]]. De paso, el defecto real es peor de lo escrito: el parser mentía en las **cuatro** cifras y en **toda** corrida con fallos.

🔴 **La verificación de la combinación COBRÓ** (acoplamiento del 15-ago calcado): el `lint` de las doce juntas salió rojo por una constante sin usar que **sólo existe al juntar #1315 con #1317** — ninguna PR podía verlo sola. Y la constante no sobraba: **faltaba el caso que la consumiera** (el corpus aseveraba que el embudo grita, no que rinda).

🐛 **Defecto de PRODUCCIÓN vivo → #1322**: `spokenLine("b@617314938.com")` **destapa** el teléfono, porque la pasada de correo quita la `@` que lo protegía; el TTS lo dirá como cantidad (#977 otra vez). Lo probado era `spokenPhones` **a solas** — nadie había mirado la composición. Cae con él la afirmación del código de que el orden de las pasadas es una «mutación equivalente». **Es el siguiente a coger.**

📡 **#1304: no había ninguna sonda que arreglar** — cero líneas del repo vigilaban Langfuse; lo que llamábamos sonda era el `curl` a `/health` de la auditoría semanal. La nueva mide el **almacén**. ⚠️ **Pero nada la ejecuta todavía**: sin disparador diario es otra señal que nadie lee. Decidir dónde vive el job.

⚠️ **Tres premisas de issues resultaron falsas, dos MÍAS**: #1309 (los `created_at` **no** empatan: están separados 8-11 ms, y su arreglo propuesto tampoco valía → [[order-by-created-at-empata-dentro-de-la-misma-transaccion]], corregido) · #1305 (cinco puntos de emisión, no cuatro) · #1052 (la asimetría de tonos que daba por heredada no existe).

▶️ **Cola libre, priorizada**: **#1322** (el único de producción) · **#1323** (`copyForChannel` escrita dos veces) · **#1327** · **#1326** · **#1325** · **#1095** · **#992** · **#991** · **#984**. `ready-for-human`: **#1324** · **#1288** · **#1307**.

⚠️ **Aviso para la #1302 de Borja**: #1204 metió `@typescript-eslint/no-unused-vars` en la raíz y el barrido de lint ve los ficheros nuevos de los DOS paquetes — si alguno de los suyos trae un símbolo sin usar, saldrá en su corrida.

⏸️ **Lo único vivo a propósito:** rama `manu/issue-1064-1212-1044-campo-aislado-y-huella` en `~/wt-1064`, **sin PR** — falta el caso-oro de #1064 y el prompt cambió, así que abrirla declararía cobertura de eval CERO sobre un cambio real (~12 $). ⚠️ **Y sigue sin saberse si Carlos usa la demo**: 1.064 trazas en cinco semanas, con días de 4 y 6 — «sin trazas» y «sin tráfico» son indistinguibles.

📚 **Estados anteriores** → [[agh-iberica-historico]] (**17-ago tarde, mediodía y madrugada** condensados ahí).

_Creds:_ `AGH Iberica` → `Open AI AGH` **por ID** (⚠️ espacio final) · SSH del host en `ssh AGH` (el ítem «186» es del PANEL, no de SSH). **`opsa`, nunca `op`**; `item get` exige `--vault`.

### Referencia sacada del dashboard el 18-ago

💡 **Discriminador gratis para esa auditoría** (medido, para no repetirlo): `present()` envuelve **solo los 7 reads de LISTA** (`capabilities.ts` `:145` clients · `:175` contacts.internal · `:182` opportunities.open · `:183` consultants · `:198` tasks · `:204` reminders · `:205` threads.open). Literales, o sea **controles internos**: `client.detail`, `client.prep`, `meetings.recall`, `capabilities` y los dos de calendario. Si la degradación aparece en los siete **y no** en los cinco, el presenter es la causa; si aparece en los dos grupos, no lo es.

- ✅ *Cerrados y sin cola: #952 (el digest entregó, 10-ago) · #988 (el teléfono se lee dígito a dígito) · #953 (los 3 hilos pasaron a `delivered`) · **#1094 y #1096 MERGEADAS** (el hub las listó como bloqueante de Borja hasta el 14-ago, ya siendo falso).*
