---
title: métrica topada por el ancho del bucket temporal debe mostrarse acumulada, no puntual
date: 2026-07-22
source: claude-code-session
tags: [dataviz, time-series, agency-portal]
metadata:
  type: learning
---

En un gráfico de serie temporal con buckets (5min/1h/1día...), una métrica como "tiempo trabajado" o "coste" tiene un TECHO MATEMÁTICO igual al ancho del bucket (no puedes trabajar >60 min dentro de una ventana de 1h). Mostrar el valor puntual de cada bucket confunde al usuario: ve la línea aplanarse en ese techo y piensa que el gráfico está "capado"/roto, cuando es la métrica en sí la que no puede superarlo — pasó 3 veces seguidas en la misma sesión antes de caer en la cuenta.

**Fix**: para métricas proporcionales a tiempo (duración, coste), mostrar el ACUMULADO desde el inicio del rango hasta cada bucket, no el valor aislado — la curva sube libremente y refleja el total real. Métricas de conteo (sesiones, nº de proyectos distintos en la ventana) SÍ tienen sentido como valor puntual del bucket; no acumular esas.

Aplica a cualquier dashboard de time-tracking/billing con selector de intervalo variable.
