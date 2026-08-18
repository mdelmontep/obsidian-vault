---
title: colima — el disco sparse no encoge al borrar, y eso hace pensar que el prune no sirvió
date: 2026-08-18
source: claude-code-session limpieza-mac
tags: [docker, colima, disco, macos]
---

Liberar 22,75 GB dentro de la VM de Colima **no devuelve ni un byte al Mac**. Son dos
cifras distintas y confundirlas lleva a repetir la limpieza creyendo que falló:

- dentro de la VM: `docker run --rm alpine df -h /` → el hueco sí aparece
- en el host: `du -sh ~/.colima/_lima` → sigue igual (54 GB tras purgar 22)

El fichero de disco es *sparse*: crece con el uso y no se contrae al borrar. El hueco
queda disponible para Docker (no volverá a crecer hasta rellenarlo), pero macOS lo
sigue contando como ocupado. Para devolverlo de verdad:

```bash
colima ssh -- sudo fstrim -av
```

Verificar siempre las dos cifras antes de concluir que una limpieza no funcionó.
`~/.claude/bin/docker-radar` las imprime separadas por este motivo.

Ver [[docker-volume-prune-no-toca-los-volumenes-con-nombre]].
