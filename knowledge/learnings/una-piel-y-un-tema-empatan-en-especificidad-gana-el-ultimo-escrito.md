---
title: una piel y un tema empatan en especificidad, y gana el que se escribió después
date: 2026-08-31
source: facturaia
tags: [css, cascada, especificidad, tokens, dark-mode]
---

Una capa de **piel/marca** (`:root[data-skin="x"]`) y la capa de **tema**
(`:root[data-theme="dark"]`) puntúan **lo mismo**: (0,2,0). No hay ganador por
especificidad, decide el **orden de fuente**. Así que una piel escrita más abajo
en el fichero pisa el valor oscuro de cualquier token que redefina, y lo pisa
**también en oscuro**.

Se ve fatal y se busca peor: en FacturaIA el bloque `[data-theme="dark"][data-skin]`
(0,3,0) **existía** y no redefinía `--field-glass-bg`, así que ganaba el valor
claro —blanco al 40 %— y TODOS los campos salían casi blancos con texto claro
encima, en el sitio donde se escribe. El bloque correcto estaba ahí, vacío.

Regla: si una piel redefine un token que el tema declara, **tiene que redefinirlo
en las dos ramas**. Un token declarado solo en la rama clara no es un token de
tema, es un bug esperando al modo oscuro.

Segunda cara del mismo día: un primitivo con `color: inherit; font: inherit`
**hereda del contenedor donde caiga**, no del campo — dentro de un `.field` que
pinta su label con `font-weight: 600`, el texto ESCRITO sale en negrita. Un
primitivo declara lo suyo; heredar es delegar el estilo en el sitio de la llamada.

Ver [[style-inyectado-con-root-pierde-contra-root-data-theme]]
