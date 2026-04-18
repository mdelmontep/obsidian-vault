---
title: apps limpiadoras dejan agentes y daemons persistentes al desinstalar
date: 2026-04-15
source: claude-code-session
tags: [macos, cleanup, desinstalar]
---

Las apps "limpiadoras" o "optimizadoras" de Mac (CleanMyMac, MacKeeper, MacPaw, iStat, etc.) **no se desinstalan arrastrando la .app a la papelera**. Dejan múltiples agentes y daemons residentes, además de docenas de archivos de soporte.

Patrón general al desinstalar:

### 1. LaunchDaemons y LaunchAgents

```
/Library/LaunchDaemons/<bundleId>.plist          # daemon root, arranca con el sistema
/Library/LaunchAgents/<bundleId>.plist           # agente global
~/Library/LaunchAgents/<bundleId>.plist          # agente de usuario
```

Borrar con `launchctl unload <plist>` + `rm <plist>` (los de `/Library` requieren sudo).

### 2. Procesos menu bar helper y health monitor

Muchas de estas apps instalan "Menu" y "HealthMonitor" como apps separadas dentro de `~/Library/Application Support/<App>/`. Hay que matarlos con `pkill` antes de borrar archivos.

### 3. Rutas de soporte a barrer

```
~/Library/Application Support/<App>*
~/Library/Caches/<bundleId>*
~/Library/Preferences/<bundleId>*.plist
~/Library/HTTPStorages/<bundleId>*
~/Library/Logs/<App>*
~/Library/WebKit/<bundleId>*
~/Library/Group Containers/*<bundleId>*
~/Library/Application Scripts/*<bundleId>*
~/Library/Containers/<bundleId>*
~/Library/Saved Application State/<bundleId>*
```

Búsqueda exhaustiva antes de borrar:

```bash
find ~/Library -maxdepth 3 -iname '*<app>*' -o -iname '*<vendor>*' 2>/dev/null
```

### Caso documentado — CleanMyMac X (2026-04-15)

Al desinstalar: 1 daemon en `/Library/LaunchDaemons/com.macpaw.CleanMyMac4.Agent.plist`, 1 LaunchAgent de usuario para el updater, 2 procesos residentes (`CleanMyMac X Menu`, `CleanMyMac X HealthMonitor`), **27 rutas de soporte** en `~/Library/{Caches,HTTPStorages,Logs,Preferences,Group Containers,Application Support,WebKit,Application Scripts}`. Barrer solo la `.app` deja ~24 de esas 27 rutas activas.

### Regla general

Asumir siempre que apps que "optimizan" el Mac tienen persistencia agresiva. El desinstalador de la propia app suele ser el camino correcto cuando existe. Si no existe, el barrido manual del patrón de arriba es obligatorio.
