---
title: ADR-059 — la cadencia del runner vive en la BD; el cron es un latido tonto
date: 2026-08-27
status: accepted
tags: [adr, agency-portal, flota-ia, crons]
---

## Contexto
El juez de Flota IA (fase 2) gasta dinero por tanda. Hace falta ver y cambiar cada
cuánto corre, y poder pausarlo, desde `/agency/agents/judge` — no entrando en Dokploy.

## Opciones consideradas
- **A · Tick fijo + política en BD** — Dokploy llama cada 15 min y el portal decide si
  toca. La cadencia real nunca baja de 15 min.
- **B · El portal reescribe el schedule por la API de Dokploy** — cadencia exacta, pero
  exige un token con **escritura sobre la propia infraestructura del portal** y deja la
  política fuera de la BD: sin RLS, sin auditoría, sin histórico de tandas.
- **C · Dejarlo en el cron y editarlo a mano** — cero código, cero visibilidad, y el
  botón de pausa lo tiene quien tenga acceso al panel de infra.

## Decisión
**A**, porque el gasto se controla desde donde ya hay RLS y `logAuditEvent`, y porque
un token de escritura sobre Dokploy es una superficie desproporcionada para elegir un
intervalo. La granularidad de 15 min es suficiente: la Batch API tarda horas.

## Consecuencias
El panel debe **decir** que un intervalo menor que el tick no se cumple, en vez de
fingirlo. El claim de la tanda pasa a ser una RPC atómica (`for update skip locked`):
desde PostgREST no se puede expresar, ver [[postgrest-sdk-or-no-compara-columnas]].
Y `runFleetJudgeEnqueue`/`runFleetJudgeDrain`, hoy sin scope, necesitan `agencyId`.
