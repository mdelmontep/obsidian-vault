---
title: rama de canal nuevo en un workflow no hereda los side-effects de la rama original
date: 2026-07-28
source: claude-code-session
tags: [n8n, retell, clinica-zen, blueprint]
---
Al añadir un canal (voz) a un workflow que ya servía a otro (chat), la rama nueva replica
el camino feliz — crear entidad, crear evento — y se deja fuera los efectos del FINAL de la
original: emails, notificaciones, filas de log. Nadie lo nota porque la reserva SÍ se crea:
el fallo solo se ve desde fuera ("no llegan los correos", meses después).

Caso real (Clínica Zen, `RN0wl8RaRmwLpnfQ`): la rama de voz terminaba en Calendar + Kommo +
Postgres y nunca tocaba `Build Emails HTML`. Además dos nodos de confirmación por WhatsApp
existían pero con CERO conexiones — el agente prometía un mensaje que ningún nodo enviaba.

Revisión: listar los nodos terminales de cada rama y compararlos entre canales; y buscar
nodos huérfanos (`connections` sin entrada NI salida) — un nodo desconectado en un workflow
activo es casi siempre una promesa incumplida, no basura. Ver [[clinica-zen]]
