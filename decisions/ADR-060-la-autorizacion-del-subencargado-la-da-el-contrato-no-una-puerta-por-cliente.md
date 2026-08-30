---
title: la autorización del subencargado la da el contrato, no una puerta por cliente
date: 2026-08-28
status: aceptada
tags: [rgpd, flota-ia, agency-portal]
---

## Contexto
La fase 2 de Flota IA manda transcripciones (scrubbeadas) a un tercero nuevo — Anthropic u
OpenAI. §032-B construyó una puerta por cliente en BD (`clients.ai_evaluation_notified_at`
/ `_basis` / `_opt_out_at`, migración `20260827130000`) con **default cerrado**: pantalla
`/agency/agents/coverage`, gate en encolado, en submit y en el proponente.

## Decisión
Retirarla (`a6a7711`, rama `fix/fleet-sin-cobertura-art28` → PR #545). El **Anexo III §8
«Subencargados»** del contrato de alta (`src/lib/pricing/contract-template.ts`) ya otorga
autorización general para «proveedores de inteligencia artificial»: la puerta volvía a
preguntar lo que el contrato firmado concede. Una segunda llave para la misma puerta no
añade cobertura jurídica, solo impide entrar — con las tres columnas a null en los doce
clientes, el juez no encolaba a nadie.

## Alternativas
- Mantenerla y marcar los clientes a mano: trabajo real y re-deriva una conclusión legal ya
  cerrada por el contrato.
- Preaviso de 15 días antes de arrancar: valorado y descartado por Manu el 29-ago.

## Consecuencias
La oposición de un cliente deja de tener columna propia; la palanca pasa a ser pausar el
juez para esa agencia (`fleet_judge_settings`, [[ADR-059-la-cadencia-del-runner-vive-en-la-bd-no-en-el-cron|cadencia en BD]]).
Y desaparece el bloqueo de «anexo de Anthropic sin firmar»: no hay anexo que firmar.
