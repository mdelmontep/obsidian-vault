---
title: cryptobruj-bot
date: 2026-07-31
updated: 2026-08-03
tags: [proyecto, trading, python, dokploy]
---

# cryptobruj-bot

Bot de trading algorítmico propio. Python 3.11 + ccxt + FastAPI + PostgreSQL, Docker en
Dokploy. **Exchange: BingX.** Panel en `https://cryptobruj-bot.185.99.186.76.sslip.io`.
Despliegue = webhook de Dokploy con `X-GitHub-Event: push`. **`autoDeploy` está a true pero
el repo no tiene webhook**: todos los despliegues son manuales.
✅ **El webhook NO estaba perdido** (03-ago): el item vive en el vault `Agentesia`, que sí
existe, y resuelve. Lo que de verdad falta es peor: **`ADMIN_TOKEN` no está en 1Password**
(el vault `Trading` que citaba la nota no existe) y **la contraseña del panel guardada da
401**. Con eso, la única credencial operativa es el webhook — y redesplegar NO cambia el
modo, porque el env vive en el panel. Nadie puede parar el bot sin Manu.

## 🔴 ABIERTO — sigue en `live`, y son 76 horas, no 32 (03-ago)

`/health` → `{"mode":"live","uptime":273000}`: opera en real **sin interrupción desde ~31-jul**.
El incidente del 01-ago nunca se cerró, solo se abortó el despliegue de `ce89e3f`.
Medido entonces: 451 ops, −0,244R, PF 0,58, **−1.613,33 USDT**.

**La que opera en real es `scalp-5m`** —`LIVE_STRATEGY` en el panel—, no `conservador-1h`
(el default del código). Es la de 5 minutos, medida en **−0,515R**, la que esta misma nota
recomendaba dejar pausada. Tiene **1 posición abierta**. El resto va en paper:
`swing-1h` 3 abiertas, `tendencia-1d` 65, `conservador-1h` 2.

**Orden correcto para pararlo — no es "poner paper":**
1. `POST /strategies/scalp-5m/stop` (necesita `X-Admin-Token`). Corta entradas nuevas y
   **sigue gestionando salidas y reponiendo el SL de emergencia** (`main.py:806`). Reversible
   con `/resume`, y persiste a reinicios.
2. Solo con esa posición ya cerrada, `TRADING_MODE=paper` en el panel + Deploy. Hacerlo antes
   deja la posición real huérfana: el bot pasaría a tratarlo todo como paper y nadie la vigila.

Sigue pendiente confirmar en BingX el nocional real (`/config/live` dice `max_notional 10`
frente a posiciones de 1.632 USDT).
Ver [[no-hardcodear-el-modo-lo-hace-inverificable-desde-el-repo]] ·
[[una-guarda-que-mata-el-proceso-deja-huerfano-lo-que-ya-esta-en-vuelo]]

## Lo que hay que saber antes de tocar nada

**La metodología Cryptobruj (contra-tendencia: comprar en soporte, objetivo 2R) NO tiene
ventaja.** Medido limpio: **−0,180R, PF 0,72** sobre 8.982 operaciones. No es un fallo de
implementación — 500 configuraciones probadas y ninguna supera el margen; el argmax de una
mitad de los datos da −0,282R en la otra (percentil 0,01). La literatura dice lo mismo del
análisis técnico en cripto tras ajustar por data snooping.

`regime_filter` sí funciona (+0,074 a +0,157R en las cuatro submuestras): lleva de −0,18R a
≈0,00R. Deja de sangrar, no gana. Propuesto en el panel, **sin aplicar**.

## Estado (02-ago) — `ce89e3f` en `main`, SIN desplegar

- **5 estrategias Cryptobruj** con expectancy negativa. Confirmado con dinero: −1.613 USDT.
- **`tendencia-1d` («Corriente 1d»)** — familia opuesta: SMA 10/40 diario, sin objetivo,
  sale por cruce inverso o stop 3×ATR. Ahora **217 pares BingX** (los 253 de Binance menos
  los 36 que BingX no lista) y riesgo **repartido**: presupuesto 13% ÷ 217 = **0,0599% por
  operación**, no el 0,2% que anunciaba `/explain`.
- **`tendencia-obj-1d` («objetivo 2R»)** — NUEVA, corre **en paralelo** a la anterior, no la
  sustituye. Único cambio: objetivo a 2R + brecha mínima del 2% entre medias. Es **lo único
  del proyecto que no encoge en reserva ciega** (+0,0729R contra +0,0453R de la base) y a
  nivel de cartera gana en las dos direcciones: **CAGR 5,12% → 6,66% y caída −23% → −20%**,
  porque cerrar en 2R libera el par para reentrar (6.688 ops contra 5.926).
- **Sigue sin estar probada: t=1,45 sobre 24 intentos** (listón estricto ≈2,8). Por eso
  compite en paper en vez de reemplazar. Ver el plazo real abajo.
- **250 tests**, dry-run limpio contra BingX. Gate del checklist que NO cumple, a propósito:
  winrate 39,8% y PF 1,284 contra el ≥50% / ≥1,3 — ese umbral se escribió para la familia
  contra-tendencia; un sistema de tendencia gana pocas veces y cobra en las colas.

## El plazo real, y por qué no hay atajo

Saber si tiene ventaja pide **~15 meses**, no 3. La variación **entre trimestres** es 0,395R,
cuatro veces el prior — un trimestre malo no prueba nada (2025-T2 dio −0,321R sin que nada
fallara). Acumular operaciones dentro de un mismo régimen no acerca la respuesta.
Ver [[muestra-efectiva-son-los-periodos-no-las-observaciones-si-comparten-regimen]].

Lo que **sí** se contesta en días: si el bot **ejecuta** lo que dice el backtest
(`src/conciliacion.py`, comparación determinista). Ahí han estado los tres fallos caros.
Ver [[la-pregunta-determinista-se-contesta-con-diez-casos-la-estadistica-con-mil]].

## No tocar sin pensarlo

- **SMA 10/40 son pre-registradas** (arxiv 2009.12155, elegidas antes de mirar los datos).
  Probar "12/45 a ver si mejora" destruye esa propiedad. No editables en el panel a
  propósito. Ver [[reservar-datos-ciegos-y-preregistrar-parametros-antes-de-buscar]].
- **El filtro de pendiente SÍ se eligió mirando 2025-26.** Lo sostiene la validación en 20
  pares vírgenes (−0,074R → +0,050R), no el pre-registro.
- **No quitar los cortos** aunque los números de un periodo lo pidan: en 2019-24 ganaban los
  largos (+0,698R) y en 2025-26 está al revés (cortos +0,294R). Quitarlos habría dejado el
  sistema perdiendo en el periodo siguiente.
- **La reserva ciega lleva DOS aperturas** (solo-largos, y el objetivo 2R). Lo que queda son
  las **dos celdas libres del 2×2** —impares+reciente y pares+antiguo—, y solo valen para
  juzgar hipótesis YA fijadas, sin elegir nada.
  Ver [[celdas-libres-del-diseno-2x2-son-dos-reservas-mas-sin-gastar]]
- **El objetivo ADAPTATIVO está medido y descartado** ("2R o más según los indicadores"): 79
  combinaciones, top-2 empatados en búsqueda (+0,0535 / +0,0531) y opuestos fuera (+0,0826 /
  −0,0645). En las celdas libres el 2R fijo gana en 3 de 4. **Cobrar siempre en 2R.** Y las
  10 características de entrada, una a una, no separan ganadoras de perdedoras (mediana
  −0,001R): predecir el signo con indicadores no funciona aquí.
  Ver [[dos-finalistas-empatados-que-divergen-fuera-de-muestra-son-ruido]]
- **El presupuesto de riesgo se REPARTE por tamaño, nunca rechaza señales.** Implementarlo
  como puerta tiraba el 38% de las entradas y llevaba el CAGR de 14,76% a 1,66%. Hay un test
  que lo fija. Ver [[presupuesto-de-riesgo-que-rechaza-no-es-el-que-reparte-tamano]]
- **Marcos rápidos medidos y descartados**: 1h −0,041R, 15m −0,290R, 5m −0,515R. El coste es
  fijo por operación y el riesgo se encoge con el marco (en R: 1d 0,007 · 5m 0,168).
- **`_evaluate_live` no soporta la familia tendencia** y falla en seguro. Habilitarla en real
  exige portar señal por familia, cierre por cruce y bloqueo tras stop, más el SL sin TP en
  `place_order`.

## Pendiente (mío)

- 🔴 **Decidir sobre el modo `live`** (ver bloque de arriba) — bloquea el despliegue.
- 🔴 **Recuperar la URL del webhook de Dokploy** y guardarla en un vault que exista.
- 🔴 **Rotar `ADMIN_TOKEN`** — se usó en claro durante la sesión del 30/31-jul.
- 🔴 **Crear el webhook de GitHub** para que `autoDeploy` sirva de algo.
- 🟠 Posición real en BingX a **15x y sin TP** (no los 10x configurados): solo sale por stop
  o a mano.
- Documentar el acceso SSH de `185.99.186.76` (puerto **5251**) en 1Password: la contraseña
  root no está y ninguna del fleet sirve.

## Learnings nacidos aquí

[[muestra-efectiva-son-los-periodos-no-las-observaciones-si-comparten-regimen]] ·
[[el-argmax-de-una-mitad-medido-en-la-otra-dice-si-la-superficie-existe]] ·
[[reservar-datos-ciegos-y-preregistrar-parametros-antes-de-buscar]] ·
[[la-pregunta-determinista-se-contesta-con-diez-casos-la-estadistica-con-mil]] ·
[[una-alarma-que-salta-el-primer-dia-deja-de-leerse]] ·
[[probar-el-productor-y-no-el-consumidor-deja-un-500-con-la-suite-verde]] ·
[[una-constante-tipica-sin-fuente-contamina-todo-lo-construido-encima]] ·
[[celdas-libres-del-diseno-2x2-son-dos-reservas-mas-sin-gastar]] ·
[[dos-finalistas-empatados-que-divergen-fuera-de-muestra-son-ruido]] ·
[[no-hardcodear-el-modo-lo-hace-inverificable-desde-el-repo]] ·
[[presupuesto-de-riesgo-que-rechaza-no-es-el-que-reparte-tamano]]
