---
title: cryptobruj-bot
date: 2026-07-31
updated: 2026-07-31
tags: [proyecto, trading, python, dokploy]
---

# cryptobruj-bot

Bot de trading algorítmico propio. Python 3.11 + ccxt + FastAPI + PostgreSQL, Docker en
Dokploy. Panel en `https://cryptobruj-bot.185.99.186.76.sslip.io`.
Despliegue = webhook de Dokploy con `X-GitHub-Event: push` (token en 1Password, vault
Agentesia, cuenta `agentesialab.1password.eu`). **`autoDeploy` está a true pero el repo no
tiene webhook**: todos los despliegues son manuales.

## Lo que hay que saber antes de tocar nada

**La metodología Cryptobruj (contra-tendencia: comprar en soporte, objetivo 2R) NO tiene
ventaja.** Medido limpio: **−0,180R, PF 0,72** sobre 8.982 operaciones. No es un fallo de
implementación — 500 configuraciones probadas y ninguna supera el margen; el argmax de una
mitad de los datos da −0,282R en la otra (percentil 0,01). La literatura dice lo mismo del
análisis técnico en cripto tras ajustar por data snooping.

`regime_filter` sí funciona (+0,074 a +0,157R en las cuatro submuestras): lleva de −0,18R a
≈0,00R. Deja de sangrar, no gana. Propuesto en el panel, **sin aplicar**.

## Estado (31-jul)

- **5 estrategias Cryptobruj** en paper con expectancy negativa; el kill switch del 5% las
  va apagando solo — eso es el sistema funcionando. `scalp-5m` pausada **a mano** (real, ~87
  USDT, tope $10).
- **`tendencia-1d` («Corriente 1d»)** — familia nueva y opuesta: cruce SMA 10/40 diario, sin
  objetivo, sale por cruce inverso o stop 3×ATR. **65 pares, riesgo 0,2%, en paper.** Lo
  único del repo con respaldo fuera de muestra: **+0,229R en 992 operaciones**, y ganó
  +13,5% en un universo que cayó −28,9%.
- **NO está probada: t=1,12** tras el filtro de pendiente. Ver el plazo real abajo.
- **211+ tests**, `main` limpio, desplegado y verificado contra producción.

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
- **La reserva ciega está GASTADA.** Mató a "solo largos" (+0,538R en búsqueda, −0,143R en
  el tramo retenido). No queda dato virgen para una tercera validación.
- **Marcos rápidos medidos y descartados**: 1h −0,041R, 15m −0,290R, 5m −0,515R. El coste es
  fijo por operación y el riesgo se encoge con el marco (en R: 1d 0,007 · 5m 0,168).
- **`_evaluate_live` no soporta la familia tendencia** y falla en seguro. Habilitarla en real
  exige portar señal por familia, cierre por cruce y bloqueo tras stop, más el SL sin TP en
  `place_order`.

## Pendiente (mío)

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
[[una-constante-tipica-sin-fuente-contamina-todo-lo-construido-encima]]
