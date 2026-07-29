---
title: un campo que muestra un formato y guarda otro descarta la edición en silencio
date: 2026-07-29
source: claude-code-session
tags: [frontend, ux, formularios, integridad, facturaia]
---

Fila que **pinta** con un formatter (`fmtDate` → `dd/mm/aaaa`, moneda, %) pero se **edita** con un
`<input type="text">` libre cuyo guardado valida contra el formato de almacenamiento:

```ts
if (rawValue && !/^\d{4}-\d{2}-\d{2}$/.test(rawValue)) return   // sin toast, sin log
```

El usuario teclea lo que ve (`23/06/2026`), el handler hace `return` mudo y **no queda rastro en
ninguna capa**: ni en el JSONB, ni en la tabla, ni en `updated_at`. Parece guardado, y aguas abajo
el dato viejo se propaga (aquí: la fecha del OCR viajó a `facturas` al aprobar la recibida).

Dos reglas, no una:
- **El control lo decide el TIPO del dato, no la comodidad de la fila.** Fecha → el `DatePicker`
  compartido, que habla ISO hacia dentro y `dd/mm/aaaa` hacia fuera. Un formatter de solo-lectura
  sobre un input libre es la propia trampa.
- **Ninguna rama de guardado sale muda.** Un `return` de validación sin feedback convierte un error
  de formato en pérdida de datos silenciosa. Si el guard sigue existiendo, que avise.

Olor a buscar: `format:`/`fmt*` en la misma fila que un `<input type="text">`, y `return` sin
`toast`/`throw` dentro de un `if` de validación. Caso TuFacturaIA #1349 (ticket #104, Chivite).
Ver [[copiloto-tool-select-campo-faltante-guard-mudo]] · [[facturaia]]
