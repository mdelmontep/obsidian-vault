---
title: una plantilla de Meta no se edita, y borrarla retiene el nombre
date: 2026-08-10
source: claude-code-session
tags: [whatsapp, meta, plantillas, agh-iberica]
---
Medido contra la Cloud API al querer corregir un emoji mal puesto en una plantilla recién creada:

- **Editar** → `POST /{template_id}` da `[100] Invalid parameter — las plantillas solo se pueden editar si se han RECHAZADO`. Ni `PENDING` ni `APPROVED`.
- **Borrar y recrear con el mismo nombre** → el `DELETE` devuelve `{"success": true}`, pero 8 altas en ~6 min fallaron con *«no es posible añadir contenido nuevo en Spanish mientras se está eliminando el contenido existente»*. La duración no está en la doc oficial; la propia Meta sugiere **usar otro nombre**.

O sea: **el ciclo «edito y ya» no existe**. Un descuido en el cuerpo cuesta un nombre quemado y una espera indeterminada.

Y dos datos más del mismo día:
- El **cuerpo** admite saltos de línea y varias variables; el **parámetro** no ([[una-medicion-correcta-puede-tener-el-alcance-de-mas]]). Meta rechaza un parámetro vacío → una lista de longitud variable necesita **una plantilla por longitud**.
- Un lote de 8 altas se aprueba **con huecos y desordenado** (2,3,5,6,8 antes que 1,4,7). Si el código elige plantilla por cantidad, lo que vale es el **tramo contiguo aprobado desde 1**, no cuántas hay creadas: apuntar a una `PENDING` **falla el envío entero**.

**Patrón:** revisar el cuerpo (imprimiendo codepoints) **antes** del alta — es la última revisión gratis; nombre por env con prefijo+sufijo, nunca cableado; y **fallback a una plantilla que ya funciona**.
