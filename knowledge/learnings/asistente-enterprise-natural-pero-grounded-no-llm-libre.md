---
title: "contestar como ChatGPT" en un asistente enterprise = natural PERO grounded, no LLM libre
date: 2026-07-09
source: claude-code-session
tags: [agentes, enterprise, arquitectura, grounding, rgpd]
---

Cuando un cliente pide que el agente "conteste tan natural como ChatGPT/Claude", el objetivo NO es
dejar que el LLM genere la respuesta final libremente. Ante clientes enterprise (multinacional, RGPD,
auditoría) eso es alucinación esperando a pasar y rompe la auditabilidad.

**El diseño correcto: el LLM interpreta y decide el ruteo; la respuesta final se formatea en CÓDIGO
sobre filas reales (grounded). "Natural Y fundamentada", no "LLM libre".** La naturalidad/contexto
(que es lo que impresiona) se gana con: ventana de turnos para anáfora, entidades recientes en el
estado, síntesis calculada ("4 oportunidades por 230.000€, la próxima el jueves") y empty-states con
siguiente paso — todo determinista/grounded, sin que el modelo invente la respuesta.

La ganancia de recall de una memoria LLM (Mem0 y cía.) casi nunca justifica su coste de
compliance/no-determinismo en enterprise: mide antes de construirla. Ver
[[recall-semantico-sin-umbral-es-confidently-wrong]] y el anti-patrón de integración en JSONB.
