---
title: email imágenes base64 bloqueadas por clientes de correo
date: 2026-05-04
source: claude-code-session
tags: [email, html, imágenes]
---

Los clientes de email (Gmail, Outlook, Apple Mail) bloquean imágenes base64 inline
por defecto. No se muestran aunque el HTML sea válido.

**Fix**: subir las imágenes a hosting público y referenciar con URL.

Patrón usado en AgentesIA:
- Repo GitHub `AgentesIAMadrid/email-assets` (público)
- URL raw: `https://raw.githubusercontent.com/AgentesIAMadrid/email-assets/main/cliente/imagen.jpg`
- Subir via API GitHub (necesita `Contents: write` en PAT fine-grained) o web UI

Para el HTML del email usar `<img src="URL_PUBLICA">` siempre.
