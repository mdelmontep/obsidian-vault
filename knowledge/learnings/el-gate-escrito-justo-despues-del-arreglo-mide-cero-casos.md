---
title: el gate que escribes justo después de arreglar el fallo mide cero casos
date: 2026-08-07
source: claude-code-session
tags: [gates, testing, metodo]
---
Arreglas algo, escribes el gate para que no vuelva, corre y sale verde. Pero sale verde **porque el
arreglo eliminó los casos que el gate cuenta**, no porque proteja.

Caso real: tres tokens CSS nombraban fuentes que nadie cargaba. El arreglo hizo que los tokens
delegaran en otra variable, así que dejaron de nombrar familias — y el gate «toda familia nombrada
tiene cargador» pasó a recorrer **cero familias**. Un bucle sobre cero casos pasa siempre. Guardaba
contra reintroducirlo, que es real, pero no discriminaba nada el día que nació.

**Dos reglas, y la segunda es la que falta casi siempre:**

1. Demuestra el rojo **contra el árbol ANTERIOR al arreglo**, no contra el actual — mútalo de vuelta.
2. Si el gate mide cero casos tras el arreglo, **le falta la otra mitad**: la que comprueba que lo
   arreglado sigue en su sitio. Aquí era «¿`body` consume los tokens?», que es exactamente lo que
   estuvo roto y lo único que hoy discrimina.

Corolario: un gate que sólo puede ponerse rojo por una regresión futura no te dice nada del presente.
