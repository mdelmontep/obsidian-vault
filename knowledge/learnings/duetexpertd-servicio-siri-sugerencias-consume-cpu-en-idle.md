---
title: duetexpertd servicio siri sugerencias consume cpu en idle
date: 2026-04-15
source: claude-code-session
tags: [macos, performance, siri]
---

`com.apple.duetexpertd` es el agente de macOS que alimenta las **sugerencias predictivas** de Siri y Spotlight (apps sugeridas, acciones sugeridas, predicciones de búsqueda, "próxima acción probable").

En Macs Intel y en máquinas con throttling térmico, es habitual verlo al **5-10% de CPU en idle**, y ocasionalmente picos superiores. Contribuye al calentamiento sostenido sin ofrecer una funcionalidad crítica.

### Desactivación segura

No se puede desactivar desde Ajustes del sistema. Su plist está en `/System/Library/LaunchAgents/com.apple.duetexpertd.plist`, protegido por SIP — no se puede modificar ni borrar sin deshabilitar SIP (no recomendado).

La forma correcta es deshabilitarlo a nivel de sesión de usuario:

```bash
launchctl disable "gui/$(id -u)/com.apple.duetexpertd"
```

Verificar:

```bash
launchctl print-disabled "gui/$(id -u)" | grep duet
# => "com.apple.duetexpertd" => disabled
```

Reversible con:

```bash
launchctl enable "gui/$(id -u)/com.apple.duetexpertd"
```

### Qué se pierde

- Sugerencias predictivas en Spotlight (las "próximas acciones probables")
- Apps sugeridas en la pantalla de bloqueo / Handoff
- Alguna contribución a Shortcuts sugeridos

### Qué NO se pierde

- Spotlight búsqueda normal (sigue funcionando igual)
- Siri con comando explícito
- Dictado
- El resto de servicios de macOS

### Cuándo aplicar

Recomendado en Macs Intel con throttling térmico, o cuando `top` / `ps` muestran `duetexpertd` consistentemente >5% CPU. En Apple Silicon el impacto es despreciable, no merece la pena desactivarlo.
