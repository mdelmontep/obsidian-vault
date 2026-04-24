---
title: daily briefing necesita alternativa al curl bloqueado en trigger
date: 2026-04-25
source: claude-code-session
tags: [inbox, slack, triggers, daily-briefing]
---

El Daily Briefing Manu (`trig_01THsqqvV3pg3WNnbgvkkdzk`) ejecuta OK y lee el vault, pero el curl a Slack está bloqueado en el sandbox del trigger.

Alternativas pendientes de investigar:
1. Trigger guarda briefing en archivo del repo (`00-home/daily-briefing.md`), n8n webhook lo lee y manda a Slack
2. PushNotification desde el trigger (si está disponible — límite 200 chars, insuficiente para briefing completo)
3. MCP de Slack en el trigger (no soportado actualmente)
4. GitHub Action post-push que lea el archivo y mande a Slack

La opción 1 es la más viable con el stack actual.
