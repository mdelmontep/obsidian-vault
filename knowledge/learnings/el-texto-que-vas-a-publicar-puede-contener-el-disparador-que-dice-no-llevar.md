---
title: el texto que vas a publicar puede contener el disparador que dice no llevar
date: 2026-09-07
source: facturaia
tags: [verificacion, github, automatizacion, metodo]
---
El cuerpo del PR #2591 explicaba que iba **deliberadamente sin** el trailer `Ticket-feedback:`, y
al escribirlo metió esa cadena literal dentro. Al mergear, el webhook parsea el cuerpo: un match
cierra el ticket del cliente **y le manda el correo de resolución**. La frase que documentaba la
ausencia era indistinguible del disparador.

- **La negación contiene el término**: «esto no lleva X» es texto que contiene X, y un parser que
  decide por presencia lee lo segundo.
- **Razonar sobre la regex no vale**. Se corre **el parser del repo** (`parseTicketRefs`), no uno
  reescrito de memoria, y **contra el texto VIVO** (`gh pr view --json title,body`): lo que lee el
  webhook está en la plataforma, y entre tu borrador y el merge alguien pudo editarlo.

Fix: antes de mergear o publicar algo con efecto sobre terceros, `grep` de los disparadores en el
texto real; si alguno aparece, correr el parser contra ese texto. Hermano de
[[un-guard-que-decide-por-mencion-bloquea-lo-que-solo-nombra-el-comando-caro]] — mismo defecto al
revés: allí la mención bloquea de más, aquí dispara de más.
