---
title: enum legal hardcodeado en ui falsifica motivos
date: 2026-05-08
source: claude-code-session
tags: [fiscal, ux-trampa, agentesia, agency-portal, facturaia]
---

Si un endpoint backend acepta un enum con consecuencias legales (motivos rectificación R1-R5, códigos contables, conceptos AEAT, modelos tributarios) y la UI fija un valor sin pedírselo al usuario, es **falsificación de facto**.

Caso real (agency-portal `FacturaiaActions`): botón "Anular" enviaba `motivo_rectificacion=R5` siempre. Resultado: TODAS las anulaciones declaradas como "R5 - otras causas" en Verifactu/AEAT, sin importar el motivo real (R1 datos incorrectos, R2 concurso, R3 incobrable, R4 judicial). Auditoría fiscal lo detecta y multa.

Fix: modal con `<select>` obligatorio + descripción opcional. Etiquetas humanas, no códigos. Server-side ya valida el enum (Zod), no es por seguridad — es por trazabilidad real.

Patrón aplicable a: códigos error AEAT, tipos retención, regímenes IVA, motivos exención, claves operación 347.
