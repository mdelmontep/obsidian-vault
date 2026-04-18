---
title: apps electron guardan cache en partitions service worker no en root
date: 2026-04-15
source: claude-code-session
tags: [macos, electron, cleanup]
---

Las apps Electron (Notion, Slack, Discord, VS Code, Obsidian, etc.) guardan el grueso de su cache en subrutas **dentro de `Partitions/`**, no en el `Cache` del directorio raíz de la app.

**Patrón a inspeccionar para limpieza:**

```
~/Library/Application Support/<App>/Partitions/<nombre>/Service Worker
~/Library/Application Support/<App>/Partitions/<nombre>/Cache
~/Library/Application Support/<App>/Partitions/<nombre>/Code Cache
~/Library/Application Support/<App>/Partitions/<nombre>/GPUCache
~/Library/Application Support/<App>/Partitions/<nombre>/DawnCache
```

**Ejemplo medido — Notion (2026-04-15):**
- `Notion/Cache` en la raíz → 0 MB (vacío o no existe)
- `Notion/Partitions/notion/Service Worker` → **4.6 GB**
- `Notion/Partitions/notion/Cache` → 479 MB

Total liberable: ~5 GB.

**Cómo auditar antes de borrar:**

```bash
du -sh ~/Library/Application\ Support/<App>/Partitions/*/* 2>/dev/null | sort -hr
```

**Reglas de limpieza seguras:**

- **Cerrar la app** antes de borrar (para no corromper la sesión activa del Service Worker)
- Borrar subcarpetas `Service Worker`, `Cache`, `Code Cache`, `GPUCache`, `DawnCache`
- **No tocar** `Cookies`, `Local Storage`, `IndexedDB`, `Session Storage` → ahí vive el login y el estado persistente
- Apps cloud-first (Notion, Slack, Discord) regeneran los caches sin pérdida de datos
