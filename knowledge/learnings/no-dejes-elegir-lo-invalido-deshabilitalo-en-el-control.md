---
title: no dejes elegir lo inválido, deshabilítalo en el control
date: 2026-07-25
source: claude-code-session
tags: [ux, formularios, validacion, copy]
---

Dos defectos hermanos, los dos encontrados usando la pantalla y ninguno por los tests.

**1. Validar después en vez de impedir antes.** El selector de fecha pintaba los sábados como seleccionables, los aceptaba, y respondía con un texto en gris debajo. Un aviso gris junto a un campo de aspecto normal **no se ve**: el usuario da por hecho que ha elegido bien y se entera al final del flujo.

- Deshabilita en el propio control lo que no es elegible.
- Si aun así el campo puede quedar inválido, que **el borde lo diga** (`aria-invalid` + color), no solo un texto.
- El texto de error va con `role="alert"` y estilo de error, no con estilo de ayuda.

Si el criterio no es un rango (día hábil, festivo, día sin turno), `min`/`max` no bastan: el primitivo necesita un predicado (`isDateDisabled`). Añádelo al componente compartido, no un workaround en la pantalla.

**2. "Formato no válido" no es un mensaje.** Un validador por regex que solo sabe decir "formato no válido" deja al usuario sin saber qué escribir. Toda regla con `pattern` necesita su mensaje propio: **qué hay que poner y un ejemplo**, redactado en positivo. Y el error se pinta junto al campo que lo causó, no solo en un toast que se va y no dice cuál era.

Caso real: FacturaIA, fecha de cargo SEPA y plantilla del concepto. Ver [[facturaia-modulo-sepa-config]].
