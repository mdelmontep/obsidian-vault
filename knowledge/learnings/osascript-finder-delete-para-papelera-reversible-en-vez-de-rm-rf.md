---
title: osascript finder delete para papelera reversible en vez de rm rf
date: 2026-04-15
source: claude-code-session
tags: [macos, shell, cleanup]
---

Para operaciones de limpieza **reversibles**, mandar archivos a la Papelera con AppleScript en lugar de `rm -rf`:

```bash
osascript -e 'tell application "Finder" to delete POSIX file "/ruta/al/archivo" as alias'
```

El archivo aparece en `~/.Trash` y se puede restaurar desde Finder. Hasta que vacíes la papelera, cero riesgo de pérdida.

### Batch de múltiples rutas

```bash
osascript <<'EOF'
set targets to {"/ruta/uno", "/ruta/dos", "/ruta/tres"}
repeat with t in targets
  try
    tell application "Finder" to delete (POSIX file (t as string) as alias)
  end try
end repeat
return "done"
EOF
```

El `try` hace que siga adelante aunque alguna ruta no exista.

### Cuándo usar cada opción

| Caso | Herramienta |
|---|---|
| Limpieza interactiva donde el usuario podría arrepentirse | `osascript ... delete` |
| Borrado de apps y sus archivos de soporte en desinstalación | `osascript ... delete` |
| Cache pura regenerable (Chrome, Playwright, Homebrew) | `rm -rf` directo |
| Miles de archivos en cache (rendimiento) | `find ... -delete` |
| Archivos con permisos root | `sudo rm` (osascript no escala bien ahí) |

### Importante

- Las rutas tienen que ser absolutas
- Si el archivo ya está en otra sesión de Finder, a veces falla silenciosamente — verificar después con `ls`
- No usar para cache masivo (miles de archivos), Finder tarda mucho en procesarlos uno a uno. Para eso `find -delete` directo
