---
title: estimar horas retroactivas sin time-tracking cruzando git log + hub de cliente + ADRs
date: 2026-08-04
source: claude-code-session
tags: [process, billing, estimation, obsidian]
---
Cliente pide "¿cuánto llevamos de X?" sin que exista time-tracking. Método en dos frentes distintos según si el trabajo dejó rastro versionado:

1. **Frente con commits** (repo de código): `git log --reverse --format='%ai %h %s'`, agrupar por gaps >2h en sesiones, sumar ventana primer-a-último commit por sesión. Ojo al autor (`git log --format='%an <%ae>'`) — puede no ser quien pregunta.
2. **Frente sin commits** (trabajo vía dashboard/API — n8n, Retell, WhatsApp Business Manager): no hay timestamps objetivos. Estimar por densidad de lo documentado en el hub del cliente (`clientes/<x>/index.md`): nº de bugs encontrados+arreglados por sesión, nº de nodos/workflows tocados, menciones explícitas de duración ("tras 3h de iteración").
3. **Cruzar con ADRs del mismo rango de fechas** (`decisions/ADR-*`) — una decisión con 3-4 opciones y cálculo de coste real (caso: ADR-013 modelando €/min de Retell) es señal de que ese día tuvo más peso analítico del que sugiere el nº de commits/cambios de infra visibles.

Reportar el rango con el método explícito por frente (objetivo vs estimado) — nunca presentar ambos con la misma confianza.
