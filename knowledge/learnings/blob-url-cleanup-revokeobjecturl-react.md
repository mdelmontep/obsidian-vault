---
title: createObjectURL en react sin revoke = memory leak silencioso
date: 2026-05-25
source: claude-code-session
tags: [react, browser-api, memory-leak]
---

`URL.createObjectURL(blob)` crea una referencia al blob en memoria del browser. **Mantiene el blob vivo hasta que el documento se descarga O hasta `URL.revokeObjectURL(url)` explícito**. Si generas blob URLs en componentes React (PDF preview, image preview, file picker preview) sin revoke, cada interacción acumula memoria — invisible hasta que el tab tira por OOM.

**Patrón cleanup completo** (3 puntos):

1. **Sobrescritura**: setter functional que revoke el previous antes de asignar nuevo.
   ```ts
   setPreviewUrl(prev => {
     if (prev) URL.revokeObjectURL(prev)
     return newUrl
   })
   ```

2. **Cierre explícito**: handler `closePreview` revoke + set null.

3. **Unmount**: `useEffect(() => { return () => { if (url) URL.revokeObjectURL(url) } }, [])` con deps vacías + eslint-disable consciente (no quieres re-correr el effect cada vez que url cambia, solo limpiar al unmount).

Caso real TuFacturaIA 2026-05-25: modal vista previa PDF en `/generar`. Cada click "Vista previa" creaba blob URL nuevo de ~200 KB. Sin revoke, después de 50 previews → 10 MB perdidos hasta refresh.

**No aplica** a blob URLs de corta vida (`a.click(); URL.revokeObjectURL(url)` inmediato) — la revocación inline antes del unmount/cierre del componente ya cubre.
