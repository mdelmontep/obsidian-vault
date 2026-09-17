---
title: si el contrato ya acepta el campo, el bug está en la pantalla — y si son tres pantallas, es un supuesto
date: 2026-09-17
source: facturaia
tags: [producto, diagnostico, api]
---
Ticket: «no se puede cambiar la fecha de los abonos». El endpoint YA aceptaba `fecha`
(validada, propagada al documento, con su guard de suelo). Quien no la mandaba era el
formulario. Antes de diseñar nada: mirar si el contrato de servidor admite ya lo que el
usuario pide — el arreglo puede ser de una pantalla, no de un modelo de datos.

El hallazgo grande vino de contar: **tres** sitios distintos escribían «hoy» sin preguntar
teniendo el campo disponible (abono, marcado de cobro en lote, fecha de operación). Uno es un
bug; tres es un **supuesto de diseño** — que se teclea el mismo día que pasa el hecho — y el
ticket solo destapa la esquina que más duele. El barrido que lo encuentra es buscar el default
(`hoy`, `new Date()`, `current_date`) en los emisores, no en los receptores.

Corolario: el usuario que pide «poder cambiar la fecha» casi nunca quiere editar a posteriori;
quiere **ponerla al crear**. Son dos features distintas y la segunda suele ser ilegal.

Ver [[cosmetico-es-una-conclusion-no-una-observacion]] · [[facturaia]]
