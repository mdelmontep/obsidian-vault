---
title: una excepción de validación sobre un campo que la UI no sabe poner es inalcanzable
date: 2026-08-03
source: claude-code-session
tags: [validacion, ux, facturaia, smoke]
---

`aprobarRecibida` bloquea con **422** una recibida en negativo *salvo* que
`tipo_documento = 'abono'`. La excepción está bien pensada. Pero **ningún control
de la app escribe ese campo en una recibida**: lo fija el pipeline de ingesta.
Verificado por SQL en el sandbox: puesto el campo a `abono`, el mismo botón
devuelve **200** y la factura pasa a `pendiente` conservando el negativo.

El mensaje al usuario existe y es claro —«Corrige la base y el total con
"Editar" antes de aprobarla»— y aun así **no se puede obedecer**: ni el modal de
la recibida ni la bandeja exponen base ni total. Manda a una puerta que no está.

Dos reglas:

- Al revisar un guard con *«salvo que \<campo\>»*, preguntar **quién pone ese
  campo**. Si es otro proceso, la excepción no existe para el usuario.
- Un mensaje de error tiene que citar una acción **que exista en la pantalla**.
  Comprobarlo abriendo la pantalla, no leyendo el `switch` de copys.

Método: la respuesta «regístralo en negativo» parecía sostenida por datos (2
recibidas negativas en prod, ningún `positive()` en la validación) y era falsa.
Y al primer smoke conclui que la UI no pintaba nada — también falso: el mensaje
salía y **mi grep del snapshot no casaba con su texto**. Filtrar un snapshot y no
encontrar algo no es prueba de que no esté; hay que mirar la pantalla completa.

Ver [[feedback_smokes_siempre_con_agent_browser]]
