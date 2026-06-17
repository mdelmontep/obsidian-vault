---
title: el LLM sobreaplica un constraint de tools vecinos si no hay anti-patrón explícito
date: 2026-06-17
source: claude-code-session
tags: [copiloto, llm, prompt, tool-use]
---

En un system-prompt con varios tools, un constraint fuerte de unos (ej. "factura/abono EXIGEN NIF, si no el sistema bloquea") **contamina** a un tool vecino que NO lo tiene (presupuesto/proforma no son fiscales → no requieren NIF).

Caso real FacturaIA: el Copiloto rechazó una proforma a un cliente sin NIF ("No puedo crear … sin NIF") pese a un bullet con "NO requieren NIF — no lo pidas". La negación SUAVE no bastó: el LLM pattern-matchea el énfasis de los tools fiscales adyacentes. El tool NO bloqueaba (un smoke de integración por `executeTool` creó P/F sin NIF); era puro comportamiento del LLM. Inconsistente además: el presupuesto al mismo cliente sí se creó.

Fix: **anti-patrón explícito**, no negación suave → "NUNCA exijas NIF; aunque no tenga, CREA igual; JAMÁS respondas 'no puedo … sin NIF'; el NIF es EXCLUSIVO de factura/abono". Verifica el comportamiento con smoke real del LLM (unit test del tool no lo caza: el tool ya estaba bien). Mismo patrón que [[persistir-propuesta-destructiva-como-texto-entrena-al-llm-a-narrar]].
