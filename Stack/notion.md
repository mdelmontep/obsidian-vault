---
title: notion — estructura y reglas
date: 2026-04-20
source: claude-md-migration
tags: [notion, organización]
---

# Notion

- Guardar en Notion toda configuración de infraestructura nueva (composes, credenciales, checklist)
- Estructura del workspace:
  - `🏢 AgentesIA — Interno` → solo empresa: web, pricing, prompts
  - `👥 Clientes` → Juan, AgentesIA Madrid, Tecnocloud (la infra de agentesia.madrid y agentesia.world va aquí, como cliente)
  - `📚 Guías Técnicas` → guías reutilizables entre proyectos
- **AgentesIA Madrid y AgentesIA World se tratan como clientes**, no como interno. Interno es solo lo de empresa (web, marca, negocio)
- Antes de crear una página nueva, buscar si ya existe una similar para evitar duplicados
- **La API de Notion no puede borrar páginas** — cuando haya páginas obsoletas, avisar al usuario para que las borre manualmente
