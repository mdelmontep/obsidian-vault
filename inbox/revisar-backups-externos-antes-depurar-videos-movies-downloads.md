---
title: revisar backups externos antes depurar videos movies downloads
date: 2026-04-15
source: claude-code-session
tags: [inbox, cleanup, backup]
---

En la auditoría de disco del 2026-04-15 quedaron **explícitamente pospuestos** dos bloques de vídeos:

### Bloque 1 — `~/Movies/GoPro` (21 GB)

Vídeos de GoPro sin revisar. Posibles candidatos a mover fuera del SSD si hay backup.

### Bloque 2 — `~/Downloads` (~10 GB en vídeos sueltos)

Archivos grandes encontrados:

- `IMG_0372.MOV` (1.1 GB)
- `GX010207.MP4` (1.1 GB)
- `IMG_9670.MOV` (885 MB)
- `GX010206.MP4` (792 MB)
- `NATALIA DEL MONTE PÉREZ.mp4` (604 MB)
- `IMG_0195.MOV` (598 MB)
- `IMG_9900.MOV` (404 MB)
- `HiFlyMadrid_20_AnaYuleisyPABONSNCHEZ_*.mp4` x3 (350 MB c/u)
- `RLN8-410-0-Recepcion-*.mov` (336 MB)
- `IMG_9899.MOV` (320 MB)
- `IMG_3248.MOV` (305 MB)

Carpeta adicional: `drive-download-20230712T115528Z-001` (2 GB, de julio 2023, casi 3 años vieja).

### Acción pendiente

**Antes** de borrar o mover nada, verificar:

1. ¿Los vídeos GoPro están duplicados en disco externo / iCloud / Drive?
2. ¿Los vídeos IMG_ de Downloads son originales únicos o copias temporales (WhatsApp, AirDrop, etc.)?
3. ¿Los HiFlyMadrid son material de clientes que hay que archivar?
4. ¿La carpeta `drive-download-2023` sigue relevante o se puede descartar entera?

Sin ese check, **no tocar**. El ahorro potencial es de ~30 GB, no es urgente dado que el disco tiene ~3 TB libres tras la limpieza.
