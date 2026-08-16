---
title: agh-iberica-historico
date: 2026-08-16
tags: [cliente, agh-iberica, historico]
---

# AGH Ibérica — histórico de estados

Estados anteriores del hub [[agh-iberica]], sacados del dashboard para que el arranque de sesión no
los pague. El detalle día a día vive en `docs/status-log/` del repo.

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
