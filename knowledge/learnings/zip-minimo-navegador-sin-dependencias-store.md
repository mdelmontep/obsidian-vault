---
title: construir un zip válido en el navegador sin dependencias usando solo store
date: 2026-07-03
source: claude-code-session
tags: [frontend, zip, download, facturaia]
---

Para empaquetar N ficheros ya comprimidos (PDFs) en un `.zip` descargable desde
el cliente sin añadir una librería: usa método STORE (sin compresión) — DEFLATE
no aporta nada sobre un PDF y evita arrastrar dependencia. El formato ZIP
mínimo son 3 bloques por fichero + 1 final, construibles a mano con `DataView`:

1. **Local file header** (30B + nombre): sig `0x04034b50`, CRC32, tamaño
   comprimido=sin comprimir (STORE), flag `0x0800` para nombre UTF-8.
2. **Central directory record** (46B + nombre) por fichero: mismos campos +
   offset del local header correspondiente.
3. **End of central directory** (22B): nº entradas, tamaño y offset del
   central directory.

CRC32 se calcula con tabla estándar (polinomio `0xedb88320`). Ensambla todo en
un único `Uint8Array` contiguo → `new Blob([...], {type:'application/zip'})`.
Cualquier descompresor estándar (Explorer, Archive Utility, 7zip) lo abre sin
problema. Ver implementación de referencia en `tufacturaia/src/lib/documents/zip.ts`.
