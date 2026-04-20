---
title: configurar agente de voz retell en workflow leads entrantes
date: 2026-04-20
source: claude-code-session
tags: [clinica-zen, retell, n8n, voz]
---

El workflow "Leads entrantes" (`RN0wl8RaRmwLpnfQ`) tiene nodos Retell para el path de voz, pero el agente de voz no está configurado para Clínica Zen. Los webhooks pueden seguir apuntando al EasyPanel viejo de gonzalo.

Pendiente:
- Verificar/actualizar URLs de webhooks Retell → dominio CZ correcto
- Configurar el agente de voz en Retell para CZ
- Verificar que el plugin Retell está instalado en el worker (ver learning sobre worker validation)
