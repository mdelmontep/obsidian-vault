---
title: sheetjs xlsx en npm está parado en una versión con CVEs, usar su CDN propio
date: 2026-07-23
source: claude-code-session
tags: [seguridad, dependencias, xlsx, facturaia]
---

El paquete `xlsx` (SheetJS) publicado en el registro npm está parado en 0.18.5, con CVEs conocidas sin parchear (prototype pollution GHSA-4r6h, ReDoS GHSA-5pgg). SheetJS dejó de publicar fixes en npm tras una disputa; los fixes reales (0.19.3+, 0.20.2+) solo se distribuyen desde su propio CDN.

**Fix**: instalar desde el tarball versionado del CDN, no "latest" flotante:
```
npm install xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz
```
Verificar el `package.json` real dentro del tarball antes de confiar en la versión (el nombre de la URL no garantiza nada por sí solo).

`exceljs` (alternativa ya común en el repo) solo lee OOXML (.xlsx moderno), no el binario BIFF legado (Excel 97-2003) — para eso hace falta `xlsx`/SheetJS, no hay otra librería JS mantenida que lo lea.
