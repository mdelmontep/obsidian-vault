---
title: facturaia — cerrar deuda E2E + perf-001 + infra-001
date: 2026-07-27
source: claude-code-session
tags: [facturaia, e2e, performance, migraciones, prompt]
---

> Prompt de arranque para la sesión que cierre esta deuda. El contexto pesado NO está aquí: vive
> en el repo (`issues/e2e-001-suite-smoke-contra-sandbox.md`, `issues/infra-001-...`,
> `issues/perf-001-...`), que es lo primero que manda leer.

Cerrar la deuda abierta de la sesión del 27-jul en TuFacturaIA: dejar la suite smoke en verde y liquidar `infra-001` y `perf-001`. Sin dejar nada pendiente y sin comprar ningún verde.

## Lee esto primero, en este orden

1. `issues/e2e-001-suite-smoke-contra-sandbox.md` — estado de la suite, fallos clasificados, y **tres advertencias de método** que te ahorran horas.
2. `issues/infra-001-migraciones-no-reconstruyen-la-bd.md` — qué está parcheado a mano en el sandbox y por qué difiere de prod.
3. `issues/perf-001-cls-banner-de-billing-y-dropzone.md` — CLS: lo arreglado y lo que falta.

## Antes de nada: rebaselinar

**No te fíes del "quedan 16"**. Desde que se escribió han entrado 5 PRs (#1249, #1251, #1254, #1256, #1258) que arreglan parte. Tu primer paso es **medir de nuevo** y publicar el número real:

```bash
npm run e2e:smoke        # ~17 min, con la máquina EN SILENCIO
npx playwright test --project=smoke --last-failed --reporter=line
```

El segundo comando separa fallo real de ruido de la tanda larga. Sin ese rebaseline no empieces a arreglar.

## Entorno

**Worktree propio, obligatorio.** El 27-jul coincidieron tres sesiones sobre los mismos ficheros: una rebobinó `main` 40+ commits y otra cambió HEAD bajo los pies de la primera. Comprueba `git worktree list` antes de crear el tuyo, y nunca trabajes en `modia-fase2`.

```bash
cd /Users/manueldelmonte/Projects/facturaia
git fetch origin && git worktree add -b <tu-rama> .claude/worktrees/<tuyo> origin/main
```

- `.env.local` apuntando al **sandbox** `vtovkkrcybstlzpgqsaq`, nunca a prod. Se reconstruye con
  `supabase projects api-keys --project-ref vtovkkrcybstlzpgqsaq -o json` (anon + service_role) más
  `NEXT_PUBLIC_APP_URL`/`SITE_URL` al puerto que uses y `NEXT_PUBLIC_BETA_FEEDBACK=true`.
- `.env.test` copiado, con `E2E_BASE_URL` al mismo puerto.
- Org de test: `Sotck test` = `7d9a2cfe-14ec-4268-a58f-37522915ffef`. Ya tiene NIF, sector Obras, las 32
  features, suscripción `complimentary`, bucket `facturas` y el cliente `Test SL`.
- SQL al sandbox: `supabase db query --linked --file <f>` **desde tu worktree**. Verifica nombres reales
  en `information_schema` antes de escribir: es `catalogo_servicios` (no `productos`),
  `profiles.user_id` (no `id`), y `billing_accounts` no tiene `org_id` (se une por
  `organizations.billing_account_id`).
- Turbopack no recarga `proxy.ts` en caliente. Y **para el dev server antes de `typecheck`**: mientras
  corre escribe `.next/dev/types/*` a medias y ensucia la salida con errores que no son tuyos.

## Los cinco frentes

### A. Conciliación — el bloque grande (8 tests, si el rebaseline lo confirma)

`conciliacion-fase2.spec.ts` (:64 comisión, :84 anticipo, :109 traspaso, :134 remesa 1↔N, :155 divisa) y
`conciliacion-vinculacion.spec.ts` (:94, :114, :185). Se despertaron al activar la feature; antes se
saltaban. `movimientos_bancarios` de la org está a **0**.

**No sirve sembrar filas al azar.** Cada flujo espera importes que cuadren con facturas concretas: un
cobro con comisión que deja remanente, un anticipo aplicable, un traspaso con dos patas opuestas, un
ingreso que cuadra dos facturas, y una factura en USD contra un movimiento en EUR con diferencia de
cambio. Lee los cinco, diseña el juego de datos, y déjalo como semilla **idempotente** en
`tests/e2e/seed-sandbox-conciliacion.sql`. Si necesitas facturas emitidas, créalas por la UI o la API
—nunca `INSERT` directo en `facturas`, que se salta `createDocument`—.

### B. Los sin diagnosticar

`generar-factura:38`, `stock-completo:141`, `ticket-simplificada:57`, `topbar-busqueda:27` y
`importar-factura-externa:52`. Varios pasan en aislado y fallan en la tanda: empieza confirmando si es
**acoplamiento entre tests** (uno deja datos que rompen al siguiente) y arréglalo aislando datos, no
subiendo timeouts.

### C. `copiloto-confirm` ×2 — decide y dilo antes de hacerlo

Manda una frase al copiloto: necesita **llamada real al LLM**. No hay clave en el entorno de E2E y no la
había antes, así que este test nunca ha corrido en local. Tres salidas: dar clave al entorno de E2E,
precondición honesta que nombre la causa, o proyecto de Playwright aparte que solo corra con clave.
**No inventes una clave y no lo silencies sin más.**

### D. `infra-001` — el `search_path`

33 llamadas a `uuid_generate_v4()` en 12 migraciones dependen del `search_path` de quien las aplica.
Preferencia escrita: **(a) migrarlas a `gen_random_uuid()`** (core de Postgres desde la 13, ya es la
convención mayoritaria del repo, y en prod esas migraciones no se re-ejecutan). Es reescribir contenido
ya aplicado: hazlo consciente y explícalo en el commit.

**El cierre de verdad de `infra-001` es probar la reconstrucción**: proyecto Supabase nuevo y vacío (o
`supabase db reset` local) y que el push llegue a la última migración **sin tocar nada a mano**. Mientras
eso no se pruebe, el issue no está cerrado. Y de paso: verifica los huecos de numeración
(`058→060`, `078→082`, `089→091`, `091→093`, `219→223`, `343→366`) uno a uno.

### E. `perf-001` — el banner de billing

`.billing-banner` no existe en el primer render y aparece después con 36 px, empujando el contenido en
**todas** las páginas de las orgs que lo disparan. Dos opciones: (a) resolver el estado de facturación
en servidor y pintarlo en el primer HTML, (b) reservar su hueco mientras se resuelve.

**Esto es decisión de producto y toca el shell de todas las páginas: pregunta a Manuel antes de
implementar**, con el coste de cada opción. Mide antes y después con atribución:
`PerformanceObserver({type:'layout-shift', buffered:true})`, filtrando `hadRecentInput` y volcando
`entry.sources[].node` con `previousRect`/`currentRect`.

### F. Baselines visuales

`npm run e2e:visual:update` **en el contenedor oficial de Playwright**. En la máquina de Manuel **docker
no está disponible**; si sigue sin estarlo, no es cuestión de tiempo: dilo y no lo simules.

## Reparto con agentes

Paraleliza el **análisis y la escritura de código**; **serializa la medición**. Cuatro dev servers y
cuatro Playwright a la vez en 10 cores es exactamente el error que invalidó dos tandas el 27-jul.

- **Agente 1 (el más largo)** — frente A, conciliación: leer los 5 flujos, diseñar el juego de datos,
  escribir la semilla. Puerto propio.
- **Agente 2** — frente B, los sin diagnosticar: causa raíz con evidencia y clasificación
  PRODUCTO / SPEC / DATO. Puerto propio.
- **Agente 3** — frente D, `search_path`: es mecánico y **no necesita navegador ni dev server**, así que
  no compite por CPU. Que verifique con `grep` que no queda ninguna llamada sin cualificar.
- **Tú** — el frente C y el E (los dos exigen una decisión, no delegues eso), la síntesis, y **las
  tandas de medición, una a una y con lo demás parado**.

A cada agente: ruta absoluta del worktree, su puerto, su scope exacto, **qué NO entra**, prohibido
`git commit`/`push`/`checkout`, y que informe con causa raíz + clasificación + evidencia. Revisa sus
diffs con criterio: el 27-jul un agente propuso cosas correctas y otro se colgó a medias dejando un
helper roto que había que terminar.

## Inviolables de esta tarea

- **Cero verdes comprados.** Ni bajar aserciones, ni subir timeouts a lo bruto, ni `test.skip` de
  conveniencia. Un `skip` vale solo si la precondición falta de verdad **y el mensaje dice cuál**.
  Cambiar `networkidle` por una espera determinista sí es legítimo.
- **Clasifica cada fallo PRODUCTO / SPEC / DATO con evidencia** (red, consola, DOM o consulta a la BD).
  Si es producto, arréglalo en el origen y que el test lo cubra.
- **Verifica en la BD que la acción tuvo efecto**, no te quedes en el toast. Que no haya confirmación
  visible con la acción hecha, y que la acción no se haga, son bugs distintos y de gravedad distinta.
- **Un locator que resuelve a 0 elementos es un test roto, no evidencia sobre el producto** — y dentro
  de un `if (isVisible)` es falso verde. Afirma por rol y nombre accesible, o por el contrato que el
  componente publica (`aria-controls`, región `aria-live`), nunca por clase de CSS Module.
- **No midas con la máquina ocupada.** Ni E2E ni Web Vitals.
- **Los toasts se desvanecen**: al depurar, mira el aviso inmediatamente tras la acción.
- Componentes compartidos de `src/components/ui/`. Copy de usuario según `docs/architecture/copy-humano.md`.
  Sin emojis. `lint` + `typecheck` + `build` + `vitest` antes de cada commit de producto.

## Los cuatro errores que cometí el 27-jul, para que no los repitas

Los cuatro fueron **concluir antes de medir**, y los cuatro costaron tiempo:

1. Dije que 41 smokes fallaban por el producto. Era **mi propia CPU**: build + vitest + Playwright a la vez.
2. Dije que un error de export no avisaba al usuario. **Sí avisaba**, a los 750 ms; yo miré 12 s tarde.
3. Escribí que `uuid-ossp` está en `public` en prod. Está en **`extensions`**; lo que resuelve es el `search_path`.
4. Reporté CLS de 0,31 y 0,20 como problemas. Medidos en silencio son **0,045 y 0,023**: no existían.

Antes de afirmar una causa, pregúntate qué comando la desmontaría en diez segundos, y córrelo.

## Definición de terminado

- Suite smoke: **0 fallos**, y cada `skip` con razón nombrada y verificada.
- `infra-001`: reconstrucción probada de cero en un proyecto vacío, sin parches a mano.
- `perf-001`: banner decidido con Manuel e implementado, con CLS medido antes y después.
- Baselines visuales regenerados, o dicho por qué no se puede.
- PRs abiertos con su verificación en el cuerpo. **Nunca merge automático.**
- Cierre: `/fia-precommit` → `/fia-cierre` → `/obsidian-1`. `.env.local` devuelto a prod, secretos del
  scratchpad barridos, `git stash list` a 0, worktrees temporales eliminados.
