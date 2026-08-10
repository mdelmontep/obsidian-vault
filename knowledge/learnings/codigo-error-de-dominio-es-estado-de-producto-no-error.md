---
title: código de error de dominio es estado de producto, no error a volcar crudo
date: 2026-06-10
source: claude-code-session
tags: [frontend, api, ux, error-handling]
---
Cuando una API propia devuelve un código de error de dominio (p.ej. 422 `{"error":"sin_facturas"}`), eso no es un fallo del usuario ni del sistema — es un estado legítimo del producto ("periodo sin actividad"). El cliente NUNCA debe volcar `res.text()` o el JSON crudo al banner de error.

Patrón:
- Parsear el body con `res.json().catch(() => null)` y mapear cada código conocido a un estado dedicado (estado vacío guiado: qué significa + qué hacer a continuación + CTA).
- Banner de error genérico solo para códigos desconocidos: `j?.detail || j?.error || \`Error ${res.status}\``.

Grep rápido para detectar el anti-patrón: `setError(await res.text())` o `setError(JSON.stringify`.

Caso real (TuFacturaIA 349, PR #177): periodo sin facturas mostraba `{"error":"sin_facturas","detail":...}` en rojo → reemplazado por tarjeta guía con CTA crear factura.

Segundo caso (10-ago-2026, ficha de herramienta): con un id inexistente la pantalla pintaba la
cadena **`not_found`** como único contenido. Y el arreglo no había que inventarlo: el cliente HTTP
del módulo **ya tenía** `mensajeDeFallo(err, porDefecto)` —que sustituye el slug por copy— y esa
vista era de las que no lo llamaba; el componente **ya tenía** el texto bueno («Herramienta no
encontrada.») como fallback, **inalcanzable** porque `error` nunca era null. Antes de escribir copy
nuevo, buscar el helper del borde HTTP y el fallback muerto: el arreglo suele ser una línea.
