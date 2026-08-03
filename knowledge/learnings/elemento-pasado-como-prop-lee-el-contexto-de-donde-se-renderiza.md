---
title: un elemento pasado como prop lee el contexto de donde se RENDERIZA, no de donde se escribió
date: 2026-08-03
source: claude-code-session
tags: [react, frontend, gotcha, facturaia, contexto]
---

Pasar `<MiAviso/>` como prop (`confirm({ extra: <MiAviso/> })`) NO lo ata al
contexto del componente que lo escribe: React resuelve el contexto por la
posición en el **árbol donde se renderiza**. Si el diálogo vive dentro de
`ToastProvider` y el provider de datos está DEBAJO, el elemento no lo ve.

Caso FacturaIA (03-ago): `dashboard-shell` montaba `PendientesProvider` dentro de
`ToastProvider`. El aviso de «falta la dirección fiscal» en el diálogo de
convertir presupuesto salía **vacío y sin error**, porque `usePendientes()`
devuelve lista vacía fuera del provider en vez de lanzar — correcto para no
tumbar una pantalla, pero convierte un error de árbol en un aviso que no aparece.

Ojo: los **portales de React sí propagan contexto** (el mismo componente dentro
de un `<Modal>` funcionaba). El problema no es el portal, es renderizarse en otro
punto del árbol.

Doble arreglo: subir el provider por encima **y** permitir pasar los datos por
prop, para que el camino no dependa del orden de dos providers de otro fichero.
Detección: si un aviso «no sale» y nada falla, mirar QUIÉN lo renderiza.
Relacionado: [[dos-sistemas-toast-usar-el-sin-provider-es-noop-silencioso]].
