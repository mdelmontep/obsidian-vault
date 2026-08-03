---
title: una excepción de validación sobre un campo que la UI no sabe poner es inalcanzable
date: 2026-08-03
source: claude-code-session
tags: [validacion, ux, facturaia, smoke]
---

`aprobarRecibida` bloquea con **422** una recibida en negativo *salvo* que
`tipo_documento = 'abono'`. La excepción está bien pensada y comentada. Pero
**ningún control de la app escribe ese campo en una recibida**: lo fija el
pipeline de ingesta. Resultado: el abono del proveedor entra como `factura` en
negativo, cae en el guard y no hay forma de sacarlo desde la interfaz.

Dos agravantes que lo vuelven invisible:

1. La UI **se traga el 422**. El endpoint devuelve hasta un `message` redactado
   para el usuario y no se pinta nada: el botón «Aprobar» parece no hacer nada.
   Se vio en la pestaña de red, no en la pantalla.
2. La cifra del modal no era la del registro (20,69 € sobre una fila de
   −60,50 €), así que ni mirando el importe se sospecha.

Al revisar un guard con `salvo que <campo>`, preguntar **quién pone ese campo**.
Si la respuesta es «otro proceso», la excepción no existe para el usuario y el
guard es un muro.

Y el método: la respuesta «regístralo en negativo» parecía sostenida por datos
(2 recibidas negativas en prod, ninguna validación `positive()` a la vista) y era
**falsa**. Lo cazó hacer el gesto en el navegador, no consultar la base.

Ver [[feedback_smokes_siempre_con_agent_browser]] ·
[[antes-de-mergear-una-validacion-que-bloquea-cuenta-a-quien-bloquea]]
