---
title: hot cache
date: 2026-07-27
tags: [stack, index]
---

# Hot Cache

**Qué entra aquí (regla, no sugerencia):** SOLO **método y riesgo transversal** — lo que no sabes que
tienes que buscar: trampas de worktrees/subagentes/gate/verificación, y patrones de integridad que se
repiten entre proyectos. **Un gotcha de un stack concreto NO entra nunca**: su casa es
`Stack/<tool>.md`, que ya se carga por disparador cuando tocas ese fichero.

**Tope: ~45 entradas.** Si para meter una hay que sacar otra, ese es el trabajo — no ampliar el tope.

Por qué esta regla (2026-07-27): el fichero se podó por fecha dos veces (40→15 el 13-jul, 146→129 el
25-jul) y **volvió a 159 en dos días**. Podar no arregla un problema de criterio de entrada. Se
retiraron 116 punteros de gotchas por-stack; ninguno se borró — siguen en `knowledge/learnings/` y los
9 que no tenían otro enlace entrante quedaron recolocados en su `Stack/<tool>.md`.

Transversales de fondo en [[index]] §Transversales y [[patterns-cross-proyecto]].

**Criterio de entrada (27-jul):** tope duro de **25 entradas**. Para meter una hay que sacar otra.
Podar por antigüedad no funcionó dos veces (129→116→159 en dos días): el problema es el criterio de
entrada, no la edad. Lo retirado vive íntegro en [[patterns-cross-proyecto]] y en `knowledge/learnings/`.

- **Un fix no está verificado hasta crear una entidad NUEVA tras el deploy** — leer los datos que arregló el backfill no prueba nada del código; el compositor no es el punto de persistencia y la suite verde no cubre el camino que tocas. Ver [[cambiar-la-semantica-de-una-columna-el-compositor-no-es-el-punto-de-persistencia]]
- **Una PR encadenada se mergea en su BASE, no en main** — si no borras la rama base al mergear la primera; «MERGED» no significa «en main», verifícalo con grep sobre `origin/main`. Ver [[pr-encadenada-se-mergea-en-su-base-si-no-borras-la-rama]]
- **Cada fix de agente medido contra el modelo real destapa el siguiente hueco** — el ruido busca cualquier `kind`; y si un turno sigue rojo tras el fix, sospecha del assert antes que del código. Ver [[cada-fix-de-agente-medido-contra-el-modelo-real-destapa-el-siguiente-hueco]]
- **Un check de coherencia no puede afirmar un desajuste si no pudo preguntar** — clave ausente/401/429 es "no verificado" (UNA alerta media), no N desajustes altos; la alerta falsa induce a recrear datos que están bien. Delator: fallan TODAS las filas con el MISMO motivo. Ver [[fallo-de-credencial-no-es-dato-ausente-en-un-check-de-coherencia]]
- **Una clave read-only NO se verifica escribiendo** — el `POST` de prueba que esperaba un 403 devolvió 200 y creó objetos reales en una cuenta live. Lo comprobable leyendo es la CUENTA (`GET /v1/account`), no la ausencia de permiso de escritura. Ver [[no-verificar-una-clave-read-only-escribiendo-con-ella]]
- **El cero de "aún no lo sé" no es el de "está vacío"** — si un contador en su valor neutro decide tamaño o presencia de un elemento, hay CLS garantizado; el estado de carga es un tercer valor. Ver [[cero-mientras-carga-no-es-cero-vacio-y-provoca-cls]]
- **Una migración placeholder vacía no se nota hasta 123 migraciones después** — prod funciona y el agujero solo sale al levantar un entorno nuevo, con prisa. Detector: `grep -rl "Applied directly on remote" supabase/migrations/`. Ver [[migracion-placeholder-vacia-rompe-la-reconstruccion-y-no-se-ve-hasta-anos-despues]]
- **`--force-with-lease` sin `fetch` no protege nada** — compara contra tu `origin/<rama>` LOCAL, así que un checkout desactualizado autoriza rebobinar `main` 40+ commits. Lease con SHA explícito, y verifica la recuperación por ÁRBOL, no por log. Ver [[force-with-lease-sin-fetch-no-protege-nada]]
- **Un locator que resuelve a 0 elementos es un test roto, no evidencia** — y dentro de un `if (isVisible)` es FALSO VERDE. Afirmar por rol/nombre accesible o por el contrato del componente (`aria-controls`, `aria-live`), nunca por clase de CSS Module ni etiqueta nativa. Ver [[locator-de-test-atado-a-la-implementacion-caduca-y-da-falso-verde]]
- **IDs de entorno cableados en un spec miden una org que no existe** — `count` a 0 y `update` que no toca filas, en silencio. Resolver del entorno y fallar con mensaje claro. Ver [[spec-con-ids-de-entorno-cableados-mide-una-org-inexistente]]
- **El stash es compartido entre worktrees** — una sesión paralela puede recuperar tu stash y dejarte sin fix; cero `stash` en repos con worktrees. Ver [[stash-es-compartido-entre-worktrees-y-rompe-sesiones-paralelas]]
- **Subagente que reporta «hecho, verde» sin que exista el código** — `git show --stat` + `grep` del símbolo + rojo-primero repetido por ti. Ver [[subagente-reporta-hecho-codigo-que-no-existe-o-no-compila]]
- **Columna jsonb con varios escritores: cualquier PATCH parcial es un borrado** — si N sitios escriben la misma columna y uno hace upsert de "lo que yo conozco", borra las claves ajenas. Inventariar escritores por nombre de columna; merge por clave + allowlist + borrado solo explícito. Ver [[jsonb-compartido-varios-escritores-patch-parcial-borra-claves-ajenas]] · [[ADR-039-org-module-config-patch-merge-con-allowlist]].
- **Un override de BD que sustituye al schema del código vuelve INESCRIBIBLES las claves que omite** — pasa al endurecer el contrato de escritura; separar schema de render (override) del de escritura (unión). Caso real: 8 cuentas del asiento contable congeladas en prod. Ver [[override-de-bd-que-sustituye-al-schema-del-codigo-congela-claves]].
- **Server Component que toca la BD en su cuerpo se prerenderiza y tumba el build ENTERO** — y si el pre-push exige build, el gate se vuelve imposible y todos bypasean. Fix: `await connection()`. Ojo: el pre-push buildea el árbol del cwd, no los commits que empujas (verde falso). Ver [[server-component-que-toca-bd-en-su-cuerpo-se-prerenderiza-y-rompe-el-build]].
- **Gate de auto-aplicación: "n≥50 y acierto ≥95%" NO sostiene el 95%** — Wilson con n=50 da [0,851 , 0,984]; una org al 90% real abre el gate el 11% de las veces. Decide por cota inferior, sweep semanal + cooldown, y cobertura como condición aparte (el silencio no es aceptación). Ver [[gate-de-automatizacion-n50-al-95-no-sostiene-el-95-usa-cota-wilson]].
- **Relajar un filtro duro que además era techo implícito de un score abre una ruta de auto que nadie diseñó** — calcula el máximo alcanzable SIN esa señal antes de tocarlo; separa `umbral_sugerencia` de `elegible_auto` y codifica el invariante, no la constante. Ver [[relajar-filtro-duro-que-era-techo-implicito-abre-automatizacion-no-disenada]].
- **En un worktree `.git` es FICHERO, no directorio** — detectar la raíz con `existsSync('.git')` + `basename(dir)` devuelve la RAMA como nombre de proyecto (rompió el panel de horas). Parsear el `gitdir:`. Ver [[git-worktree-dotgit-es-fichero-basename-devuelve-la-rama]].
- **Un staging deja de ser fuente de verdad tras el commit, y editarlo sigue "guardando"** — el buffer (JSONB de OCR, borrador, import) se copia al registro EN el aprobar/publicar; después, la pantalla del staging persiste con éxito y el registro no cambia. Tras el commit muestra el valor DEL REGISTRO, bloquea con motivo y rechaza en voz alta desde el único punto de escritura. Ver [[staging-deja-de-ser-fuente-de-verdad-tras-el-commit-y-editarlo-no-cambia-nada]] · [[editor-inline-que-compara-contra-el-valor-mostrado-encalla-al-reescribir-lo-mismo]]
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
- **Nadie vigila el EOL del runtime: Dependabot mira CVEs, no fechas** — 88 días con Node EOL en prod sin un aviso, y el bump propuesto llevaba a un tag congelado. Check mensual contra endoflife.date, alojado FUERA de la infra que puede caerse. Ver [[dependabot-no-avisa-de-eol-de-runtime]]
- **"Cierra #N" no cierra nada: GitHub solo entiende los keywords en inglés** — sistemático si escribes los PR en español; issues dadas por cerradas siguen abiertas. `Closes #N` en el cuerpo. Ver [[cierra-en-espanol-no-cierra-la-issue-de-github]]

