---
title: prompt de continuación TuFacturaIA — 26-ago-2026 (tras #2224)
date: 2026-08-26
source: facturaia
tags: [facturaia, prompt, agentic, ia, continuacion]
---

Copia desde aquí hacia abajo en la sesión nueva.

---

Repo `~/Projects/facturaia`, rama `main`. Contexto: el 26-ago se activó la IA agéntica de
`categorias` en producción (#2221 + mig 755) y el #2224 cerró las tres decisiones que
escriben solas y no tenían test (regla aprendida, auto-aprobación OCR, y una línea roja
DURA que un toggle de informes podía levantar). Verificado con 7 mutaciones / 7 víctimas y
gate entero verde (1465 ficheros, 15.464 tests).

Antes de tocar nada: `git log HEAD..origin/main` (mi checkout puede ir atrasado; con
worktrees vivos `git-guard` impide ponerlo al día, así que para AFIRMAR qué dice un fichero
usa `git show origin/main:<ruta>`).

## 1. El gap que dejó abierto el #2224 — cerrar primero

`docs/architecture/agentic-ocr-conciliacion.md` §0.bis-7 lista «transferencia interna» como
línea roja dura, pero **no dice que su detección ya no depende del toggle del usuario**. El
#2224 metió `planificarTransferencias` (`src/lib/conciliacion/transfer-pairs.ts`) justo para
eso: `detectar` sostiene el candado y la zona registrada, `marcar` sigue siendo del usuario.
Comprobado el 26-ago: `grep -n "planificarTransferencias\|ia_detectar_transferencias"
docs/architecture/agentic-ocr-conciliacion.md docs/architecture/gotchas.md` devuelve **cero**.

Un doc que contradice al código es la misma clase de fallo que causó toda esta sesión.
Añade el párrafo en §0.bis-7 y la fila correspondiente en la tabla de routing del `CLAUDE.md`
si el disparador no existe. Docs-only, sin migración; `npm run gate` igual.

## 2. Generalizar el diagnóstico que encontró los tres agujeros

El agujero no lo encontró un razonamiento, lo encontró **un grep**:

```
grep -rn "from ['\"].*<ruta-del-modulo>" src/ tests/
```

Si ningún test importa el fichero donde vive la decisión, no hay cobertura posible por muchos
tests que haya al lado. Barre con ese criterio los módulos que **escriben** sin intervención
humana (no los que leen): candidatos por orden de daño — cualquier `_parts/**/helpers.ts` de
un endpoint `internal`, los emisores de `audit_log` con `actor_type='agent'`, y los que
tocan `facturas.estado` o asientan stock. Reporta la lista de ficheros con **cero
importadores de test**, no un juicio sobre si están bien. Es medición, no opinión.

Ojo al modo de fallo hermano, ya documentado: un test que **replica** el predicado en vez de
importarlo da verde por definición. Si te encuentras copiando la condición al test, para.

## 3. La primera escritura silenciosa real, sin verificar todavía

`AgentesiaLab SL` es la única org de producción en `activo` (dominio `categorias`, gate
abierto). Sus **2 reglas aprendidas están a 1 confirmación de las 3** que exige el umbral
(`categoria_learning_n`, default 3), así que el #2224 entró ANTES de la primera aplicación
silenciosa, no después. Cuando lleguen las dos confirmaciones que faltan:

- comprueba en prod que la decisión queda en `agentic_decisions` con `zona='verde'` y la
  fuente correcta (`regla`, no `ia_sugerencia`),
- y que hay fila en `audit_log` con `actor_type='agent'`.

Lectura de prod: `psql` **como `postgres`** (el rol `claude_runner_ro` no tiene `BYPASSRLS` y
mediría ceros en silencio), credencial con `opsa read` consumida inline y **siempre**
`BEGIN READ ONLY;` — sin el `BEGIN` cada sentencia autocommitea.

## 4. Maduración: acumulación, no código. No lo confundas con una avería

El gate del OCR **no puede abrir** todavía y eso es correcto: pide ≥50 verdes resueltas en 30
días **por org**. El único freno de las 7 orgs sin inventario es `proveedor_no_confianza`
(68 de sus 261 decisiones pasarían a verde solo con que el proveedor madure); el veto de
stock aplica solo a Pescados Chivite y allí es **portante** (el 98 % de sus bandejas las mapea
un humano) — no se toca. DAORO sale de cuarentena el **28-ago**. No hay nada que programar:
si al medir sale «0 verdes», es el diseño, no un bug.

## 5. Cabos concretos, ordenados

1. **PR #2222 abierto sin mergear** — «el detalle enseña el producto que elegiste, no un
   guion» (albaranes). Renumerar si trae migración (`npm run mig:renumerar`, justo antes del
   merge, nunca a mano) y `git ls-remote origin <rama>` == `git rev-parse HEAD` antes de
   `gh pr merge`.
2. **Smoke del albarán que sí ejerce el guard** — el del 26-ago salió verde **sin ejercerlo**,
   porque la línea de la factura no traía `catalogo_id`. Repetir con una que sí, y el camino
   con lotes.
3. **22 dependencias circulares** del patrón `_parts` (barrel que reimporta a su hijo).
   Medido contra un checkout limpio de `origin/main`: son **idénticas**, deuda preexistente y
   ajena al #2224. Merece issue propio, no un arreglo de paso.
4. **`es_intracom`: el código ya está, faltan los datos** (86 casos fuera de Chivite). Ojo
   con el puntero: `PROMPT-aprendizaje-ocr-paso3.md` está **SUPERSEDED** y el área se
   **CERRÓ el 21-ago** (ADR-021 y ADR-022) — no lo ejecutes, lo dice su propia cabecera.
   `auto-approve.ts:215` ya levanta la línea roja cuando el campo está **respaldado** por una
   regla verde, igual que `tiene_irpf` en la 203. Lo que falta es que exista alguna regla
   verde: `ocr_reglas_aprendidas` está **vacía** en prod (medido el 26-ago), así que nada
   respalda nada. Acumulación otra vez, no código.
5. **Eval de `doc-extract`** — pendiente, necesita corpus de extractos bancarios ficticios.

## 6. Lo que NO es un pendiente (no lo reabras)

- **PSD2/Tink**: 0 consentimientos activos y 0 movimientos por sync es **decisión de negocio**
  (el agregador es caro, decidido el 26-ago), no avería. Los 138 movimientos de prod entraron
  por CSV (129) y PDF (9). El cron sale verde cada día sobre lista vacía. **Y hay un cebo**:
  el **PR #610 sigue abierto en draft** («Salt Edge como tercer provider PSD2»). Es trabajo
  para una integración que se aparcó por coste, así que no se retoma «porque estaba a medias»:
  o se cierra con el motivo escrito, o se etiqueta para que no vuelva a parecer un cabo. Antes
  de tocarlo, la decisión es de Manu, no del que lo encuentre abierto.
- **La zona registrada en shadow sigue siendo `verde`** aunque no se aplique nada. No la
  derives de `esVerdeAuto`: esas verdes son el **denominador** del gate de acierto
  (`src/lib/admin/ia-ops/auto-accuracy.ts` filtra `r.zona === 'verde'`), así que derivarla
  produce un gate que solo puede abrir si ya está abierto.
- **CI de GitHub Actions**: sin billing por decisión firme. El gate real es local y el
  `pre-push` es el que corre suite y build. «Gate en verde» exige haber corrido
  `npm run gate`, o nombrar qué etapas corrieron.

## 7. Reglas de la casa que aquí se pagan caras

- **Nunca rodear un hook con `--no-verify`.** En el #2224 pararon dos (`file-size` y el grafo
  de dependencias) y los dos se resolvieron por su camino: `npm run ratchet:size:update`
  auditando el diff del baseline, y `npm run deps:json`.
- **Ningún gate por pipe.** Capturar a fichero y mirar `ec=$?` (o `pipestatus[1]` en zsh): un
  `push | tail` devuelve el exit del pipe y deja pasar un abort del pre-push.
- **Si la suite da rojos con duraciones absurdas** (minutos por test), es inanición de CPU, no
  el código: mira `load` y el semáforo `fia-gate`, corre los fallidos aislados y repite la
  corrida limpia antes de diagnosticar nada.

## 8. La mejora del agente, medida el 26-ago: cuatro cosas más

Salieron de aplicar al propio subsistema el grep del §2, en vez de fiarme de que el #2224 lo
había dejado cerrado. Las cuatro están verificadas contra el árbol, con fichero y línea.

### 8.1 `DOMINIOS` está escrito a mano TRES veces y nada lo vigila

- `src/lib/agentic/automation-state.ts:18` → `const DOMINIOS: readonly Dominio[] = ['ocr','categorias']`,
  y se usa como validador: `if (!DOMINIOS.includes(dominio)) return { error: 'dominio_invalido' }`.
- `src/app/api/admin/ia-ops/auto-accuracy/route.ts:17` → la misma lista, otra vez a mano.
- `src/app/api/agentic-automation/route.ts:36` → `['ocr','categorias'] as const` alimentando un `z.enum`.

Tres copias de la unión `Dominio` y **cero candados** (`grep -rn "DOMINIOS" src --include="*.ts"`
no encuentra ni un test). Es literalmente el punto 6 de `~/.claude/rules/type-safety-ts.md`: un
array al que le falta un miembro **compila**, así que añadir un tercer dominio a la unión lo
deja rechazado como `dominio_invalido` en los tres sitios, con la suite en verde. Ya pasó en
AGH #674 — 5 de 6 variantes, una feature entregada que nunca funcionó.

**Y el repo ya tiene la forma correcta al lado**: en `src/lib/ocr/reglas-aprendidas.ts:54` la
fuente es el array (`CAMPOS_REGLA … as const`) y el tipo se **deriva** de él
(`type CampoRegla = (typeof CAMPOS_REGLA)[number]`), más un `Record<CampoRegla, string>` para
las etiquetas, que no compila si falta un miembro. Copia ese patrón: una sola fuente, el resto
derivado, y las tres copias importándola. Verifica el candado como manda la regla — añade un
miembro falso a la unión y comprueba que **no** compila.

### 8.2 `decidirMuestreo` no lo ejerce ningún test

`src/lib/agentic/muestreo.ts` aparece en cuatro ficheros y **ninguno es un test**: sus dos
consumidores (`enrich-batch/_parts/enrich-batch/helpers.ts:29` y
`whatsapp/ocr-process/route.ts:41`), `categoria-gate.ts` y él mismo. No hay
`muestreo.test.ts`.

Esto no es un detalle: el muestreo decide **qué verdes van a confirmación humana**, y esas
confirmaciones son la señal con la que se mide `auto_accuracy` (§0.bis-4: «medición viva =
muestreo de auditoría + correcciones espontáneas»). Si el muestreo está mal, el gate abre o
cierra sobre una métrica sesgada y nada se queja. Es el cuarto agujero de la misma clase que
los tres del #2224, encontrado con el mismo grep. Cúbrelo con la forma que ya funcionó:
inyectando el `rnd`, aserción sobre el clampeo (`≤0` nunca, `≥1` siempre) y una víctima de
mutación real con `~/.claude/bin/mutate`.

### 8.3 La degradación del gate no se le cuenta a nadie

`aplicarGate` (`src/lib/agentic/gate.ts:150`) hace lo correcto al cerrar: `gate_abierto=false`
y, si el modo era `activo`, lo baja a `shadow` y escribe `degradado_at` + `degradado_motivo`.
Pero esas dos columnas **se escriben y nadie las lee**: fuera de `database.types.ts`
(generado) y de los tests que comprueban la escritura, no las consume ni un componente, ni una
notificación, ni un colector de `system_alerts` (`grep -rn "degradado_at\|degradado_motivo" src`).
Tampoco el cron `agentic-gate-sweep`, que es quien lo dispara, avisa: no hay `notify` ni
`emitSystemAlert` en su ruta.

Resultado: un propietario que activó la IA a mano puede quedarse en `shadow` sin que nada se
lo diga. El diseño pide lo contrario — §0.bis-5: «CIERRA (**degrada+avisa**)». Y encaja con la
regla de la casa sobre integraciones: un estado crítico que solo vive en una columna que nadie
lee es la versión en tabla de morirse en un log. Falta la mitad `avisa`: notificación **no
silenciable** (`NON_SILENCEABLE_KINDS`, ver `gotchas.md` §Notificaciones) y que la sección de
Ajustes diga por qué está en shadow. La UI ya hace bien su parte de al lado
(`agentic-automation-section.tsx:249` deshabilita «activo» con el gate cerrado y lo explica en
la 286), así que es coherente con lo que ya hay, no un invento.

### 8.4 `aprendizaje-ocr.md` se contradice consigo mismo

- Línea **166**: «El resto del paso 3 (`es_intracom`, `tiene_irpf`) sigue pendiente».
- Líneas **250-251**: «`tiene_irpf` y `es_intracom` dejan de bloquear si su campo está
  respaldado» + «mig 731».

**Manda el código, y el código dice que está hecho**: `auto-approve.ts:203` y `:215` ya
comprueban `!respaldado(...)`. Deja una sola versión. Prosa caducada dentro de un doc vigente
es cómo una sesión rehace trabajo terminado — el mismo fallo que la cabecera de
`PROMPT-aprendizaje-ocr-cierre.md` ya documenta («la foto estaba caducada, no el árbol»).

### 8.5 Orden sugerido

9.1 y 9.2 son de una sesión corta cada uno y cierran riesgo real; 9.3 es el que cambia lo que
ve el usuario y merece decidir el copy con `docs/architecture/copy-humano.md` delante; 9.4 y
el §1 son docs y se pueden agrupar en un único PR de solo-documentación. Ninguno pide
migración. Todos: `npm run gate` entero, y víctima de mutación para lo que sea un candado.

## 9. El límite de este prompt (dicho, no escondido)

Esto cubre **un hilo**: la IA que escribe sola y lo que el #2224 dejó abierto. El hub tiene
del orden de 60 entradas más vivas que **no** están aquí y no por descuido. Las que más
pesan, para que ninguna se caiga por no estar nombrada:

- 🔴 **Los PDF de factura sin copia de seguridad de ningún tipo (#1641)** — falta crear el
  bucket `tufacturaia-storage-backup` en Backblaze (**sin** Object Lock) y pegar la clave en
  1Password. Es el pendiente de más daño potencial de todo el hub y es acción de Manu.
- 🔴 **#2100**: en una org suspendida, Ajustes → Empresa guarda la mitad y descarta la otra
  sin avisar.
- 🟠 **Cola fiscal**: siete decisiones abiertas con encargo escrito
  (`PROMPT-decisiones-fiscales-con-norma.md`), el barrido T1
  (`PROMPT-fiscal-inventario-cobros-t1.md`) y el #1899. **3T vence el 20-oct.**
- 🔴 **Obras / IET**: el catálogo equivocado cargado en prod, «Actualizar precios» que
  multiplica el precio cuando al material le falta el descuento, y los dos defectos de datos
  de `obras-097`/`-098`.
- 🔴 **Rotar las claves del sandbox `vtovkkrcybstlzpgqsaq`** (quedaron en un log).
- ⏸️ **FNMT → 036 (ROI) → NIF-IVA**, en standby por decisión de Manu del 24-ago.

El detalle de cada una vive en el dashboard de `~/Obsidian/Manu/00-home/facturaia.md`, que es
el que hay que leer al arrancar. **Si esta sesión va a atacar cualquiera de ellas, no uses
este prompt: abre el hub.** Mezclar los dos hilos es cómo se pierde el foco de los dos.
