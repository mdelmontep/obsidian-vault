---
title: chrome cache macos ruta system cache es independiente del profile
date: 2026-04-15
source: claude-code-session
tags: [macos, chrome, cleanup]
---

Chrome en macOS guarda caches en **dos ubicaciones independientes**, con implicaciones distintas para limpieza:

### 1. System cache (seguro borrar con Chrome abierto)

```
~/Library/Caches/Google/
```

- Tamaño típico tras meses de uso: 8-12 GB
- Contiene recursos cacheados a nivel sistema (imágenes, fonts, scripts descargados)
- Se puede borrar mientras Chrome esté corriendo sin afectar pestañas, login ni sesiones
- Comando seguro para limpieza selectiva por antigüedad:

  ```bash
  find ~/Library/Caches/Google -type f -mtime +30 -delete
  find ~/Library/Caches/Google -type d -empty -delete
  ```

### 2. Profile cache (NO tocar con Chrome abierto)

```
~/Library/Application Support/Google/Chrome/Default/Cache/
~/Library/Application Support/Google/Chrome/Default/Code Cache/
~/Library/Application Support/Google/Chrome/Default/GPUCache/
```

- Aquí también se cachea contenido pero está **junto al resto del profile**
- El profile contiene `Cookies`, `Login Data`, `Bookmarks`, `Sessions`, `History`
- Si borras mal, puedes cerrar sesiones de bancos, invalidar tabs activas, perder pestañas
- **Regla**: solo tocar el profile con Chrome **completamente cerrado** y solo las subcarpetas `Cache`, `Code Cache`, `GPUCache`. Nunca tocar `Cookies`, `Login Data`, `Bookmarks`, `Preferences`, `History`.

### Recomendación práctica

Para ganar espacio rápido y sin riesgo: limpiar el **system cache** con `-mtime +30`. Suele liberar 4-5 GB y no invalida nada. El profile cache solo merece la pena si Chrome está cerrado y quieres purga completa.
