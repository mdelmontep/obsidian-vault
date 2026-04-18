---
title: launchctl disable gui uid para agentes usuario sin tocar plists sip
date: 2026-04-15
source: claude-code-session
tags: [macos, launchd, sistema]
---

Para deshabilitar un agente de macOS que está protegido por SIP (ej: cualquier cosa en `/System/Library/LaunchAgents/`) **sin modificar el plist**, usar:

```bash
launchctl disable "gui/$(id -u)/<label>"
```

Donde `<label>` es el nombre del servicio (ej: `com.apple.duetexpertd`).

El agente queda marcado como deshabilitado para la sesión del usuario actual. No se borra nada del disco, es reversible con `launchctl enable`.

**Verificar que quedó deshabilitado:**

```bash
launchctl print-disabled "gui/$(id -u)" | grep <label>
```

Debe devolver `"com.apple.duetexpertd" => disabled`.

**Casos de uso típicos:**

- Servicios de Siri/Spotlight que consumen CPU en idle (`com.apple.duetexpertd`, `com.apple.knowledge-agent`, `com.apple.parsec-fbf`)
- Agentes de localización o analytics del sistema
- Servicios de "sugerencias" que no se pueden desactivar desde Ajustes

**No usar para:**

- LaunchAgents o LaunchDaemons de terceros en `/Library/LaunchAgents/`, `/Library/LaunchDaemons/`, `~/Library/LaunchAgents/` — esos **sí** se pueden borrar directamente con `launchctl unload <plist>` + `rm <plist>` (no están protegidos por SIP)
- Servicios críticos de macOS (audio, red, window manager) — disabling puede romper el sistema
