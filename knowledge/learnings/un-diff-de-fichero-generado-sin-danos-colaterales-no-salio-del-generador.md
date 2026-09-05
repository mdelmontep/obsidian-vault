---
title: un diff de fichero generado que solo añade un bloque no salió del generador
date: 2026-09-05
source: facturaia
tags: [forense, tipos-generados, git, gates]
---
Un fichero que se produce entero de una pasada (tipos de BD, OpenAPI, lockfile, grafo de
dependencias, snapshots) **arrastra en su diff toda la deriva pendiente**, no solo lo que fuiste a
buscar: si al regenerar había otra cosa desfasada, sale también. Así que un diff de
`+66 / -0` que toca **un único bloque** y nada más es la firma de un injerto a mano, no de una
regeneración.

- Es medible sin reproducir nada: cuenta borrados y bloques tocados. Cero borrados y un bloque
  es un pegado; una regeneración de verdad casi nunca sale limpia.
- Importa porque el fichero **sigue pasando el typecheck y el gate**: es sintácticamente válido y
  coherente consigo mismo. Lo que miente es su relación con la fuente.
- Caso real (5-sep-2026, FacturaIA): `database.types.ts` recibió el bloque de una tabla nueva y
  se quedó sin otra que llevaba dos días aplicada en prod. El guard `gen:types:check` **sí**
  discriminaba —falsado retirando un bloque entero: rojo y con el remedio— así que no había bug:
  falló el gesto humano de regenerar. → [[gen-types-linked-no-db-url]] ·
  [[una-fk-nueva-hacia-una-tabla-ya-referenciada-rompe-los-embeds-de-postgrest]]
- Para fechar el orden de lo aplicado cuando la tabla de registro no tiene fecha, el `ctid` de una
  tabla append-only da el orden físico de inserción. Fue lo que descartó la explicación cómoda.
