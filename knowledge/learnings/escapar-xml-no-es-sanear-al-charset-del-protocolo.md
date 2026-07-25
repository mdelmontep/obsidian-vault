---
title: Escapar XML no es sanear al charset del protocolo
date: 2026-07-25
source: claude-code-session
tags: [sepa, pain008, xml, validacion, facturaia]
---

Son dos capas distintas y hacen falta **las dos**:

1. **Escapar XML** (`&` → `&amp;`, `<` → `&lt;`) hace que el documento esté bien formado.
2. **Sanear al charset del protocolo** hace que el destinatario lo acepte.

El juego de caracteres SEPA (EPC217-08, anexo III de los rulebooks; el Cuaderno 19.14 lo hereda) es solo `a-z A-Z 0-9 / - ? : ( ) . , ' +` y el espacio. Fuera quedan tildes, ñ, ç, `&`, `€`, `º`, `!`, `#`, `%`, `@`, `"`, `;` y las comillas tipográficas.

`Pérez & Hijos` escapado da `Pérez &amp; Hijos`: XML impecable, y el banco lo rechaza igual, porque el contenido sigue llevando una tilde y un `&`. Y el rechazo llega **después** de subir el fichero, cuando el cobro de ese mes ya no sale.

En FacturaIA el bug llevaba tiempo latente en `Dbtr/Nm` y `Cdtr/Nm` de pain.008 y pain.001. No explotaba porque los conceptos eran literales de máquina (`Documento A2026-0001`), pero cualquier cliente llamado `Muñoz` ya lo disparaba. Y había **tests que consagraban el comportamiento incorrecto**, esperando `<Nm>Pérez &amp; Hijos &lt;SL&gt;</Nm>` como si fuera lo correcto.

Detalles de implementación que costaron:

- **Sanear ANTES de validar**, no después: la sanitización cambia la longitud (`Pérez`→`Perez`, `&`→`+`, `€`→`EUR`), así que comprobar los límites de 70 y 140 sobre el original mide algo que no es lo que se emite.
- **Un regex con flag `g` arrastra `lastIndex` entre llamadas a `.test()`** y devuelve true/false alternos sobre la misma entrada. Si el mismo patrón se usa para reemplazar y para comprobar, hacen falta dos constantes.
- Un texto que **se queda vacío** tras sanear (todo caracteres prohibidos) debe fallar ruidosamente o caer a un default, no colarse: un `RmtInf` vacío invalida el fichero entero.

Generalizable a cualquier formato con charset restringido: EDIFACT, ficheros AEAT, SWIFT MT.

Ver [[facturaia-modulo-sepa-config]].
