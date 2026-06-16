---
title: tool con feature-gate que lanza error deja al LLM inventar un dato falso
date: 2026-06-16
source: claude-code-session
tags: [llm, tool-use, feature-gating, hallucination]
---
Un tool con required_feature que lanza `feature_unavailable` y devuelve el error
como tool_result deja al LLM PARAFRASEAR el error en una afirmación factual
falsa. Caso TuFacturaIA 2026-06-16: `compararEmpresas` con módulo multiempresa
OFF → el copiloto respondió "solo tienes una empresa registrada" (mentira; el
user tiene 2). No es un "error técnico" que el prompt anti-alucinación capte:
suena plausible. Patrón: cuando un tool está gated/no disponible, el runner debe
devolver un mensaje determinista honesto ("comparar empresas no está en tu plan")
en vez de dejar que el modelo improvise sobre el error. Aplica a cualquier agente
con tools gateados por plan/permiso. Ver [[llm-error-categorizar-no-exponer-crudo-a-logs]]
y [[componentes-que-duplican-feature-check-se-desincronizan-del-provider]].
