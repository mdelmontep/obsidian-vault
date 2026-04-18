---
title: easypanel y dominio custom pueden resolver a ips distintas
date: 2026-04-18
source: claude-code-session
tags: [infraestructura, dns, easypanel]
---

`clinica-zen-n8n.aestk3.easypanel.host` resuelve a `72.61.165.23` mientras que `n8nclinicazen.agentesia.madrid` resuelve a `185.47.13.168`. Son servidores completamente distintos.

Nunca asumir que un dominio EasyPanel y un dominio custom apuntan al mismo servidor. Antes de configurar webhooks en servicios externos (Retell, Meta, Chatwoot), verificar con:

```bash
dig +short dominio-easypanel.host
dig +short dominio-custom.com
```

Si las IPs no coinciden, las URLs de webhook apuntan al servidor equivocado y las llamadas fallan o llegan a una instancia vieja/abandonada.
