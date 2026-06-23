---
title: el atributo download del <a> se ignora en redirects cross-origin
date: 2026-06-23
source: claude-code-session
tags: [browser, supabase-storage, signed-url, descarga]
---

Síntoma: `<a href="/api/x" download>` que hace 302 a una URL firmada de
Supabase Storage (otro host) abre el fichero en el visor en vez de
descargarlo. El navegador **descarta el atributo `download` al seguir un
redirect cross-origin**, y Storage sirve el objeto con `Content-Disposition:
inline` por defecto.

Fix de raíz (no parche en el `<a>`): firmar la URL con la opción `download`
de Supabase → añade `&download=<filename>` y Storage responde
`Content-Disposition: attachment`. Funciona aunque el redirect sea
cross-origin porque el header lo pone el servidor de Storage.

```ts
admin.storage.from(bucket).createSignedUrl(path, ttl, { download: 'nombre.pdf' })
// download: true → usa el nombre del objeto; string → fija el filename
```

Caso real FacturaIA #452: "Descargar PDF" de presupuesto abría el visor;
`render-pdf` GET acepta `?download=1` y firma con la opción. Aplica a
cualquier descarga vía Storage firmado + 302. Relacionado:
[[signed-url-proxy-endpoint-vs-cached-en-bd]].
